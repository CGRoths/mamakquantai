import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.job_loader import load_job_from_dir  # noqa: E402
from orchestrator.job_state import infer_state  # noqa: E402
from orchestrator.gate_policy import evaluate  # noqa: E402
from tests._helpers import fixture_dir  # noqa: E402


class TestGatePolicy(unittest.TestCase):
    def _eval(self, name):
        job = load_job_from_dir(fixture_dir(name))
        return job, evaluate(job, infer_state(job))

    def test_low_next_is_plan(self):
        _, ge = self._eval("low_docs_job")
        self.assertEqual(ge.tier, "LOW")
        self.assertEqual(ge.next_gate, "plan")

    def test_high_next_is_validation(self):
        _, ge = self._eval("high_security_job")
        self.assertEqual(ge.next_gate, "validation")

    def test_medium_awaiting_final_commit(self):
        _, ge = self._eval("medium_code_patch_job")
        self.assertEqual(ge.next_gate, "final_commit")
        self.assertTrue(ge.human_required)

    def test_push_never_done_without_flag(self):
        for name in ("low_docs_job", "high_security_job", "medium_code_patch_job"):
            _, ge = self._eval(name)
            push = [g for g in ge.gates if g.name == "push"][0]
            self.assertNotEqual(push.status, "done")

    def test_blocked_actions_present(self):
        _, ge = self._eval("high_security_job")
        joined = " ".join(ge.blocked_actions)
        self.assertIn("push", joined)


if __name__ == "__main__":
    unittest.main()
