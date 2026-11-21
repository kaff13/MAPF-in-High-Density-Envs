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
    from .plots import render_plots

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
    filtered = bool(solvers or maps or densities)
    if output is None:
        output = run_dir / "reports" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") if filtered else run_dir
    output = output.resolve()
    if filtered and output == run_dir:
        raise ValueError("filtered reports need a separate output directory")
    if output != run_dir:
        output.mkdir(parents=True, exist_ok=False)
        for folder in ("instances", "logs", "plans", "replays"):
            for row in selected:
                if folder == "instances":
                    relative = Path(folder) / f'{row["instance_id"]}.json'
                elif folder == "plans":
                    if not row.get("plan_path"):
                        continue
                    relative = Path(row["plan_path"])
                else:
                    suffix = ".log" if folder == "logs" else ".html"
                    relative = Path(folder) / row["solver"] / f'{row["instance_id"]}{suffix}'
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
    plots = render_plots(selected, baseline, output / "plots")
    destination = write_html_report(output, selected, baseline, plots)
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


def replay_run(args):
    from .replay import load_plan, write_replay

    directory = args.run_dir.resolve()
    manifest = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    if args.scenario not in manifest["instance_ids"] or args.solver not in manifest["solvers"]:
        raise ValueError("scenario or solver is absent from this run")
    if not IDENTIFIER.fullmatch(args.scenario) or not IDENTIFIER.fullmatch(args.solver):
        raise ValueError("invalid scenario or solver name")
    instance = Instance.from_json(json.loads(
        inside_run(directory, Path("instances") / f"{args.scenario}.json").read_text(encoding="utf-8")
    ))
    rows = read_results(directory / "results.csv")
    row = next((row for row in rows if row["instance_id"] == args.scenario and row["solver"] == args.solver), None)
    if row is None:
        raise ValueError("this scenario and solver have no recorded result")
    replay_dir = directory / "replays" / args.solver
    plan_path = inside_run(directory, row["plan_path"]) if row.get("plan_path") else directory / "plans" / args.solver / f"{args.scenario}.json.gz"
    if args.rerun:
        replay_dir.mkdir(parents=True, exist_ok=True)
        budget = row["timeout_s"] if args.timeout is None else args.timeout
        if budget is None or not 0 < budget < float("inf"):
            raise ValueError("replay timeout must be finite and positive")
        entrypoint = manifest["solvers"][args.solver]
        solver = Solver(args.solver, entrypoint)
        archive = archived_source(directory, manifest) if entrypoint else None
        plan_path = replay_dir / f"{args.scenario}.rerun.json.gz"
        if plan_path.exists():
            raise ValueError("rerun already exists; use replay without --rerun to view it")
        with tempfile.TemporaryDirectory(prefix="mapf-hd-replay-") as temporary:
            baseline_root = Path(temporary) / "baseline"
            if entrypoint is None:
                extract_baseline(baseline_root)
            attempt = run_attempt(
                solver, instance, budget, baseline_root, replay_dir / f"{args.scenario}.log",
                plan_path, source_root=archive,
            )
        rerun_metadata = {
            "instance_id": args.scenario, "solver": args.solver,
            "recorded_status": row["status"], "recorded_makespan": row["makespan"],
            "rerun_status": attempt.status, "rerun_makespan": attempt.makespan,
            "rerun_time_s": attempt.computation_time_s, "timeout_s": budget,
            "source_root": str(archive) if archive else None,
            "source_provenance": "fingerprinted archive" if archive else "pinned PHANS" if entrypoint is None else "current Python adapter",
            "recorded_solver_source_sha256": row.get("solver_source_sha256"),
            "solver_source_sha256": attempt.source_sha256,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "detail": attempt.detail,
        }
        (replay_dir / f"{args.scenario}.rerun-metadata.json").write_text(
            json.dumps(rerun_metadata, indent=2) + "\n", encoding="utf-8",
        )
        if not attempt.plan_path:
            raise ValueError(f"replay attempt returned no trace: {attempt.status}. {attempt.detail}")
    elif not plan_path.is_file():
        rerun_plan = replay_dir / f"{args.scenario}.rerun.json.gz"
        if rerun_plan.is_file():
            plan_path = rerun_plan
        else:
            raise ValueError("no saved trace; add --rerun to obtain a new plan without changing recorded metrics")
    plan = load_plan(plan_path)
    if plan.get("instance_id") != instance.id or plan.get("solver") != args.solver:
        raise ValueError("saved plan belongs to another scenario or solver")
    detail = plan.get("detail", "")
    if plan_path.name.endswith(".rerun.json.gz"):
        metadata_file = replay_dir / f"{args.scenario}.rerun-metadata.json"
        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        source_provenance = metadata.get("source_provenance")
        if source_provenance is None:
            source_provenance = (
                "fingerprinted archive" if metadata.get("source_root") else
                "pinned PHANS" if manifest["solvers"][args.solver] is None else "current Python adapter"
            )
        provenance = {
            "fingerprinted archive": "Исполнены архивные исходники, проверенные по хешам.",
            "pinned PHANS": "Исполнен закреплённый оригинальный PHANS.",
            "current Python adapter": "Исполнена текущая версия Python-адаптера.",
        }[source_provenance]
        detail = "Отдельная попытка для просмотра. Исходные метрики сохранены. " + provenance + " " + detail
    destination = args.out or replay_dir / f"{args.scenario}.html"
    if destination.suffix.lower() != ".html" or destination.resolve() == directory / "report.html":
        raise ValueError("replay output must be an HTML player file distinct from report.html")
    page = write_replay(instance, plan["frames"], destination, solver_name=args.solver, status=plan["status"], detail=detail)
    print(page, flush=True)
    return page
