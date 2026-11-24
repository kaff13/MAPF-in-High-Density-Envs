"""PHANS entrypoints for weighted target routes and reverse potentials."""

from research._shared.runtime import solve_planner
from ._route_search import (
    Potential1AStar,
    Potential2AStar,
    Potential3AStar,
    PotentialOnly2AStar,
    Potential2HoleQuarterAStar,
    Potential2HoleHalfAStar,
)


def solve(instance):
    """Use occupied-entry penalty two in g and the reverse potential."""
    return solve_planner(instance, search_class=Potential2AStar)


def weight1(instance):
    return solve_planner(instance, search_class=Potential1AStar)


def weight3(instance):
    return solve_planner(instance, search_class=Potential3AStar)


def only_potential(instance):
    """Keep unit g; use the weighted potential only as a search bias."""
    return solve_planner(instance, search_class=PotentialOnly2AStar)


def hole_quarter(instance):
    return solve_planner(instance, search_class=Potential2HoleQuarterAStar)


def hole_half(instance):
    return solve_planner(instance, search_class=Potential2HoleHalfAStar)
