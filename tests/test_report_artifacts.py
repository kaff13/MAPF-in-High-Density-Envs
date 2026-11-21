import csv
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from benchmark.reports import validate_results
from tests.test_benchmark import corridor_json


class ReportArtifactTests(unittest.TestCase):
    def test_numpy_trace_remains_solved_when_saved(self):
        from benchmark.maps import Instance
        from benchmark.runner import Solver, run_attempt

        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            plan_path = folder / "trace.json.gz"
            attempt = run_attempt(
                Solver.parse("numpy=tests.fixture_solvers:numpy_plan"),
                Instance.from_json(corridor_json()), 5,
                folder / "unused-baseline", folder / "log.txt", plan_path,
            )
            self.assertEqual(attempt.status, "solved", attempt.detail)
            self.assertEqual(attempt.makespan, 2)
            with gzip.open(plan_path, "rt", encoding="utf-8") as stream:
                self.assertEqual(json.load(stream)["frames"][-1], [[1, 0], [2, 0]])

    def test_invalid_completed_metrics_are_rejected(self):
        manifest = {"instance_ids": ["a"], "solvers": {"phans": None}}
        row = {
            "instance_id": "a", "solver": "phans", "map": "tiny",
            "density_pct": 90, "targets": 1, "timeout_s": 1,
            "status": "solved", "computation_time_s": 2, "makespan": 1,
        }
        with self.assertRaisesRegex(ValueError, "time budget"):
            validate_results([row], manifest)
        row["computation_time_s"] = 0.5
        validate_results([row], manifest)

    def test_cli_run_saves_trace_and_can_replay_without_planning(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            scenario = folder / "scenario.json"
            scenario.write_text(json.dumps(corridor_json()), encoding="utf-8")
            output = folder / "run"
            command = [
                sys.executable, "-m", "benchmark", "run", "--scenario", str(scenario),
                "--solver", "good=tests.fixture_solvers:move_blocker",
                "--solver", "bad=tests.fixture_solvers:follow_blocker",
                "--baseline", "good", "--timeout", "2", "--out", str(output),
            ]
            run = subprocess.run(command, capture_output=True, text=True, timeout=90)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            with (output / "results.csv").open(encoding="utf-8", newline="") as stream:
                row = next(row for row in csv.DictReader(stream) if row["solver"] == "good")
            with gzip.open(output / row["plan_path"], "rt", encoding="utf-8") as stream:
                plan = json.load(stream)
            self.assertEqual(plan["frames"], [[[0, 0], [1, 0]], [[0, 0], [2, 0]], [[1, 0], [2, 0]]])
            report = (output / "report.html").read_text(encoding="utf-8")
            self.assertIn("data:image/png;base64,", report)
            self.assertIn("pairs.csv", report)
            self.assertNotIn("Автоматические выводы", report)
            original = (output / "results.csv").read_bytes()
            playback = subprocess.run(
                [sys.executable, "-m", "benchmark", "replay", str(output),
                 "--scenario", "corridor", "--solver", "good"],
                capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(playback.returncode, 0, playback.stderr)
            self.assertTrue((output / "replays" / "good" / "corridor.html").is_file())
            self.assertEqual((output / "results.csv").read_bytes(), original)
            filtered = folder / "filtered"
            report_result = subprocess.run(
                [sys.executable, "-m", "benchmark", "report", str(output),
                 "--solver", "bad", "--out", str(filtered)],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(report_result.returncode, 0, report_result.stderr)
            filtered_manifest = json.loads((filtered / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(set(filtered_manifest["solvers"]), {"good", "bad"})
            with (filtered / "pairs.csv").open(encoding="utf-8", newline="") as stream:
                pair, = csv.DictReader(stream)
            self.assertEqual(pair["outcome"], "baseline_only")
            rejected = subprocess.run(
                [sys.executable, "-m", "benchmark", "replay", str(output),
                 "--scenario", "corridor", "--solver", "good", "--out", str(output / "results.csv")],
                capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual((output / "results.csv").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
