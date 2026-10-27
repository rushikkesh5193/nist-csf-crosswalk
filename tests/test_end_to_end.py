import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from csf_crosswalk import analyse, load
from csf_crosswalk.report import crosswalk_csv, profile_csv, to_markdown

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "examples" / "sample_assessment.json"
EXPECTED = {
    ("A.9.4.1", "UNKNOWN_CONTROL"), ("DE.CM", "BELOW_TARGET"), ("PR.AT", "CATEGORY_NOT_ASSESSED"),
    ("RC.RP", "BELOW_TARGET"), ("RS.AN", "BELOW_TARGET"), ("GV.RM", "CATEGORY_EXCLUDED"),
    ("ID.IM", "DECLARED_ABOVE_EVIDENCE"), ("RC.CO", "NO_ISO_CONTROLS"), ("RS.MI", "BELOW_TARGET"),
    ("GV.SC", "UNASSESSED_CONTROLS"),
}


class TestSample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(SAMPLE)
        cls.res = analyse(cls.data)

    def test_finds_exactly_the_injected_problems(self):
        got = {(i["ref"], i["check"]) for i in self.res["issues"]}
        self.assertEqual(got - EXPECTED, set(), "false positives")
        self.assertEqual(EXPECTED - got, set(), "missed")

    def test_sorted_by_severity(self):
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        s = [order[i["severity"]] for i in self.res["issues"]]
        self.assertEqual(s, sorted(s))

    def test_roadmap_matches_gaps(self):
        self.assertEqual({r["id"] for r in self.res["roadmap"]}, {"DE.CM", "RS.AN", "RS.MI", "RC.RP"})
        self.assertEqual(self.res["roadmap"][0]["gap"], 2)

    def test_csv_outputs(self):
        rows = list(csv.reader(io.StringIO(crosswalk_csv())))
        self.assertEqual(len(rows), 94)                           # header + 93 controls
        self.assertEqual(len(list(csv.reader(io.StringIO(profile_csv(self.res))))), 23)   # header + 22 categories

    def test_markdown_states_heuristic(self):
        self.assertIn("indicative", to_markdown(self.res, "X").lower())


class TestCli(unittest.TestCase):
    def run_cli(self, *a):
        return subprocess.run([sys.executable, "-m", "csf_crosswalk", *a], cwd=ROOT, capture_output=True, text=True)

    def test_writes_files(self):
        with tempfile.TemporaryDirectory() as d:
            r = self.run_cli(str(SAMPLE), "--out-dir", d)
            self.assertEqual(r.returncode, 0, r.stderr)
            for f in ("report.md", "report.json", "csf_profile.csv", "iso_to_csf_crosswalk.csv"):
                self.assertTrue((Path(d) / f).is_file(), f)
            self.assertEqual(len(json.loads((Path(d) / "report.json").read_text())["issues"]), len(EXPECTED))

    def test_exit_codes(self):
        self.assertEqual(self.run_cli(str(SAMPLE), "--fail-on", "high").returncode, 1)
        self.assertEqual(self.run_cli("missing.json").returncode, 2)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            p.write_text(json.dumps({"targets": {"GV.OC": 7}, "controls": {}}))
            r = self.run_cli(str(p))
            self.assertEqual(r.returncode, 2)
            self.assertIn("tier must be 1..4", r.stderr)
            p.write_text("{not json")
            self.assertEqual(self.run_cli(str(p)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
