"""Render descriptive figures: failures never become relative measurements."""

from collections import defaultdict
from hashlib import sha256
import json
from math import ceil, isfinite
from pathlib import Path
from statistics import median, quantiles

from .reports import by_solver, group_key, solver_pairs

PLOT_NAMES = (
    "success", "runtime", "makespan", "budget", "paired", "runtime_box",
    "makespan_box", "success_box", "success_heatmap",
)
METRIC_LABELS = {
    "success": "Решённые задачи (%)",
    "runtime": "Сокращение времени (%)",
    "makespan": "Сокращение makespan (%)",
}


def solver_color(solver):
    """Keep colors stable across figures, runs, and filter selections."""
    palette = ("#2563eb", "#ea580c", "#059669", "#7c3aed", "#dc2626",
               "#0891b2", "#a16207", "#db2777", "#4d7c0f", "#475569")
    index = int.from_bytes(sha256(solver.encode("utf-8")).digest()[:4], "big") % len(palette)
    return palette[index]


def _valid_number(value, positive=False):
    return isinstance(value, (int, float)) and isfinite(value) and (value > 0 if positive else value >= 0)


def relative_values(rows, baseline, metric):
    """Percent reductions for common solutions, excluding zero baselines."""
    from .reports import pair_rows

    key = {"runtime": "time_reduction_pct", "makespan": "makespan_reduction_pct"}[metric]
    values = {solver: [] for solver in sorted(by_solver(rows)) if solver != baseline}
    for pair in pair_rows(rows, baseline):
        value = pair[key]
        if pair["both_solved"] and value is not None and isfinite(value):
            values[pair["solver"]].append(value)
    return values


def success_values(rows):
    """One equally weighted rate per map × density × targets group."""
    observations = {}
    for solver, cases in sorted(by_solver(rows).items()):
        groups = defaultdict(list)
        for row in cases:
            groups[group_key(row)].append(row)
        observations[solver] = [
            100 * sum(row["status"] == "solved" for row in group) / len(group)
            for _, group in sorted(groups.items())
        ]
    return observations


def _empty(axis, message="Нет общих решённых задач"):
    axis.text(0.5, 0.5, message, transform=axis.transAxes, ha="center", va="center", color="0.4",
              bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9})


def density_plot(axis, rows, kind, baseline=None):
    """Success on all attempts; paired reductions or explicit solved-only data."""
    densities = sorted({row["density_pct"] for row in rows})
    has_values = False
    for solver, solver_rows in sorted(by_solver(rows).items()):
        if kind != "success" and solver == baseline:
            continue
        centers, lower, upper, counts = [], [], [], []
        for density in densities:
            cases = [row for row in solver_rows if row["density_pct"] == density]
            if kind == "success":
                values = [100.0 * (row["status"] == "solved") for row in cases]
                center = sum(values) / len(values) if values else float("nan")
                low = high = center
            else:
                if baseline is not None:
                    panel = [row for row in rows if row["density_pct"] == density]
                    values = relative_values(panel, baseline, kind).get(solver, [])
                else:
                    key = "computation_time_s" if kind == "runtime" else "makespan"
                    values = [row[key] for row in cases if row["status"] == "solved" and _valid_number(row[key])]
                center = median(values) if values else float("nan")
                low, high = ((center, center) if len(values) < 2 else
                             quantiles(values, n=4, method="inclusive")[::2])
            centers.append(center)
            lower.append(low)
            upper.append(high)
            counts.append(len(values))
        if not any(isfinite(value) for value in centers):
            continue
        has_values = True
        color = solver_color(solver)
        axis.plot(densities, centers, marker="o", label=solver, color=color)
        if kind != "success":
            axis.fill_between(densities, lower, upper, color=color, alpha=0.13)
        for density, value, count in zip(densities, centers, counts):
            if isfinite(value):
                axis.annotate(f"n={count}", (density, value), xytext=(3, 6),
                              textcoords="offset points", fontsize=7, color=color)
    if kind == "success":
        axis.set_ylim(-3, 110)
    elif baseline is not None:
        axis.axhline(0, color="0.45", linestyle="--", linewidth=1, label=f"{baseline}: 0%")
    axis.set_xticks(densities)
    axis.set_xlabel("Плотность размещения (%)")
    ylabel = METRIC_LABELS[kind]
    if baseline is None and kind != "success":
        ylabel = "Время (с), только решения" if kind == "runtime" else "Makespan (такты), только решения"
    axis.set_ylabel(ylabel)
    axis.margins(y=0.15)
    if not has_values:
        _empty(axis, "Нет попыток" if kind == "success" else "Нет подходящих решённых задач")


