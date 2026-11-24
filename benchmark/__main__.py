"""Run and inspect the MAPF-HD benchmark from a PHANS checkout."""

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
import math
import platform
from pathlib import Path
import subprocess
import sys
import tempfile

from .maps import DATASET_VERSION, DEFAULT_DENSITIES, DEFAULT_SEEDS, MAPS, Instance, parse_scenario, scenario_ids
from .reports import RESULT_FIELDS, write_reports
from .runner import PHANS_COMMIT, PHANS_PARAMETERS, ROOT, Solver, extract_baseline, run_attempt
from .plots import REPORT_PLOT_NAMES

PLOT_NAMES = ("success", "runtime", "makespan", "budget", "paired",
              "runtime_box", "makespan_box", "success_box", "success_heatmap")


def add_profile_arguments(parser):
    parser.add_argument("--density", nargs="+", type=int, help="target occupancy in percent")
    parser.add_argument("--seeds", type=int, help="use seeds 0 through N-1 (default: 10)")


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    catalogue = commands.add_parser("list", help="list maps, or scenario IDs on one map")
    catalogue.add_argument("--map", choices=MAPS)
    add_profile_arguments(catalogue)

    run = commands.add_parser("run", help="run one scenario, one map, or the six-map pool")
    selection = run.add_mutually_exclusive_group(required=True)
    selection.add_argument("--scenario", help="scenario ID or a saved instance JSON")
    selection.add_argument("--map", choices=MAPS)
    selection.add_argument("--pool", action="store_true")
    add_profile_arguments(run)
    run.add_argument("--solver", action="append", help="repeat 'phans' or NAME=module:function (default: phans)")
    run.add_argument("--baseline", default="phans", help="solver name used in paired comparisons")
    run.add_argument("--timeout", type=float, default=180, metavar="SECONDS")
    run.add_argument("--out", type=Path, help="a new output directory")

    report = commands.add_parser("report", help="build an HTML report from one or more benchmark runs")
    report.add_argument("run_dirs", nargs="+", type=Path,
                        help="one or more run folders containing run.json and results.csv")
    report.add_argument("--out", type=Path, help="new folder for an exported report")
    report.add_argument("--solver", action="append", dest="solvers", help="select solver names")
    report.add_argument("--solver-label", action="append", default=[], metavar="NAME=LABEL",
                        help="display a solver ID under a readable label in the report")
    report.add_argument("--map", action="append", dest="maps")
    report.add_argument("--density", nargs="+", type=int)

    replay = commands.add_parser("replay", help="compare two plans in a synchronized HTML player")
    replay.add_argument("run_dir", type=Path)
    replay.add_argument("--scenario", required=True, help="saved scenario ID")
    replay.add_argument("--solver", required=True, help="candidate name in run.json")
    replay.add_argument("--baseline", help="reference name (default: the run's comparison baseline)")
    replay.add_argument("--rerun", action="store_true", help="recompute both plans for this replay")
    replay.add_argument("--timeout", type=float, help="budget for obtaining a missing or recomputed plan")
    replay.add_argument("--out", type=Path, help="output HTML file")

    plot = commands.add_parser("plot", help="draw PNG plots from a completed run")
    plot.add_argument("run_dir", type=Path)
    plot.add_argument("--kind", nargs="+", choices=PLOT_NAMES, default=REPORT_PLOT_NAMES)
    plot.add_argument("--map", action="append", dest="maps")
    plot.add_argument("--density", nargs="+", type=int)
    plot.add_argument("--solver", action="append", dest="solvers", help="repeat to select solver names")
    return parser


def profile(args):
    densities = tuple(dict.fromkeys(args.density or DEFAULT_DENSITIES))
    seeds = DEFAULT_SEEDS if args.seeds is None else args.seeds
    if seeds < 1 or any(not 1 <= density <= 99 for density in densities):
        raise ValueError("expected a positive seed count and densities from 1 to 99")
    return densities, seeds


def list_catalogue(args):
    if args.map:
        densities, seeds = profile(args)
        for identifier in scenario_ids((args.map,), densities, seeds):
            parse_scenario(identifier)
            print(identifier)
        return
    if args.density is not None or args.seeds is not None:
        raise ValueError("use --map to list scenarios for a particular profile")
    for grid in MAPS.values():
        print(f"{grid.id:16} {grid.width:3}x{grid.height:<3}  {len(grid.goals):2} targets   {len(grid.walls):4} wall cells")


def select_instances(args):
    if args.scenario is not None:
        if args.density is not None or args.seeds is not None:
            raise ValueError("a single scenario already has a fixed density and seed")
        scenario = args.scenario
        if scenario.lower().endswith(".json"):
            return [Instance.from_json(json.loads(Path(scenario).read_text(encoding="utf-8-sig")))]
        return [parse_scenario(scenario)]
    maps = (args.map,) if args.map else tuple(MAPS)
    densities, seeds = profile(args)
    return [parse_scenario(identifier) for identifier in scenario_ids(maps, densities, seeds)]


