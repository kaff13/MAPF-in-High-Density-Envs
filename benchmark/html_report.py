"""Self-contained, descriptive report pages for completed benchmark runs."""

from base64 import b64encode
from collections import defaultdict
from html import escape
import json
from pathlib import Path

from .reports import compare, grouped, number, pair_rows, summarize


STYLE = """
:root { color-scheme: light; font-family: Inter, Arial, sans-serif; color: #172b3a; background: #edf2f5; }
* { box-sizing: border-box; }
body { margin: 0; }
main { max-width: 1480px; margin: auto; padding: 36px 24px 72px; }
header { margin-bottom: 28px; }
h1 { font-size: clamp(28px, 4vw, 44px); margin: 10px 0; letter-spacing: -.035em; }
h2 { margin-top: 0; font-size: 23px; }
h3 { font-size: 18px; }
p { line-height: 1.65; max-width: 105ch; }
a { color: #14648b; }
nav { display: flex; flex-wrap: wrap; gap: 18px; padding-top: 12px; }
section { margin: 20px 0; padding: 26px; background: white; border: 1px solid #d6e0e7; border-radius: 12px; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; font-variant-numeric: tabular-nums; }
th { text-align: left; background: #f1f5f7; white-space: nowrap; }
th, td { border-bottom: 1px solid #e1e8ed; padding: 11px 12px; vertical-align: top; }
td { white-space: nowrap; }
tbody tr:hover { background: #f3f8fa; }
.wrap { white-space: normal; min-width: 200px; }
.muted, figcaption { color: #526a7a; }
.good { color: #0e725a; }
.bad { color: #ae3542; }
.numeric { font-variant-numeric: tabular-nums; }
.facts { display: flex; flex-wrap: wrap; gap: 12px 30px; }
.facts div { min-width: 120px; }
.facts strong { display: block; font-size: 24px; margin-top: 5px; }
figure { margin: 24px 0 0; }
figure img { display: block; width: 100%; height: auto; }
figcaption { line-height: 1.6; padding: 8px 0 16px; }
details { margin: 16px 0; }
summary { cursor: pointer; font-weight: 600; }
input { font: inherit; padding: 10px 12px; margin: 10px 0 16px; width: min(100%, 500px); border: 1px solid #bccdd7; border-radius: 6px; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #f2f6f8; padding: 16px; border-radius: 6px; }
code { font-family: Consolas, monospace; font-size: .9em; }
.searchable { margin-bottom: 22px; }
@media print { body { background: white; } nav, input { display: none; } section { break-inside: avoid; } }
"""

SCRIPT = """
document.querySelectorAll('input[data-table]').forEach(input => {
  input.addEventListener('input', () => {
    const needle = input.value.toLocaleLowerCase();
    document.querySelectorAll('#' + input.dataset.table + ' tbody tr').forEach(row => {
      row.hidden = !row.textContent.toLocaleLowerCase().includes(needle);
    });
  });
});
"""

CHARTS = (
    ("runtime_box", "Относительное сокращение времени",
     "Точки соответствуют общим решённым сценариям. Выше нуля — меньше времени, ниже нуля — больше."),
    ("makespan_box", "Относительное сокращение makespan",
     "Точки соответствуют общим решённым сценариям с ненулевым makespan baseline. Равные планы дают 0%."),
    ("success_box", "Распределение success rate по группам",
     "Одна точка — доля решений на комбинации карта × плотность × число целей. Каждая группа имеет одинаковый вес на этом графике."),
    ("success_heatmap", "Success rate по картам и плотностям",
     "В ячейках показаны доли и числа решений в пределах лимита."),
    ("success", "Success rate от плотности", "В знаменателе находятся все выбранные сценарии."),
    ("runtime", "Время от плотности", "Состав выборки и число наблюдений указаны на графике."),
    ("makespan", "Makespan от плотности", "Состав выборки и число наблюдений указаны на графике."),
    ("budget", "Доля решений от бюджета времени",
     "Каждая ступень соответствует завершённому валидному решению. Отказы остаются в знаменателе."),
    ("paired", "Время и makespan на общих решениях",
     "Каждая точка — один общий решённый сценарий. Ускорение больше 1 означает меньшее время кандидата."),
)


