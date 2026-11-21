"""CSV export and paired comparison over the same instances."""

from collections import defaultdict
import csv
import math
from statistics import median

RESULT_FIELDS = (
    "instance_id", "map", "density_pct", "actual_density_pct", "paper_density_pct",
    "empty_cells", "targets", "seed", "solver", "solver_source_sha256", "status", "computation_time_s",
    "makespan", "timeout_s", "detail", "plan_path",
)
SUMMARY_FIELDS = (
    "map", "density_pct", "targets", "solver", "solved", "total", "success_rate",
    "median_time_s", "median_makespan", "timeouts", "unsolved", "invalid", "crashes",
    "success_rate_gain_pp", "success_rate_change_pct",
    "median_time_reduction_pct", "median_makespan_reduction_pct",
    "both_solved", "time_pairs", "makespan_pairs", "candidate_only", "baseline_only",
)
COMPARISON_FIELDS = (
    "map", "density_pct", "targets", "solver", "baseline", "paired", "both_solved",
    "baseline_only", "candidate_only", "neither_solved", "median_speedup",
    "median_makespan_delta", "shorter", "equal", "longer",
    "success_rate_gain_pp", "success_rate_change_pct",
    "median_time_reduction_pct", "median_makespan_reduction_pct",
    "time_pairs", "makespan_pairs",
)
PAIR_FIELDS = (
    "instance_id", "map", "density_pct", "targets", "solver", "baseline",
    "baseline_status", "status", "both_solved", "outcome",
    "baseline_time_s", "computation_time_s", "baseline_makespan", "makespan",
    "speedup", "makespan_delta", "time_reduction_pct", "makespan_reduction_pct",
)


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_results(path):
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        for key in ("density_pct", "targets", "makespan"):
            row[key] = int(row[key]) if row[key] else None
        for key in ("computation_time_s", "timeout_s"):
            row[key] = float(row[key]) if row[key] else None
        row.setdefault("plan_path", "")
    return rows


def validate_results(rows, manifest):
    expected = {(case, solver) for case in manifest["instance_ids"] for solver in manifest["solvers"]}
    actual = {(row["instance_id"], row["solver"]) for row in rows}
    if actual != expected or len(rows) != len(expected):
        raise ValueError("run is incomplete or its results differ from the manifest")
    groups = {}
    for row in rows:
        key = (row["map"], row["density_pct"], row["targets"], row["timeout_s"])
        previous = groups.setdefault(row["instance_id"], key)
        if previous != key:
            raise ValueError(f"inconsistent scenario metadata or time budgets for {row['instance_id']}")
        if row["status"] not in {"solved", "timeout", "unsolved", "invalid", "crash"}:
            raise ValueError("unknown result status")
        limit = row["timeout_s"]
        time = row["computation_time_s"]
        if limit is None or not math.isfinite(limit) or limit <= 0:
            raise ValueError("invalid time budget")
        if time is not None and (not math.isfinite(time) or time < 0):
            raise ValueError("invalid computation time")
        if row["status"] == "solved":
            if time is None or time > limit or row["makespan"] is None or row["makespan"] < 0:
                raise ValueError("solved result has missing metrics or exceeds its time budget")


def group_key(row):
    return row["map"], row["density_pct"], row["targets"]


