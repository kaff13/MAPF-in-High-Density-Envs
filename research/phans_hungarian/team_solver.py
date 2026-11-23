"""Benchmark adapter: candidate=team_solver:solve."""
from .phans_hungarian import PHANSHungarian


def _valid_solution(frames, starts, goals, width, height, walls):
    if not frames or tuple(frames[0]) != tuple(starts):
        return False
    previous = None
    reached = False
    for raw in frames:
        frame = tuple(tuple(p) for p in raw)
        if len(frame) != len(starts) or len(set(frame)) != len(frame):
            return False
        old_cells = set(previous or ())
        for i, (x, y) in enumerate(frame):
            if not (0 <= x < width and 0 <= y < height) or (x, y) in walls:
                return False
            if previous is not None and frame[i] != previous[i]:
                old = previous[i]
                if abs(x - old[0]) + abs(y - old[1]) != 1 or frame[i] in old_cells:
                    return False
        if frame[:len(goals)] == tuple(goals):
            reached = True
        previous = frame
    return reached


def solve(instance):
    grid = instance.map
    planner = PHANSHungarian(grid.width, grid.height, static_obstacles=sorted(grid.walls))
    frames = planner.run_loop(list(instance.starts), list(grid.goals),
                              a_star_max_iter=-1, max_loop=300)
    # Baseline may return a partial or invalid trace on reaching max_loop.
    # Do not count this as a successful candidate solution.
    if not _valid_solution(frames, instance.starts, grid.goals,
                           grid.width, grid.height, grid.walls):
        return None
    return frames
