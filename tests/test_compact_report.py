import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.job_loader import load_job_from_dir  # noqa: E402
from orchestrator.job_state import infer_state  # noqa: E402
from orchestrator.gate_policy import evaluate  # noqa: E402
from orchestrator import compact_report, eval_runner  # noqa: E402
from tests._helpers import copy_fixture  # noqa: E402


class TestCompactReport(unittest.TestCase):
    def setUp(self):
        self.dir = copy_fixture("medium_code_patch_job")
        self.job = load_job_from_dir(self.dir)
        self.state = infer_state(self.job)
        self.gates = evaluate(self.job, self.state)

    def tearDown(self):
        shutil.rmtree(self.dir.parent, ignore_errors=True)

    def test_report_written(self):
        dest = compact_report.build(self.job, self.state, self.gates, ["orchestrator/foo.py"])
        text = dest.read_text(encoding="utf-8")
        self.assertIn("Compact Report", text)
        self.assertIn("next action", text)
        self.assertIn("push", text.lower())

    def test_eval_runner_writes_json(self):
        dest = eval_runner.run_and_write(self.job)
        self.assertTrue(dest.exists())
        import json
        payload = json.loads(dest.read_text(encoding="utf-8"))
        gates = {r["gate"] for r in payload}
        self.assertIn("secret_scan", gates)
        self.assertIn("risk_tier_assignment", gates)
        # never fake pass: statuses are from the allowed set
        for r in payload:
            self.assertIn(r["status"], ("pass", "fail", "skipped"))


if __name__ == "__main__":
    unittest.main()
