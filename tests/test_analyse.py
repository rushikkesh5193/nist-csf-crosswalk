import unittest

from csf_crosswalk.analyse import indicative_tier, analyse
from csf_crosswalk.mapping import controls_for
from helpers import CFG, all_impl, run, cat, checks


class TestTiering(unittest.TestCase):
    def test_threshold_boundaries(self):
        for cov, want in [(0, 1), (29.9, 1), (30, 2), (64.9, 2), (65, 3), (94.9, 3), (95, 4), (100, 4)]:
            self.assertEqual(indicative_tier(cov, CFG), want, cov)
        self.assertIsNone(indicative_tier(None, CFG))


class TestCoverage(unittest.TestCase):
    def test_all_implemented_gives_full_coverage_and_no_gaps(self):
        res = run()
        self.assertEqual(res["roadmap"], [])
        self.assertEqual(cat(res, "PR.AA")["coverage"], 100.0)
        self.assertEqual(cat(res, "PR.AA")["indicative_tier"], 4)

    def test_partial_counts_half_and_planned_zero(self):
        ctrls = controls_for("DE.CM")                          # 3 controls
        c = all_impl(**{ctrls[0]: {"status": "partial"}, ctrls[1]: {"status": "planned"}})
        self.assertEqual(cat(run(c), "DE.CM")["coverage"], round(100 * (0.5 + 0 + 1) / 3, 1))

    def test_not_applicable_is_excluded_from_denominator(self):
        ctrls = controls_for("DE.CM")
        c = all_impl(**{ctrls[0]: {"status": "not_applicable"}, ctrls[1]: {"status": "not_implemented"}})
        res = run(c)
        self.assertEqual(cat(res, "DE.CM")["applicable"], 2)
        self.assertEqual(cat(res, "DE.CM")["coverage"], 50.0)

    def test_unassessed_controls_count_as_zero_and_are_flagged(self):
        ctrls = controls_for("PR.DS")
        c = all_impl()
        del c[ctrls[0]]
        res = run(c)
        self.assertEqual(cat(res, "PR.DS")["unassessed"], 1)
        self.assertLess(cat(res, "PR.DS")["coverage"], 100)
        self.assertIn(("PR.DS", "UNASSESSED_CONTROLS"), checks(res))

    def test_a_control_mapped_to_two_categories_counts_in_both(self):
        c = all_impl(**{"A.5.26": {"status": "not_implemented"}})   # maps to RS.MA, RS.MI and RC.RP
        res = run(c)
        for k in ("RS.MA", "RS.MI", "RC.RP"):
            self.assertLess(cat(res, k)["coverage"], 100, k)


class TestIssues(unittest.TestCase):
    def test_clean_assessment_only_reports_the_structural_gap(self):
        self.assertEqual(checks(run()), {("RC.CO", "NO_ISO_CONTROLS")})

    def test_below_target_severity_by_gap_size(self):
        ctrls = controls_for("DE.CM")
        weak = all_impl(**{c: {"status": "not_implemented"} for c in ctrls})        # tier 1, target 3 -> gap 2
        res = run(weak)
        self.assertEqual([i["severity"] for i in res["issues"] if i["check"] == "BELOW_TARGET" and i["ref"] == "DE.CM"], ["high"])
        res = run(weak, targets={"DE.CM": 2})                                          # gap 1 -> medium
        self.assertEqual([i["severity"] for i in res["issues"] if i["check"] == "BELOW_TARGET" and i["ref"] == "DE.CM"], ["medium"])
        res = run(weak, targets={"DE.CM": 1})                                          # target met
        self.assertNotIn(("DE.CM", "BELOW_TARGET"), checks(res))

    def test_roadmap_orders_largest_gap_first(self):
        c = all_impl(**{x: {"status": "not_implemented"} for x in controls_for("DE.CM") + controls_for("GV.RM")})
        res = run(c, targets={"DE.CM": 4, "GV.RM": 2})
        self.assertEqual([r["id"] for r in res["roadmap"]][:2], ["DE.CM", "GV.RM"])

    def test_category_not_assessed_and_excluded(self):
        c = all_impl()
        for x in controls_for("PR.AT"):
            del c[x]
        for x in controls_for("GV.RM"):
            c[x] = {"status": "not_applicable"}
        got = checks(run(c))
        self.assertIn(("PR.AT", "CATEGORY_NOT_ASSESSED"), got)
        self.assertIn(("GV.RM", "CATEGORY_EXCLUDED"), got)

    def test_unknown_control_flagged(self):
        got = checks(run(all_impl(**{"A.9.4.1": {"status": "implemented"}})))
        self.assertIn(("A.9.4.1", "UNKNOWN_CONTROL"), got)

    def test_declared_tier_overrides_but_is_challenged(self):
        weak = all_impl(**{x: {"status": "not_implemented"} for x in controls_for("ID.IM")})   # indicative tier 1
        res = run(weak, declared_tiers={"ID.IM": 3})
        self.assertEqual(cat(res, "ID.IM")["current"], 3)
        self.assertEqual(cat(res, "ID.IM")["basis"], "declared")
        self.assertIn(("ID.IM", "DECLARED_ABOVE_EVIDENCE"), checks(res))
        res = run(weak, declared_tiers={"ID.IM": 2})                                          # within margin of 1
        self.assertNotIn(("ID.IM", "DECLARED_ABOVE_EVIDENCE"), checks(res))

    def test_default_target_is_used_when_not_set(self):
        self.assertEqual(cat(run(), "PR.AA")["target"], 3)
        self.assertEqual(cat(run(default_target=2), "PR.AA")["target"], 2)

    def test_function_summary(self):
        res = run()
        f = {x["id"]: x for x in res["functions"]}
        self.assertEqual(f["RC"]["no_iso_controls"], 1)
        self.assertEqual(f["GV"]["categories"], 6)


class TestValidation(unittest.TestCase):
    def test_bad_inputs_rejected(self):
        for bad in ({"targets": {"XX.YY": 3}}, {"targets": {"GV.OC": 5}}, {"declared_tiers": {"GV.OC": 0}}, {"default_target": 9}):
            with self.assertRaises(ValueError, msg=str(bad)):
                run(**bad)
        with self.assertRaises(ValueError):
            run(all_impl(**{"A.5.1": {"status": "done"}}))


if __name__ == "__main__":
    unittest.main()
