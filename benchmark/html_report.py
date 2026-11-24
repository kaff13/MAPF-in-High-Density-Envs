"""Build a readable, offline HTML report for a completed MAPF-HD run."""

from base64 import b64encode
from html import escape
import json
from statistics import mean, median
from .reports import compare, number, summarize

STYLE = """
:root { color-scheme:light; font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
  color:#172b3a; background:#edf2f6; --muted:#657789; --line:#dce5ec; --blue:#2563eb; --orange:#ea580c; }
* { box-sizing:border-box; }
body { margin:0; }
main { max-width:1240px; margin:auto; padding:38px 28px 64px; }
h1 { font-size:clamp(30px,4vw,42px); margin:0 0 8px; letter-spacing:-.035em; }
h2 { font-size:22px; margin:0 0 8px; letter-spacing:-.02em; }
h3 { font-size:17px; margin:0; }
p { color:var(--muted); line-height:1.55; }
a { color:#14648b; }
.subtitle { margin:0 0 26px; }
.toolbar { display:flex; flex-wrap:wrap; align-items:center; gap:12px 22px; margin:0 0 20px; }
.toolbar label,.control label { display:grid; gap:6px; font-size:13px; font-weight:650; color:#425466; }
select { min-width:210px; font:inherit; color:inherit; padding:10px 40px 10px 13px; border:1px solid #bccdd7; border-radius:8px;
  appearance:none; background-color:white; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23425466' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat; background-position:right 14px center; }
section { margin:18px 0; padding:25px; background:white; border:1px solid var(--line); border-radius:14px;
  box-shadow:0 4px 16px rgba(32,56,76,.035); }
.section-note { margin:0 0 18px; font-size:14px; }
.facts { display:grid; grid-template-columns:repeat(auto-fit,minmax(145px,1fr)); gap:12px; margin:0 0 18px; }
.fact { padding:16px 18px; background:#fff; border:1px solid var(--line); border-radius:12px; color:var(--muted); font-size:13px; }
.fact strong { display:block; color:#172b3a; font-size:25px; margin-top:6px; font-variant-numeric:tabular-nums; }
.scroll { overflow-x:auto; }
table { border-collapse:collapse; width:100%; font-size:14px; font-variant-numeric:tabular-nums; }
th { background:#f1f5f8; text-align:left; color:#425466; font-weight:700; }
th,td { padding:12px 14px; border-bottom:1px solid #e4ebf0; vertical-align:top; }
tbody tr:hover { background:#f7fafc; }
td:not(:first-child) { white-space:nowrap; }
.pooled-table { width:max-content; min-width:100%; table-layout:fixed; }
.pooled-table thead tr:first-child th:first-child,.pooled-table tbody th[scope="row"] { width:250px; min-width:250px; max-width:250px; }
.pooled-table thead tr:nth-child(2) th,.pooled-table tbody td { width:116px; min-width:116px; }
.pooled-table thead th:first-child { position:sticky; left:0; z-index:4; background:#f1f5f8; }
.pooled-table tbody th[scope="row"] { position:sticky; left:0; z-index:2; background:white; }
.pooled-table tbody tr:hover th[scope="row"] { background:#f7fafc; }
.pooled-table thead tr:first-child th:not(:first-child) { text-align:center; }
.pooled-table thead tr:nth-child(2) th { font-size:12px; }
.pooled-table .density-separator { border-right:2px solid #b9c8d3; }
.solver { font-weight:700; }
.muted { color:var(--muted); }
.table-group { margin:20px 0 8px; color:#425466; }
.charts { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; }
figure { min-width:0; margin:14px 0 0; padding:14px; border:1px solid #e5ecf1; border-radius:10px; }
figure img { display:block; width:100%; height:auto; }
figcaption { display:flex; gap:14px; padding-top:9px; font-size:13px; }
.downloads { display:flex; flex-wrap:wrap; gap:12px 20px; }
.replay-controls { display:flex; flex-wrap:wrap; align-items:end; gap:14px; margin:18px 0 12px; }
.control { display:grid; gap:6px; font-size:13px; font-weight:650; color:#425466; }
.replay-status { margin:4px 0 12px; color:var(--muted); font-size:13px; }
.player-frame { width:100%; height:min(78vh,820px); min-height:560px; border:1px solid var(--line); border-radius:10px; background:#f8fafc; }
.empty-replay { padding:22px; border:1px dashed #bccdd7; border-radius:10px; color:var(--muted); }
details { margin-top:10px; }
summary { cursor:pointer; color:#14648b; font-weight:650; }
[hidden] { display:none !important; }
@media(max-width:760px) { main { padding:24px 12px 42px; } section { padding:17px; }
  .charts { grid-template-columns:1fr; } .player-frame { min-height:430px; height:70vh; } }
"""

