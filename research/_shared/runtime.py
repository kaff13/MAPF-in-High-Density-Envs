"""Explicit PHANS adapters: raw search/copy/trace unless deliberately replaced.

No experiment is executed on import. Each benchmark solver runs in a separate
process; temporary module-local substitutions are restored even on exceptions.
"""
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import patch

import solver.phans_null_agent_swapping as original
import research._shared.phans as scaffold

PHANS_COMMIT = 'a82ed819d37932ff845e170805f41e24c82e550b'
PARAMETERS = {'a_star_max_iter': -1, 'max_loop': 300}


def solve_planner(instance, *, planner_class=None, planner_kwargs=None,
                  search_class=None, copier=None, postprocess=None):
    """Run exactly original defaults except the explicitly supplied components."""
    with ExitStack() as stack:
        for module in (original, scaffold):
            if search_class is not None:
                stack.enter_context(patch.object(module, 'AStarFollowingConflict', search_class))
            if copier is not None:
                stack.enter_context(patch.object(module, 'copy', SimpleNamespace(deepcopy=copier)))
        grid = instance.map
        cls = original.PHANS if planner_class is None else planner_class
        planner = cls(grid.width, grid.height, static_obstacles=sorted(grid.walls),
                      **(planner_kwargs or {}))
        frames = planner.run_loop(list(instance.starts), list(grid.goals), **PARAMETERS)
        return frames if postprocess is None else postprocess(frames)
