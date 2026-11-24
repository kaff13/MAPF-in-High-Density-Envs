import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def corridor_json():
    return {
        "id": "corridor",
        "map": {"id": "corridor", "width": 3, "height": 1, "walls": [], "goals": [[1, 0]]},
        "starts": [[0, 0], [1, 0]],
        "density": 67,
        "seed": 0,
    }


class BenchmarkTests(unittest.TestCase):
    def test_default_pool_has_240_replayable_cases(self):
        from benchmark.__main__ import instance_set_hash
        from benchmark.maps import MAPS, make_instance, parse_scenario, scenario_ids

        identifiers = scenario_ids(tuple(MAPS), (50, 75, 90, 95), 10)
        self.assertEqual(len(set(identifiers)), 240)
        self.assertEqual(
            instance_set_hash(parse_scenario(identifier) for identifier in identifiers),
            "63aecaffe90cd4e2132bb8517dc34affeb52271f3cde4449ac9a282d6cc73a09",
        )
        case = parse_scenario("toyota-env2-d095-s000")
        self.assertEqual(case, make_instance("toyota-env2", 95, 0))
        self.assertEqual(len(case.map.walls), 12)
        self.assertEqual(len(case.starts), 82)
        self.assertEqual(len(set(case.starts)), 82)
        self.assertEqual(case.empty_cells, 4)
        self.assertEqual(case.starts[:5], ((6, 5), (6, 0), (7, 0), (8, 0), (5, 4)))
        self.assertEqual(len(MAPS["pillars-70x42"].walls), 216)
        self.assertEqual(len(MAPS["aisles-100x60"].walls), 2112)

    def test_validator_counts_transitions_and_rejects_following(self):
        from benchmark.maps import Instance
        from benchmark.validation import check_trace
        from tests.fixture_solvers import follow_blocker, move_blocker

        instance = Instance.from_json(corridor_json())
        self.assertEqual(check_trace(instance, move_blocker(instance)).makespan, 2)
        self.assertEqual(check_trace(instance, follow_blocker(instance)).status, "invalid")
        self.assertEqual(check_trace(instance, [instance.starts]).status, "unsolved")
        self.assertEqual(check_trace(instance, None).status, "unsolved")
        self.assertEqual(check_trace(instance, [instance.starts, ((0, 0),)]).status, "invalid")

    def test_validator_keeps_wait_ticks_and_accepts_zero_ticks(self):
        from benchmark.maps import Instance
        from benchmark.validation import check_trace
        from tests.fixture_solvers import move_blocker

        instance = Instance.from_json(corridor_json())
        self.assertEqual(check_trace(instance, [instance.starts, *move_blocker(instance)]).makespan, 3)
        data = corridor_json()
        data["starts"].reverse()
        solved = Instance.from_json(data)
        self.assertEqual(check_trace(solved, [solved.starts]).makespan, 0)

    def test_windows_solver_log_paths_are_unique(self):
        result = subprocess.run(
            [
                sys.executable, "-m", "benchmark", "run", "--scenario", "toyota-env1-d090-s000",
                "--solver", "Demo=tests.fixture_solvers:stall", "--solver", "demo=tests.fixture_solvers:stall",
            ],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("solver names must be unique", result.stderr)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib") and importlib.util.find_spec("numpy"), "install PHANS dependencies")
    def test_phans_and_checkout_agree_on_one_map(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            result = subprocess.run(
                [
                    sys.executable, "-m", "benchmark", "run", "--map", "toyota-env2",
                    "--density", "90", "--seeds", "1", "--timeout", "10",
                    "--solver", "phans", "--solver", "checkout=tests.fixture_solvers:checkout_phans",
                    "--out", str(output),
                ],
                capture_output=True, text=True, timeout=45,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with (output / "comparison.csv").open(encoding="utf-8", newline="") as stream:
                overall, on_map = list(csv.DictReader(stream))
            self.assertEqual(on_map["map"], "toyota-env2")
            self.assertEqual(overall["both_solved"], "1")
            self.assertEqual(overall["median_makespan_delta"], "0")
            plot = subprocess.run(
                [sys.executable, "-m", "benchmark", "plot", str(output),
                 "--kind", "paired", "--solver", "checkout"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(plot.returncode, 0, plot.stderr)
            self.assertTrue((output / "plots" / "maps__densities__checkout" / "paired.png").is_file())

    def test_cli_counts_failure_and_writes_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            scenario = directory / "scenario.json"
            scenario.write_text(json.dumps(corridor_json()), encoding="utf-8")
            output = directory / "run"
            result = subprocess.run(
                [
                    sys.executable, "-m", "benchmark", "run", "--scenario", str(scenario),
                    "--solver", "good=tests.fixture_solvers:move_blocker",
                    "--solver", "bad=tests.fixture_solvers:follow_blocker",
                    "--solver", "slow=tests.fixture_solvers:stall",
                    "--solver", "lazy=tests.fixture_solvers:lazy_plan",
                    "--solver", "broken=tests.fixture_solvers:fail",
                    "--baseline", "good", "--timeout", "0.2", "--out", str(output),
                ],
                capture_output=True, text=True, timeout=35,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with (output / "results.csv").open(encoding="utf-8", newline="") as stream:
                rows = {row["solver"]: row for row in csv.DictReader(stream)}
            self.assertEqual(rows["good"]["makespan"], "2")
            self.assertEqual(rows["bad"]["status"], "invalid")
            self.assertEqual(rows["bad"]["makespan"], "")
            self.assertEqual(rows["slow"]["status"], "timeout")
            self.assertEqual(rows["lazy"]["status"], "timeout")
            self.assertEqual(rows["broken"]["status"], "crash")
            with (output / "summary.csv").open(encoding="utf-8", newline="") as stream:
                rows = {row["solver"]: row for row in csv.DictReader(stream)}
            self.assertEqual(float(rows["good"]["success_rate"]), 1)
            self.assertEqual(float(rows["slow"]["success_rate"]), 0)
            self.assertTrue((output / "instances" / "corridor.json").exists())
            self.assertIn("Baseline only", (output / "report.md").read_text(encoding="utf-8"))
            self.assertTrue((output / "run.json").exists())

            if importlib.util.find_spec("matplotlib"):
                plotted = subprocess.run(
                    [sys.executable, "-m", "benchmark", "plot", str(output)],
                    capture_output=True, text=True, timeout=45,
                )
                self.assertEqual(plotted.returncode, 0, plotted.stderr)
                from benchmark.plots import REPORT_PLOT_NAMES
                for name in REPORT_PLOT_NAMES:
                    path = output / "plots" / f"{name}.png"
                    self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                csv_path = output / "results.csv"
                prefix = csv_path.read_text(encoding="utf-8").splitlines()[:-1]
                csv_path.write_text("\n".join(prefix), encoding="utf-8")
                partial = subprocess.run(
                    [sys.executable, "-m", "benchmark", "plot", str(output)],
                    capture_output=True, text=True, timeout=20,
                )
                self.assertEqual(partial.returncode, 2)
                self.assertIn("incomplete", partial.stderr)


if __name__ == "__main__":
    unittest.main()
