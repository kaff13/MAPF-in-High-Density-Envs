"""Unit checks for raw PHANS route scoring; no benchmark instances or timing."""

import importlib.util
from pathlib import Path

import unittest

from solver.a_star import AStarFollowingConflict, Location, State


def route_module():
    path = Path(__file__).resolve().parents[1] / "_route_search.py"
    assert path.is_file(), "The pure raw route-search implementation is missing"
    spec = importlib.util.spec_from_file_location("raw_route_search_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def search_args(**overrides):
    args = dict(
        dimension=(5, 3),
        agent={"start": (0, 1), "goal": (4, 1)},
        obstacles=set(),
        agent_start_pos_lst=[(0, 1), (1, 1), (2, 1), (3, 1)],
        null_agent_pos_lst=[(0, 0), (4, 1)],
        a_star_max_iter=200,
    )
    args.update(overrides)
    return args


def positions(path):
    return [(step["x"], step["y"]) for step in path]


def test_zero_surcharge_preserves_raw_path_and_iterations(route_module):
    args = search_args(moving_obstacles=[(2, 0, 2)])
    raw = AStarFollowingConflict(**args)
    candidate = route_module.ClearanceAStar(**args, blocker_cost=0, hole_weight=0)
    assert candidate.compute_solution() == raw.compute_solution()
    assert candidate.iter == raw.iter


def test_blocker_surcharge_routes_around_occupied_cells(route_module):
    args = search_args()
    raw = AStarFollowingConflict(**args)
    candidate = route_module.Block2AStar(**args)
    assert positions(raw.compute_solution()) == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
    result = positions(candidate.compute_solution())
    assert len(result) == 7
    assert not ({(1, 1), (2, 1), (3, 1)} & set(result))


def test_reverse_potential_charges_entered_cell(route_module):
    cases = [
        ("Potential1AStar", {(2, 0): 0, (1, 0): 2, (0, 0): 4}),
        ("Potential2AStar", {(2, 0): 0, (1, 0): 3, (0, 0): 6}),
        ("Potential3AStar", {(2, 0): 0, (1, 0): 4, (0, 0): 8}),
        ("PotentialOnly2AStar", {(2, 0): 0, (1, 0): 3, (0, 0): 6}),
        ("Potential2HoleQuarterAStar", {(2, 0): 0, (1, 0): 3.5, (0, 0): 6.75}),
        ("Potential2HoleHalfAStar", {(2, 0): 0, (1, 0): 4, (0, 0): 7.5}),
    ]
    args = search_args(
        dimension=(3, 1), agent={"start": (0, 0), "goal": (2, 0)},
        agent_start_pos_lst=[(1, 0), (2, 0)], null_agent_pos_lst=[(0, 0)],
    )
    for class_name, expected in cases:
        search = getattr(route_module, class_name)(**args)
        assert search._goal_potential == expected, class_name


def test_weighted_variants_return_raw_state_objects(route_module):
    for class_name in ["Block4AStar", "Block2HoleAStar", "Potential2AStar"]:
        states = getattr(route_module, class_name)(**search_args())._search()
        assert all(isinstance(state, State) for state in states)
        assert all(isinstance(state.location, Location) for state in states)
        assert states[0].location == Location(0, 1)
        assert states[-1].location == Location(4, 1)


def test_null_mode_is_identical_to_original_without_any_null_positions(route_module):
    args = search_args(is_dst_add=False, null_agent_pos_lst=[],
                       moving_obstacles=[(1, 1, 1), (2, 0, -2)])
    raw = AStarFollowingConflict(**args)
    candidate = route_module.Potential2HoleHalfAStar(**args)
    assert candidate.compute_solution() == raw.compute_solution()
    assert candidate.iter == raw.iter


def test_weighted_routes_respect_raw_following_and_permanent_constraints(route_module):
    args = search_args(
        dimension=(3, 2), agent={"start": (0, 0), "goal": (2, 0)},
        agent_start_pos_lst=[(0, 0), (1, 0)], null_agent_pos_lst=[(0, 1)],
        moving_obstacles=[(1, 0, 1), (1, 1, -3)],
        moving_obstacle_edges=[(2, 1, 1, 1)], considering_cycle_conflict=False,
    )
    candidate = route_module.Block2AStar(**args)
    states = candidate._search()
    assert states and states[-1].location == Location(2, 0)
    assert all(not (state.location == Location(1, 0) and state.time <= 2) for state in states)
    assert all(not (state.location == Location(1, 1) and state.time >= 3) for state in states)
    raw_validator = AStarFollowingConflict(**args)
    for current, neighbor in zip(states, states[1:]):
        assert raw_validator._state_valid(neighbor)
        assert raw_validator._transition_valid(current, neighbor)


def test_cycle_edge_mode_preserves_original_search(route_module):
    args = search_args(moving_obstacle_edges=[(1, 0, 2, 0)])
    raw = AStarFollowingConflict(**args)
    candidate = route_module.Block2AStar(**args)
    assert candidate.compute_solution() == raw.compute_solution()
    assert candidate.iter == raw.iter


def test_weighted_search_dispatches_to_raw_neighbor_method(route_module):
    class ConstrainedSearch(route_module.Block2AStar):
        def _get_neighbors(self, state):
            return [neighbor for neighbor in super()._get_neighbors(state)
                    if neighbor.location != Location(2, 1)]

    states = ConstrainedSearch(**search_args())._search()
    assert states and states[-1].location == Location(4, 1)
    assert all(state.location != Location(2, 1) for state in states)


def test_null_distance_uses_raw_manhattan_arithmetic(route_module):
    search = route_module.ClearanceAStar(**search_args(null_agent_pos_lst=[(4, 2), (0, 0)]))
    assert search._null_distance(3, 0) == 3
    assert search._null_distance(4, 2) == 0


def test_empty_null_list_preserves_raw_numpy_error(route_module):
    args = search_args(null_agent_pos_lst=[])
    with unittest.TestCase().assertRaises(ValueError):
        AStarFollowingConflict(**args).compute_solution()
    with unittest.TestCase().assertRaises(ValueError):
        route_module.ClearanceAStar(**args).compute_solution()


def test_iteration_limit_returns_no_solution(route_module):
    candidate = route_module.Block2AStar(**search_args(a_star_max_iter=1))
    assert candidate.compute_solution() == {}
    assert candidate.iter == 1


def load_tests(loader, tests, pattern):
    """Expose function checks through unittest without a third-party runner."""
    suite = unittest.TestSuite()
    for name, check in sorted(globals().items()):
        if name.startswith("test_") and callable(check):
            def run(check=check):
                check(route_module())
            suite.addTest(unittest.FunctionTestCase(run, description=name))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)
