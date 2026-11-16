# Бенчмарк MAPF-HD

Встроенный решатель `phans` загружается из официального коммита Toyota `a82ed819d37932ff845e170805f41e24c82e550b`. Локальные правки в `solver/` влияют только на подключённый вариант команды. Используйте Git-клон с историей, содержащей этот коммит.

## Установка

Из корня клона запустите команды установки и просмотра карт.

~~~sh
conda env create -f environment.yml
conda activate phans
python -m benchmark list
~~~

Для существующего окружения Python 3.11 или 3.12 подойдёт `python -m pip install "numpy==2.3.5" "matplotlib==3.9.4"`.

## Карты и запуски

| Карта | Размер | Целей | Геометрия |
| --- | ---: | ---: | --- |
| `toyota-env1` | 14×7 | 2 | Открытая сетка, цели в углах одной стороны |
| `toyota-env2` | 14×7 | 2 | Две группы препятствий 2×3 |
| `toyota-env3` | 35×21 | 12 | Открытый склад, цели по периметру |
| `toyota-env4` | 35×21 | 12 | Склад с группами колонн и целями по периметру |
| `pillars-70x42` | 70×42 | 12 | 24 столба 3×3 в 6 столбцах и 4 рядах |
| `aisles-100x60` | 100×60 | 12 | Два ряда по 12 стеллажей 4×22, продольные проходы в 3 клетки и поперечный в 4 |

Геометрия и порядок целей первых четырёх карт взяты из `run_env1.py`–`run_env4.py`. Полный профиль содержит 240 задач при плотностях 50%, 75%, 90%, 95% и seed от 0 до 9. Плотность — доля проходимых клеток, занятых всеми агентами на старте. Таймаут по умолчанию — 180 секунд на попытку. Его можно задать через `--timeout`. Встроенный PHANS сохраняет оригинальные параметры `max_loop=300` и `a_star_max_iter=-1`.

~~~sh
# Один сценарий по ID
python -m benchmark run --scenario toyota-env4-d090-s003

# Одна карта, по три расстановки для двух плотностей
python -m benchmark run --map toyota-env4 --density 90 95 --seeds 3 --out benchmark-results/env4

# Полный пул
python -m benchmark run --pool --out benchmark-results/full

# Список ID и точное воспроизведение сохранённого экземпляра
python -m benchmark list --map toyota-env4 --density 90 --seeds 3
python -m benchmark run --scenario benchmark-results/env4/instances/toyota-env4-d090-s000.json
~~~

Путь `--out` должен указывать на новую папку. По умолчанию создаётся папка с меткой времени в `benchmark-results/`. Для точного повторения опыта используйте JSON из исходного прогона.

## Подключение своего решателя

Создайте в корне клона `team_solver.py`. Функция принимает `benchmark.maps.Instance`. `instance.starts` хранит координаты агентов, `instance.map.goals` задаёт цели для первых агентов в том же порядке. Координаты нумеруются с нуля. Для стохастического варианта используйте `instance.seed`.

~~~python
from benchmark.maps import Instance
from solver.phans_null_agent_swapping import PHANS


def solve(instance: Instance):
    grid = instance.map
    planner = PHANS(grid.width, grid.height, static_obstacles=sorted(grid.walls))
    return planner.run_loop(list(instance.starts), list(grid.goals))
~~~

Замените вызов PHANS в `solve` своей реализацией. Возвращайте кадры с позициями **всех** агентов в исходном порядке, начиная с `t=0`. При отсутствии решения можно вернуть `None`. Агент может ожидать или перейти в соседнюю клетку, свободную в начале такта.

~~~sh
python -m benchmark run --map toyota-env4 --solver phans --solver candidate=team_solver:solve --out benchmark-results/compare
~~~

## Отчёт и графики

- `results.csv` содержит метрики по каждой попытке. Makespan — число тактов до одновременного достижения целей. Время включает подготовку внутри решателя и поиск плана. Проверка и запись отчёта выполняются после замера. У таймаута в поле времени указан лимит.
- `summary.csv` и `report.md` показывают success rate как число валидных решений в пределах бюджета, делённое на все попытки. Медианы времени и makespan считаются по успешным попыткам.
- `comparison.csv` показывает успехи и потери относительно PHANS. Ускорение `время PHANS / время кандидата` и разность `makespan кандидата − makespan PHANS` считаются на общих решённых экземплярах.
- `run.json`, `instances/` и `logs/` содержат настройки, исходные экземпляры и логи решателей. Манифест фиксирует коммит и хеш набора. В `results.csv` для Python-адаптера сохраняется хеш его файла, если он доступен.

~~~sh
# Все пять графиков из существующего прогона
python -m benchmark plot benchmark-results/compare

# Только время и makespan на одной карте при двух плотностях
python -m benchmark plot benchmark-results/compare --kind runtime makespan --map toyota-env4 --density 90 95
~~~

Графики сохраняются в `plots/`. Доступны `success`, `runtime` и `makespan` от плотности, `budget` с долей всех задач, решённых к заданному моменту, и `paired` с ускорением и изменением makespan для каждого общего решения. Полоса разброса на графиках времени и makespan показывает диапазон между 25-м и 75-м перцентилями.

Проверка бенчмарка запускается через `python -m unittest discover -s tests -v`.
