from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest

from benchmark.html_report import write_html_report
from tests.test_report_metrics import result


class Views(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.current = None
        self.depth = 0
        self.text = {}
        self.links = {}
        self.hidden = {}
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and "data-report-view" in attrs:
            self.current = attrs["data-report-view"]
            self.depth = 1
            self.text[self.current] = ""
            self.links[self.current] = []
            self.hidden[self.current] = "hidden" in attrs
        elif self.current is not None:
            if tag == "div":
                self.depth += 1
            if tag == "a":
                self.links[self.current].append(attrs["href"])

    def handle_data(self, data):
        if self.current is not None:
            self.text[self.current] += data

    def handle_endtag(self, tag):
        if tag == "div" and self.current is not None:
            self.depth -= 1
            if self.depth == 0:
                self.current = None


class ReportViewTests(unittest.TestCase):
    def test_each_map_has_its_own_metrics_and_data_links(self):
        first = [result("a", "phans", time=4, makespan=12), result("a", "new", time=2, makespan=8)]
        second = [result("b", "phans", time=10, makespan=30), result("b", "new", "timeout")]
        for row in first:
            row["map"] = "map-a"
        for row in second:
            row["map"] = "map-b"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            path = write_html_report(output, first + second, "phans", [], map_plots={"map-a": [], "map-b": []})
            document = Views(path.read_text(encoding="utf-8"))
        self.assertEqual(set(document.text), {"", "map-a", "map-b"})
        self.assertFalse(document.hidden[""])
        self.assertTrue(document.hidden["map-a"])
        self.assertTrue(document.hidden["map-b"])
        self.assertIn("50.0%", document.text[""])
        self.assertNotIn("50.0%", document.text["map-b"])
        self.assertIn("0.0%", document.text["map-b"])
        self.assertIn("100.0%", document.text["map-a"])
        self.assertIn("maps/map-a/results.csv", document.links["map-a"])
        self.assertIn("maps/map-b/pairs.csv", document.links["map-b"])
        self.assertIn("results.csv", document.links[""])


if __name__ == "__main__":
    unittest.main()
