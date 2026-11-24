"""Regression checks for reports prepared after long benchmark runs."""
import csv
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from benchmark.artifacts import build_report
from benchmark.reports import RESULT_FIELDS


def saved_run(folder, cases, solvers, rows):
    folder.mkdir()
    (folder / "run.json").write_text(json.dumps({
        "dataset_version": "unit", "comparison_baseline": "phans",
        "phans_commit": "fixed", "instance_ids": cases,
        "solvers": {name: None if name == "phans" else "tests.fixture_solvers:empty_plan"
                    for name in solvers},
    }), encoding="utf-8")
    with (folder / "results.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        for case, solver, limit, source in rows:
            writer.writerow(dict(instance_id=case, solver=solver, map="corridor",
                                 density_pct=67, targets=1, seed=0, timeout_s=limit,
                                 status="timeout", computation_time_s=limit,
                                 solver_source_sha256=source))


class ReportIntegrityTests(unittest.TestCase):
    def test_csv_distinguishes_own_and_common_success_medians(self):
        from benchmark.reports import write_reports
        from tests.test_report_metrics import result
        rows = [result("a", "phans", time=1), result("a", "new", time=2),
                result("b", "phans", time=1000), result("b", "new", "timeout")]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            write_reports(output, rows, "phans")
            with (output / "summary.csv").open(encoding="utf-8", newline="") as stream:
                baseline = next(row for row in csv.DictReader(stream)
                                if row["map"] == "all" and row["solver"] == "phans")
            self.assertEqual(float(baseline["median_time_s"]), 500.5)
            self.assertEqual(float(baseline["paired_median_time_s"]), 1)
            self.assertEqual(int(baseline["paired_samples"]), 1)

    def test_absolute_html_medians_use_common_solved_cases(self):
        from benchmark.html_report import summary_table
        from tests.test_report_metrics import result
        rows = [result("a", "phans", time=1), result("a", "new", time=2),
                result("b", "phans", time=1000), result("b", "new", "timeout")]
        document = summary_table(rows, "phans")
        time_row = next(row for row in re.findall(r"<tr>(.*?)</tr>", document)
                        if "Медианное время" in row)
        values = re.findall(r"<td[^>]*>(.*?)</td>", time_row)
        self.assertEqual(values, ["1", "2"])

    def test_replay_sampling_keeps_all_metric_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "run"
            rows = [(case, name, 15, "") for case in ("a", "b") for name in ("phans", "new")]
            saved_run(source, ["a", "b"], ["phans", "new"], rows)
            original = (source / "results.csv").read_bytes()
            with patch("benchmark.plots.render_plots", return_value=[]), \
                    patch("benchmark.artifacts.build_report_replays", return_value=[]) as players:
                build_report(source, replay_sample_per_group=1)
            self.assertEqual(len(players.call_args.args[1]), 2)
            self.assertEqual((source / "results.csv").read_bytes(), original)

    def test_baseline_only_report_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "run"
            saved_run(source, ["a"], ["phans"], [("a", "phans", 15, "")])
            with patch("benchmark.plots.render_plots", return_value=[]):
                result = build_report(source)
            self.assertTrue(result.is_file())

    def test_incomplete_pair_is_rejected_before_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "run"
            saved_run(source, ["a", "b"], ["phans", "new"],
                      [("a", "phans", 15, ""), ("a", "new", 15, "same"),
                       ("b", "new", 15, "same")])
            with self.assertRaisesRegex(ValueError, "incomplete|paired"):
                build_report(source, output=root / "report")
            self.assertFalse((root / "report").exists())

    def test_disjoint_seeds_cannot_hide_different_solver_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for case, fingerprint in (("a", "old"), ("b", "new")):
                saved_run(root / case, [case], ["phans", "new"],
                          [(case, "phans", 15, ""), (case, "new", 15, fingerprint)])
            with self.assertRaisesRegex(ValueError, "source differs|different source"):
                build_report([root / "a", root / "b"], output=root / "report")
            self.assertFalse((root / "report").exists())

    def test_partial_larger_budget_cannot_make_unequal_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved_run(root / "old", ["a"], ["phans", "new"],
                      [("a", "phans", 5, ""), ("a", "new", 5, "same")])
            saved_run(root / "partial", ["a"], ["phans", "new"],
                      [("a", "phans", 15, "")])
            with self.assertRaisesRegex(ValueError, "time budgets|metadata"):
                build_report([root / "old", root / "partial"], output=root / "report")
            self.assertFalse((root / "report").exists())

    def test_multiple_candidates_get_separate_native_reports(self):
        from benchmark import artifacts
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "run"
            saved_run(source, ["a"], ["phans", "first", "second"],
                      [("a", name, 15, "") for name in ("phans", "first", "second")])
            with patch.object(artifacts, "build_report", return_value=source / "pair.html") as render:
                artifacts.build_run_reports(source)
            self.assertEqual([call.kwargs["solvers"] for call in render.call_args_list],
                             [["first"], ["second"]])
            self.assertTrue((source / "report.html").exists())
