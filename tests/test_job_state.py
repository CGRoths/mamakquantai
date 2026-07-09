import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.job_loader import load_job_from_dir  # noqa: E402
from orchestrator.job_state import infer_state  # noqa: E402
from tests._helpers import fixture_dir  # noqa: E402


class TestJobState(unittest.TestCase):
    def _state(self, name):
        return infer_state(load_job_from_dir(fixture_dir(name))).current_state

    def test_low_scaffolded(self):
        self.assertEqual(self._state("low_docs_job"), "scaffolded")

    def test_high_executed(self):
        # reviews + plan approval + exec approval + execution_summary, no validation yet
        self.assertEqual(self._state("high_security_job"), "executed")

    def test_medium_review_passed(self):
        # reviews + validation + executed-diff review, no final approval
        self.assertEqual(self._state("medium_code_patch_job"), "review_passed")

    def test_not_hardcoded(self):
        # three different fixtures resolve to three different states
        states = {self._state(n) for n in
                  ("low_docs_job", "high_security_job", "medium_code_patch_job")}
        self.assertEqual(len(states), 3)


if __name__ == "__main__":
    unittest.main()
