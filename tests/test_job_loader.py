import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.job_loader import load_job_from_dir  # noqa: E402
from tests._helpers import fixture_dir  # noqa: E402


class TestJobLoader(unittest.TestCase):
    def test_load_low(self):
        job = load_job_from_dir(fixture_dir("low_docs_job"))
        self.assertEqual(job.job_id, "FIX-LOW-DOCS")
        self.assertEqual(job.risk_tier, "LOW")
        self.assertIn("docs/**", job.allowed_writes)
        self.assertEqual(job.flags.get("product_repo_writes_allowed"), False)

    def test_load_high(self):
        job = load_job_from_dir(fixture_dir("high_security_job"))
        self.assertEqual(job.risk_tier, "HIGH")
        self.assertTrue(job.flags.get("execution_authorized"))
        self.assertEqual(job.target_repos, ["fix_product_repo"])

    def test_load_medium(self):
        job = load_job_from_dir(fixture_dir("medium_code_patch_job"))
        self.assertEqual(job.risk_tier, "MEDIUM")
        self.assertIn("plan", job.gates)
        self.assertIn("closeout", job.gates)

    def test_objective_block_scalar(self):
        # MQAI-0005 uses a folded block scalar objective; ensure it parses to a string.
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        job = load_job_from_dir(os.path.join(root, "jobs", "active", "MQAI-0005"))
        self.assertTrue(isinstance(job.objective, str) and len(job.objective) > 20)


if __name__ == "__main__":
    unittest.main()
