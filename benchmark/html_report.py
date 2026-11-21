"""Compact self-contained benchmark report."""

from base64 import b64encode
from html import escape
from statistics import median

from .reports import compare, number, summarize

STYLE = """
:root { color-scheme:light; font-family:Inter,Arial,sans-serif; color:#172b3a; background:#edf2f5; }
* { box-sizing:border-box; }
body { margin:0; }
main { max-width:1100px; margin:auto; padding:32px 24px 56px; }
h1 { font-size:32px; margin:0 0 24px; letter-spacing:-.025em; }
h2 { font-size:21px; margin:0 0 18px; }
h3 { font-size:17px; margin:0; }
a { color:#14648b; }
section { margin:20px 0; padding:24px; background:white; border:1px solid #d6e0e7; border-radius:10px; }
.facts { display:flex; flex-wrap:wrap; gap:16px 36px; margin-bottom:28px; }
.facts strong { display:block; font-size:23px; margin-top:5px; }
.scroll { overflow-x:auto; }
table { border-collapse:collapse; width:100%; font-size:14px; font-variant-numeric:tabular-nums; }
th { background:#f1f5f7; text-align:left; }
th,td { padding:12px; border-bottom:1px solid #e1e8ed; }
td:not(:first-child) { white-space:nowrap; }
tbody tr:hover { background:#f3f8fa; }
figure { margin:24px 0 0; }
figure img { display:block; width:100%; height:auto; }
figcaption { display:flex; gap:14px; padding:8px 0 18px; font-size:13px; }
.downloads { display:flex; flex-wrap:wrap; gap:16px; }
.map-picker { display:flex; align-items:center; gap:12px; margin:0 0 24px; font-weight:600; }
select { font:inherit; color:inherit; padding:10px 14px; border:1px solid #bccdd7; border-radius:6px; background:white; max-width:100%; }
[hidden] { display:none !important; }
@media(max-width:600px) { main { padding:20px 12px; } section { padding:16px; } th,td { padding:10px 8px; } }
"""

CHARTS = (
    ("runtime_box", "Computation time"),
    ("makespan_box", "Makespan"),
    ("success_heatmap", "Success rate по плотностям"),
    ("success", "Success rate от плотности"),
)


def text(value):
    return escape(str(value), quote=True)


def signed(value, suffix="%"):
    return "—" if value is None else f"{value:+.2f}{suffix}"


def summary_table(rows, baseline):
    from .plots import absolute_values

    summaries = list(summarize(rows, ("all", None, None)))
    comparisons = {row["solver"]: row for row in compare(rows, ("all", None, None), baseline)}
    times = absolute_values(rows, "runtime", baseline)
    makespans = absolute_values(rows, "makespan", baseline)
    columns = []
    for row in summaries:
        solver = row["solver"]
        comparison = comparisons.get(solver, {})
        raw_times, raw_makespans = times.get(solver, []), makespans.get(solver, [])
        columns.append([
            f'{row["solved"]} / {row["total"]}',
            f'{row["success_rate"]:.2%}',
            number(median(raw_times) if raw_times else None),
            number(median(raw_makespans) if raw_makespans else None),
            str(len(raw_times)),
            signed(comparison.get("median_time_reduction_pct")),
            signed(comparison.get("median_makespan_reduction_pct")),
            signed(comparison.get("success_rate_change_pct")),
            signed(comparison.get("success_rate_gain_pp"), " п.п."),
            text(comparison.get("both_solved", "—")),
            text(comparison.get("candidate_only", "—")),
            text(comparison.get("baseline_only", "—")),
        ])
    labels = (
        "Решено / всего", "Success rate", "Computation time, с · медиана общих решений",
        "Makespan, такты · медиана общих решений", "N общих для абсолютных метрик",
        "Сокращение времени, медиана пар", "Сокращение makespan, медиана пар",
        "Δ success rate, отн.", "Δ success rate, п.п.", "N пар с baseline", "Новые решения", "Потерянные решения",
    )
    heading = "".join(f"<th>{text(label)}</th>" for label in ("Метрика", *(row["solver"] for row in summaries)))
    body = "".join(
        f"<tr><td>{text(label)}</td>" + "".join(f"<td>{column[index]}</td>" for column in columns) + "</tr>"
        for index, label in enumerate(labels)
    )
    return f'<div class="scroll"><table><thead><tr>{heading}</tr></thead><tbody>{body}</tbody></table></div>'


def report_view(output, rows, baseline, plots, *, scope="", index=0):
    count = len({row["instance_id"] for row in rows})
    map_count = len({row["map"] for row in rows})
    budgets = ", ".join(number(value, " с") for value in sorted({row["timeout_s"] for row in rows}))
    available = {path.stem: path for path in plots if path.suffix == ".png"}
    figures = []
    for name, title in CHARTS:
        if name not in available:
            continue
        path = available[name]
        encoded = b64encode(path.read_bytes()).decode("ascii")
        png = path.relative_to(output).as_posix()
        svg = path.with_suffix(".svg").relative_to(output).as_posix()
        figures.append(
            f'<figure><h3>{text(title)}</h3><img loading="lazy" src="data:image/png;base64,{encoded}" alt="{text(title)}">'
            f'<figcaption><a href="{text(png)}">PNG</a><a href="{text(svg)}">SVG</a></figcaption></figure>'
        )
    prefix = f"maps/{scope}/" if scope else ""
    downloads = "".join(
        f'<a href="{text(prefix + name)}">{name}</a>'
        for name in ("summary.csv", "comparison.csv", "pairs.csv", "results.csv")
    )
    downloads += '<a href="run.json">run.json</a>'
    hidden = " hidden" if scope else ""
    return f"""<div data-report-view="{text(scope)}"{hidden}>
<div class="facts"><div>Сценариев<strong>{count}</strong></div><div>Карт<strong>{map_count}</strong></div>
<div>Реализаций<strong>{len({row["solver"] for row in rows})}</strong></div><div>Лимит<strong>{text(budgets)}</strong></div></div>
<section id="overview-{index}"><h2>Сводная таблица</h2>{summary_table(rows, baseline)}</section>
<section id="plots-{index}"><h2>Графики</h2>{"".join(figures)}</section>
<section id="files-{index}"><h2>Данные</h2><div class="downloads">{downloads}</div></section>
</div>"""


def write_html_report(output, rows, baseline, plots, *, map_plots=None):
    map_plots = map_plots or {}
    options = '<option value="">Все карты</option>' + "".join(
        f'<option value="{text(map_id)}">{text(map_id)}</option>' for map_id in sorted(map_plots)
    )
    views = [report_view(output, rows, baseline, plots)]
    for index, map_id in enumerate(sorted(map_plots), start=1):
        cases = [row for row in rows if row["map"] == map_id]
        views.append(report_view(output, cases, baseline, map_plots[map_id], scope=map_id, index=index))
    selector = f'<div class="map-picker"><label for="map-filter">Карта</label><select id="map-filter">{options}</select></div>' if map_plots else ""
    script = """
const picker = document.getElementById("map-filter");
if (picker) picker.addEventListener("change", () => {
  for (const view of document.querySelectorAll("[data-report-view]")) {
    view.hidden = view.dataset.reportView !== picker.value;
  }
});
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