def git_text(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.stdout.strip() if result.returncode == 0 else None


def dependency_versions():
    versions = {}
    for dependency in ("numpy", "matplotlib"):
        try:
            versions[dependency] = version(dependency)
        except PackageNotFoundError:
            versions[dependency] = None
    return versions


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def instance_set_hash(instances):
    digest = sha256()
    for instance in instances:
        digest.update(json.dumps(instance.to_json(), sort_keys=True, separators=(",", ":")).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def run_benchmark(args):
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        raise ValueError("--timeout must be positive and finite")
    solvers = [Solver.parse(spec) for spec in (args.solver or ["phans"])]
    if len(solvers) != len({solver.name.casefold() for solver in solvers}):
        raise ValueError("solver names must be unique")
    if args.baseline != "phans" and args.baseline not in {solver.name for solver in solvers}:
        raise ValueError("--baseline must name a selected solver")
    instances = select_instances(args)
    timestamp = datetime.now(timezone.utc)
    output = (args.out or Path("benchmark-results") / timestamp.strftime("%Y%m%dT%H%M%S%fZ")).resolve()
    git_head = git_text("rev-parse", "HEAD")
    git_status = git_text("status", "--porcelain")
    with tempfile.TemporaryDirectory(prefix="mapf-hd-") as temporary:
        baseline_root = Path(temporary) / "phans"
        if any(solver.entrypoint is None for solver in solvers):
            extract_baseline(baseline_root)
        output.mkdir(parents=True)
        (output / "instances").mkdir()
        (output / "logs").mkdir()
        write_json(output / "run.json", {
            "dataset_version": DATASET_VERSION,
            "started_at": timestamp.isoformat(),
            "instance_ids": [instance.id for instance in instances],
            "instance_set_sha256": instance_set_hash(instances),
            "solvers": {solver.name: solver.entrypoint for solver in solvers},
            "comparison_baseline": args.baseline,
            "phans_commit": PHANS_COMMIT,
            "phans_parameters": PHANS_PARAMETERS,
            "checkout_commit": git_head,
            "checkout_dirty": bool(git_status) if git_status is not None else None,
            "python": sys.version,
            "platform": platform.platform(),
            "cpu": platform.processor(),
            "dependencies": dependency_versions(),
            "timeout_s": args.timeout,
        })
        results = execute(output, instances, solvers, args.timeout, baseline_root)
        manifest_path = output / "run.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
        write_json(manifest_path, manifest)
        from .artifacts import build_report

        build_report(output)
    print(f"Reports: {output}", flush=True)


def execute(output, instances, solvers, timeout_s, baseline_root):
    rows = []
    for solver in solvers:
        (output / "logs" / solver.name).mkdir()
        (output / "plans" / solver.name).mkdir(parents=True, exist_ok=True)
    with (output / "results.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        for index, instance in enumerate(instances):
            write_json(output / "instances" / f"{instance.id}.json", instance.to_json())
            # Rotate first position so adjacent cases do not always start with the same solver.
            offset = index % len(solvers)
            for solver in solvers[offset:] + solvers[:offset]:
                log = output / "logs" / solver.name / f"{instance.id}.log"
                plan = output / "plans" / solver.name / f"{instance.id}.json.gz"
                attempt = run_attempt(solver, instance, timeout_s, baseline_root, log, plan)
                row = {
                    "instance_id": instance.id, "map": instance.map.id, "density_pct": instance.density,
                    "actual_density_pct": instance.actual_density * 100, "paper_density_pct": instance.paper_density * 100,
                    "empty_cells": instance.empty_cells, "targets": len(instance.map.goals), "seed": instance.seed,
                    "solver": solver.name, "solver_source_sha256": attempt.source_sha256,
                    "status": attempt.status, "computation_time_s": attempt.computation_time_s,
                    "makespan": attempt.makespan, "timeout_s": timeout_s, "detail": attempt.detail,
                    "plan_path": Path(attempt.plan_path).relative_to(output).as_posix() if attempt.plan_path else "",
                }
                writer.writerow(row)
                stream.flush()
                rows.append(row)
                print(f"{len(rows):4}/{len(instances) * len(solvers)}  {instance.id}  {solver.name}  {attempt.status}", flush=True)
    for solver in solvers:
        solved = sum(row["solver"] == solver.name and row["status"] == "solved" for row in rows)
        print(f"{solver.name}: {solved}/{len(instances)} solved ({solved / len(instances):.1%})")
    return rows


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        if args.command == "list":
            list_catalogue(args)
        elif args.command == "run":
            run_benchmark(args)
        elif args.command == "plot":
            from .plots import plot_results

            plot_results(args)
        elif args.command == "report":
            from .artifacts import build_report

            labels = {}
            for item in args.solver_label:
                name, separator, label = item.partition("=")
                if not separator or not name.strip() or not label.strip():
                    raise ValueError("--solver-label must use NAME=LABEL")
                labels[name.strip()] = label.strip()
            build_report(args.run_dirs, output=args.out, solvers=args.solvers, maps=args.maps,
                         densities=args.density, solver_labels=labels)
        elif args.command == "replay":
            from .artifacts import replay_run

            replay_run(args)
    except (KeyError, TypeError, ValueError, OSError, ImportError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
