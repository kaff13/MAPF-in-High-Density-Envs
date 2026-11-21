import unittest

from benchmark.reports import compare, pair_rows


def result(case, solver, status="solved", time=10, makespan=20):
    return {
        "instance_id": case, "solver": solver, "status": status,
        "map": "tiny", "density_pct": 90, "targets": 1,
        "computation_time_s": time, "makespan": makespan if status == "solved" else None,
        "timeout_s": 30,
    }


class ReportMetricTests(unittest.TestCase):
    def test_relative_metrics_use_common_solutions_and_keep_lost_cases(self):
        rows = [
            result("a", "phans"), result("a", "new", time=5, makespan=15),
            result("b", "phans"), result("b", "new", "timeout"),
            result("c", "phans", "timeout"), result("c", "new"),
            result("d", "phans", "timeout"), result("d", "new"),
        ]
        pairs = pair_rows(rows, "phans")
        self.assertEqual(len(pairs), 4)
        self.assertEqual(pairs[0]["time_reduction_pct"], 50)
        self.assertEqual(pairs[0]["makespan_reduction_pct"], 25)
        self.assertIsNone(pairs[1]["time_reduction_pct"])
        summary, = compare(rows, ("tiny", 90, 1), "phans")
        self.assertEqual(summary["both_solved"], 1)
        self.assertEqual(summary["baseline_only"], 1)
        self.assertEqual(summary["candidate_only"], 2)
        self.assertEqual(summary["success_rate_gain_pp"], 25)
        self.assertEqual(summary["success_rate_change_pct"], 50)
        self.assertEqual(summary["median_time_reduction_pct"], 50)
        self.assertEqual(summary["median_makespan_reduction_pct"], 25)

    def test_zero_baseline_has_undefined_relative_rate_and_makespan(self):
        rows = [result("a", "phans", "timeout"), result("a", "new")]
        summary, = compare(rows, ("tiny", 90, 1), "phans")
        self.assertIsNone(summary["success_rate_change_pct"])
        self.assertEqual(summary["success_rate_gain_pp"], 100)
        rows = [result("b", "phans", makespan=0), result("b", "new", makespan=0)]
        pair, = pair_rows(rows, "phans")
        self.assertIsNone(pair["makespan_reduction_pct"])
        self.assertEqual(pair["makespan_delta"], 0)


if __name__ == "__main__":
    unittest.main()
