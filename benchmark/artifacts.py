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


def build_report_replays(directory, rows, baseline, solver_labels=None):
    """Create offline paired players from the traces already saved in a run."""
    from .replay import load_plan, write_paired_replay

    solver_labels = solver_labels or {}
    grouped = {}
    for row in rows:
        grouped.setdefault(row["instance_id"], {})[row["solver"]] = row
    candidates = sorted({row["solver"] for row in rows if row["solver"] != baseline})
    pages = []
    for instance_id, solver_rows in sorted(grouped.items()):
        if baseline not in solver_rows:
            continue
        instance_path = inside_run(directory, Path("instances") / f"{instance_id}.json")
        if not instance_path.is_file():
            continue
        instance = Instance.from_json(json.loads(instance_path.read_text(encoding="utf-8")))
        for candidate in candidates:
            if candidate not in solver_rows:
                continue
            plans = []
            for name in (baseline, candidate):
                row = solver_rows[name]
                path = inside_run(directory, row["plan_path"]) if row.get("plan_path") else None
                if path is not None and path.is_file():
                    plan = load_plan(path)
                else:
                    plan = {
                        "instance_id": instance_id, "solver": name,
                        "status": row["status"], "frames": [instance.starts],
                        "trace_available": False, "detail": row.get("detail", ""),
                    }
                plan["recorded_status"] = row["status"]
                plan["recorded_makespan"] = row["makespan"]
                plans.append(plan)
            relative = Path("replays") / f"{baseline}-vs-{candidate}" / f"{instance_id}.html"
            write_paired_replay(
                instance, plans[0], plans[1], inside_run(directory, relative),
                baseline_name=solver_labels.get(baseline, "PHANS"),
                candidate_name=solver_labels.get(candidate, candidate),
            )
            before, after = solver_rows[baseline], solver_rows[candidate]
            baseline_solved = before["status"] == "solved"
            candidate_solved = after["status"] == "solved"
            delta = after["makespan"] - before["makespan"] if baseline_solved and candidate_solved else None
            if baseline_solved and candidate_solved:
                category = "candidate_better" if delta < 0 else "baseline_better" if delta > 0 else "equal"
            elif candidate_solved:
                category = "candidate_only"
            elif baseline_solved:
                category = "baseline_only"
            else:
                category = "neither"
            pages.append({
                "scenario": instance_id, "map": before["map"],
                "density": before["density_pct"], "seed": before["seed"],
                "solver": candidate, "baseline_status": before["status"],
                "status": after["status"], "makespan_delta": delta,
                "category": category, "path": relative.as_posix(),
            })
    return pages


def read_run(directory, *, allow_incomplete=False):
    directory = directory.resolve()
    manifest = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    rows = read_results(directory / "results.csv")
    validate_results(rows, manifest, require_complete=not allow_incomplete)
    return manifest, rows


def inside_run(directory, relative):
    root = directory.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("artifact path must stay inside its run directory")
    return path


def _load_report_sources(run_dirs):
    directories = [Path(path).resolve() for path in run_dirs]
    if not directories:
        raise ValueError("provide at least one source run folder")
    if len(directories) != len(set(directories)):
        raise ValueError("the same source run folder was supplied more than once")

    manifests, rows, origins = [], [], {}
    baseline = dataset_version = phans_commit = None
    solver_entries, seen, scenario_metadata = {}, {}, {}
    for directory in directories:
        manifest, source_rows = read_run(directory, allow_incomplete=True)
        if baseline is None:
            baseline = manifest["comparison_baseline"]
        elif manifest["comparison_baseline"] != baseline:
            raise ValueError("all source runs must use the same comparison baseline")
        if dataset_version is None:
            dataset_version = manifest.get("dataset_version")
        elif manifest.get("dataset_version") != dataset_version:
            raise ValueError("all source runs must use the same dataset version")
        if manifest.get("phans_commit"):
            if phans_commit is None:
                phans_commit = manifest["phans_commit"]
            elif manifest["phans_commit"] != phans_commit:
                raise ValueError("all source runs must use the same pinned PHANS baseline")

        for name, entrypoint in manifest["solvers"].items():
            if name in solver_entries and solver_entries[name] != entrypoint:
                raise ValueError(f"solver {name!r} has different entrypoints across source runs")
            solver_entries[name] = entrypoint

        for row in source_rows:
            key = (row["instance_id"], row["solver"])
            metadata = (row["map"], row["density_pct"], row["seed"], row["targets"])
            previous_metadata = scenario_metadata.setdefault(row["instance_id"], metadata)
            if previous_metadata != metadata:
                raise ValueError(f"scenario metadata differs across source runs for {row['instance_id']}")
            if key in seen:
                index, previous_row = seen[key]
                previous_hash = previous_row.get("solver_source_sha256")
                current_hash = row.get("solver_source_sha256")
                if previous_hash and current_hash and previous_hash != current_hash:
                    raise ValueError(f"solver source differs for duplicate scenario {key[0]} and solver {key[1]}")
                if row == previous_row:
                    continue
                if row["timeout_s"] == previous_row["timeout_s"]:
                    raise ValueError(f"duplicate result with the same time limit for scenario {key[0]} and solver {key[1]}")
                if row["timeout_s"] > previous_row["timeout_s"]:
                    rows[index] = row
                    origins[key] = directory
                    seen[key] = (index, row)
                continue
            seen[key] = (len(rows), row)
            rows.append(row)
            origins[key] = directory
        manifests.append((directory, manifest))

    if not rows:
        raise ValueError("source runs contain no recorded results")
    return directories, manifests, rows, origins, baseline, solver_entries


