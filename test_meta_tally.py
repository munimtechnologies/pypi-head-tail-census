"""Self-contained tests for meta_tally (no studies.csv needed to pass).

They pin the taxonomy logic to the documented 30-study corpus snapshot
(9 of 28 directional predictions held) so the meta-post headline is
reproducible and guarded.
"""
import unittest

import meta_tally


class TestTally(unittest.TestCase):
    def test_corpus_snapshot(self):
        # The 2026-10-28 snapshot of studies.csv, by outcome.
        outcomes = (
            ["HELD"] * 9
            + ["REVERSED"] * 14
            + ["NULL"] * 4
            + ["REPLICATION-FAILED"] * 1
            + ["DESCRIPTIVE"] * 1
            + ["METHOD"] * 1
        )
        r = meta_tally.tally(outcomes)
        self.assertEqual(r["total_studies"], 30)
        self.assertEqual(
            r["grouped_5way"],
            {"reversed": 14, "held": 9, "null": 4,
             "replication_failed": 1, "descriptive": 2},
        )
        # Directional = everything except DESCRIPTIVE and METHOD.
        self.assertEqual(r["directional_total"], 28)
        self.assertEqual(r["directional_held"], 9)

    def test_method_folds_into_descriptive(self):
        r = meta_tally.tally(["DESCRIPTIVE", "METHOD", "HELD"])
        self.assertEqual(r["grouped_5way"]["descriptive"], 2)
        self.assertEqual(r["directional_total"], 1)
        self.assertEqual(r["directional_held"], 1)

    def test_case_and_whitespace_insensitive(self):
        r = meta_tally.tally([" held ", "reversed"])
        self.assertEqual(r["directional_held"], 1)
        self.assertEqual(r["directional_total"], 2)

    def test_unknown_outcome_raises(self):
        with self.assertRaises(ValueError):
            meta_tally.tally(["HELD", "BOGUS"])


if __name__ == "__main__":
    unittest.main()