def budget_plot(axis, rows):
    limit = min(row["timeout_s"] for row in rows)
    for solver, cases in sorted(by_solver(rows).items()):
        times = sorted(row["computation_time_s"] for row in cases
                       if row["status"] == "solved" and row["computation_time_s"] <= limit)
        points = [0, *sorted(set(times)), limit]
        fractions = [100 * sum(time <= point for time in times) / len(cases) for point in points]
        axis.step(points, fractions, where="post", label=f"{solver} (N={len(cases)})", color=solver_color(solver))
    axis.set_xlim(0, limit)
    axis.set_ylim(-2, 104)
    axis.set_xlabel("Бюджет времени (с)")
    axis.set_ylabel("Решено к этому времени (% всех задач)")


def paired_plot(axis, rows, baseline):
    has_points = False
    for candidate, pairs in sorted(solver_pairs(rows, baseline)):
        measurements = []
        for reference, attempt in pairs:
            if reference["status"] != "solved" or attempt["status"] != "solved":
                continue
            before, after = reference["computation_time_s"], attempt["computation_time_s"]
            if _valid_number(before, positive=True) and _valid_number(after, positive=True):
                measurements.append((before / after, attempt["makespan"] - reference["makespan"]))
        if measurements:
            has_points = True
            speedups, deltas = zip(*measurements)
            axis.scatter(speedups, deltas, alpha=0.65, s=25, edgecolors="white", linewidths=0.3,
                         label=f"{candidate} (n={len(measurements)})", color=solver_color(candidate))
    axis.axvline(1, color="0.5", linestyle="--", linewidth=1)
    axis.axhline(0, color="0.5", linestyle="--", linewidth=1)
    axis.set_xscale("log")
    axis.set_xlabel(f"Ускорение: время {baseline} / время кандидата")
    axis.set_ylabel("Makespan кандидата − базы (такты)")
    if not has_points:
        _empty(axis, "Нет общих решений с положительным временем")


def _box_plot(axis, observations, ylabel, relative=False):
    """Q1–Q3 boxes, medians, 1.5-IQR whiskers, and every observation."""
    solvers = sorted(observations)
    any_values = False
    for index, solver in enumerate(solvers, 1):
        values = observations[solver]
        if not values:
            continue
        any_values = True
        color = solver_color(solver)
        axis.boxplot([values], positions=[index], widths=0.48, patch_artist=True,
                     showfliers=False, whis=1.5,
                     boxprops={"facecolor": color, "alpha": 0.23, "edgecolor": color},
                     medianprops={"color": "#111827", "linewidth": 1.7},
                     whiskerprops={"color": color}, capprops={"color": color})
        offsets = [0] if len(values) == 1 else [0.18 * ((i * 0.61803398875) % 1 - 0.5) for i in range(len(values))]
        axis.scatter([index + offset for offset in offsets], values,
                     color=color, s=17, alpha=0.48, edgecolors="white", linewidths=0.3, zorder=3)
    axis.set_xticks(range(1, len(solvers) + 1), [f"{solver}\nn={len(observations[solver])}" for solver in solvers])
    if len(solvers) > 4:
        axis.tick_params(axis="x", labelsize=8)
        for label in axis.get_xticklabels():
            label.set_rotation(25)
            label.set_ha("right")
    if solvers:
        axis.set_xlim(0.4, len(solvers) + 0.6)
    if relative:
        axis.axhline(0, color="0.4", linewidth=1, linestyle="--")
    else:
        axis.set_ylim(-3, 103)
    axis.set_ylabel(ylabel)
    axis.margins(y=0.1)
    if not any_values:
        _empty(axis)