CHARTS_ALL = (
    ("runtime_box", "Время вычисления"),
    ("makespan_box", "Длина плана (makespan)"),
    ("success_heatmap", "Успешность по картам и плотности"),
)
CHARTS_MAP = (
    ("runtime_box", "Время вычисления"),
    ("makespan_box", "Длина плана"),
    ("success_heatmap", "Успешность по плотности"),
)


def text(value):
    return escape(str(value), quote=True)


def signed(value, suffix="%"):
    return "—" if value is None else f"{value:+.2f}{suffix}"


def _outcomes(comparison, candidate_label):
    if not comparison:
        return "—"
    return (f'оба: {comparison["both_solved"]}; только {candidate_label}: {comparison["candidate_only"]}; '
            f'только PHANS: {comparison["baseline_only"]}; ни один: {comparison["neither_solved"]}')


def _paired_summaries(rows, key):
    """Success uses all cases; absolute medians use identical solved cases."""
    from .plots import absolute_values

    times = absolute_values(rows, "runtime")
    lengths = absolute_values(rows, "makespan")
    for item in summarize(rows, key):
        name = item["solver"]
        item["median_time_s"] = median(times[name]) if times[name] else None
        item["median_makespan"] = median(lengths[name]) if lengths[name] else None
        item["paired_samples"] = len(times[name])
        yield item


def summary_table(rows, baseline, solver_labels=None, *, pooled=False):
    solver_labels = solver_labels or {}
    candidates = sorted({row["solver"] for row in rows if row["solver"] != baseline})
    names = [baseline, *candidates]
    group_cases = {}
    for row in rows:
        key = (row["map"], row["density_pct"]) if pooled else (row["density_pct"],)
        group_cases.setdefault(key, []).append(row)
    ordered_groups = sorted(group_cases, key=(lambda key: (_map_order(key[0]), key[1])) if pooled else lambda key: key[0])
    metrics = (
        ("Решено", lambda s, c: f'{s["solved"]} / {s["total"]}'),
        ("Доля решений, %", lambda s, c: f'{s["success_rate"]:.1%}'),
        ("Медианное время, с", lambda s, c: number(s["median_time_s"])),
        ("Медианная длина плана, такты", lambda s, c: number(s["median_makespan"])),
        ("Общих решений для абсолютных метрик", lambda s, c: str(s["paired_samples"])),
        ("Сокращение времени, %", lambda s, c: signed(c.get("median_time_reduction_pct")) if c else "—"),
        ("Сокращение длины плана, %", lambda s, c: signed(c.get("median_makespan_reduction_pct")) if c else "—"),
        ("Новые решения", lambda s, c: str(c["candidate_only"]) if c else "—"),
        ("Потерянные решения", lambda s, c: str(c["baseline_only"]) if c else "—"),
    )
    cells = {}
    for key, cases in group_cases.items():
        summary_key = (key[0] if pooled else "all", key[-1], None)
        summaries = {item["solver"]: item for item in _paired_summaries(cases, summary_key)}
        comparisons = {item["solver"]: item for item in compare(cases, summary_key, baseline)}
        cells[key] = summaries, comparisons

    first_header = '<th rowspan="2">Метрика</th>'
    algorithm_headers = []
    for group_index, key in enumerate(ordered_groups):
        separator = ' class="density-separator"' if group_index < len(ordered_groups) - 1 else ""
        label = f'{_map_label(key[0])} · {key[1]}%' if pooled else f'{key[0]}%'
        first_header += f'<th colspan="{len(names)}"{separator}>{text(label)}</th>'
        for solver_index, name in enumerate(names):
            solver_separator = separator if solver_index == len(names) - 1 else ""
            algorithm_headers.append(
                f'<th{solver_separator}>{text("PHANS" if name == baseline else solver_labels.get(name, name))}</th>'
            )

    table_rows = []
    for metric, render in metrics:
        values = []
        for group_index, key in enumerate(ordered_groups):
            summaries, comparisons = cells[key]
            for solver_index, name in enumerate(names):
                summary = summaries.get(name)
                comparison = comparisons.get(name)
                separator = ' class="density-separator"' if (
                    solver_index == len(names) - 1 and group_index < len(ordered_groups) - 1
                ) else ""
                values.append(f'<td{separator}>{render(summary, comparison) if summary else "—"}</td>')
        table_rows.append(f'<tr><th scope="row">{text(metric)}</th>{"".join(values)}</tr>')
    return ('<div class="scroll"><table class="pooled-table"><thead><tr>' + first_header +
            '</tr><tr>' + "".join(algorithm_headers) + '</tr></thead><tbody>' + "".join(table_rows) +
            '</tbody></table></div>')


