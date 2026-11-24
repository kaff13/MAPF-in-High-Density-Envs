"""Run all five isolated PHANS ideas at 15 seconds, resume, and export reports.

Usage: python -m benchmark.campaign
Inspect the workload with --plan; repeat the same command to resume.
Use --report-only to rebuild HTML without rerunning any measurements.
"""
import argparse
import csv
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
from uuid import uuid4

from .__main__ import dependency_versions, instance_set_hash
from .artifacts import inside_run
from .checkpoints import (CampaignLock, atomic_json, digest, file_hash,
                          load_checkpoints, save_checkpoint)
from .maps import DATASET_VERSION, MAPS, make_instance, scenario_id
from .reports import RESULT_FIELDS, validate_results, write_csv
from .runner import PHANS_COMMIT, PHANS_PARAMETERS, ROOT, Solver, extract_baseline, run_attempt

TIMEOUT_S = 15.0
IDEAS = ("engineering", "execution_commit", "detour", "route_potential", "blocker_window")
VARIANTS = (
    ("engineering", "engineering", "solve", "PHANS + engineering"),
    ("execution_commit", "h2", "h2", "PHANS + execution h2"),
    ("execution_commit", "h4", "h4", "PHANS + execution h4"),
    ("detour", "detour", "solve", "PHANS + detour"),
    ("route_potential", "potential2", "solve", "PHANS + route potential 2"),
    ("blocker_window", "window4", "k4", "PHANS + blocker window 4"),
)


@dataclass(frozen=True)
class Settings:
    maps: tuple = tuple(MAPS)
    densities: tuple = (50, 75, 90, 95)
    seeds: int = 10
    seed_start: int = 100
    ideas: tuple = IDEAS
    workers: int = 4

    def __post_init__(self):
        if (not self.maps or len(set(self.maps)) != len(self.maps)
                or any(name not in MAPS for name in self.maps)
                or not self.densities or len(set(self.densities)) != len(self.densities)
                or any(type(d) is not int or not 1 <= d <= 99 for d in self.densities)
                or type(self.seeds) is not int or self.seeds < 1
                or type(self.seed_start) is not int or self.seed_start < 0
                or not self.ideas or len(set(self.ideas)) != len(self.ideas)
                or any(name not in IDEAS for name in self.ideas)
                or type(self.workers) is not int or not 1 <= self.workers <= 64):
            raise ValueError("invalid campaign profile")

    @property
    def scenario_count(self):
        return len(self.maps) * len(self.densities) * self.seeds


def campaign_solvers(ideas):
    return [Solver("phans")] + [
        Solver(name, f"research.{idea}.solver:{function}")
        for idea, name, function, _ in VARIANTS if idea in ideas
    ]


def instances(settings):
    # Cover every map/density early; later seeds are independent fresh samples.
    for seed in range(settings.seed_start, settings.seed_start + settings.seeds):
        for map_id in settings.maps:
            for density in settings.densities:
                yield make_instance(map_id, density, seed)


def source_files():
    folders = [ROOT / name for name in ("benchmark", "solver", "tests")]
    folders += [ROOT / "research" / name for name in (*IDEAS, "_shared")]
    paths = {ROOT / "research/__init__.py"}
    for folder in folders:
        paths.update(path for path in folder.rglob("*.py")
                     if "results" not in path.relative_to(ROOT).parts
                     and "__pycache__" not in path.parts)
    paths.update((ROOT / "benchmark").glob("*.html"))
    return {path.relative_to(ROOT).as_posix(): path for path in sorted(paths) if path.is_file()}


def measurement_sources():
    fixed = {"benchmark/maps.py", "benchmark/runner.py", "benchmark/validation.py",
             "benchmark/campaign.py", "benchmark/checkpoints.py"}
    return {name: file_hash(path) for name, path in source_files().items()
            if name in fixed or name.startswith(("solver/", "research/"))}


def environment():
    return {"python": sys.version, "executable": sys.executable,
            "platform": platform.platform(), "processor": platform.processor(),
            "dependencies": dependency_versions()}


def write_or_check(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"frozen input or source changed: {path}")
    else:
        temporary = path.with_name(path.name + ".preparing")
        temporary.write_bytes(data)
        temporary.replace(path)


