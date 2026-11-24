"""PHANS restricted to the first k distinct blockers per target and phase."""

from research._shared.runtime import solve_planner
from research._shared.phans import ExperimentalPHANS


def solve_with_k(instance, k):
    """Use a positive blocker count, or None for the complete original suffix."""
    return solve_planner(
        instance,
        planner_class=ExperimentalPHANS,
        planner_kwargs={"lookahead": k},
    )


def solve(instance):
    """Canonical entrypoint: four distinct blockers per target."""
    return solve_with_k(instance, 4)


def k1(instance):
    return solve_with_k(instance, 1)


def k2(instance):
    return solve_with_k(instance, 2)


def k4(instance):
    return solve_with_k(instance, 4)


def k6(instance):
    return solve_with_k(instance, 6)


def k8(instance):
    return solve_with_k(instance, 8)


def k12(instance):
    return solve_with_k(instance, 12)


def k16(instance):
    return solve_with_k(instance, 16)