def _copy_report_artifacts(output, selected, origins):
    copied_instances = set()
    for row in selected:
        directory = origins[(row["instance_id"], row["solver"])]
        instance_id = row["instance_id"]
        instance_relative = Path("instances") / f"{instance_id}.json"
        source_instance = inside_run(directory, instance_relative)
        if not source_instance.is_file():
            raise ValueError(f"missing saved instance {instance_id} in {directory}")
        target_instance = inside_run(output, instance_relative)
        if instance_id not in copied_instances:
            target_instance.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_instance, target_instance)
            copied_instances.add(instance_id)
        elif source_instance.read_bytes() != target_instance.read_bytes():
            raise ValueError(f"saved instance differs across source runs for {instance_id}")

        relatives = [Path(row["plan_path"])] if row.get("plan_path") else []
        relatives.append(Path("logs") / row["solver"] / f"{instance_id}.log")
        for relative in relatives:
            source = inside_run(directory, relative)
            if source.is_file():
                target = inside_run(output, relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.copy2(source, target)


def build_report(run_dirs, *, output=None, solvers=None, maps=None, densities=None, solver_labels=None):
    from .plots import REPORT_PLOT_NAMES, render_plots

    if isinstance(run_dirs, (str, Path)):
        run_dirs = [run_dirs]
    directories, manifests, rows, origins, baseline, solver_entries = _load_report_sources(run_dirs)
    manifest_labels = {}
    for _, source_manifest in manifests:
        manifest_labels.update(source_manifest.get("solver_labels", {}))
    solver_labels = manifest_labels | (solver_labels or {})
    if any(name not in solver_entries for name in solver_labels):
        raise ValueError("display label names an unknown solver")
    solver_labels.setdefault(baseline, "PHANS")
    if solvers and any(name not in solver_entries for name in solvers):
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
    candidates = {row["solver"] for row in selected} - {baseline}
    if len(candidates) != 1:
        raise ValueError("a report compares PHANS with one modification; select one with --solver NAME")
    if any(not IDENTIFIER.fullmatch(row["map"]) for row in selected):
        raise ValueError("invalid map ID in report data")

    filtered = bool(solvers or maps or densities)
    if output is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        if len(directories) > 1:
            output = Path("benchmark-results") / f"combined-report-{timestamp}"
        else:
            output = directories[0] / "reports" / timestamp if filtered else directories[0]
    output = output.resolve()
    if len(directories) > 1 and output in directories:
        raise ValueError("a combined report needs its own output folder")
    if filtered and len(directories) == 1 and output == directories[0]:
        raise ValueError("filtered reports need a separate output directory")

    if output not in directories:
        output.mkdir(parents=True, exist_ok=False)
        _copy_report_artifacts(output, selected, origins)
        chosen_solvers = {row["solver"] for row in selected}
        manifest = {
            "dataset_version": manifests[0][1].get("dataset_version"),
            "comparison_baseline": baseline,
            "solvers": {name: entry for name, entry in solver_entries.items() if name in chosen_solvers},
            "solver_labels": {name: label for name, label in solver_labels.items() if name in chosen_solvers},
            "instance_ids": sorted({row["instance_id"] for row in selected}),
            "timeout_budgets_s": sorted({row["timeout_s"] for row in selected}),
        }
        for key in ("phans_commit", "phans_parameters"):
            values = [source_manifest.get(key) for _, source_manifest in manifests]
            if values and values[0] is not None and all(value == values[0] for value in values):
                manifest[key] = values[0]
        manifest["source_runs"] = [
            {"path": str(directory), "started_at": source_manifest.get("started_at"),
             "finished_at": source_manifest.get("finished_at"), "timeout_s": source_manifest.get("timeout_s")}
            for directory, source_manifest in manifests
        ]
        manifest["report_created_at"] = datetime.now(timezone.utc).isoformat()
        manifest["report_filters"] = {"solvers": solvers, "maps": maps, "densities": densities}
        from .__main__ import instance_set_hash

        instances = [
            Instance.from_json(json.loads((output / "instances" / f"{case}.json").read_text(encoding="utf-8")))
            for case in manifest["instance_ids"]
        ]
        manifest["instance_set_sha256"] = instance_set_hash(instances)
        (output / "run.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        fields = list(dict.fromkeys([*RESULT_FIELDS, *(key for row in selected for key in row)]))
        write_csv(output / "results.csv", fields, selected)

    write_reports(output, selected, baseline)
    plots = render_plots(selected, baseline, output / "plots", REPORT_PLOT_NAMES, solver_labels=solver_labels)
    map_plots = {}
    for map_id in sorted({row["map"] for row in selected}):
        cases = [row for row in selected if row["map"] == map_id]
        map_output = output / "maps" / map_id
        map_output.mkdir(parents=True, exist_ok=True)
        write_reports(map_output, cases, baseline)
        fields = list(dict.fromkeys([*RESULT_FIELDS, *(key for row in cases for key in row)]))
        write_csv(map_output / "results.csv", fields, cases)
        map_plots[map_id] = render_plots(cases, baseline, map_output / "plots", REPORT_PLOT_NAMES,
                                         solver_labels=solver_labels)
    replays = build_report_replays(output, selected, baseline, solver_labels)
    destination = write_html_report(output, selected, baseline, plots, map_plots=map_plots,
                                    replays=replays, solver_labels=solver_labels)
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
