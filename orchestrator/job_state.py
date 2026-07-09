"""Infer a job's fine-grained state from job.yaml + review/ + output/ artifacts.

Generic and evidence-driven (NOT hardcoded to any single job id). The mapping is a
documented V1 heuristic — see docs/state_machine.md.
"""
from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import List

from .schemas import JobSpec, StateResult

STATES = [
    "drafted",
    "scaffolded",
    "plan_reviewed",
    "plan_approved",
    "execution_ready",
    "execution_authorized",
    "executed",
    "validation_passed",
    "review_passed",
    "synthesis_required",
    "synthesis_done",
    "final_approval_required",
    "commit_authorized",
    "committed",
    "post_audit_required",
    "completed",
    "failed",
    "blocked",
]


def _glob_any(directory: Path, patterns: List[str]) -> List[str]:
    if not directory.exists():
        return []
    hits: List[str] = []
    for f in sorted(directory.rglob("*")):
        if not f.is_file():
            continue
        name = f.name
        for pat in patterns:
            if fnmatch.fnmatch(name.lower(), pat.lower()):
                hits.append(str(f.relative_to(directory.parent)))
                break
    return hits


def infer_state(job: JobSpec) -> StateResult:
    rev = job.review_dir
    out = job.output_dir
    flags = job.flags

    reviews = _glob_any(rev, ["*review*.md", "*scaffold_review*.md"])
    plan_approvals = _glob_any(
        rev, ["cray_*plan*approval*.md", "*scaffold*approval*.md", "cray_decision.md",
              "cray_base_replay_approval.md", "approved_plan.md"]
    )
    exec_approvals = _glob_any(rev, ["cray_execution_approval*.md", "approved_execution.md"])
    final_approvals = _glob_any(rev, ["cray_final_approval*.md", "approved_final_commit.md"])
    synthesis = _glob_any(rev, ["gpt_synthesis*.md"])
    diff_reviews = _glob_any(rev, ["*executed_diff*review*.md", "*executed*diff*.md"])
    blocked_marker = _glob_any(rev, ["blocked.md", "*blocked*.md"])

    has_execution = (out / "execution_summary.md").exists()
    has_validation = (out / "validation_results.md").exists()
    has_commit = (out / "commit_records.md").exists()

    # Handoff / continuity signals (orthogonal to the progress ladder).
    handoff_dir = out / "handoff"
    handoff_state = {}
    hs_file = handoff_dir / "handoff_state.json"
    if hs_file.exists():
        try:
            import json as _json
            handoff_state = _json.loads(hs_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            handoff_state = {}
    handoff_ready = (handoff_dir / "latest_handoff.md").exists()

    signals = {
        "job_yaml": (job.job_dir / "job.yaml").exists(),
        "reviews": reviews,
        "plan_approvals": plan_approvals,
        "exec_approvals": exec_approvals,
        "final_approvals": final_approvals,
        "synthesis": synthesis,
        "diff_reviews": diff_reviews,
        "has_execution_summary": has_execution,
        "has_validation_results": has_validation,
        "has_commit_records": has_commit,
        "execution_authorized": bool(flags.get("execution_authorized")),
        "commit_authorized": bool(flags.get("commit_authorized")),
        "push_authorized": bool(flags.get("push_authorized")),
        "location": job.location,
        "status_field": job.status,
        "handoff_ready": handoff_ready,
        "latest_handoff_path": (str((handoff_dir / "latest_handoff.md").relative_to(job.job_dir.parent.parent))
                                if handoff_ready else None),
        "resume_prompt_path": (str((handoff_dir / "resume_prompt.md").relative_to(job.job_dir.parent.parent))
                               if (handoff_dir / "resume_prompt.md").exists() else None),
        "recommended_next_agent": handoff_state.get("recommended_next_agent"),
        "last_stop_reason": handoff_state.get("stop_reason"),
    }

    evidence: List[str] = []

    def note(cond, label):
        if cond:
            evidence.append(label)
        return cond

    # Highest-precedence terminal / override states first.
    if job.location == "failed" or job.status.lower() == "failed":
        return StateResult("failed", signals, ["job in failed/ or status=failed"])
    if blocked_marker or job.status.lower() == "blocked":
        return StateResult("blocked", signals, ["blocked marker/status"])
    if job.location == "completed" or job.status.lower() == "completed":
        return StateResult("completed", signals, ["job in completed/ or status=completed"])

    # Progress ladder (return furthest reached).
    ladder = [
        ("committed", note(has_commit, "output/commit_records.md")),
        ("commit_authorized", note(bool(final_approvals) or signals["commit_authorized"],
                                   "final approval / commit_authorized flag")),
        ("synthesis_done", note(bool(synthesis), "review/gpt_synthesis*.md")),
        ("review_passed", note(bool(diff_reviews), "executed-diff review")),
        ("validation_passed", note(has_validation, "output/validation_results.md")),
        ("executed", note(has_execution, "output/execution_summary.md")),
        ("execution_authorized", note(bool(exec_approvals) or signals["execution_authorized"],
                                      "execution approval / execution_authorized flag")),
        ("plan_approved", note(bool(plan_approvals), "plan/scaffold approval")),
        ("plan_reviewed", note(bool(reviews), "review artifact present")),
        ("scaffolded", note(signals["job_yaml"], "job.yaml present")),
    ]
    for state, reached in ladder:
        if reached:
            return StateResult(state, signals, evidence)
    return StateResult("drafted", signals, ["no artifacts yet"])
