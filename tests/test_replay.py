import gzip
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from benchmark.maps import Instance


class ReplayDocument(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.payload = ""
        self.in_payload = False
        self.in_script = False
        self.script = ""
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.ids.add(attrs.get("id"))
        self.in_payload = tag == "script" and attrs.get("id") == "replay-data"
        self.in_script = tag == "script" and attrs.get("type") != "application/json"

    def handle_data(self, data):
        if self.in_payload:
            self.payload += data
        if self.in_script:
            self.script += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_payload = False
            self.in_script = False


def corridor():
    return Instance.from_json({
        "id": "corridor",
        "map": {"id": "corridor", "width": 3, "height": 1,
                "walls": [], "goals": [[1, 0]]},
        "starts": [[0, 0], [1, 0]], "density": 67, "seed": 0,
    })


class ReplayTests(unittest.TestCase):
    def test_export_preserves_waits_and_exposes_player_controls(self):
        from benchmark.replay import write_replay

        frames = [((0, 0), (1, 0)), ((0, 0), (1, 0)),
                  ((0, 0), (2, 0)), ((1, 0), (2, 0)), ((1, 0), (2, 0))]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "nested" / "replay.html"
            self.assertEqual(write_replay(corridor(), frames, output, solver_name="PHANS"), output)
            document = ReplayDocument(output.read_text(encoding="utf-8"))
        payload = json.loads(document.payload)
        self.assertEqual(payload["frames"], [
            [[0, 0], [1, 0]], [[0, 0], [1, 0]], [[0, 0], [2, 0]],
            [[1, 0], [2, 0]], [[1, 0], [2, 0]],
        ])
        self.assertEqual(payload["makespan"], 3)
        self.assertEqual(payload["status"], "solved")
        self.assertEqual(payload["solver"], "PHANS")
        self.assertTrue({"canvas", "play", "back", "forward", "timeline", "speed",
                         "show-ids", "zoom", "fit"}.issubset(document.ids))

    def test_incomplete_trace_cannot_claim_solved(self):
        from benchmark.replay import write_replay

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "replay.html"
            write_replay(corridor(), [corridor().starts], output, status="solved")
            payload = json.loads(ReplayDocument(output.read_text(encoding="utf-8")).payload)
        self.assertEqual(payload["status"], "unsolved")
        self.assertEqual(payload["reported_status"], "solved")
        self.assertIsNone(payload["makespan"])

    def test_rejects_invalid_paths_and_noninteger_coordinates(self):
        from benchmark.replay import write_replay

        cases = [
            ([corridor().starts, ((1, 0), (2, 0))], "following conflict"),
            ([corridor().starts, ((0.5, 0), (2, 0))], "integer cell pairs"),
            ([corridor().starts, ((False, 0), (2, 0))], "integer cell pairs"),
            ([corridor().starts, ((0, 0),)], "wrong agent count"),
            ([((0, 0), (2, 0))], "starts or agent order differ"),
            ([], "at least one frame"),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "replay.html"
            for frames, message in cases:
                with self.subTest(message=message):
                    with self.assertRaisesRegex(ValueError, message):
                        write_replay(corridor(), frames, output)
                    self.assertFalse(output.exists())

    def test_metadata_cannot_escape_json_script_element(self):
        from benchmark.replay import write_replay

        injected = '</script><script>alert("x")</script>&\u2028'
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "replay.html"
            write_replay(corridor(), [corridor().starts], output, solver_name=injected,
                         detail=injected)
            html = output.read_text(encoding="utf-8")
        self.assertNotIn(injected, html)
        payload = json.loads(ReplayDocument(html).payload)
        self.assertEqual(payload["solver"], injected)
        self.assertEqual(payload["detail"], injected)

    def test_loads_plain_and_gzip_plan_objects(self):
        from benchmark.replay import load_plan

        plan = {"instance_id": "corridor", "frames": [[[0, 0], [1, 0]]]}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            plain = directory / "plan.json"
            zipped = directory / "plan.json.gz"
            plain.write_text(json.dumps(plan), encoding="utf-8")
            with gzip.open(zipped, "wt", encoding="utf-8") as stream:
                json.dump(plan, stream)
            self.assertEqual(load_plan(plain), plan)
            self.assertEqual(load_plan(zipped), plan)
            plain.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON object"):
                load_plan(plain)


class PairedReplayTests(unittest.TestCase):
    def plans(self):
        return (
            {"solver": "PHANS", "status": "solved", "instance_id": "corridor",
             "frames": [[[0, 0], [1, 0]], [[0, 0], [2, 0]], [[1, 0], [2, 0]]]},
            {"solver": "candidate", "status": "solved", "instance_id": "corridor",
             "provenance": {"kind": "rerun"}, "recorded_status": "timeout", "replay_attempt": True,
             "frames": [[[0, 0], [1, 0]], [[0, 0], [1, 0]], [[0, 0], [2, 0]],
                        [[0, 0], [2, 0]], [[1, 0], [2, 0]]]},
        )

    def document(self, baseline, candidate):
        from benchmark.replay import write_paired_replay

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "paired.html"
            self.assertEqual(write_paired_replay(corridor(), baseline, candidate, output), output)
            return ReplayDocument(output.read_text(encoding="utf-8"))

    def test_exports_same_scenario_with_unequal_lengths_and_waits(self):
        baseline, candidate = self.plans()
        payload = json.loads(self.document(baseline, candidate).payload)
        self.assertEqual(payload["instance"]["id"], "corridor")
        self.assertEqual(payload["baseline"]["frames"], baseline["frames"])
        self.assertEqual(payload["candidate"]["frames"], candidate["frames"])
        self.assertEqual(payload["baseline"]["last_tick"], 2)
        self.assertEqual(payload["candidate"]["last_tick"], 4)
        self.assertEqual(payload["baseline"]["makespan"], 2)
        self.assertEqual(payload["candidate"]["makespan"], 4)
        self.assertEqual(payload["max_tick"], 4)
        self.assertEqual(payload["candidate"]["provenance"], {"kind": "rerun"})
        self.assertEqual(payload["candidate"]["recorded_status"], "timeout")
        self.assertTrue(payload["candidate"]["replay_attempt"])
        self.assertFalse(payload["autoplay"])

    def test_partial_candidate_retains_recorded_outcome(self):
        baseline, candidate = self.plans()
        candidate["frames"] = candidate["frames"][:3]
        candidate["status"] = "timeout"
        payload = json.loads(self.document(baseline, candidate).payload)
        self.assertEqual(payload["candidate"]["status"], "unsolved")
        self.assertEqual(payload["candidate"]["reported_status"], "timeout")
        self.assertIsNone(payload["candidate"]["makespan"])

    def test_rejects_invalid_baseline_without_replacing_existing_output(self):
        from benchmark.replay import write_paired_replay

        baseline, candidate = self.plans()
        baseline["frames"] = [baseline["frames"][0], [[1, 0], [2, 0]]]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "paired.html"
            output.write_text("previous replay", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "baseline: tick 1: following conflict"):
                write_paired_replay(corridor(), baseline, candidate, output)
            self.assertEqual(output.read_text(encoding="utf-8"), "previous replay")

    def test_rejects_different_scenario_metadata(self):
        baseline, candidate = self.plans()
        candidate["instance_id"] = "another-scenario"
        with self.assertRaisesRegex(ValueError, "candidate:.*instance"):
            self.document(baseline, candidate)

    def test_absent_trace_cannot_claim_zero_tick_solution(self):
        from benchmark.replay import write_paired_replay

        data = corridor().to_json()
        data["starts"] = ((1, 0), (0, 0))
        instance = Instance.from_json(data)
        baseline = {"solver": "PHANS", "status": "solved", "frames": [instance.starts]}
        candidate = {"solver": "candidate", "status": "timeout", "frames": [instance.starts],
                     "trace_available": False, "detail": "Трасса отсутствует"}
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "paired.html"
            write_paired_replay(instance, baseline, candidate, output)
            payload = json.loads(ReplayDocument(output.read_text(encoding="utf-8")).payload)
        self.assertEqual(payload["baseline"]["status"], "solved")
        self.assertEqual(payload["baseline"]["makespan"], 0)
        self.assertEqual(payload["candidate"]["status"], "unavailable")
        self.assertFalse(payload["candidate"]["trace_available"])
        self.assertIsNone(payload["candidate"]["makespan"])
        self.assertEqual(payload["candidate"]["reported_status"], "timeout")

    @unittest.skipUnless(shutil.which("node"), "Node required for offline player interaction check")
    def test_player_starts_paused_and_holds_shorter_trace_at_shared_last_tick(self):
        document = self.document(*self.plans())
        # Execute the exported script against small DOM/canvas stand-ins. This
        # checks actual initialization and event handling without browser I/O.
        harness = r'''
const assert = require("node:assert/strict");
const elements = new Map();
let scheduled = 0;
const context = new Proxy({}, {get: () => () => {}});
function element() {
  return {style:{}, handlers:{}, clientWidth:650, clientHeight:380,
    textContent:"", value:"1", checked:false, width:0, height:0,
    append(){}, setAttribute(){}, addEventListener(name, callback){this.handlers[name]=callback;},
    getContext(){return context;}, scrollTo(){}, getBoundingClientRect(){return {left:0,top:0};}};
}
global.document = {hidden:false, createElement:element, addEventListener(){},
  getElementById(id){if (!elements.has(id)) elements.set(id,element()); return elements.get(id);}};
global.window = {devicePixelRatio:1,addEventListener(){}};
global.requestAnimationFrame = () => {scheduled++; return scheduled;};
global.cancelAnimationFrame = () => {};
document.getElementById("replay-data").textContent = PAYLOAD;
PLAYER
assert.equal(scheduled, 0, "opening the replay must not start playback");
assert.equal(elements.get("play").textContent, "Пуск");
assert.equal(Number(elements.get("timeline").max), 4);
elements.get("timeline").handlers.input({target:{value:"4"}});
assert.equal(elements.get("baseline-tick").textContent, "Такт: 2 / 2");
assert.equal(elements.get("candidate-tick").textContent, "Такт: 4 / 4");
assert.equal(elements.get("tick").textContent, "Такт: 4 / 4");
assert.equal(scheduled, 0, "scrubbing must leave playback paused");
'''.replace("PAYLOAD", json.dumps(document.payload)).replace("PLAYER", document.script)
        result = subprocess.run([shutil.which("node"), "-"], input=harness,
                                encoding="utf-8", capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