def _success_heatmap(figure, axis, rows):
    import numpy as np

    solvers = sorted(by_solver(rows))
    groups = sorted({group_key(row) for row in rows})
    cells = defaultdict(list)
    for row in rows:
        cells[(group_key(row), row["solver"])].append(row)
    rates = np.full((len(groups), len(solvers)), np.nan)
    for y, group in enumerate(groups):
        for x, solver in enumerate(solvers):
            cases = cells[(group, solver)]
            if not cases:
                axis.text(x, y, "—", ha="center", va="center", color="0.5", fontsize=8)
                continue
            solved = sum(row["status"] == "solved" for row in cases)
            value = 100 * solved / len(cases)
            rates[y, x] = value
            axis.text(x, y, f"{value:.0f}%\n{solved}/{len(cases)}", ha="center", va="center",
                      color="white" if value >= 65 else "#111827", fontsize=8)
    heatmap = axis.imshow(np.ma.masked_invalid(rates), cmap="YlGnBu", vmin=0, vmax=100, aspect="auto")
    axis.set_xticks(range(len(solvers)), solvers)
    axis.set_yticks(range(len(groups)), [f"{map_id} · {density}% · целей: {targets}" for map_id, density, targets in groups])
    axis.set_xlabel("Алгоритм")
    axis.grid(False)
    figure.colorbar(heatmap, ax=axis, label="Решённые задачи (%)", shrink=0.8)


def _panels(rows):
    panels = defaultdict(list)
    for row in rows:
        map_id, _, targets = group_key(row)
        panels[(map_id, targets)].append(row)
    return [(f"{map_id} · целей: {targets}", panel) for (map_id, targets), panel in sorted(panels.items())]


def _validate_rows(rows):
    if not rows:
        raise ValueError("no rows to plot")
    seen = set()
    instances = {}
    for row in rows:
        key = row["instance_id"], row["solver"]
        if key in seen:
            raise ValueError(f"duplicate result for instance/solver: {key}")
        seen.add(key)
        metadata = (*group_key(row), row["timeout_s"])
        if row["instance_id"] in instances and instances[row["instance_id"]] != metadata:
            raise ValueError(f"inconsistent instance metadata: {row['instance_id']}")
        instances[row["instance_id"]] = metadata
        if row["status"] not in {"solved", "timeout", "unsolved", "invalid", "crash"}:
            raise ValueError(f"unknown result status: {key}")
        if not _valid_number(row["timeout_s"], positive=True):
            raise ValueError(f"invalid timeout: {key}")
        if row["status"] == "solved":
            if not all(_valid_number(row[field]) for field in ("computation_time_s", "makespan")):
                raise ValueError(f"invalid solved metrics: {key}")
            if row["computation_time_s"] > row["timeout_s"]:
                raise ValueError(f"solved runtime exceeds its timeout: {key}")


