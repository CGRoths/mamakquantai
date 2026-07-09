import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.job_loader import load_job_from_dir  # noqa: E402
from orchestrator.job_state import infer_state  # noqa: E402
from orchestrator.gate_policy import evaluate  # noqa: E402
from orchestrator import context_pack, agent_prompt_builder  # noqa: E402
from tests._helpers import copy_fixture  # noqa: E402


class TestContextPack(unittest.TestCase):
    def setUp(self):
        self.dir = copy_fixture("high_security_job")
        self.job = load_job_from_dir(self.dir)
        self.state = infer_state(self.job)
        self.gates = evaluate(self.job, self.state)

    def tearDown(self):
        shutil.rmtree(self.dir.parent, ignore_errors=True)

    def test_context_pack_written(self):
        dest = context_pack.build(self.job, self.state, self.gates)
        self.assertTrue(dest.exists())
        text = dest.read_text(encoding="utf-8")
        self.assertIn(self.job.job_id, text)
        self.assertIn("Next allowed action", text)
        self.assertIn("Hard stops", text)

    def test_prompts_written(self):
        written = agent_prompt_builder.build(self.job, self.state, self.gates)
        names = {p.name for p in written}
        self.assertIn("claude_reviewer_prompt.md", names)
        self.assertIn("codex_builder_prompt.md", names)
        self.assertIn("gpt_synthesis_prompt.md", names)


if __name__ == "__main__":
    unittest.main()