def prepare(root, settings, report_only):
    profile = json.loads(json.dumps(asdict(settings)))
    manifest_path = root / "run.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        keys = ("profile", "measurement_sources", "environment", "timeout_s",
                "phans_commit", "parameters", "dataset_version")
        if (digest({key: manifest[key] for key in keys}) != manifest["configuration_digest"]
                or manifest["timeout_s"] != TIMEOUT_S
                or manifest["phans_commit"] != PHANS_COMMIT):
            raise ValueError("saved campaign configuration was modified")
        if manifest["profile"] != profile:
            raise ValueError("campaign profile/configuration differs from the saved run")
        if not report_only and (manifest["measurement_sources"] != measurement_sources()
                                or manifest["environment"] != environment()):
            raise ValueError("measurement code/source or environment changed; use a new campaign")
    else:
        if report_only:
            raise ValueError("incomplete campaign: no saved manifest")
        if any(path.name != ".campaign.lock" for path in root.iterdir()):
            raise ValueError("output has files but no campaign manifest")
        hashes = {name: file_hash(path) for name, path in source_files().items()}
        measured = measurement_sources()
        configuration = {"profile": profile, "measurement_sources": measured,
                         "environment": environment(), "timeout_s": TIMEOUT_S,
                         "phans_commit": PHANS_COMMIT, "parameters": PHANS_PARAMETERS,
                         "dataset_version": DATASET_VERSION}
        manifest = {
            **configuration, "configuration_digest": digest(configuration),
            "comparison_baseline": "phans", "source_sha256": hashes,
            "campaign_source_digest": digest(hashes),
            "solvers": {solver.name: solver.entrypoint for solver in campaign_solvers(settings.ideas)},
            "solver_labels": {name: label for idea, name, _, label in VARIANTS if idea in settings.ideas},
            "started_at": datetime.now(timezone.utc).isoformat(),
            "campaign_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"),
            "instance_ids": [scenario_id(m, d, s)
                             for s in range(settings.seed_start, settings.seed_start + settings.seeds)
                             for m in settings.maps for d in settings.densities],
            "instance_set_sha256": None,
        }
        atomic_json(manifest_path, manifest)
    # Preparation can resume after interruption before the first measurement.
    for relative, expected in manifest["source_sha256"].items():
        target = inside_run(root / "sources", relative)
        if not target.exists():
            if report_only or file_hash(ROOT / relative) != expected:
                raise ValueError(f"frozen source missing: {relative}")
            write_or_check(target, (ROOT / relative).read_bytes())
        if file_hash(target) != expected:
            raise ValueError(f"frozen source changed: {relative}")
    cases = {}
    for case in instances(settings):
        payload = json.dumps(case.to_json(), sort_keys=True, separators=(",", ":")).encode() + b"\n"
        path = root / "instances" / (case.id + ".json")
        if report_only and not path.exists():
            raise ValueError(f"frozen input missing: {case.id}")
        write_or_check(path, payload)
        cases[case.id] = file_hash(path)
    set_hash = instance_set_hash(instances(settings))
    if manifest["instance_set_sha256"] not in (None, set_hash):
        raise ValueError("frozen scenario set changed")
    manifest["instance_set_sha256"] = set_hash
    atomic_json(manifest_path, manifest)
    with tempfile.TemporaryDirectory(prefix="phans-baseline-") as tmp:
        baseline = Path(tmp) / "baseline"
        extract_baseline(baseline)
        for path in baseline.rglob("*"):
            if path.is_file():
                relative = path.relative_to(baseline)
                write_or_check(root / "baseline" / relative, path.read_bytes())
                if relative.as_posix() in ("solver/a_star.py", "solver/phans_null_agent_swapping.py"):
                    # Git stores LF while a Windows checkout may contain CRLF.
                    if (root / "sources" / relative).read_text(encoding="utf-8") != path.read_text(encoding="utf-8"):
                        raise ValueError("candidate base solver differs from pinned PHANS")
    fingerprints = {name: (None if entrypoint is None else
                    manifest["source_sha256"][entrypoint.partition(":")[0].replace(".", "/") + ".py"])
                    for name, entrypoint in manifest["solvers"].items()}
    return manifest, cases, fingerprints


def attempt_row(root, solver, case, attempt):
    return {
        "instance_id": case.id, "map": case.map.id, "density_pct": case.density,
        "actual_density_pct": case.actual_density * 100,
        "paper_density_pct": case.paper_density * 100,
        "empty_cells": case.empty_cells, "targets": len(case.map.goals), "seed": case.seed,
        "solver": solver.name, "solver_source_sha256": attempt.source_sha256,
        "status": attempt.status, "computation_time_s": attempt.computation_time_s,
        "makespan": attempt.makespan, "timeout_s": TIMEOUT_S, "detail": attempt.detail,
        "plan_path": Path(attempt.plan_path).relative_to(root).as_posix() if attempt.plan_path else "",
    }


