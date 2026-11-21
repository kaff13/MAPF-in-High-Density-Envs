"""Build reports and replay pages from saved benchmark artifacts."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile

from .html_report import write_html_report
from .maps import IDENTIFIER, Instance
from .reports import RESULT_FIELDS, read_results, validate_results, write_csv, write_reports
from .runner import Solver, extract_baseline, run_attempt


def read_run(directory):
    directory = directory.resolve()
    manifest = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    rows = read_results(directory / "results.csv")
    validate_results(rows, manifest)
    return manifest, rows


def inside_run(directory, relative):
    root = directory.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("artifact path must stay inside its run directory")
    return path


def build_report(run_dir, *, output=None, solvers=None, maps=None, densities=None):
    from .plots import REPORT_PLOT_NAMES, render_plots

    run_dir = run_dir.resolve()
    manifest, rows = read_run(run_dir)
    baseline = manifest["comparison_baseline"]
    if solvers and any(name not in manifest["solvers"] for name in solvers):
        raise ValueError("report filter names an unknown solver")
    selected_solvers = set(solvers) | {baseline} if solvers else None
    selected = [
        row for row in rows
        if (not selected_solvers or row["solver"] in selected_solvers)
        and (not maps or row["map"] in maps)
        and (not densities or row["density_pct"] in densities)
    ]
    if not selected:
        raise ValueError("no rows match report filters")
    if any(not IDENTIFIER.fullmatch(row["map"]) for row in selected):
        raise ValueError("invalid map ID in report data")
    filtered = bool(solvers or maps or densities)
    if output is None:
        output = run_dir / "reports" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") if filtered else run_dir
    output = output.resolve()
    if filtered and output == run_dir:
        raise ValueError("filtered reports need a separate output directory")
    if output != run_dir:
        output.mkdir(parents=True, exist_ok=False)
        for folder in ("instances", "logs", "plans"):
            for row in selected:
                if folder == "instances":
                    relative = Path(folder) / f'{row["instance_id"]}.json'
                elif folder == "plans":
                    if not row.get("plan_path"):
                        continue
                    relative = Path(row["plan_path"])
                else:
                    relative = Path(folder) / row["solver"] / f'{row["instance_id"]}.log'
                source = inside_run(run_dir, relative)
                if source.is_file():
                    target = inside_run(output, relative)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if not target.exists():
                        shutil.copy2(source, target)
        if (run_dir / "sources").is_dir():
            shutil.copytree(run_dir / "sources", output / "sources")
        manifest = dict(manifest)
        manifest["source_run"] = str(run_dir)
        manifest["report_created_at"] = datetime.now(timezone.utc).isoformat()
        manifest["report_filters"] = {"solvers": solvers, "maps": maps, "densities": densities}
        chosen_solvers = {row["solver"] for row in selected}
        manifest["solvers"] = {name: entrypoint for name, entrypoint in manifest["solvers"].items() if name in chosen_solvers}
        chosen_ids = {row["instance_id"] for row in selected}
        manifest["instance_ids"] = [case for case in manifest["instance_ids"] if case in chosen_ids]
        from .__main__ import instance_set_hash

        instances = [
            Instance.from_json(json.loads((output / "instances" / f"{case}.json").read_text(encoding="utf-8")))
            for case in manifest["instance_ids"]
        ]
        manifest["source_instance_set_sha256"] = manifest["instance_set_sha256"]
        manifest["instance_set_sha256"] = instance_set_hash(instances)
        (output / "run.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        fields = list(dict.fromkeys([*RESULT_FIELDS, *(key for row in selected for key in row)]))
        write_csv(output / "results.csv", fields, selected)
    write_reports(output, selected, baseline)
    plots = render_plots(selected, baseline, output / "plots", REPORT_PLOT_NAMES)
    map_plots = {}
    for map_id in sorted({row["map"] for row in selected}):
        cases = [row for row in selected if row["map"] == map_id]
        map_output = output / "maps" / map_id
        map_output.mkdir(parents=True, exist_ok=True)
        write_reports(map_output, cases, baseline)
        fields = list(dict.fromkeys([*RESULT_FIELDS, *(key for row in cases for key in row)]))
        write_csv(map_output / "results.csv", fields, cases)
        map_plots[map_id] = render_plots(cases, baseline, map_output / "plots", REPORT_PLOT_NAMES)
    destination = write_html_report(output, selected, baseline, plots, map_plots=map_plots)
    print(destination, flush=True)
    return destination


def archived_source(run_dir, manifest):
    archive = run_dir / "sources"
    if not archive.is_dir():
        return None
    hashes = manifest.get("source_sha256")
    if not hashes:
        raise ValueError("archived sources exist without source fingerprints")
    for relative, expected in hashes.items():
        source = inside_run(archive, relative)
        if not source.is_file() or sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError(f"archived source fingerprint differs for {relative}")
    return archive


def prepare_replay_trace(plan, instance):
    if not plan.get("frames"):
        plan["frames"] = [instance.starts]
        plan["trace_available"] = False
    return plan


def replay_plan(directory, manifest, instance, row, generation_dir, pair_dir, *, force=False, timeout=None):
    from .replay import load_plan

    solver_name = row["solver"]
    paths = []
    if row.get("plan_path"):
        paths.append(inside_run(directory, row["plan_path"]))
    paths.append(directory / "plans" / solver_name / f"{instance.id}.json.gz")
    cached = pair_dir / instance.id
    if cached.is_dir():
        paths.extend(sorted(cached.glob(f"*/{solver_name}.json.gz"), reverse=True))
    paths.append(directory / "replays" / solver_name / f"{instance.id}.rerun.json.gz")
    if not force:
        for path in paths:
            if path.is_file():
                plan = load_plan(path)
                if plan.get("instance_id") != instance.id or plan.get("solver") != solver_name:
                    raise ValueError("saved plan belongs to another scenario or solver")
                metadata_path = path.with_name(path.name.removesuffix(".json.gz") + ".metadata.json")
                if not metadata_path.is_file() and path.name.endswith(".rerun.json.gz"):
                    metadata_path = path.with_name(path.name.removesuffix(".rerun.json.gz") + ".rerun-metadata.json")
                if metadata_path.is_file():
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                    plan["provenance"] = metadata.get("source_provenance") or (
                        "fingerprinted archive" if metadata.get("source_root") else
                        "pinned PHANS" if manifest["solvers"][solver_name] is None else "current Python adapter"
                    )
                    plan["replay_attempt"] = True
                return prepare_replay_trace(plan, instance)

    budget = row["timeout_s"] if timeout is None else timeout
    if budget is None or not 0 < budget < float("inf"):
        raise ValueError("replay timeout must be finite and positive")
    entrypoint = manifest["solvers"][solver_name]
    archive = archived_source(directory, manifest) if entrypoint else None
    generation_dir.mkdir(parents=True, exist_ok=True)
    plan_path = generation_dir / f"{solver_name}.json.gz"
    with tempfile.TemporaryDirectory(prefix="mapf-hd-replay-") as temporary:
        baseline_root = Path(temporary) / "baseline"
        if entrypoint is None:
            extract_baseline(baseline_root)
        attempt = run_attempt(
            Solver(solver_name, entrypoint), instance, budget, baseline_root,
            generation_dir / f"{solver_name}.log", plan_path, source_root=archive,
        )
    provenance = "fingerprinted archive" if archive else "pinned PHANS" if entrypoint is None else "current Python adapter"
    metadata = {
        "instance_id": instance.id, "solver": solver_name,
        "recorded_status": row["status"], "recorded_makespan": row["makespan"],
        "rerun_status": attempt.status, "rerun_makespan": attempt.makespan,
        "rerun_time_s": attempt.computation_time_s, "timeout_s": budget,
        "source_root": str(archive) if archive else None, "source_provenance": provenance,
        "solver_source_sha256": attempt.source_sha256, "detail": attempt.detail,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (generation_dir / f"{solver_name}.metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8",
    )
    if attempt.plan_path:
        plan = load_plan(plan_path)
    else:
        plan = {
            "instance_id": instance.id, "solver": solver_name,
            "status": attempt.status, "frames": [instance.starts],
            "trace_available": False, "detail": attempt.detail,
        }
    plan["provenance"] = provenance
    plan["replay_attempt"] = True
    return prepare_replay_trace(plan, instance)


def replay_run(args):
    from .replay import write_paired_replay

    directory = args.run_dir.resolve()
    manifest = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    baseline = args.baseline or manifest["comparison_baseline"]
    candidate = args.solver
    if candidate == baseline:
        raise ValueError("choose a candidate different from the baseline for paired playback")
    names = (baseline, candidate)
    if args.scenario not in manifest["instance_ids"] or any(name not in manifest["solvers"] for name in names):
        raise ValueError("scenario, baseline or candidate is absent from this run")
    if not all(IDENTIFIER.fullmatch(value) for value in (args.scenario, *names)):
        raise ValueError("invalid scenario or solver name")
    pair_dir = directory / "replays" / f"{baseline}-vs-{candidate}"
    destination = args.out or pair_dir / f"{args.scenario}.html"
    if destination.suffix.lower() != ".html" or destination.resolve() == directory / "report.html":
        raise ValueError("replay output must be an HTML player file distinct from report.html")
    if args.timeout is not None and not 0 < args.timeout < float("inf"):
        raise ValueError("replay timeout must be finite and positive")
    instance = Instance.from_json(json.loads(
        inside_run(directory, Path("instances") / f"{args.scenario}.json").read_text(encoding="utf-8")
    ))
    matching = [
        row for row in read_results(directory / "results.csv")
        if row["instance_id"] == args.scenario and row["solver"] in names
    ]
    if len(matching) != 2 or {row["solver"] for row in matching} != set(names):
        raise ValueError("the scenario must have one recorded result for each selected solver")
    result_by_solver = {row["solver"]: row for row in matching}
    generation_dir = pair_dir / args.scenario / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    plans = [
        replay_plan(
            directory, manifest, instance, result_by_solver[name], generation_dir, pair_dir,
            force=args.rerun, timeout=args.timeout,
        )
        for name in names
    ]
    for name, plan in zip(names, plans):
        plan["recorded_status"] = result_by_solver[name]["status"]
        plan["recorded_makespan"] = result_by_solver[name]["makespan"]
    page = write_paired_replay(instance, plans[0], plans[1], destination)
    print(page, flush=True)
    return page
