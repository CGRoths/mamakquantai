"""Gate policy: which gates a job needs by risk tier, and the next allowed action.

Pipeline (canonical order): plan -> execution -> validation -> executed_diff_review
-> synthesis -> final_commit -> [push] -> closeout.

`push` is NEVER inferred from commit approval; it is always a separate manual gate and is
not part of the required-to-close set.
"""
from __future__ import annotations

from typing import Dict, List

from .schemas import GateEvaluation, GateStatus, JobSpec, StateResult

# Which gates are required per tier (ordered). push/closeout handled separately.
TIER_GATES: Dict[str, List[str]] = {
    "LOW": ["plan", "validation", "closeout"],
    "MEDIUM": ["plan", "validation", "executed_diff_review", "final_commit", "closeout"],
    "HIGH": [
        "plan", "execution", "validation", "executed_diff_review",
        "synthesis", "final_commit", "closeout",
    ],
    "CRITICAL": [
        "plan", "execution", "validation", "executed_diff_review",
        "synthesis", "final_commit", "closeout",
    ],
}

# Gates that require an explicit human (Cray) approval artifact.
HUMAN_GATES = {"execution", "final_commit", "push", "closeout"}


def _gate_done(gate: str, job: JobSpec, state: StateResult) -> bool:
    s = state.signals
    if gate == "plan":
        # plan done when a review exists; higher tiers also need a plan/scaffold approval.
        if job.risk_tier in ("HIGH", "CRITICAL", "MEDIUM"):
            return bool(s.get("reviews")) and bool(s.get("plan_approvals"))
        return bool(s.get("reviews"))
    if gate == "execution":
        return bool(s.get("exec_approvals")) or bool(s.get("execution_authorized"))
    if gate == "validation":
        return bool(s.get("has_validation_results"))
    if gate == "executed_diff_review":
        return bool(s.get("diff_reviews"))
    if gate == "synthesis":
        return bool(s.get("synthesis"))
    if gate == "final_commit":
        return bool(s.get("final_approvals")) or bool(s.get("commit_authorized"))
    if gate == "push":
        return bool(s.get("push_authorized"))
    if gate == "closeout":
        return s.get("location") == "completed" or str(s.get("status_field", "")).lower() == "completed"
    return False


def _pending_evidence_ready(gate: str, job: JobSpec, state: StateResult) -> bool:
    """For a human gate: is the pre-approval evidence already present (so we're waiting on Cray)?"""
    s = state.signals
    if gate == "execution":
        return bool(s.get("reviews"))  # plan reviewed -> ready for execution approval
    if gate == "final_commit":
        # ready when validation + diff review (+ synthesis for HIGH) exist
        base = s.get("has_validation_results") and bool(s.get("diff_reviews"))
        if job.risk_tier in ("HIGH", "CRITICAL"):
            return bool(base and s.get("synthesis"))
        return bool(base)
    if gate == "closeout":
        return _gate_done("final_commit", job, state) or job.risk_tier == "LOW"
    return True


def evaluate(job: JobSpec, state: StateResult) -> GateEvaluation:
    tier = job.risk_tier if job.risk_tier in TIER_GATES else "HIGH"
    gates: List[GateStatus] = []
    next_gate = None
    next_action = "No further action — job complete."
    human_required = False

    for gate in TIER_GATES[tier]:
        done = _gate_done(gate, job, state)
        if done:
            gates.append(GateStatus(gate, "done", gate in HUMAN_GATES, "satisfied"))
            continue
        human = gate in HUMAN_GATES
        if human and _pending_evidence_ready(gate, job, state):
            status = "awaiting_approval"
            detail = f"evidence ready; awaiting Cray approval for '{gate}'"
        else:
            status = "pending"
            detail = f"produce evidence for '{gate}'"
        gates.append(GateStatus(gate, status, human, detail))
        if next_gate is None:
            next_gate = gate
            human_required = human
            next_action = _action_for(gate, status, job)

    # push is always an explicit, separate, optional gate.
    push_done = _gate_done("push", job, state)
    gates.append(
        GateStatus(
            "push",
            "done" if push_done else "na",
            True,
            "push authorized" if push_done else "separate manual authorization only; never inferred",
        )
    )

    blocked = _blocked_actions(job, state)
    return GateEvaluation(
        tier=tier,
        gates=gates,
        next_action=next_action,
        next_gate=next_gate,
        human_required=human_required,
        blocked_actions=blocked,
    )


def _action_for(gate: str, status: str, job: JobSpec) -> str:
    if status == "awaiting_approval":
        artifact = {
            "execution": "review/cray_execution_approval.md",
            "final_commit": "review/cray_final_approval.md",
            "closeout": "review/cray_closeout_approval.md",
        }.get(gate, f"review/cray_{gate}_approval.md")
        return f"AWAIT Cray approval for gate '{gate}' (create {artifact})"
    guidance = {
        "plan": "produce a plan/scaffold review (and Cray plan approval for MEDIUM+).",
        "execution": "produce a proposed-execution review, then obtain Cray execution approval.",
        "validation": "run validation and write output/validation_results.md.",
        "executed_diff_review": "produce review/claude_executed_diff_review.md over the staged diff.",
        "synthesis": "produce review/gpt_synthesis.md.",
        "final_commit": "complete validation+diff review (+synthesis), then Cray final approval.",
        "closeout": "ensure required artifacts exist, then close out.",
    }.get(gate, f"advance gate '{gate}'.")
    return f"NEXT: {guidance}"


def _blocked_actions(job: JobSpec, state: StateResult) -> List[str]:
    blocked: List[str] = []
    s = state.signals
    if not (bool(s.get("exec_approvals")) or s.get("execution_authorized")):
        blocked.append("product-repo writes (no execution approval)")
    if not (bool(s.get("final_approvals")) or s.get("commit_authorized")):
        blocked.append("commit of product-repo changes (no final approval)")
    if not s.get("push_authorized"):
        blocked.append("push (never inferred; requires explicit push authorization)")
    if not bool(job.flags.get("product_repo_writes_allowed", False)):
        blocked.append("any product-repo mutation (job does not allow product writes)")
    return blocked
