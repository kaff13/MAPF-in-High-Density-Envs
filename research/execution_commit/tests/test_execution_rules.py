from contextlib import redirect_stdout
from io import StringIO
import unittest

from benchmark.maps import GridMap, Instance, make_instance
from benchmark.validation import check_trace
from research._shared.runtime import solve_planner as original_phans


class ExecutionCommitTests(unittest.TestCase):
    def test_finished_target_is_protected_while_other_target_continues(self):
        from research.execution_commit.solver import CommittedPHANS
        planner = CommittedPHANS(5, 4, lookahead=4, horizon=4)
        planner.task_len = 2
        planner.tgt_ag_path_lst = [[(0, 0), (1, 0), (2, 0)], [(0, 2), (1, 2), (2, 2)]]
        planner.tgt_cur_steps = [1, 0]
        planner.ag_cur_pos_lst = [(2, 0), (0, 2), (2, 3)]
        paths = [[(2, 1), (2, 0)], [(0, 3), (1, 3), (2, 3)]]
        self.assertTrue(planner._continue_phase(True, 1, paths))
        self.assertEqual(planner.goal_ag_idx_lst, [0])
        self.assertEqual(paths[0], [])
        self.assertEqual(len(paths[1]), 3)

    def test_late_first_progress_does_not_extend_deadline_on_later_progress(self):
        from research.execution_commit.solver import CommittedPHANS
        planner = CommittedPHANS(10, 2, lookahead=4, horizon=4)
        planner.task_len = 1
        planner.tgt_ag_path_lst = [[(x, 0) for x in range(10)]]
        planner.tgt_cur_steps = [0]
        planner.ag_cur_pos_lst = [(0, 0), (5, 1)]
        paths = [[(4, 1), (5, 1)]]
        self.assertTrue(planner._continue_phase(False, 1, paths))
        planner.ag_cur_pos_lst[0] = (1, 0)
        self.assertTrue(planner._continue_phase(True, 3, paths))
        planner.ag_cur_pos_lst[0] = (2, 0)
        self.assertTrue(planner._continue_phase(True, 4, paths))
        self.assertFalse(planner._continue_phase(False, 6, paths))
        # Beginning a new phase resets the previous commitment deadline.
        self.assertTrue(planner._continue_phase(False, 1, paths))
        planner.ag_cur_pos_lst[0] = (3, 0)
        self.assertTrue(planner._continue_phase(True, 2, paths))
        self.assertFalse(planner._continue_phase(False, 5, paths))

    def test_no_useful_remainder_stops_early(self):
        from research.execution_commit.solver import CommittedPHANS
        planner = CommittedPHANS(4, 2, lookahead=4, horizon=4)
        planner.task_len = 1
        planner.tgt_ag_path_lst = [[(0, 0), (1, 0), (2, 0), (3, 0)]]
        planner.tgt_cur_steps = [0]
        planner.ag_cur_pos_lst = [(1, 0), (2, 0)]
        self.assertFalse(planner._continue_phase(True, 1, []))

    def test_horizon_one_reproduces_complete_original_trace(self):
        from research.execution_commit.solver import solve_with_horizon
        for map_id in ('toyota-env1', 'toyota-env2'):
            case = make_instance(map_id, 95, 0)
            with redirect_stdout(StringIO()):
                self.assertEqual(solve_with_horizon(case, 1), original_phans(case))

    def test_continuation_refreshes_progress_and_protects_advanced_target(self):
        from research.execution_commit.solver import CommittedPHANS
        planner = CommittedPHANS(4, 3, lookahead=4, horizon=2)
        planner.task_len = 1
        planner.tgt_ag_path_lst = [[(0, 0), (1, 0), (2, 0)]]
        planner.tgt_cur_steps = [0]
        planner.ag_cur_pos_lst = [(1, 0), (2, 2)]
        null_paths = [[(1, 1), (1, 0)], [(0, 2), (1, 2), (2, 2)]]
        self.assertTrue(planner._continue_phase(True, 1, null_paths))
        self.assertEqual(planner.tgt_cur_steps, [1])
        self.assertEqual(null_paths[0], [])
        self.assertEqual(len(null_paths[1]), 3)
        planner.ag_cur_pos_lst[0] = (2, 0)
        self.assertFalse(planner._continue_phase(True, 2, null_paths))
        self.assertEqual(planner.goal_ag_idx_lst, [0])

    def test_full_solutions_remain_valid_with_commitment(self):
        from research.execution_commit.solver import h2, h4
        for map_id in ('toyota-env1', 'toyota-env2'):
            case = make_instance(map_id, 95, 0)
            for solve in (h2, h4):
                with self.subTest(map=map_id, solver=solve.__name__), redirect_stdout(StringIO()):
                    result = check_trace(case, solve(case))
                    self.assertEqual(result.status, 'solved', result.detail)

    def test_commitment_respects_tick_cap(self):
        from research.execution_commit.solver import CommittedPHANS
        grid = GridMap('commit-cap', 5, 2, frozenset(), ((4, 0),))
        case = Instance('commit-cap', grid, ((0, 0), (2, 0), (3, 0), (4, 0)), 40, 0)
        planner = CommittedPHANS(5, 2, lookahead=4, horizon=4)
        with redirect_stdout(StringIO()):
            trace = planner.run_loop(list(case.starts), list(grid.goals), max_loop=2)
        self.assertLessEqual(len(trace), 3)
        self.assertNotEqual(check_trace(case, trace).status, 'invalid')


if __name__ == '__main__':
    unittest.main()
