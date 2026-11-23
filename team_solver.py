from benchmark.maps import Instance
from solver.phans_null_agent_swapping import PHANS


def solve(instance: Instance):
    grid = instance.map
    planner = PHANS(
        grid.width,
        grid.height,
        static_obstacles=sorted(grid.walls),
    )
    return planner.run_loop(list(instance.starts), list(grid.goals))