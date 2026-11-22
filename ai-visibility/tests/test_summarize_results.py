import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/summarize_results.py"
SPEC = importlib.util.spec_from_file_location("summary", SCRIPT)
summary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(summary)


def row(run_id="r1", **changes):
    result = dict.fromkeys(summary.REQUIRED, "")
    result.update(
        run_id=run_id, experiment_id="e1", phase="baseline", platform="Test",
        surface="consumer-search-on", model="unknown", locale="en-US", prompt_id="U01",
        query_type="unbranded", recorded_at="2026-11-22T12:00:00Z", status="ok",
        offer_in_scope="0",
        brand_mentioned="1", brand_recommended="0", owned_page_cited="0",
        third_party_brand_cited="0", answer_artifact="raw/r1.txt",
    )
    result.update(changes)
    return result


class SummaryTests(unittest.TestCase):
    def load(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "answers.csv"
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=summary.REQUIRED)
                writer.writeheader()
                writer.writerows(rows)
            return summary.load_rows(path)

    def test_failures_are_reported_not_counted_as_zero_answers(self):
        error = row("r3", status="error", notes="Provider timeout", answer_artifact="", offer_in_scope="",
                    **dict.fromkeys(summary.METRICS, ""))
        records = self.load([row(), row("r2", brand_mentioned="0"), error])
        group = summary.summarize(records)["groups"][0]
        self.assertEqual(group["status_counts"], {"ok": 2, "error": 1, "not_run": 0})
        metric = group["metrics"]["brand_mentioned"]
        self.assertEqual((metric["positive"], metric["measured"], metric["rate"]), (1, 2, 0.5))
        self.assertAlmostEqual(group["collection_success_rate"], 2 / 3)

    def test_prompt_weighting_exposes_unequal_repeats(self):
        records = self.load([row("r1"), row("r2"), row("r3"),
                             row("r4", prompt_id="U02", brand_mentioned="0")])
        metric = summary.summarize(records)["groups"][0]["metrics"]["brand_mentioned"]
        self.assertEqual(metric["rate"], 0.75)
        self.assertEqual(metric["equal_prompt_mean"], 0.5)

    def test_offer_omissions_remain_in_denominator(self):
        records = self.load([row(offer_in_scope="1", offer_accurate="1"),
                             row("r2", offer_in_scope="1", offer_accurate="0"), row("r3")])
        metric = summary.summarize(records)["groups"][0]["metrics"]["offer_accurate"]
        self.assertEqual((metric["positive"], metric["measured"], metric["not_applicable"]), (1, 2, 1))

    def test_no_observations_is_unmeasured_not_zero_percent(self):
        record = row(status="not_run", notes="No product access", answer_artifact="", offer_in_scope="",
                     **dict.fromkeys(summary.METRICS, ""))
        result = summary.summarize(self.load([record]))
        self.assertEqual(result["measurement_status"], "unmeasured")
        self.assertIsNone(result["groups"][0]["metrics"]["brand_mentioned"]["rate"])
        self.assertEqual(summary.summarize(self.load([]))["groups"], [])

    def test_each_comparison_dimension_stays_separate(self):
        records = [row("r0")]
        changes = {"experiment_id": "e2", "phase": "followup", "platform": "Other",
                   "surface": "api-search", "model": "new-version", "locale": "zh-CN",
                   "query_type": "branded"}
        records += [row(f"r{i}", **{key: value}) for i, (key, value) in enumerate(changes.items(), 1)]
        self.assertEqual(len(summary.summarize(self.load(records))["groups"]), 8)

    def test_duplicate_ids_and_missing_flags_rejected(self):
        for records in ([row(), row()], [row(brand_mentioned="")], [row(brand_mentioned="true")]):
            with self.subTest(records=records), self.assertRaises(ValueError):
                self.load(records)

    def test_inconsistent_recommendation_or_offer_rejected(self):
        for change in ({"brand_recommended": "1"}, {"offer_accurate": "1"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.load([row(brand_mentioned="0", **change)])

    def test_owned_citation_can_exist_without_mention(self):
        records = self.load([row(brand_mentioned="0", owned_page_cited="1")])
        group = summary.summarize(records)["groups"][0]
        self.assertEqual(group["metrics"]["owned_page_cited"]["rate"], 1)
        self.assertEqual(group["metrics"]["brand_mentioned"]["rate"], 0)

    def test_invalid_status_timestamp_and_missing_artifact_rejected(self):
        for change in ({"status": "success"}, {"recorded_at": "2026-11-22"},
                       {"recorded_at": "garbage"}, {"answer_artifact": ""}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.load([row(**change)])

    def test_failed_runs_cannot_carry_observations(self):
        with self.assertRaises(ValueError):
            self.load([row(status="error", notes="Timeout")])

    def test_wilson_interval_for_zero_and_full_success(self):
        self.assertIsNone(summary.wilson(0, 0))
        low, high = summary.wilson(0, 10)
        self.assertAlmostEqual(low, 0)
        self.assertAlmostEqual(high, 0.2775328, places=6)
        low, high = summary.wilson(10, 10)
        self.assertAlmostEqual(low, 0.7224672, places=6)
        self.assertAlmostEqual(high, 1)

    def test_csv_quoted_unicode_notes_roundtrip(self):
        records = self.load([row(notes='准确, quoted "offer"\nsecond line')])
        self.assertEqual(records[0]["notes"], '准确, quoted "offer"\nsecond line')

    def test_unknown_citations_preserve_observed_recommendations(self):
        records = self.load([row(brand_recommended="1", owned_page_cited="",
                                 third_party_brand_cited="", notes="Citations were not saved")])
        group = summary.summarize(records)["groups"][0]
        self.assertEqual(group["status_counts"]["ok"], 1)
        self.assertEqual(group["metrics"]["brand_recommended"]["rate"], 1)
        metric = group["metrics"]["owned_page_cited"]
        self.assertEqual(metric["unknown"], 1)
        self.assertEqual(metric["possible_rate_bounds"], [0, 1])
        self.assertIsNone(metric["rate"])

    def test_out_of_scope_offer_cannot_be_scored(self):
        with self.assertRaises(ValueError):
            self.load([row(offer_accurate="0")])

    def test_timestamp_range_uses_instants_not_local_clock_strings(self):
        records = self.load([row(recorded_at="2026-11-22T15:00:00+08:00"),
                             row("r2", recorded_at="2026-11-22T08:00:00Z")])
        observed_range = summary.summarize(records)["groups"][0]["observed_at_range_utc"]
        self.assertEqual(observed_range, ["2026-11-22T07:00:00+00:00", "2026-11-22T08:00:00+00:00"])


if __name__ == "__main__":
    unittest.main()
