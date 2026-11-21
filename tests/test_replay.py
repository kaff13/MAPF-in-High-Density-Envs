import gzip
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest

from benchmark.maps import Instance


class ReplayDocument(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.payload = ""
        self.in_payload = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.ids.add(attrs.get("id"))
        self.in_payload = tag == "script" and attrs.get("id") == "replay-data"

    def handle_data(self, data):
        if self.in_payload:
            self.payload += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_payload = False


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