def render_plots(rows, baseline, output_dir, kinds=None):
    """Save PNG and SVG charts without needing a manifest; return paths.

    Relative samples use pairwise common solutions. Success-box samples are
    scenario-group rates. Invalid observations fail before any file is written.
    """
    rows = list(rows)
    _validate_rows(rows)
    kinds = list(PLOT_NAMES if kinds is None else ([kinds] if isinstance(kinds, str) else kinds))
    if not kinds or any(kind not in PLOT_NAMES for kind in kinds):
        raise ValueError(f"plot kinds must be selected from {', '.join(PLOT_NAMES)}")
    kinds = list(dict.fromkeys(kinds))
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none"}):
        for kind in kinds:
            panels = _panels(rows)
            if kind in ("runtime_box", "makespan_box"):
                panels = [("Все выбранные задачи", rows), *panels] if len(panels) > 1 else panels
            if kind in ("success_box", "success_heatmap"):
                panels = [("Все выбранные группы", rows)]
            columns = min(2, len(panels))
            height = ceil(len(panels) / columns)
            size = (7.2 * columns, 4.6 * height)
            if kind == "success_box":
                size = (max(8, 1.4 * len(by_solver(rows))), 4.8)
            if kind == "success_heatmap":
                size = (max(8, 2 * len(by_solver(rows)) + 4), max(3.8, 0.57 * len({group_key(row) for row in rows}) + 2))
            figure, axes = plt.subplots(height, columns, figsize=size, squeeze=False, layout="constrained")
            absolute_only = kind in ("runtime", "makespan") and set(by_solver(rows)) == {baseline}
            try:
                for axis, (title, panel) in zip(axes.flat, panels):
                    if kind == "budget":
                        budget_plot(axis, panel)
                    elif kind == "paired":
                        paired_plot(axis, panel, baseline)
                    elif kind in ("runtime_box", "makespan_box"):
                        metric = kind.removesuffix("_box")
                        _box_plot(axis, relative_values(panel, baseline, metric), METRIC_LABELS[metric], relative=True)
                    elif kind == "success_box":
                        _box_plot(axis, success_values(panel), "Доля решений в группе (%)")
                    elif kind == "success_heatmap":
                        _success_heatmap(figure, axis, panel)
                    else:
                        density_plot(axis, panel, kind, None if absolute_only else baseline)
                    axis.set_title(title, fontsize=11, pad=12)
                    if kind != "success_heatmap":
                        axis.grid(axis="y", alpha=0.2)
                        axis.set_axisbelow(True)
                    _, labels = axis.get_legend_handles_labels()
                    if labels:
                        axis.legend(fontsize=8, loc="best")
                for axis in list(axes.flat)[len(panels):]:
                    axis.set_visible(False)
                if absolute_only:
                    title = "Время решения (с)" if kind == "runtime" else "Makespan решений (такты)"
                    note = "Только решённые задачи; линия: медиана; полоса: Q1–Q3; n = число решений."
                elif kind in ("runtime", "makespan", "runtime_box", "makespan_box"):
                    metric = "времени" if kind.startswith("runtime") else "makespan"
                    title = f"Сокращение {metric} относительно {baseline}"
                    note = "100 × (база − кандидат) / база; только общие решения с базой > 0; n = число пар."
                    if kind.endswith("_box"):
                        note += "\nТочки: все пары; ящик: Q1–Q3 и медиана; усы: 1,5 IQR."
                    else:
                        note += "\nЛиния: медиана; полоса: Q1–Q3. Наборы пар могут различаться между кандидатами."
                elif kind == "success_box":
                    title = "Распределение доли решений по группам"
                    note = "Одна точка = map × density × targets; группы имеют одинаковый вес; n = число групп.\nЯщик: Q1–Q3 и медиана; усы: 1,5 IQR. Все статусы входят в знаменатель."
                elif kind == "success_heatmap":
                    title = "Доля решений в каждой группе"
                    note = "Ячейка: процент и решено / всего; все статусы входят в знаменатель."
                elif kind == "paired":
                    title = f"Время и makespan на общих решениях с {baseline}"
                    note = "Одна точка = общая решённая задача; оба времени > 0. Справа — ускорение, ниже — меньше тактов."
                elif kind == "budget":
                    title = "Доля решённых задач при разном бюджете времени"
                    note = "Знаменатель: все задачи алгоритма; учитываются только валидные решения.\nОбщая ось времени ограничена минимальным лимитом выбранных попыток."
                else:
                    title = "Доля решённых задач по плотности"
                    note = "В знаменателе все задачи; n = число попыток."
                figure.suptitle(title, fontsize=14, fontweight="bold")
                figure.supxlabel(note, fontsize=8, color="0.35")
                for extension in ("png", "svg"):
                    target = output_dir / f"{kind}.{extension}"
                    figure.savefig(target, dpi=160, bbox_inches="tight")
                    paths.append(target)
            finally:
                plt.close(figure)
    return paths


def plot_results(args):
    """CLI adapter: validate the full run before applying plot filters."""
    from .reports import read_results, validate_results

    rows = read_results(args.run_dir / "results.csv")
    manifest = json.loads((args.run_dir / "run.json").read_text(encoding="utf-8"))
    validate_results(rows, manifest)
    baseline = manifest["comparison_baseline"]
    selected = [row for row in rows
                if (not args.maps or row["map"] in args.maps)
                and (not args.density or row["density_pct"] in args.density)]
    visible = [row for row in selected if not args.solvers or row["solver"] in args.solvers]
    if not visible:
        raise ValueError("no rows match the plot filters")
    plot_dir = args.run_dir / "plots"
    if args.maps or args.density or args.solvers:
        filters = ["-".join(args.maps or ["maps"]),
                   "-".join(map(str, args.density or ())) or "densities",
                   "-".join(args.solvers or ["solvers"])]
        if not all(value.replace("-", "").replace("_", "").isalnum() for value in filters):
            raise ValueError("invalid plot filter")
        plot_dir = plot_dir / "__".join(filters)
    for kind in args.kind:
        data = visible
        if kind in ("runtime", "makespan", "runtime_box", "makespan_box", "paired"):
            data = [row for row in selected if not args.solvers or row["solver"] in args.solvers or row["solver"] == baseline]
        for path in render_plots(data, baseline, plot_dir, [kind]):
            print(path)
