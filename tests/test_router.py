import unittest

from router import choose_backend
from router.context_policy import classify
from router.scheduler import RouterState


class RouterPolicyTest(unittest.TestCase):
    def test_primary_below_peak(self):
        self.assertEqual(choose_backend(100, 100, 7), "primary")

    def test_spillover_at_peak(self):
        self.assertEqual(choose_backend(100, 100, 8), "spillover")

    def test_long_context(self):
        self.assertEqual(choose_backend(40000, 100, 0), "long_context")

    def test_rejects_oversize(self):
        with self.assertRaises(ValueError):
            choose_backend(131072, 1, 0)

    def test_negative_token_count_is_rejected(self):
        with self.assertRaises(ValueError):
            classify(-1, 100)

    def test_long_context_does_not_fall_back_to_primary(self):
        state = RouterState()
        self.assertEqual(state.ordered_backends(40_000, 1_000, now=0), ["spillover"])

    def test_primary_failure_uses_spillover(self):
        state = RouterState()
        state.cooldowns.mark_failed("primary", now=0)
        self.assertEqual(state.ordered_backends(100, 100, now=1)[0], "spillover")

    def test_primary_returns_after_cooldown(self):
        state = RouterState()
        state.cooldowns.mark_failed("primary", now=0)
        self.assertEqual(state.ordered_backends(100, 100, now=16)[0], "primary")

    def test_peak_routes_to_spillover(self):
        state = RouterState(primary_active=8)
        self.assertEqual(state.ordered_backends(100, 100, now=0)[0], "spillover")


if __name__ == "__main__":
    unittest.main()
