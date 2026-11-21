"""Statistical sample and export contracts for benchmark charts."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

from benchmark import plots


def result(instance, solver, status="solved", runtime=2.0, makespan=10, density=90):
    return dict(instance_id=instance, solver=solver, status=status, map="map-a",
                density_pct=density, targets=1, computation_time_s=runtime,
                makespan=makespan if status == "solved" else None, timeout_s=10.0)


class PlotStatisticsTests(unittest.TestCase):
    def test_relative_samples_use_common_solutions_and_positive_baseline(self):
        rows = [
            result("a", "base", runtime=4, makespan=20),
            result("a", "candidate", runtime=2, makespan=10),
            result("b", "base", runtime=2, makespan=10),
            result("b", "candidate", "timeout", runtime=10),
            result("c", "base", "timeout", runtime=10),
            result("c", "candidate", runtime=1, makespan=2),
            result("d", "base", runtime=0, makespan=0),
            result("d", "candidate", runtime=0, makespan=0),
            result("e", "base", runtime=2, makespan=10),
            result("e", "candidate", runtime=4, makespan=15),
        ]
        self.assertTrue(hasattr(plots, "relative_values"), "paired reduction sample API is missing")
        self.assertEqual(plots.relative_values(rows, "base", "runtime"), {"candidate": [50.0, -100.0]})
        self.assertEqual(plots.relative_values(rows, "base", "makespan"), {"candidate": [50.0, -50.0]})

    def test_success_distribution_weights_each_scenario_group_once(self):
        rows = [result("a", "base"), result("b", "base", "timeout"),
                result("c", "base", density=95), result("d", "base", density=95),
                result("e", "base", density=95), result("f", "base", density=95)]
        self.assertTrue(hasattr(plots, "success_values"), "group success sample API is missing")
        self.assertEqual(plots.success_values(rows), {"base": [50.0, 100.0]})


@unittest.skipUnless(importlib.util.find_spec("matplotlib"), "install matplotlib")
class PlotExportTests(unittest.TestCase):
    def test_budget_curve_stops_at_the_shortest_observation_limit(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        rows = [result("a", "base", runtime=0.5), result("b", "base", runtime=2)]
        rows[0]["timeout_s"] = 1
        rows[1]["timeout_s"] = 3
        figure, axis = plt.subplots()
        try:
            plots.budget_plot(axis, rows)
            self.assertEqual(tuple(axis.get_xlim()), (0, 1))
            self.assertEqual(list(axis.lines[0].get_xdata()), [0, 0.5, 1])
            self.assertEqual(list(axis.lines[0].get_ydata()), [0, 50, 50])
        finally:
            plt.close(figure)

    def test_pure_renderer_exports_every_chart_without_a_manifest(self):
        self.assertTrue(hasattr(plots, "render_plots"), "manifest-independent renderer is missing")
        rows = [result("a", "base"), result("a", "candidate", runtime=1, makespan=8),
                result("b", "base", "timeout"), result("b", "candidate", "crash")]
        with tempfile.TemporaryDirectory() as directory:
            paths = plots.render_plots(rows, "base", Path(directory))
            expected = {f"{kind}.{extension}" for kind in
                        ("success", "runtime", "makespan", "budget", "paired", "runtime_box",
                         "makespan_box", "success_box", "success_heatmap")
                        for extension in ("png", "svg")}
            self.assertEqual({path.name for path in paths}, expected)
            for path in paths:
                if path.suffix == ".png":
                    self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                else:
                    self.assertIn("<svg", path.read_text(encoding="utf-8"))

    def test_renderer_rejects_duplicate_attempts_before_writing_charts(self):
        self.assertTrue(hasattr(plots, "render_plots"), "manifest-independent renderer is missing")
        row = result("a", "base")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "duplicate"):
                plots.render_plots([row, row], "base", Path(directory))
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_failed_only_runs_still_export_valid_charts(self):
        self.assertTrue(hasattr(plots, "render_plots"), "manifest-independent renderer is missing")
        rows = [result("a", "base", "timeout"), result("a", "candidate", "invalid")]
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(len(plots.render_plots(rows, "base", Path(directory))), 18)

    def test_unknown_status_is_rejected_instead_of_counted_as_failure(self):
        row = result("a", "base", "corrupt-status")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "status"):
                plots.render_plots([row], "base", Path(directory), ["success"])

    def test_baseline_only_curves_remain_in_absolute_units(self):
        with tempfile.TemporaryDirectory() as directory:
            plots.render_plots([result("a", "base")], "base", Path(directory), ["runtime", "makespan"])
            runtime_svg = (Path(directory) / "runtime.svg").read_text(encoding="utf-8")
            makespan_svg = (Path(directory) / "makespan.svg").read_text(encoding="utf-8")
            self.assertIn("Время (с), только решения", runtime_svg)
            self.assertIn("Makespan (такты), только решения", makespan_svg)
            self.assertNotIn("Сокращение", runtime_svg + makespan_svg)


if __name__ == "__main__":
    unittest.main()