def measure_attempt(run_fn, output, solver, case):
    """Run one isolated solver attempt; the coordinator persists its result."""
    log = output / "logs" / solver.name / (case.id + ".log")
    plan = output / "plans" / solver.name / (case.id + ".json.gz")
    log.parent.mkdir(parents=True, exist_ok=True)
    plan.parent.mkdir(parents=True, exist_ok=True)
    attempt = run_fn(solver, case, TIMEOUT_S, output / "baseline", log, plan,
                     source_root=output / "sources")
    return solver, case, attempt


def export_reports(root, manifest, replay_mode="sample", force=False):
    """Publish native pair reports only after all measurements are durable."""
    from .artifacts import build_report
    generator = {name: file_hash(path) for name, path in source_files().items()
                 if name.startswith("benchmark/")}
    published = []
    for idea in manifest["profile"]["ideas"]:
        base = ROOT / "research" / idea / "results/15s" / manifest["campaign_id"]
        base.mkdir(parents=True, exist_ok=True)
        own = []
        for owner, name, _, _ in VARIANTS:
            if owner != idea:
                continue
            destination = base / name if idea == "execution_commit" else base / "paired"
            key = digest({"csv": file_hash(root / "results.csv"), "generator": generator,
                          "solver": name, "replays": replay_mode})
            marker = destination / "report-complete.json"
            cached = json.loads(marker.read_text(encoding="utf-8")) if marker.exists() else {}
            if (not force and cached.get("key") == key
                    and all((destination / file).is_file() for file in cached.get("files", []))):
                own.append(destination / "report.html")
                continue
            building = base / (".report-build-" + uuid4().hex)
            limit = None if replay_mode == "all" else 0 if replay_mode == "none" else 1
            build_report(root, output=building, solvers=[name],
                         replay_sample_per_group=limit)
            atomic_json(building / "report-complete.json", {
                "key": key, "files": [p.relative_to(building).as_posix()
                                       for p in building.rglob("*") if p.is_file()],
            })
            # Keep any previous report recoverable; never delete measurements.
            if destination.exists():
                previous = base / (".previous-" + name + "-" + uuid4().hex)
                assert previous.parent.resolve() == destination.parent.resolve()
                destination.rename(previous)
            building.rename(destination)
            own.append(destination / "report.html")
        links = "".join(f'<li><a href="{escape(os.path.relpath(path, base).replace(os.sep, "/"))}">'
                        f'{escape(path.parent.name)}</a></li>' for path in own)
        (base / "report.html").write_text('<!doctype html><html lang="ru"><meta charset="utf-8">'
                                         f'<title>PHANS: {escape(idea)}</title><h1>{escape(idea)}</h1>'
                                         f'<p>15 seconds; baseline PHANS; {len(manifest["instance_ids"])} scenarios.</p>'
                                         '<ul>' + links + '</ul></html>', encoding="utf-8")
        published.append(base / "report.html")
    links = "".join(f'<li><a href="{escape(os.path.relpath(path, root).replace(os.sep, "/"))}">'
                    f'{escape(path.parents[3].name)}</a></li>' for path in published)
    (root / "report.html").write_text('<!doctype html><html lang="ru"><meta charset="utf-8">'
                                     '<title>PHANS campaign</title><h1>PHANS: five ideas, 15 seconds</h1><ul>'
                                     + links + '</ul></html>', encoding="utf-8")
    return [str(path) for path in published]


