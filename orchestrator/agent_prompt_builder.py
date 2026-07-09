"""Generate compact, role-specific agent prompt files (reference files, not huge dumps)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .schemas import GateEvaluation, JobSpec, StateResult

ROLES = {
    "claude_reviewer": {
        "file": "claude_reviewer_prompt.md",
        "role": "Claude — reviewer / reasoning auditor",
        "charter": [
            "Review artifacts and any staged diff; identify contradictions and scope violations.",
            "Do NOT execute changes. Write a verdict block (approve/request_changes/reject).",
            "Confirm boundary + secret-handling; rely on metadata for secret-like removals.",
        ],
    },
    "codex_builder": {
        "file": "codex_builder_prompt.md",
        "role": "Codex — builder / code executor",
        "charter": [
            "Obey allowed_writes exactly; never `git add -A`; stop at hard stops.",
            "Write only approved paths; stage only; do not commit/push unless a gate authorizes it.",
            "Emit an output note describing what changed and any assumptions.",
        ],
    },
    "gpt_synthesis": {
        "file": "gpt_synthesis_prompt.md",
        "role": "GPT — synthesis / architecture judge (HIGH/CRITICAL)",
        "charter": [
            "Reconcile the builder result and reviewer verdict; state consensus + unresolved risk.",
            "Do not authorize execution; set/confirm the remaining gate conditions.",
        ],
    },
}


def _common_header(job: JobSpec, state: StateResult, gates: GateEvaluation, role_title: str) -> List[str]:
    read_files = [
        f"- `jobs/active/{job.job_id}/job.yaml`",
        f"- `jobs/active/{job.job_id}/output/context_pack.md`",
        f"- `jobs/active/{job.job_id}/output/compact_report.md`",
    ]
    handoff_dir = job.output_dir / "handoff"
    if (handoff_dir / "latest_handoff.md").exists():
        read_files.append(f"- `jobs/active/{job.job_id}/output/handoff/latest_handoff.md`")
    if (handoff_dir / "resume_prompt.md").exists():
        read_files.append(f"- `jobs/active/{job.job_id}/output/handoff/resume_prompt.md`")
    return [
        f"# {role_title} — {job.job_id}",
        "",
        f"- objective: {job.objective or job.title}",
        f"- state: {state.current_state}  ·  tier: {gates.tier}  ·  next gate: {gates.next_gate}",
        f"- next action: {gates.next_action}",
        "",
        "## Read these (do not paste them wholesale; do NOT rely on chat history)",
        *read_files,
        "",
        "## Hard stops",
        "- no push · no history rewrite · no secret-content inspection · no unrestricted `git diff --cached`",
        "- no product-repo writes unless the job authorizes it · no `git add -A` in product repos",
        "",
        "## Allowed writes",
        *[f"- `{w}`" for w in (job.allowed_writes or ["(none)"])],
        "",
    ]


def build(job: JobSpec, state: StateResult, gates: GateEvaluation) -> List[Path]:
    prompts_dir = job.output_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []
    for key, meta in ROLES.items():
        lines = _common_header(job, state, gates, meta["role"])
        lines.append("## Your charter")
        lines += [f"- {c}" for c in meta["charter"]]
        lines.append("")
        lines.append("## Expected output (compact)")
        lines.append("- verdict/result · findings · changed files · blockers · required human decision")
        lines.append("")
        dest = prompts_dir / meta["file"]
        dest.write_text("\n".join(lines), encoding="utf-8")
        written.append(dest)
    return written
