"""PHANS entrypoints that change representation and copying, not decisions."""

from research._shared.runtime import solve_planner
from ._indexed import IndexedAStar
from ._tuple import TupleAStar
from ._copy import fast_deepcopy
from ._planner import EngineeringPHANS


def solve(instance):
    """Enable tuple search, fast copying, and equivalent vacancy selection."""
    return solve_planner(
        instance,
        planner_class=EngineeringPHANS,
        search_class=TupleAStar,
        copier=fast_deepcopy,
    )


def indexed(instance):
    """Index reservations and cache distances; retain object states and copying."""
    return solve_planner(instance, search_class=IndexedAStar)


def indexed_copy(instance):
    """Combine indexed object-state search with specialized copying."""
    return solve_planner(
        instance, search_class=IndexedAStar, copier=fast_deepcopy
    )


def tuple_only(instance):
    """Use tuple search and fast copying with the original vacancy selector."""
    return solve_planner(instance, search_class=TupleAStar, copier=fast_deepcopy)
