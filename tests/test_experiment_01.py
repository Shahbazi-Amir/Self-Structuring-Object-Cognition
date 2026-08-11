from __future__ import annotations

import unittest

from scripts.run_experiment_01 import run


class Experiment01Tests(unittest.TestCase):
    def test_core_passes_preregistered_cases_and_beats_baseline(self) -> None:
        result = run()
        core = result["rational_core_0_1"]
        baseline = result["naive_baseline"]
        self.assertEqual(core["total"], core["correct"])
        self.assertGreater(core["accuracy"], baseline["accuracy"])


if __name__ == "__main__":
    unittest.main()

