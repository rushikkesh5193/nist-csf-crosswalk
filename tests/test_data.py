import unittest

from csf_crosswalk.annex_a import CONTROLS
from csf_crosswalk.data import CATEGORIES, FUNCTIONS, TIERS
from csf_crosswalk.mapping import ISO_TO_CSF, controls_for


class TestReferenceData(unittest.TestCase):
    def test_csf_20_shape(self):
        self.assertEqual(list(FUNCTIONS.values()), ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"])
        self.assertEqual(len(CATEGORIES), 22)
        per = {f: sum(c.startswith(f + ".") for c in CATEGORIES) for f in FUNCTIONS}
        self.assertEqual(per, {"GV": 6, "ID": 3, "PR": 5, "DE": 2, "RS": 4, "RC": 2})
        self.assertEqual(list(TIERS.values()), ["Partial", "Risk Informed", "Repeatable", "Adaptive"])

    def test_govern_is_new_in_20(self):
        self.assertIn("GV.SC", CATEGORIES)

    def test_every_annex_a_control_is_mapped_exactly_once_or_more(self):
        self.assertEqual(len(CONTROLS), 93)
        self.assertEqual(set(ISO_TO_CSF), set(CONTROLS))
        self.assertTrue(all(len(v) >= 1 for v in ISO_TO_CSF.values()))

    def test_mapping_only_uses_real_categories(self):
        used = {c for v in ISO_TO_CSF.values() for c in v}
        self.assertLessEqual(used, set(CATEGORIES))

    def test_recovery_communication_has_no_iso_control(self):
        # A known gap between the frameworks; the tool reports it rather than hiding it.
        self.assertEqual(controls_for("RC.CO"), [])
        self.assertEqual(set(CATEGORIES) - {c for v in ISO_TO_CSF.values() for c in v}, {"RC.CO"})

    def test_spot_checks(self):
        self.assertIn("PR.AA", ISO_TO_CSF["A.5.15"])      # access control
        self.assertIn("GV.SC", ISO_TO_CSF["A.5.19"])      # supplier relationships
        self.assertIn("DE.CM", ISO_TO_CSF["A.8.16"])      # monitoring activities
        self.assertIn("PR.AT", ISO_TO_CSF["A.6.3"])       # awareness and training


if __name__ == "__main__":
    unittest.main()
