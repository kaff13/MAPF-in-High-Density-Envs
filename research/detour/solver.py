"""PHANS with conditional graph-distance correction of vacancy assignments."""

from research._shared.runtime import solve_planner
from ._planner import DetourPHANS, has_manhattan_path, nearest_holes


def solve(instance):
    """Retain raw search, copying, all blockers, and execution rules; no retiming."""
    return solve_planner(instance, planner_class=DetourPHANS)