def run_campaign(output, settings, *, report=True, report_only=False,
                 max_attempts=None, run_fn=None, replay_mode="sample"):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_fn = run_attempt if run_fn is None else run_fn
    with CampaignLock(output / ".campaign.lock"):
        manifest, cases, fingerprints = prepare(output, settings, report_only)
        completed = load_checkpoints(output, manifest, cases, fingerprints)
        # The per-attempt JSON files are authoritative; repair an interrupted CSV.
        write_csv(output / "results.csv", RESULT_FIELDS, completed.values())
        if any(row["status"] in ("invalid", "crash") for row in completed.values()):
            raise ValueError("campaign contains invalid/crash results; inspect logs before continuing")
        expected = settings.scenario_count * len(manifest["solvers"])
        if report_only and len(completed) != expected:
            raise ValueError("incomplete campaign: report-only never runs missing attempts")
        added = 0
        if not report_only:
            solvers = campaign_solvers(settings.ideas)
            jobs = []
            for index, case in enumerate(instances(settings)):
                offset = index % len(solvers)
                for solver in solvers[offset:] + solvers[:offset]:
                    if (case.id, solver.name) not in completed:
                        jobs.append((solver, case))
            if max_attempts is not None:
                jobs = jobs[:max_attempts]
            with (output / "results.csv").open("a", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=RESULT_FIELDS)
                with ThreadPoolExecutor(max_workers=settings.workers,
                                        thread_name_prefix="phans-attempt") as pool:
                    remaining = iter(jobs)
                    pending = {}

                    def submit_one():
                        try:
                            solver, case = next(remaining)
                        except StopIteration:
                            return False
                        future = pool.submit(measure_attempt, run_fn, output, solver, case)
                        pending[future] = solver, case
                        return True

                    for _ in range(min(settings.workers, len(jobs))):
                        submit_one()
                    while pending:
                        done, _ = wait(tuple(pending), return_when=FIRST_COMPLETED)
                        for future in done:
                            solver, case = pending.pop(future)
                            _, _, attempt = future.result()
                            key = case.id, solver.name
                            row = attempt_row(output, solver, case, attempt)
                            validate_results([row], {"instance_ids": [case.id], "solvers": {solver.name: None}})
                            if row["solver_source_sha256"] != fingerprints[solver.name]:
                                raise ValueError("executed solver fingerprint differs from frozen source")
                            if row["status"] == "solved" and not row["plan_path"]:
                                raise ValueError("solved attempt did not save its trace")
                            save_checkpoint(output, row, manifest["configuration_digest"], cases[case.id])
                            writer.writerow(row)
                            stream.flush()
                            completed[key] = row
                            added += 1
                            print(f'{len(completed)}/{expected} {case.id} {solver.name}: {row["status"]}', flush=True)
                            if row["status"] in ("invalid", "crash"):
                                for queued in pending:
                                    queued.cancel()
                                log = output / "logs" / solver.name / (case.id + ".log")
                                raise RuntimeError(f'{solver.name}: {row["status"]}; inspect {log}')
                            submit_one()
        complete = len(completed) == expected
        reports = []
        if complete:
            validate_results(list(completed.values()), manifest)
            manifest.setdefault("finished_at", datetime.now(timezone.utc).isoformat())
            atomic_json(output / "run.json", manifest)
            if report:
                reports = export_reports(output, manifest, replay_mode, force=report_only)
        return {"complete": complete, "attempts": len(completed), "expected": expected,
                "reports": reports, "output": str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("benchmark-results/phans-15s-10x4"))
    parser.add_argument("--maps", nargs="+", choices=tuple(MAPS))
    parser.add_argument("--density", nargs="+", type=int)
    parser.add_argument("--seeds", type=int, help="independent seeds per map/density; default 10")
    parser.add_argument("--seed-start", type=int, help="first fresh seed; default 100")
    parser.add_argument("--workers", type=int, help="parallel isolated attempts; default 4")
    parser.add_argument("--ideas", nargs="+", choices=IDEAS)
    parser.add_argument("--plan", action="store_true", help="print workload without executing or writing")
    parser.add_argument("--report-only", action="store_true", help="rebuild reports; never rerun solvers")
    parser.add_argument("--no-report", action="store_true", help="save measurements; export HTML separately later")
    parser.add_argument("--replays", choices=("sample", "all", "none"), default="sample",
                        help="sample: one saved replay per map/density/outcome; metrics always use all cases")
    parser.add_argument("--max-attempts", type=int, help="pause after this many new attempts; diagnostic use")
    args = parser.parse_args()
    try:
        saved = args.out / "run.json"
        old = json.loads(saved.read_text(encoding="utf-8"))["profile"] if saved.exists() else {}
        defaults = asdict(Settings()) | old
        settings = Settings(
            maps=tuple(args.maps or defaults["maps"]),
            densities=tuple(args.density or defaults["densities"]),
            seeds=defaults["seeds"] if args.seeds is None else args.seeds,
            seed_start=defaults["seed_start"] if args.seed_start is None else args.seed_start,
            ideas=tuple(args.ideas or defaults["ideas"]),
            workers=defaults["workers"] if args.workers is None else args.workers,
        )
        total = settings.scenario_count * len(campaign_solvers(settings.ideas))
        print(f'{settings.scenario_count} scenarios; {total} attempts; 15 s each; '
              f'{settings.workers} workers; {total * TIMEOUT_S / 3600:.1f} CPU-hours maximum; '
              f'{total * TIMEOUT_S / settings.workers / 60:.0f} min idealized planning wall time '
              '(excluding setup/validation/reporting).', flush=True)
        if args.plan:
            print(json.dumps(asdict(settings), ensure_ascii=False, indent=2))
            return 0
        if args.max_attempts is not None and args.max_attempts < 1:
            raise ValueError("max-attempts must be positive")
        result = run_campaign(args.out, settings, report=not args.no_report,
                              report_only=args.report_only, max_attempts=args.max_attempts,
                              replay_mode=args.replays)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError) as error:
        print(f'Campaign stopped: {error}\nMeasurements already checkpointed are preserved. '
              'Repeat the same command to resume; use --report-only for HTML recovery.', file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Interrupted. Completed checkpoints are preserved; repeat the command to resume.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