def density_summary_table(rows, baseline, solver_labels=None):
    """Summarize each density with equal map weight, then show the pooled total."""
    solver_labels = solver_labels or {}
    candidates = sorted({row["solver"] for row in rows if row["solver"] != baseline})
    names = [baseline, *candidates]
    groups = []
    for density in sorted({row["density_pct"] for row in rows}):
        density_rows = [row for row in rows if row["density_pct"] == density]
        per_map = {}
        map_ids = sorted({row["map"] for row in density_rows}, key=_map_order)
        for map_id in map_ids:
            map_rows = [row for row in density_rows if row["map"] == map_id]
            summaries = {item["solver"]: item for item in _paired_summaries(map_rows, ("all", density, None))}
            comparisons = {item["solver"]: item for item in compare(map_rows, ("all", density, None), baseline)}
            per_map[map_id] = summaries, comparisons
        groups.append((f"{density}%", per_map))

    all_summaries = {item["solver"]: item for item in _paired_summaries(rows, ("all", None, None))}
    all_comparisons = {item["solver"]: item for item in compare(rows, ("all", None, None), baseline)}
    groups.append(("Все прогоны", {"__all__": (all_summaries, all_comparisons)}))

    def average(values):
        values = [value for value in values if value is not None]
        return mean(values) if values else None

    metrics = (
        "Решено задач (суммарно)", "Доля решений, %", "Медианное время, с",
        "Медианная длина плана, такты", "Сокращение времени, %",
        "Сокращение длины плана, %",
    )

    def get_values(group, solver, comparison=False):
        entries = []
        for summaries, comparisons in group.values():
            item = (comparisons if comparison else summaries).get(solver)
            if item:
                entries.append(item)
        return entries

    # Helper closures are local so both the density groups and the all-runs
    # group use the same renderers while retaining their distinct aggregation.
    def render_metric(metric_index, group, solver):
        if metric_index == 0:
            entries = get_values(group, solver)
            solved = sum(entry["solved"] for entry in entries)
            total = sum(entry["total"] for entry in entries)
            return f"{solved} / {total}" if total else "—"
        field = ("success_rate", "median_time_s", "median_makespan",
                 "median_time_reduction_pct", "median_makespan_reduction_pct")[metric_index - 1]
        is_comparison = metric_index >= 4
        entries = get_values(group, solver, comparison=is_comparison)
        values = [entry.get(field) for entry in entries]
        value = average(values)
        if value is None:
            return "—"
        if metric_index == 1:
            return f"{value:.1%}"
        return signed(value) if is_comparison else number(value)

    header = '<th rowspan="2">Метрика</th>'
    solver_headers = []
    for index, (label, _) in enumerate(groups):
        separator = ' class="density-separator"' if index < len(groups) - 1 else ""
        header += f'<th colspan="{len(names)}"{separator}>{text(label)}</th>'
        for solver_index, solver in enumerate(names):
            solver_separator = separator if solver_index == len(names) - 1 else ""
            solver_headers.append(f'<th{solver_separator}>{text("PHANS" if solver == baseline else solver_labels.get(solver, solver))}</th>')
    body = []
    for metric_index, label in enumerate(metrics):
        cells = []
        for group_index, (_, group) in enumerate(groups):
            for solver_index, solver in enumerate(names):
                separator = ' class="density-separator"' if solver_index == len(names) - 1 and group_index < len(groups) - 1 else ""
                cells.append(f'<td{separator}>{render_metric(metric_index, group, solver)}</td>')
        body.append(f'<tr><th scope="row">{text(label)}</th>{"".join(cells)}</tr>')
    return ('<div class="scroll"><table class="pooled-table density-summary"><thead><tr>' + header +
            '</tr><tr>' + "".join(solver_headers) + '</tr></thead><tbody>' + "".join(body) +
            '</tbody></table></div>')


