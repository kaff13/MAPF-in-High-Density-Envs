"""Map catalogue and versioned scenario generation."""

from dataclasses import dataclass
from operator import index
from random import Random
import re

Point = tuple[int, int]
DATASET_VERSION = "mapf-hd-v1"
DEFAULT_DENSITIES = (50, 75, 90, 95)
DEFAULT_SEEDS = 10
IDENTIFIER = re.compile(r"(?!(?:CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])$)[A-Z0-9][A-Z0-9_-]*", re.IGNORECASE | re.ASCII)


def point(value) -> Point:
    x, y = value
    if isinstance(x, bool) or isinstance(y, bool):
        raise ValueError("coordinates must be integers")
    return index(x), index(y)


@dataclass(frozen=True)
class GridMap:
    id: str
    width: int
    height: int
    walls: frozenset[Point]
    goals: tuple[Point, ...]

    def __post_init__(self):
        if not IDENTIFIER.fullmatch(self.id) or min(self.width, self.height) < 1:
            raise ValueError("invalid map ID or dimensions")
        if any(not self.in_bounds(cell) for cell in self.walls):
            raise ValueError("wall outside map")
        if not self.goals or len(set(self.goals)) != len(self.goals):
            raise ValueError("expected one or more distinct goals")
        if any(not self.is_free(cell) for cell in self.goals):
            raise ValueError("goal lies in a wall or outside map")

    @property
    def free_count(self):
        return self.width * self.height - len(self.walls)

    def in_bounds(self, cell: Point):
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, cell: Point):
        return self.in_bounds(cell) and cell not in self.walls


@dataclass(frozen=True)
class Instance:
    id: str
    map: GridMap
    starts: tuple[Point, ...]
    density: int
    seed: int

    def __post_init__(self):
        if not IDENTIFIER.fullmatch(self.id) or not 1 <= self.density <= 99 or self.seed < 0:
            raise ValueError("invalid scenario ID, density or seed")
        if not len(self.map.goals) <= len(self.starts) < self.map.free_count:
            raise ValueError("expected one start per goal and at least one empty cell")
        if len(set(self.starts)) != len(self.starts):
            raise ValueError("starts must be distinct")
        if any(not self.map.is_free(cell) for cell in self.starts):
            raise ValueError("start lies in a wall or outside map")

    @property
    def empty_cells(self):
        return self.map.free_count - len(self.starts)

    @property
    def actual_density(self):
        return len(self.starts) / self.map.free_count

    @property
    def paper_density(self):
        blockers = len(self.starts) - len(self.map.goals)
        return (blockers + len(self.map.walls)) / (self.map.width * self.map.height)

    def to_json(self):
        return {
            "id": self.id,
            "map": {
                "id": self.map.id,
                "width": self.map.width,
                "height": self.map.height,
                "walls": sorted(self.map.walls),
                "goals": self.map.goals,
            },
            "starts": self.starts,
            "density": self.density,
            "seed": self.seed,
        }

    @classmethod
    def from_json(cls, data):
        layout = data["map"]
        grid = GridMap(
            layout["id"], index(layout["width"]), index(layout["height"]),
            frozenset(point(cell) for cell in layout["walls"]),
            tuple(point(cell) for cell in layout["goals"]),
        )
        return cls(
            data["id"], grid, tuple(point(cell) for cell in data["starts"]),
            index(data["density"]), index(data["seed"]),
        )


def rectangles(blocks):
    return frozenset(
        (x, y)
        for left, top, width, height in blocks
        for x in range(left, left + width)
        for y in range(top, top + height)
    )


def perimeter_goals(width, height):
    return (
        (0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1),
        (width // 3, 0), (width - 1, height // 3),
        (2 * width // 3, height - 1), (0, 2 * height // 3 - 1),
        (2 * width // 3, 0), (width - 1, 2 * height // 3 - 1),
        (width // 3, height - 1), (0, height // 3),
    )


# The first four maps reproduce the geometry and ordered goals in run_env1.py–run_env4.py.
MAPS = {
    grid.id: grid
    for grid in (
        GridMap("toyota-env1", 14, 7, frozenset(), ((0, 0), (13, 0))),
        GridMap("toyota-env2", 14, 7, rectangles([(2, 2, 2, 3), (10, 2, 2, 3)]), ((0, 0), (13, 0))),
        GridMap("toyota-env3", 35, 21, frozenset(), perimeter_goals(35, 21)),
        GridMap(
            "toyota-env4", 35, 21,
            rectangles([
                (0, 9, 2, 3), (9, 9, 4, 3), (22, 9, 4, 3), (33, 9, 2, 3),
                *((x, y, 3, 3) for x in (4, 16, 28) for y in (3, 15)),
            ]),
            perimeter_goals(35, 21),
        ),
        GridMap(
            "pillars-70x42", 70, 42,
            rectangles((6 + 11 * column, 5 + 9 * row, 3, 3) for column in range(6) for row in range(4)),
            perimeter_goals(70, 42),
        ),
        GridMap(
            "aisles-100x60", 100, 60,
            rectangles((10 + 7 * column, y, 4, 22) for column in range(12) for y in (6, 32)),
            perimeter_goals(100, 60),
        ),
    )
}


def scenario_id(map_id, density, seed):
    return f"{map_id}-d{density:03d}-s{seed:03d}"


def scenario_ids(map_ids, densities, seeds):
    return [
        scenario_id(map_id, density, seed)
        for map_id in map_ids
        for density in densities
        for seed in range(seeds)
    ]


def make_instance(map_id, density, seed):
    grid = MAPS[map_id]
    if not 1 <= density <= 99 or seed < 0:
        raise ValueError("expected density from 1 to 99 and a nonnegative seed")
    count = round(grid.free_count * density / 100)
    if not len(grid.goals) <= count < grid.free_count:
        raise ValueError(f"{density}% on {map_id} leaves too few starts or empty cells")
    free = [(x, y) for x in range(grid.width) for y in range(grid.height) if grid.is_free((x, y))]
    rng = Random(seed)
    goals = set(grid.goals)
    # Seeded random() has a reproducible sequence across Python versions.
    # Ranking the candidates keeps this dataset independent of random.sample's implementation.
    targets = sorted((cell for cell in free if cell not in goals), key=lambda _: rng.random())[:len(goals)]
    target_set = set(targets)
    blockers = sorted((cell for cell in free if cell not in target_set), key=lambda _: rng.random())[:count - len(targets)]
    return Instance(scenario_id(map_id, density, seed), grid, tuple(targets + blockers), density, seed)


def parse_scenario(identifier):
    match = re.fullmatch(r"(.+)-d([0-9]{3})-s([0-9]{3,})", identifier)
    if not match:
        raise ValueError("expected a scenario ID such as toyota-env2-d090-s003 or a JSON file")
    map_id, density, seed = match.groups()
    return make_instance(map_id, int(density), int(seed))
