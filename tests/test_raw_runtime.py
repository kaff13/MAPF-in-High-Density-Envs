from contextlib import redirect_stdout
from io import StringIO
import unittest

from benchmark.maps import GridMap, Instance, make_instance
from benchmark.validation import check_trace
import solver.phans_null_agent_swapping as original
from solver.a_star import AStarFollowingConflict


class RawRuntimeTests(unittest.TestCase):
    def test_default_scaffold_reproduces_original_trace(self):
        from research._shared.phans import ExperimentalPHANS
        from research._shared.runtime import solve_planner
        for map_id in ('toyota-env1', 'toyota-env2'):
            case = make_instance(map_id, 90, 0)
            grid = case.map
            with redirect_stdout(StringIO()):
                expected = original.PHANS(grid.width, grid.height, sorted(grid.walls)).run_loop(
                    list(case.starts), list(grid.goals), a_star_max_iter=-1, max_loop=300)
                actual = solve_planner(case, planner_class=ExperimentalPHANS)
            self.assertEqual(actual, expected)
            self.assertEqual(check_trace(case, actual).status, 'solved')

    def test_default_runtime_is_raw_original(self):
        from research._shared.runtime import solve_planner
        import research._shared.phans as scaffold
        grid = GridMap('raw-unit', 3, 2, frozenset(), ((2, 0),))
        case = Instance('raw-unit', grid, ((0, 0), (1, 0)), 33, 0)
        before = (original.AStarFollowingConflict, original.copy, scaffold.AStarFollowingConflict, scaffold.copy)
        with redirect_stdout(StringIO()):
            trace = solve_planner(case)
        self.assertEqual(check_trace(case, trace).status, 'solved')
        self.assertEqual(before, (original.AStarFollowingConflict, original.copy,
                                  scaffold.AStarFollowingConflict, scaffold.copy))
        self.assertIs(original.AStarFollowingConflict, AStarFollowingConflict)

    def test_adapter_restores_local_bindings_on_exception(self):
        from research._shared.runtime import solve_planner
        import research._shared.phans as scaffold
        class Alternative(AStarFollowingConflict):
            pass
        class Failing(original.PHANS):
            def run_loop(self, *args, **kwargs):
                raise RuntimeError('controlled failure')
        case = make_instance('toyota-env1', 50, 0)
        before = (original.AStarFollowingConflict, original.copy, scaffold.AStarFollowingConflict, scaffold.copy)
        with self.assertRaisesRegex(RuntimeError, 'controlled failure'):
            solve_planner(case, planner_class=Failing, search_class=Alternative, copier=lambda x: x)
        self.assertEqual(before, (original.AStarFollowingConflict, original.copy,
                                  scaffold.AStarFollowingConflict, scaffold.copy))


if __name__ == '__main__':
    unittest.main()