def text(value):
    return escape(str(value), quote=True)


def signed(value, suffix="%"):
    return "—" if value is None else f"{value:+.2f}{suffix}"


def table(headers, rows, table_id="", searchable=False):
    identifier = f' id="{text(table_id)}"' if table_id else ""
    heading = "".join(f"<th>{text(header)}</th>" for header in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    search = (
        f'<input type="search" aria-label="Фильтр таблицы" placeholder="Карта, реализация или ID сценария" data-table="{text(table_id)}">'
        if searchable else ""
    )
    return f'{search}<div class="scroll"><table{identifier}><thead><tr>{heading}</tr></thead><tbody>{body}</tbody></table></div>'


def summary_table(rows, baseline):
    summaries = list(summarize(rows, ("all", None, None)))
    comparisons = {row["solver"]: row for row in compare(rows, ("all", None, None), baseline)}
    columns = []
    for row in summaries:
        comparison = comparisons.get(row["solver"], {})
        columns.append([
            f'{row["solved"]} / {row["total"]}',
            f'{row["success_rate"]:.2%}',
            signed(comparison.get("median_time_reduction_pct")),
            signed(comparison.get("median_makespan_reduction_pct")),
            signed(comparison.get("success_rate_change_pct")),
            signed(comparison.get("success_rate_gain_pp"), " п.п."),
            text(comparison.get("both_solved", "—")),
            text(comparison.get("time_pairs", "—")),
            text(comparison.get("makespan_pairs", "—")),
        ])
    labels = [
        "Решено / всего", "Success rate", "Сокращение времени, медиана",
        "Сокращение makespan, медиана", "Δ success rate, относительно baseline",
        "Δ success rate, процентные пункты", "Общих решений с baseline",
        "N для сокращения времени", "N для сокращения makespan",
    ]
    return table(
        ["Метрика", *(row["solver"] for row in summaries)],
        [[text(label), *(column[index] for column in columns)] for index, label in enumerate(labels)],
    )


def absolute_table(summaries):
    return table(
        ["Карта", "Плотность", "Целей", "Реализация", "Решено / всего", "Success rate",
         "Время, мед., с", "Makespan, мед.", "Timeout", "Unsolved", "Invalid", "Crash"],
        [[text(row["map"]), number(row["density_pct"], "%"), number(row["targets"]),
          text(row["solver"]), f'{row["solved"]}/{row["total"]}', f'{row["success_rate"]:.2%}',
          number(row["median_time_s"]), number(row["median_makespan"]),
          str(row["timeouts"]), str(row["unsolved"]), str(row["invalid"]), str(row["crashes"])]
         for row in summaries],
        "absolute", searchable=True,
    )


def comparison_table(comparisons):
    return table(
        ["Карта", "Плотность", "Реализация", "Общих / пар", "Новые", "Потеряны", "Не решили оба",
         "Δ success, п.п.", "Сокращение времени", "Сокращение makespan", "Короче / равны / длиннее"],
        [[text(row["map"]), number(row["density_pct"], "%"), text(row["solver"]),
          f'{row["both_solved"]}/{row["paired"]}', str(row["candidate_only"]),
          str(row["baseline_only"]), str(row["neither_solved"]),
          signed(row["success_rate_gain_pp"], " п.п."), signed(row["median_time_reduction_pct"]),
          signed(row["median_makespan_reduction_pct"]),
          f'{row["shorter"]} / {row["equal"]} / {row["longer"]}'] for row in comparisons],
        "comparison", searchable=True,
    )


def case_time(status, value):
    return "лимит " + number(value) if status == "timeout" else number(value)


def case_table(pairs, output, table_id="cases"):
    rows = []
    for row in pairs:
        instance_id, solver = row["instance_id"], row["solver"]
        replay = Path("replays") / solver / f"{instance_id}.html"
        plan_link = f'<a href="{text(replay.as_posix())}">Смотреть</a>' if (output / replay).is_file() else "—"
        command = f'python -m benchmark replay RUN --scenario {instance_id} --solver "{solver}"'
        rows.append([
            text(instance_id), text(solver), text(row["outcome"]),
            text(row["baseline_status"]), text(row["status"]),
            case_time(row["baseline_status"], row["baseline_time_s"]),
            case_time(row["status"], row["computation_time_s"]),
            number(row["baseline_makespan"]), number(row["makespan"]),
            signed(row["time_reduction_pct"]), signed(row["makespan_reduction_pct"]),
            plan_link, f'<code>{text(command)}</code>',
        ])
    return table(
        ["Сценарий", "Реализация", "Исход пары", "Baseline", "Кандидат",
         "Baseline, с", "Кандидат, с", "Baseline, такты", "Кандидат, такты",
         "Сокращение времени", "Сокращение makespan", "План", "Открыть сохранённый план"],
        rows, table_id, searchable=True,
    )


def changed_cases(pairs, output):
    sections = []
    selections = [
        ("Новые решения", [row for row in pairs if row["outcome"] == "candidate_only"]),
        ("Потерянные решения", [row for row in pairs if row["outcome"] == "baseline_only"]),
    ]
    for title, metric in (
        ("До 10 крупнейших относительных увеличений времени", "time_reduction_pct"),
        ("До 10 крупнейших относительных увеличений makespan", "makespan_reduction_pct"),
    ):
        regressions = [row for row in pairs if row[metric] is not None and row[metric] < 0]
        selections.append((title, sorted(regressions, key=lambda row: row[metric])[:10]))
    for index, (title, cases) in enumerate(selections):
        content = case_table(cases, output, f"changed-{index}") if cases else "<p>Таких сценариев в выбранных данных нет.</p>"
        sections.append(f"<details><summary>{text(title)} · {len(cases)}</summary>{content}</details>")
    return "".join(sections)


def replay_links(output, rows):
    links = []
    for row in rows:
        relative = Path("replays") / row["solver"] / f'{row["instance_id"]}.html'
        if (output / relative).is_file():
            links.append(f'<li><a href="{text(relative.as_posix())}">{text(row["solver"])} · {text(row["instance_id"])}</a></li>')
    return "<ul>" + "".join(links) + "</ul>" if links else "<p>Откройте нужный план командой ниже. Плеер сохраняется отдельным HTML-файлом.</p>"


def write_html_report(output, rows, baseline, plots):
    manifest = json.loads((output / "run.json").read_text(encoding="utf-8"))
    count = len({row["instance_id"] for row in rows})
    map_count = len({row["map"] for row in rows})
    solver_count = len({row["solver"] for row in rows})
    budgets = ", ".join(number(value, " с") for value in sorted({row["timeout_s"] for row in rows}))
    groups = {("all", None, None): rows, **grouped(rows)}
    summaries = [row for key, cases in groups.items() for row in summarize(cases, key)]
    comparisons = [row for key, cases in groups.items() for row in compare(cases, key, baseline)]
    pairs = pair_rows(rows, baseline)
    available = {path.stem: path for path in plots if path.suffix == ".png"}
    figures = []
    for name, title, caption in CHARTS:
        if name not in available:
            continue
        path = available[name]
        encoded = b64encode(path.read_bytes()).decode("ascii")
        svg = path.with_suffix(".svg").relative_to(output).as_posix()
        figures.append(
            f'<figure><h3>{text(title)}</h3><img loading="lazy" src="data:image/png;base64,{encoded}" alt="{text(title)}">'
            f'<figcaption>{text(caption)} <a href="{text(svg)}">SVG</a></figcaption></figure>'
        )
    downloads = " · ".join(
        f'<a href="{name}">{name}</a>'
        for name in ("summary.csv", "comparison.csv", "pairs.csv", "results.csv", "run.json")
    )
    page = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MAPF-HD — результаты эксперимента</title><style>{STYLE}</style></head>
<body><main>
<header><p class="muted">MAPF-HD · baseline {text(baseline)}</p><h1>Результаты эксперимента</h1>
<div class="facts"><div>Сценариев<strong>{count}</strong></div><div>Карт<strong>{map_count}</strong></div>
<div>Реализаций<strong>{solver_count}</strong></div><div>Лимит на попытку<strong>{text(budgets)}</strong></div></div>
<nav><a href="#overview">Сводка</a><a href="#plots">Графики</a><a href="#groups">По картам и плотностям</a>
<a href="#cases-section">Сценарии</a><a href="#plans">Исполнение планов</a><a href="#protocol">Условия</a></nav></header>
<section id="overview"><h2>Сводная таблица</h2>
<p>Относительные время и makespan считаются попарно на сценариях, решённых обеими реализациями.
Положительное сокращение означает меньшее значение у кандидата. Success rate учитывает все попытки.</p>
{summary_table(rows, baseline)}
<p>В boxplot и медианы сокращения входят только пары с ненулевым значением baseline.
Колонки N показывают число таких пар отдельно для каждой метрики. Таймаут учитывается как отказ.</p></section>
<section id="plots"><h2>Графики</h2>
<p>В boxplot линия обозначает медиану, коробка — 25–75-й перцентили, усы — диапазон до 1,5 межквартильного размаха.
Отдельные точки сохраняют видимость всех наблюдений. На графиках указано число наблюдений.</p>
{"".join(figures)}</section>
<section id="groups"><h2>По картам и плотностям</h2>
<h3>Абсолютные значения</h3><p>Медианы секунд и тактов рассчитаны по успешным попыткам каждой реализации.</p>
{absolute_table(summaries)}
<h3>Парное сравнение с {text(baseline)}</h3>
<p>Новые и потерянные решения учитывают все пары. Короче, равны и длиннее относятся к общим решениям.</p>
{comparison_table(comparisons)}</section>
<section id="cases-section"><h2>Сценарии</h2>
<p>В pairs.csv доступны все пары, включая новые и потерянные решения.
Ниже можно найти конкретный ID, реализацию или исход пары.</p>
{changed_cases(pairs, output)}
<h3>Все пары</h3>{case_table(pairs, output)}</section>
<section id="plans"><h2>Исполнение планов</h2>
{replay_links(output, rows)}
<p>Команду выполняйте из корня клона, указав путь этой папки результатов вместо RUN.</p>
<pre>python -m benchmark replay RUN --scenario ID --solver NAME</pre>
<p>Для старого прогона без трасс добавьте --rerun, чтобы отдельно получить план.
Новая попытка сохраняется в replays и не заменяет исходные измерения.</p></section>
<section id="protocol"><h2>Метрики и условия</h2>
<p>Сокращение времени или makespan = 100 × (baseline − кандидат) / baseline.
В таблицах показана медиана парных процентов. Относительное изменение success rate = 100 × (SR кандидата − SR baseline) / SR baseline.
Разность в процентных пунктах = 100 × (SR кандидата − SR baseline). При нулевом знаменателе выводится «—».</p>
<p>Makespan — число тактов до первого одновременного достижения всех целей. Время включает подготовку в решателе и получение плана.
Проверка, сохранение трасс и графики выполняются после замера.</p>
<p>Статусы solved, timeout, unsolved, invalid и crash означают валидное решение, превышение лимита,
завершение без решения, нарушение правил движения и ошибку процесса соответственно.</p>
<p>При timeout в CSV записан лимит, а точное время нахождения решения неизвестно. Такие попытки не входят в парные проценты времени и makespan.</p>
<p>{downloads}</p>
<details><summary>Манифест прогона, окружение и происхождение данных</summary>
<pre>{text(json.dumps(manifest, ensure_ascii=False, indent=2))}</pre></details></section>
</main><script>{SCRIPT}</script></body></html>"""
    destination = output / "report.html"
    destination.write_text(page, encoding="utf-8")
    return destination