def grouped(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[group_key(row)].append(row)
    return groups


def by_solver(rows):
    solvers = defaultdict(list)
    for row in rows:
        solvers[row["solver"]].append(row)
    return solvers


def summarize(rows, key):
    for solver, runs in by_solver(rows).items():
        solved = [row for row in runs if row["status"] == "solved"]
        statuses = [row["status"] for row in runs]
        yield dict(
            zip(SUMMARY_FIELDS[:3], key), solver=solver, solved=len(solved), total=len(runs),
            success_rate=len(solved) / len(runs),
            median_time_s=median(row["computation_time_s"] for row in solved) if solved else None,
            median_makespan=median(row["makespan"] for row in solved) if solved else None,
            timeouts=statuses.count("timeout"), unsolved=statuses.count("unsolved"),
            invalid=statuses.count("invalid"), crashes=statuses.count("crash"),
        )


def solver_pairs(rows, baseline):
    solvers = by_solver(rows)
    reference = {row["instance_id"]: row for row in solvers.get(baseline, ())}
    for candidate, cases in solvers.items():
        if candidate == baseline:
            continue
        pairs = [(reference[row["instance_id"]], row) for row in cases if row["instance_id"] in reference]
        if pairs:
            yield candidate, pairs


def paired_metrics(reference, candidate):
    speedup = None
    if candidate["computation_time_s"] > 0 and reference["computation_time_s"] > 0:
        speedup = reference["computation_time_s"] / candidate["computation_time_s"]
    return speedup, candidate["makespan"] - reference["makespan"]


def reduction_pct(reference, candidate):
    if reference is None or candidate is None or reference <= 0:
        return None
    return 100 * (reference - candidate) / reference


def pair_rows(rows, baseline):
    pairs = []
    for candidate, cases in solver_pairs(rows, baseline):
        for reference, attempt in cases:
            ref_solved = reference["status"] == "solved"
            new_solved = attempt["status"] == "solved"
            both = ref_solved and new_solved
            speedup, delta = paired_metrics(reference, attempt) if both else (None, None)
            outcome = "both_solved" if both else (
                "baseline_only" if ref_solved else "candidate_only" if new_solved else "neither_solved"
            )
            pairs.append({
                "instance_id": attempt["instance_id"], "map": attempt["map"],
                "density_pct": attempt["density_pct"], "targets": attempt["targets"],
                "solver": candidate, "baseline": baseline,
                "baseline_status": reference["status"], "status": attempt["status"],
                "both_solved": both, "outcome": outcome,
                "baseline_time_s": reference["computation_time_s"],
                "computation_time_s": attempt["computation_time_s"],
                "baseline_makespan": reference["makespan"], "makespan": attempt["makespan"],
                "speedup": speedup, "makespan_delta": delta,
                "time_reduction_pct": reduction_pct(reference["computation_time_s"], attempt["computation_time_s"]) if both else None,
                "makespan_reduction_pct": reduction_pct(reference["makespan"], attempt["makespan"]) if both else None,
            })
    return pairs


def compare(rows, key, baseline):
    for candidate, pairs in solver_pairs(rows, baseline):
        speedups, deltas = [], []
        baseline_only = candidate_only = neither = 0
        for reference, attempt in pairs:
            ref_solved = reference["status"] == "solved"
            new_solved = attempt["status"] == "solved"
            if ref_solved and new_solved:
                speedup, delta = paired_metrics(reference, attempt)
                if speedup is not None:
                    speedups.append(speedup)
                deltas.append(delta)
            elif ref_solved:
                baseline_only += 1
            elif new_solved:
                candidate_only += 1
            else:
                neither += 1
        yield dict(
            zip(COMPARISON_FIELDS[:3], key), solver=candidate, baseline=baseline, paired=len(pairs),
            both_solved=len(deltas), baseline_only=baseline_only, candidate_only=candidate_only,
            neither_solved=neither, median_speedup=median(speedups) if speedups else None,
            median_makespan_delta=median(deltas) if deltas else None,
            shorter=sum(delta < 0 for delta in deltas),
            equal=deltas.count(0), longer=sum(delta > 0 for delta in deltas),
            **relative_summary(pairs),
        )


def relative_summary(pairs):
    baseline_count = sum(reference["status"] == "solved" for reference, _ in pairs)
    candidate_count = sum(attempt["status"] == "solved" for _, attempt in pairs)
    times, makespans = [], []
    for reference, attempt in pairs:
        if reference["status"] != "solved" or attempt["status"] != "solved":
            continue
        time = reduction_pct(reference["computation_time_s"], attempt["computation_time_s"])
        makespan = reduction_pct(reference["makespan"], attempt["makespan"])
        if time is not None:
            times.append(time)
        if makespan is not None:
            makespans.append(makespan)
    return {
        "success_rate_gain_pp": 100 * (candidate_count - baseline_count) / len(pairs),
        "success_rate_change_pct": 100 * (candidate_count - baseline_count) / baseline_count if baseline_count else None,
        "median_time_reduction_pct": median(times) if times else None,
        "median_makespan_reduction_pct": median(makespans) if makespans else None,
        "time_pairs": len(times), "makespan_pairs": len(makespans),
    }


def number(value, suffix=""):
    return "—" if value is None else f"{value:.4g}{suffix}"


def write_reports(output, rows, baseline):
    groups = {("all", None, None): rows, **grouped(rows)}
    summaries = [summary for key, cases in groups.items() for summary in summarize(cases, key)]
    comparisons = [comparison for key, cases in groups.items() for comparison in compare(cases, key, baseline)]
    lookup = {(row["map"], row["density_pct"], row["targets"], row["solver"]): row for row in comparisons}
    for row in summaries:
        relative = lookup.get((row["map"], row["density_pct"], row["targets"], row["solver"]), {})
        row.update({field: relative.get(field) for field in SUMMARY_FIELDS[13:]})
    write_csv(output / "summary.csv", SUMMARY_FIELDS, summaries)
    write_csv(output / "comparison.csv", COMPARISON_FIELDS, comparisons)
    write_csv(output / "pairs.csv", PAIR_FIELDS, pair_rows(rows, baseline))
    lines = [
        "# MAPF-HD benchmark",
        "",
        "Success requires a valid plan within the configured limit. Time and makespan medians use solved runs.",
        "",
        "| Map | Density | Targets | Solver | Solved | Success | Median time | Median makespan | Timeout / unsolved / invalid / crash |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summaries:
        lines.append(
            f"| {row['map']} | {number(row['density_pct'], '%')} | {number(row['targets'])} | {row['solver']} "
            f"| {row['solved']}/{row['total']} | {row['success_rate']:.1%} "
            f"| {number(row['median_time_s'], ' s')} | {number(row['median_makespan'])} "
            f"| {row['timeouts']} / {row['unsolved']} / {row['invalid']} / {row['crashes']} |"
        )
    if comparisons:
        lines.extend([
            "", f"## Paired comparison with {baseline}", "",
            "Speedup above 1 favors the candidate. Negative makespan delta means a shorter plan.",
            "",
            "| Map | Density | Targets | Candidate | Both solved / paired | Baseline only | Candidate only | Neither | Median speedup | Median makespan delta |",
            "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ])
        for row in comparisons:
            lines.append(
                f"| {row['map']} | {number(row['density_pct'], '%')} | {number(row['targets'])} | {row['solver']} "
                f"| {row['both_solved']}/{row['paired']} | {row['baseline_only']} | {row['candidate_only']} "
                f"| {row['neither_solved']} | {number(row['median_speedup'], 'x')} "
                f"| {number(row['median_makespan_delta'])} |"
            )
        lines.extend([
            "", "## Relative metrics", "",
            "Positive reductions mean a smaller candidate value. Percentages are calculated per common solved scenario, then aggregated by median.",
            "",
            "| Map | Density | Candidate | Success gain, pp | Success change, % | Time reduction, % | Makespan reduction, % | N time / makespan |",
            "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
        ])
        for row in comparisons:
            lines.append(
                f"| {row['map']} | {number(row['density_pct'], '%')} | {row['solver']} "
                f"| {number(row['success_rate_gain_pp'])} | {number(row['success_rate_change_pct'])} "
                f"| {number(row['median_time_reduction_pct'])} | {number(row['median_makespan_reduction_pct'])} "
                f"| {row['time_pairs']} / {row['makespan_pairs']} |"
            )
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
