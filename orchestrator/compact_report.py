"""Generate the compact status report for a job."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .schemas import GateEvaluation, JobSpec, StateResult


def build(job: JobSpec, state: StateResult, gates: GateEvaluation,
          changed_files: Optional[List[str]] = None) -> Path:
    changed_files = changed_files or []
    passed = [g.name for g in gates.gates if g.status == "done"]
    pending = [f"{g.name}({g.status})" for g in gates.gates if g.status not in ("done", "na")]

    product_touched = "no (product writes not authorized)" if not job.flags.get(
        "product_repo_writes_allowed") else "possible (job authorizes product writes)"

    lines: List[str] = []
    A = lines.append
    A(f"# Compact Report — {job.job_id}")
    A("")
    A(f"- **job**: {job.title}")
    A(f"- **status**: {job.status}  ·  **state**: {state.current_state}  ·  **tier**: {gates.tier}")
    A(f"- **next action**: {gates.next_action}")
    A(f"- **gates passed**: {', '.join(passed) or 'none'}")
    A(f"- **gates pending**: {', '.join(pending) or 'none'}")
    A(f"- **product repos touched**: {product_touched}")
    A(f"- **push**: {'authorized' if job.flags.get('push_authorized') else 'NOT authorized'}")
    A("")
    A("## Changed MQAI files (this pass)")
    if changed_files:
        for f in changed_files:
            A(f"- `{f}`")
    else:
        A("- (none recorded)")
    A("")
    A("## Validation summary")
    ev = job.review_dir / "eval_results.json"
    A(f"- eval_results.json: {'present' if ev.exists() else 'not run yet'}")
    A(f"- validation_results.md: {'present' if (job.output_dir / 'validation_results.md').exists() else 'absent'}")
    A("")
    A("## Blockers")
    for b in gates.blocked_actions or ["(none)"]:
        A(f"- {b}")
    A("")
    A("## Required human decision")
    if gates.human_required:
        A(f"- Cray approval required for gate `{gates.next_gate}` → {gates.next_action}")
    else:
        A("- none pending (or next action is an automated MQAI-local step)")
    A("")
    s = state.signals
    A("## Handoff / continuity")
    A(f"- handoff_ready: {'true' if s.get('handoff_ready') else 'false'}")
    A(f"- latest_handoff_path: {s.get('latest_handoff_path') or '(none)'}")
    A(f"- resume_prompt_path: {s.get('resume_prompt_path') or '(none)'}")
    A(f"- recommended_next_agent: {s.get('recommended_next_agent') or '(none)'}")
    A(f"- last_stop_reason: {s.get('last_stop_reason') or '(none)'}")
    A("")

    job.output_dir.mkdir(parents=True, exist_ok=True)
    dest = job.output_dir / "compact_report.md"
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest
