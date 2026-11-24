"""Behavioral checks for bounded blocker lookahead in the PHANS experiment."""

from contextlib import redirect_stdout
from io import StringIO
import unittest

from benchmark.maps import GridMap, Instance, make_instance
from benchmark.validation import check_trace
from research._shared.phans import ExperimentalPHANS as WindowedPHANS
from solver.phans_null_agent_swapping import PHANS


def separated_lanes():
    grid = GridMap("window-lanes", 4, 4, frozenset(), ((3, 0), (3, 3)))
    starts = ((0, 0), (0, 3), (1, 0), (2, 0), (3, 0), (1, 3), (2, 3), (3, 3))
    return Instance("window-lanes", grid, starts, 50, 0)


def run(planner, instance):
    with redirect_stdout(StringIO()):
        return planner.run_loop(list(instance.starts), list(instance.map.goals))


class WindowedTests(unittest.TestCase):
    def test_disabled_and_nonbinding_limits_preserve_complete_trace(self):
        instance = separated_lanes()
        expected = run(PHANS(4, 4), instance)
        self.assertEqual(check_trace(instance, expected).status, "solved")
        self.assertEqual(run(WindowedPHANS(4, 4), instance), expected)
        for cap in (None, 100):
            with self.subTest(cap=cap):
                planner = WindowedPHANS(4, 4, lookahead=cap)
                self.assertEqual(run(planner, instance), expected)

    def test_one_blocker_is_considered_for_each_target_not_globally(self):
        instance = separated_lanes()
        trace = run(WindowedPHANS(4, 4, lookahead=1), instance)
        self.assertEqual(check_trace(instance, trace).status, "solved")
        # Both disjoint target lanes clear their first blocker in the first tick.
        self.assertEqual(trace[1][2], (1, 1))
        self.assertEqual(trace[1][5], (1, 2))
        # Farther blockers are deliberately left for later planning phases.
        for index in (3, 4, 6, 7):
            self.assertEqual(trace[1][index], instance.starts[index])

    def test_short_windows_produce_valid_solutions_on_toyota_maps(self):
        for map_id in ("toyota-env1", "toyota-env2"):
            instance = make_instance(map_id, 90, 0)
            for cap in (1, 2, 4):
                with self.subTest(map_id=map_id, cap=cap):
                    grid = instance.map
                    planner = WindowedPHANS(
                        grid.width, grid.height, static_obstacles=sorted(grid.walls),
                        lookahead=cap,
                    )
                    result = check_trace(instance, run(planner, instance))
                    self.assertEqual(result.status, "solved", result.detail)

    def test_invalid_windows_fail_before_search(self):
        for value in (0, -1, 1.5, True, "2"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    WindowedPHANS(4, 4, lookahead=value)


if __name__ == "__main__":
    unittest.main()