def _map_order(map_id):
    import re
    match = re.fullmatch(r"toyota-env([1-4])", map_id)
    if match:
        return (0, int(match.group(1)), map_id)
    if map_id == "pillars-70x42":
        return (1, 0, map_id)
    return (2, 0, map_id)


def _map_label(map_id):
    import re
    match = re.fullmatch(r"toyota-env([1-4])", map_id)
    if match:
        return f"Toyota env{match.group(1)}"
    return "Pillars 70×42" if map_id == "pillars-70x42" else map_id


def _replay_section(replays, solver_labels, scope=""):
    available = [row for row in replays if not scope or row["map"] == scope]
    if not available:
        return ('<section><h2>Просмотр планов</h2><p class="empty-replay">Для выбранных сценариев нет сохранённых парных трасс.</p></section>')
    candidates = sorted({row["solver"] for row in available})
    payload = json.dumps({"rows": available, "labels": solver_labels}, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    candidate_label = solver_labels.get(candidates[0], candidates[0])
    return f"""<section class="replay-section">
<h2>Просмотр планов</h2>
<div class="replay-controls">
<label class="control">Результат сравнения<select data-replay-filter>
<option value="all">Все сценарии</option><option value="both">Оба решили</option>
<option value="candidate_better">{text(candidate_label)} лучше по длине плана</option><option value="baseline_better">PHANS лучше по длине плана</option>
<option value="candidate_only">Решил только {text(candidate_label)}</option><option value="baseline_only">Решил только PHANS</option>
<option value="neither">Не решили оба</option></select></label>
<label class="control">Сценарий<select data-replay-case></select></label>
</div>
<div class="replay-status" data-replay-status></div>
<iframe class="player-frame" data-replay-frame title="Синхронное воспроизведение планов" loading="lazy"></iframe>
<script type="application/json" data-replay-data>{payload}</script>
</section>"""


def report_view(output, rows, baseline, plots, solver_labels=None, *, scope="", replays=()):
    solver_labels = solver_labels or {}
    available = {path.stem: path for path in plots if path.suffix == ".png"}
    charts = CHARTS_MAP if scope else CHARTS_ALL
    figures = []
    for name, title in charts:
        if name not in available:
            continue
        path = available[name]
        encoded = b64encode(path.read_bytes()).decode("ascii")
        png = path.relative_to(output).as_posix()
        svg = path.with_suffix(".svg").relative_to(output).as_posix()
        figures.append(
            f'<figure><h3>{text(title)}</h3><img loading="lazy" src="data:image/png;base64,{encoded}" alt="{text(title)}">'
            f'<figcaption><a href="{text(png)}">Скачать PNG</a><a href="{text(svg)}">Скачать SVG</a></figcaption></figure>'
        )
    prefix = f"maps/{scope}/" if scope else ""
    downloads = "".join(f'<a href="{text(prefix + name)}">{name}</a>'
                        for name in ("summary.csv", "comparison.csv", "pairs.csv", "results.csv"))
    downloads += '<a href="run.json">run.json — параметры запуска</a>'
    return f"""<div data-report-view="{text(scope)}"{" hidden" if scope else ""}>
<section><h2>{"Сравнение по карте" if scope else "Результаты по картам и плотностям"}</h2>
<p>Доля решений рассчитана по всем сценариям. Медианы времени и длины плана — по общим решениям сравниваемых реализаций. В summary.csv им соответствуют paired_median_time_s и paired_median_makespan; поля median_time_s и median_makespan сохраняют медианы по собственным успехам каждого солвера.</p>
{summary_table(rows, baseline, solver_labels, pooled=not bool(scope))}
{"<h3 class='table-group'>Среднее по картам при каждой плотности</h3>" + density_summary_table(rows, baseline, solver_labels) if not scope else ""}</section>
<section><h2>Графики</h2><div class="charts">{"".join(figures)}</div></section>
{_replay_section(replays, solver_labels, scope)}
<details><summary>Данные и воспроизводимость</summary><p class="downloads">{downloads}</p></details>
</div>"""


def write_html_report(output, rows, baseline, plots, *, map_plots=None, replays=None, solver_labels=None):
    map_plots = map_plots or {}
    replays = replays or []
    solver_labels = solver_labels or {}
    map_ids = sorted(map_plots, key=_map_order)
    options = '<option value="">Все карты</option>' + "".join(
        f'<option value="{text(map_id)}">{text(_map_label(map_id))}</option>' for map_id in map_ids
    )
    views = [report_view(output, rows, baseline, plots, solver_labels, replays=replays)]
    for map_id in map_ids:
        cases = [row for row in rows if row["map"] == map_id]
        views.append(report_view(output, cases, baseline, map_plots[map_id], solver_labels, scope=map_id, replays=replays))
    selector = (f'<div class="toolbar"><label>Карта<select id="map-filter">{options}</select></label></div>'
                if map_plots else "")
    script = """
const picker = document.getElementById("map-filter");
if (picker) picker.addEventListener("change", () => {
  for (const view of document.querySelectorAll("[data-report-view]")) view.hidden = view.dataset.reportView !== picker.value;
});
for (const section of document.querySelectorAll(".replay-section")) {
  const payload = JSON.parse(section.querySelector("[data-replay-data]").textContent);
  const data = payload.rows, labels = payload.labels;
  const filter = section.querySelector("[data-replay-filter]");
  const scenario = section.querySelector("[data-replay-case]");
  const frame = section.querySelector("[data-replay-frame]");
  const status = section.querySelector("[data-replay-status]");
  function update() {
    const choices = data.filter(row =>
      (filter.value === "all" || filter.value === "both" && ["candidate_better","baseline_better","equal"].includes(row.category) || row.category === filter.value));
    scenario.replaceChildren(...choices.map(row => {
      const option = document.createElement("option"); option.value = row.path;
const delta = row.makespan_delta === null ? "" : ` · Δ длины плана ${row.makespan_delta > 0 ? "+" : ""}${row.makespan_delta} такт.`;
      const categories = {candidate_better:`${labels[row.solver] || row.solver} лучше по длине плана`, baseline_better:"PHANS лучше по длине плана", equal:"Одинаковая длина плана", candidate_only:`Решил только ${labels[row.solver] || row.solver}`, baseline_only:"Решил только PHANS", neither:"Не решили оба"};
      option.textContent = `${row.scenario} · ${row.density}% · seed ${row.seed} · ${categories[row.category]}${delta}`;
      return option;
    }));
    if (!choices.length) {
      frame.removeAttribute("src"); status.textContent = "В этой категории нет сценариев."; return;
    }
    frame.src = choices[0].path; status.textContent = `Сценариев: ${choices.length}`;
  }
  scenario.addEventListener("change", () => { frame.src = scenario.value; });
  filter.addEventListener("change", update); update();
}
"""
    document = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MAPF-HD — результаты эксперимента</title><style>{STYLE}</style></head>
<body><main><h1>MAPF-HD</h1>
{selector}{"".join(views)}
</main><script>{script}</script></body></html>"""
    destination = output / "report.html"
    destination.write_text(document, encoding="utf-8")
    return destination
