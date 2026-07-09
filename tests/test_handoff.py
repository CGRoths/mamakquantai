import io
import os
import shutil
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.job_loader import load_job_from_dir  # noqa: E402
from orchestrator.job_state import infer_state  # noqa: E402
from orchestrator.gate_policy import evaluate  # noqa: E402
from orchestrator import handoff, compact_report, mqai_runner  # noqa: E402
from tests._helpers import copy_fixture  # noqa: E402


class TestHandoff(unittest.TestCase):
    def setUp(self):
        self.dir = copy_fixture("high_security_job")
        self.job = load_job_from_dir(self.dir)
        self.state = infer_state(self.job)
        self.gates = evaluate(self.job, self.state)

    def tearDown(self):
        shutil.rmtree(self.dir.parent, ignore_errors=True)

    def test_generates_core_artifacts(self):
        written = handoff.build_handoff(self.job, self.state, self.gates,
                                        "codex", "claude", "context_exhausted")
        names = {p.name for p in written}
        hd = self.job.output_dir / "handoff"
        self.assertTrue((hd / "latest_handoff.md").exists())
        self.assertTrue((hd / "codex_to_claude.md").exists())
        self.assertTrue((hd / "resume_prompt.md").exists())
        self.assertIn("handoff_state.json", names)

    def test_stop_reason_context_exhausted(self):
        handoff.build_handoff(self.job, self.state, self.gates, "codex", "claude", "context_exhausted")
        text = (self.job.output_dir / "handoff" / "latest_handoff.md").read_text(encoding="utf-8")
        self.assertIn("context_exhausted", text)

    def test_stop_reason_defaults_unknown(self):
        self.assertEqual(handoff.normalize_stop_reason(None), "unknown")
        self.assertEqual(handoff.normalize_stop_reason("bogus"), "unknown")

    def test_resume_prompt_says_no_chat_history(self):
        handoff.build_handoff(self.job, self.state, self.gates, "codex", "claude")
        text = (self.job.output_dir / "handoff" / "resume_prompt.md").read_text(encoding="utf-8")
        self.assertIn("Do NOT rely on chat history", text)

    def test_compact_report_handoff_ready(self):
        handoff.build_handoff(self.job, self.state, self.gates, "codex", "claude")
        state2 = infer_state(self.job)  # re-infer after handoff artifacts exist
        dest = compact_report.build(self.job, state2, evaluate(self.job, state2))
        text = dest.read_text(encoding="utf-8")
        self.assertIn("handoff_ready: true", text)
        self.assertIn("recommended_next_agent: claude", text)

    def _run_cli(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = mqai_runner.main(argv)
        return code, buf.getvalue()

    def test_cli_handoff_and_resume(self):
        # Point the loader at the temp fixture by placing it under a jobs/active layout.
        # Simpler: call the router functions directly for CLI-equivalent smoke via load_job_from_dir
        # is not id-based; so we exercise mqai_runner against MQAI-0005 in the real repo (read-only-ish,
        # writes only to that job's output/handoff which is allowed).
        code, out = self._run_cli(["handoff", "MQAI-0005", "--from", "codex", "--to", "claude",
                                   "--stop-reason", "context_exhausted"])
        self.assertEqual(code, 0)
        self.assertIn("handoff", out)
        code2, out2 = self._run_cli(["resume", "MQAI-0005", "--agent", "claude"])
        self.assertEqual(code2, 0)
        self.assertIn("resume prompt", out2)


if __name__ == "__main__":
    unittest.main()
