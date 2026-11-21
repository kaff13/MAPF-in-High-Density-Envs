from time import sleep


def move_blocker(instance):
    return [instance.starts, ((0, 0), (2, 0)), ((1, 0), (2, 0))]


def follow_blocker(instance):
    return [instance.starts, ((1, 0), (2, 0))]


def numpy_plan(instance):
    import numpy as np

    return np.array(move_blocker(instance))


def waited_plan(instance):
    return [instance.starts, *move_blocker(instance)]


def empty_plan(instance):
    return []


def stall(instance):
    sleep(5)


class DelayedTrace:
    def __init__(self, instance):
        self.instance = instance

    def __iter__(self):
        sleep(1)
        yield from move_blocker(self.instance)


def lazy_plan(instance):
    return DelayedTrace(instance)


def fail(instance):
    raise RuntimeError("fixture failure")


def checkout_phans(instance):
    from solver.phans_null_agent_swapping import PHANS

    grid = instance.map
    planner = PHANS(grid.width, grid.height, static_obstacles=sorted(grid.walls))
    return planner.run_loop(list(instance.starts), list(grid.goals))
