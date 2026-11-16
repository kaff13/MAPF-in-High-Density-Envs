"""Draw analysis plots from saved results without running solvers."""

from collections import defaultdict
import json
from math import ceil
from statistics import median, quantiles

from .reports import by_solver, group_key, paired_metrics, read_results, solver_pairs

METRIC_LABELS = {
    "success": "Success rate (%)",
    "runtime": "Computation time (s)",
    "makespan": "Makespan (ticks)",
}


def density_plot(axis, rows, kind):
    densities = sorted({row["density_pct"] for row in rows})
    has_values = False
    for solver, solver_rows in by_solver(rows).items():
        by_density = defaultdict(list)
        for row in solver_rows:
            by_density[row["density_pct"]].append(row)
        central, lower, upper = [], [], []
        for density in densities:
            cases = by_density[density]
            solved = [row for row in cases if row["status"] == "solved"]
            if kind == "success":
                central.append(100 * len(solved) / len(cases) if cases else float("nan"))
                continue
            key = "computation_time_s" if kind == "runtime" else "makespan"
            values = [row[key] for row in solved if kind != "runtime" or row[key] > 0]
            center = median(values) if values else float("nan")
            low, high = (center, center) if len(values) < 2 else quantiles(values, n=4, method="inclusive")[::2]
            central.append(center)
            lower.append(low)
            upper.append(high)
        if not any(value == value for value in central):
            continue
        has_values = True
        line, = axis.plot(densities, central, marker="o", label=solver)
        if kind != "success":
            axis.fill_between(densities, lower, upper, color=line.get_color(), alpha=0.15)
    if kind == "success":
        axis.set_ylim(-2, 102)
    if kind == "runtime" and has_values:
        axis.set_yscale("log")
    axis.set_xticks(densities)
    axis.set_xlabel("Target occupancy (%)")
    axis.set_ylabel(METRIC_LABELS[kind])
    if not has_values:
        axis.text(0.5, 0.5, "No solved runs", transform=axis.transAxes, ha="center")


def budget_plot(axis, rows):
    limit = max(row["timeout_s"] for row in rows)
    for solver, cases in by_solver(rows).items():
        times = sorted(row["computation_time_s"] for row in cases if row["status"] == "solved")
        fractions = [100 * count / len(cases) for count in range(1, len(times) + 1)]
        axis.step([0, *times, limit], [0, *fractions, 100 * len(times) / len(cases)], where="post", label=solver)
    axis.set_xlim(0, limit)
    axis.set_ylim(-2, 102)
    axis.set_xlabel("Time budget (s)")
    axis.set_ylabel("All tasks solved by budget (%)")


def paired_plot(axis, rows, baseline):
    has_points = False
    for candidate, pairs in solver_pairs(rows, baseline):
        measurements = [
            paired_metrics(reference, attempt)
            for reference, attempt in pairs
            if reference["status"] == attempt["status"] == "solved"
        ]
        measurements = [(speedup, delta) for speedup, delta in measurements if speedup is not None]
        if measurements:
            has_points = True
            speedups, deltas = zip(*measurements)
            axis.scatter(speedups, deltas, alpha=0.65, label=candidate)
    axis.axvline(1, color="0.5", linestyle="--", linewidth=1)
    axis.axhline(0, color="0.5", linestyle="--", linewidth=1)
    axis.set_xscale("log")
    axis.set_xlabel(f"Speedup relative to {baseline}")
    axis.set_ylabel("Candidate − baseline makespan (ticks)")
    if not has_points:
        axis.text(0.5, 0.5, "No common solved tasks", transform=axis.transAxes, ha="center")


def plot_results(args):
    rows = read_results(args.run_dir / "results.csv")
    manifest = json.loads((args.run_dir / "run.json").read_text(encoding="utf-8"))
    expected = {(case, solver) for case in manifest["instance_ids"] for solver in manifest["solvers"]}
    actual = {(row["instance_id"], row["solver"]) for row in rows}
    if expected != actual or len(rows) != len(expected):
        raise ValueError("run is incomplete or its results differ from the manifest")
    baseline = manifest["comparison_baseline"]
    selected = [
        row for row in rows
        if (not args.maps or row["map"] in args.maps)
        and (not args.density or row["density_pct"] in args.density)
    ]
    if not selected or not any(not args.solvers or row["solver"] in args.solvers for row in selected):
        raise ValueError("no rows match the plot filters")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plot_dir = args.run_dir / "plots"
    plot_dir.mkdir(exist_ok=True)
    # Filtered charts have their own output folder so an earlier report stays intact.
    if args.maps or args.density or args.solvers:
        filters = [
            "-".join(args.maps or ["maps"]),
            "-".join(map(str, args.density or ())) or "densities",
            "-".join(args.solvers or ["solvers"]),
        ]
        if not all(value.replace("-", "").replace("_", "").isalnum() for value in filters):
            raise ValueError("invalid plot filter")
        plot_dir = plot_dir / "__".join(filters)
        plot_dir.mkdir(exist_ok=True)
    for kind in args.kind:
        panels = defaultdict(list)
        for row in selected:
            if not args.solvers or row["solver"] in args.solvers or (kind == "paired" and row["solver"] == baseline):
                map_id, _, targets = group_key(row)
                panels[(map_id, targets)].append(row)
        columns = min(2, len(panels))
        height = ceil(len(panels) / columns)
        figure, axes = plt.subplots(height, columns, figsize=(6 * columns, 3.8 * height), squeeze=False, layout="constrained")
        for axis, ((map_id, targets), panel) in zip(axes.flat, sorted(panels.items())):
            if kind == "budget":
                budget_plot(axis, panel)
            elif kind == "paired":
                paired_plot(axis, panel, baseline)
            else:
                density_plot(axis, panel, kind)
            axis.set_title(f"{map_id} · {targets} goals")
            axis.grid(alpha=0.2)
            _, labels = axis.get_legend_handles_labels()
            if labels:
                axis.legend()
        for axis in list(axes.flat)[len(panels):]:
            axis.set_visible(False)
        target = plot_dir / f"{kind}.png"
        figure.savefig(target, dpi=140)
        plt.close(figure)
        print(target)
