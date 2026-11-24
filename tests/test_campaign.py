"""Campaign correctness: sampling, durable resume, and report-only recovery."""
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from benchmark.campaign import TIMEOUT_S, Settings, campaign_solvers, instances, run_campaign
from benchmark.checkpoints import CampaignLock, atomic_json
from benchmark.runner import Attempt


class CampaignTests(unittest.TestCase):
    def test_failed_html_can_be_rebuilt_without_measurement_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            calls = []
            with patch("benchmark.campaign.export_reports", side_effect=RuntimeError("HTML failure")):
                with self.assertRaisesRegex(RuntimeError, "HTML failure"):
                    run_campaign(root, self.settings(), run_fn=self.fake_attempt(calls))
            with patch("benchmark.campaign.export_reports", return_value=[]):
                run_campaign(root, self.settings(), run_fn=self.fake_attempt(calls))
            self.assertEqual(len(calls), 2)

    def test_missing_solved_trace_is_rejected_before_new_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            original = self.fake_attempt([])
            def solved(*args, **kwargs):
                value = original(*args, **kwargs)
                plan = args[5]
                plan.write_text('{}', encoding="utf-8")
                return Attempt("solved", 0.01, 0, source_sha256=value.source_sha256,
                               plan_path=str(plan))
            run_campaign(root, self.settings(), report=False, max_attempts=1, run_fn=solved)
            next((root / "plans").glob("*/*.gz")).unlink()
            with self.assertRaisesRegex(ValueError, "trace changed|missing"):
                run_campaign(root, self.settings(), report=False, run_fn=self.fake_attempt([]))

    def settings(self):
        return Settings(maps=("toyota-env1",), densities=(50,),
                        seeds=1, seed_start=100, ideas=("engineering",))

    def fake_attempt(self, calls):
        def run(solver, instance, timeout_s, baseline_root, log_path,
                plan_path=None, source_root=None):
            calls.append((solver.name, instance.id, timeout_s))
            log_path.write_text("fixture", encoding="utf-8")
            fingerprint = None
            if solver.entrypoint:
                module = solver.entrypoint.partition(":")[0]
                fingerprint = sha256((source_root / (module.replace(".", "/") + ".py")).read_bytes()).hexdigest()
            return Attempt("unsolved", 0.01, source_sha256=fingerprint)
        return run

    def test_default_grid_reserves_overhead_within_two_hours(self):
        settings = Settings()
        self.assertEqual((len(settings.maps), settings.densities, settings.seeds, settings.seed_start),
                         (6, (50, 75, 90, 95), 2, 100))
        self.assertEqual(settings.scenario_count, 48)
        self.assertEqual(len(campaign_solvers(settings.ideas)), 7)
        attempts = settings.scenario_count * len(campaign_solvers(settings.ideas))
        self.assertEqual(attempts, 336)
        self.assertEqual(attempts * TIMEOUT_S, 84 * 60)
        self.assertGreaterEqual(2 * 3600 - attempts * TIMEOUT_S, 36 * 60)

    def test_sampling_has_balanced_cells_and_distinct_seeds(self):
        settings = Settings(maps=("toyota-env1", "toyota-env2"), densities=(90, 95), seeds=2)
        cases = list(instances(settings))
        self.assertEqual(len(cases), 8)
        self.assertEqual(len({case.id for case in cases}), 8)
        self.assertEqual([case.seed for case in cases[:4]], [100] * 4)

    def test_interrupted_campaign_resumes_without_repeating_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            calls = []
            first = run_campaign(root, self.settings(), report=False, max_attempts=1,
                                 run_fn=self.fake_attempt(calls))
            self.assertFalse(first["complete"])
            final = run_campaign(root, self.settings(), report=False, run_fn=self.fake_attempt(calls))
            self.assertTrue(final["complete"])
            self.assertEqual([call[0] for call in calls], ["phans", "engineering"])
            self.assertTrue(all(call[2] == 15 for call in calls))

    def test_modified_source_rejects_resume_before_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            calls = []
            run_campaign(root, self.settings(), report=False, max_attempts=1,
                         run_fn=self.fake_attempt(calls))
            with patch("benchmark.campaign.measurement_sources", return_value={"changed.py": "different"}):
                with self.assertRaisesRegex(ValueError, "source|code"):
                    run_campaign(root, self.settings(), report=False, run_fn=self.fake_attempt(calls))
            self.assertEqual(len(calls), 1)

    def test_changed_profile_rejects_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            calls = []
            run_campaign(root, self.settings(), report=False, max_attempts=1,
                         run_fn=self.fake_attempt(calls))
            changed = Settings(maps=("toyota-env1",), densities=(50,), seeds=2,
                               seed_start=100, ideas=("engineering",))
            with self.assertRaisesRegex(ValueError, "configuration|profile"):
                run_campaign(root, changed, report=False, run_fn=self.fake_attempt(calls))
            self.assertEqual(len(calls), 1)

    def test_report_only_does_not_invoke_solvers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            run_campaign(root, self.settings(), report=False, run_fn=self.fake_attempt([]))
            with patch("benchmark.campaign.export_reports", return_value=[]):
                result = run_campaign(root, self.settings(), report_only=True,
                                      run_fn=lambda *a, **k: self.fail("measurement rerun"))
            self.assertTrue(result["complete"])

    def test_incomplete_campaign_cannot_claim_final_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            run_campaign(root, self.settings(), report=False, max_attempts=1,
                         run_fn=self.fake_attempt([]))
            with self.assertRaisesRegex(ValueError, "incomplete"):
                run_campaign(root, self.settings(), report_only=True)

    def test_checkpoint_corruption_is_not_silently_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            run_campaign(root, self.settings(), report=False, max_attempts=1,
                         run_fn=self.fake_attempt([]))
            checkpoint = next((root / "checkpoints").glob("*/*.json"))
            payload = json.loads(checkpoint.read_text(encoding="utf-8"))
            payload["row"]["timeout_s"] = 5
            atomic_json(checkpoint, payload)
            with self.assertRaisesRegex(ValueError, "checkpoint|budget"):
                run_campaign(root, self.settings(), report=False, run_fn=self.fake_attempt([]))

    def test_lock_excludes_a_second_writer_and_releases(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lock"
            with CampaignLock(path):
                with self.assertRaisesRegex(RuntimeError, "already|locked"):
                    with CampaignLock(path):
                        self.fail("second writer entered")
            with CampaignLock(path):
                pass
