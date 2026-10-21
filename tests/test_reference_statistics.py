"""Independent reference fixtures for the ADR/MA Extension statistical contract.

These tests do not compile or run Pine. They verify documented mathematical
semantics against a deliberately simple Python reference implementation.
Run: python -m unittest discover -s tests -v
"""
import math
import unittest


def nearest_rank(values, percentile):
    ordered = sorted(values)
    if not ordered:
        return None
    index = max(0, min(len(ordered) - 1,
                       math.ceil(len(ordered) * percentile / 100) - 1))
    return ordered[index]


def magnitude_stats(values):
    if len(values) < 2:
        return None
    mean = math.fsum(values) / len(values)
    variance = math.fsum((x - mean) ** 2 for x in values) / len(values)
    return mean, math.sqrt(variance)


class ReferenceStream:
    """Simple recalculation oracle; production Pine uses incremental state."""

    def __init__(self, lookback=252, min_prior=21, min_samples=2):
        self.history = []
        self.lookback = lookback  # None = cumulative
        self.min_prior = min_prior
        self.min_samples = min_samples

    def observe(self, multiple, method="sd", threshold=1):
        prior = self.history if self.lookback is None else self.history[-self.lookback:]
        positives = [x for x in prior if x is not None and x > 0]
        negatives = [-x for x in prior if x is not None and x < 0]
        registered = len(prior) >= self.min_prior

        def calc(values):
            if not registered or len(values) < self.min_samples:
                return None
            if method == "percentile":
                return nearest_rank(values, threshold)
            result = magnitude_stats(values)
            return None if result is None else result[0] + threshold * result[1]

        up, down = calc(positives), calc(negatives)
        result = {
            "registered_bars": len(prior),
            "registered": registered,
            "up_count": len(positives),
            "down_count": len(negatives),
            "up_threshold": up,
            "down_threshold": down,
            "up_highlight": multiple is not None and multiple > 0
                            and up is not None and multiple >= up,
            "down_highlight": multiple is not None and multiple < 0
                              and down is not None and -multiple >= down,
        }
        self.history.append(multiple)
        return result


class StatisticsContractTests(unittest.TestCase):
    def test_first_eligible_bar_has_21_prior_bars(self):
        stream = ReferenceStream(lookback=504)
        for i in range(21):
            result = stream.observe(1.0)
            self.assertFalse(result["registered"], msg=f"bar {i+1} registered early")
        result = stream.observe(2.0)
        self.assertTrue(result["registered"])
        self.assertEqual(result["registered_bars"], 21)

    def test_user_target_larger_than_ipo_history(self):
        stream = ReferenceStream(lookback=50_000)
        for i in range(30):
            stream.observe(1.0 + i / 100)
        result = stream.observe(2.0)
        self.assertTrue(result["registered"])
        self.assertEqual(result["registered_bars"], 30)
        self.assertEqual(result["up_count"], 30)

    def test_rolling_lookback_not_hardcoded_to_504(self):
        stream = ReferenceStream(lookback=756)
        for _ in range(780):
            stream.observe(2.0)
        self.assertEqual(stream.observe(3.0)["registered_bars"], 756)

    def test_window_counts_all_bars_not_only_positive(self):
        stream = ReferenceStream(lookback=21)
        for i in range(35):
            stream.observe(1.0 if i % 2 == 0 else -1.0)
        result = stream.observe(1.5)
        self.assertEqual(result["registered_bars"], 21)
        self.assertEqual(result["up_count"] + result["down_count"], 21)

    def test_missing_and_zero_entries_not_qualifying_samples(self):
        stream = ReferenceStream(lookback=21)
        for i in range(21):
            stream.observe(None if i % 3 == 0 else 0.0)
        result = stream.observe(4.0)
        self.assertTrue(result["registered"])
        self.assertEqual(result["up_count"], 0)
        self.assertIsNone(result["up_threshold"])

    def test_current_bar_excluded_from_statistics(self):
        stream = ReferenceStream(lookback=21)
        for _ in range(21):
            stream.observe(1.0)
        result = stream.observe(100.0)
        self.assertEqual(result["up_threshold"], 1.0)
        self.assertTrue(result["up_highlight"])

    def test_population_standard_deviation(self):
        self.assertEqual(magnitude_stats([1, 3]), (2.0, 1.0))
        self.assertEqual(magnitude_stats([2, 2, 2]), (2.0, 0.0))

    def test_sd_and_inclusive_trigger(self):
        stream = ReferenceStream(lookback=21)
        for i in range(21):
            stream.observe(1.0 if i % 2 == 0 else 3.0)
        self.assertTrue(stream.observe(5.0, threshold=3)["up_highlight"])
        self.assertFalse(stream.observe(1.0, threshold=3)["up_highlight"])

    def test_exact_nearest_rank_percentiles(self):
        values = range(1, 11)
        for p, expected in [(80, 8), (90, 9), (95, 10), (99, 10)]:
            self.assertEqual(nearest_rank(values, p), expected)

    def test_downside_uses_positive_magnitude(self):
        stream = ReferenceStream(lookback=21)
        for _ in range(21):
            stream.observe(-2.0)
        result = stream.observe(-3.0)
        self.assertEqual(result["down_threshold"], 2.0)
        self.assertIsNone(result["up_threshold"])
        self.assertTrue(result["down_highlight"])

    def test_cumulative_does_not_discard_old_bars(self):
        stream = ReferenceStream(lookback=None)
        for _ in range(505):
            stream.observe(2.0)
        result = stream.observe(3.0)
        self.assertEqual(result["registered_bars"], 505)
        self.assertEqual(result["up_count"], 505)

    def test_per_side_minimum_qualifying_samples(self):
        stream = ReferenceStream(lookback=21, min_samples=4)
        for i in range(21):
            stream.observe(-1.0 if i < 19 else 1.0)
        result = stream.observe(4.0)
        self.assertTrue(result["registered"])
        self.assertIsNone(result["up_threshold"])
        self.assertIsNotNone(result["down_threshold"])

    def test_percentile_equality_is_a_signal(self):
        stream = ReferenceStream(lookback=21)
        for _ in range(21):
            stream.observe(2.0)
        result = stream.observe(2.0, method="percentile", threshold=95)
        self.assertTrue(result["up_highlight"])

    def test_rolling_eviction_changes_high_percentile(self):
        stream = ReferenceStream(lookback=21)
        stream.observe(100.0)
        for _ in range(20):
            stream.observe(1.0)
        old = stream.observe(3.0, method="percentile", threshold=99)
        self.assertEqual(old["up_threshold"], 100.0)
        new = stream.observe(3.0, method="percentile", threshold=99)
        self.assertEqual(new["up_threshold"], 3.0)


if __name__ == "__main__":
    unittest.main()
