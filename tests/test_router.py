import unittest

from router import choose_backend


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


if __name__ == "__main__":
    unittest.main()

