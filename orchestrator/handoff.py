"""Agent continuity / handoff layer.

Generates file-based handoff + resume artifacts so a different agent or a new session can continue
a job from MQAI files instead of chat memory. V1 = prompt/file continuity only (no agent APIs).
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .job_loader import repo_root
from .schemas import GateEvaluation, JobSpec, StateResult

STOP_REASONS = {
    "context_exhausted", "quota_exhausted", "tool_error", "validation_failed",
    "human_approval_required", "hard_stop_triggered", "unknown",
}

AGENTS = {"codex", "claude", "gpt"}

_ROLE_INSTRUCTION = {
    "codex": "You are Codex (builder/executor). Continue building/patching ONLY within allowed_writes. "
             "Never `git add -A` in product repos; stop at hard stops; write output notes.",
    "claude": "You are Claude (reviewer/auditor OR builder-continuation). Review artifacts/diffs and "
              "identify contradictions; if continuing a build, obey allowed_writes and hard stops.",
    "gpt": "You are GPT (synthesis/architecture judge). Reconcile builder result + reviewer verdict; "
           "state consensus and unresolved risk; do not authorize execution/commit yourself.",
}


def normalize_stop_reason(stop_reason: Optional[str]) -> str:
    if not stop_reason:
        return "unknown"
    sr = stop_reason.strip().lower()
    return sr if sr in STOP_REASONS else "unknown"


def _handoff_dir(job: JobSpec) -> Path:
    d = job.output_dir / "handoff"
    d.mkdir(parents=True, exist_ok=True)
    return d


def read_handoff_state(job: JobSpec) -> Optional[dict]:
    f = job.output_dir / "handoff" / "handoff_state.json"
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _gates_split(gates: GateEvaluation):
    passed = [g.name for g in gates.gates if g.status == "done"]
    pending = [f"{g.name}({g.status})" for g in gates.gates if g.status not in ("done", "na")]
    return passed, pending


def _handoff_markdown(job: JobSpec, state: StateResult, gates: GateEvaluation,
                      from_agent: str, to_agent: str, stop_reason: str) -> str:
    passed, pending = _gates_split(gates)
    product_touched = "no (product writes not authorized by this job)" if not job.flags.get(
        "product_repo_writes_allowed") else "possible (job authorizes product writes — see product execution job)"
    L: List[str] = []
    A = L.append
    A(f"# Handoff — {job.job_id}  ({from_agent} -> {to_agent})")
    A("")
    A(f"- generated: {datetime.now().isoformat(timespec='seconds')}")
    A(f"- job_id: {job.job_id}")
    A(f"- objective: {job.objective or job.title}")
    A(f"- current_state: {state.current_state}  ·  risk_tier: {gates.tier}")
    A(f"- from_agent: {from_agent}")
    A(f"- to_agent: {to_agent}  (recommended_next_agent)")
    A(f"- stop_reason: {stop_reason}")
    A("")
    A("## Progress")
    A(f"- last completed (inferred): reached state `{state.current_state}` "
      f"(evidence: {', '.join(state.evidence) or 'none'})")
    A(f"- next intended action: {gates.next_action}")
    A(f"- gates passed: {', '.join(passed) or 'none'}")
    A(f"- gates pending: {', '.join(pending) or 'none'}")
    A("")
    A("## Repo / change state")
    A(f"- product repos touched: {product_touched}")
    A(f"- target_repos: {', '.join(job.target_repos) or '(none — MQAI-local job)'}")
    A("- MQAI files changed: see `git status` in the MQAI repo (this job's writes are under "
      f"`jobs/active/{job.job_id}/` + declared allowed_writes).")
    A("- product files changed: none by MQAI control plane (product mutation only in an authorized "
      "product execution job).")
    A("- current branches / staged files: not captured by V1 handoff for MQAI-local jobs; for "
      "product execution jobs see that job's `output/` git-status captures.")
    A("")
    A("## Validation status")
    ev = job.review_dir / "eval_results.json"
    A(f"- eval_results.json: {'present' if ev.exists() else 'not run'}")
    A(f"- validation_results.md: {'present' if (job.output_dir / 'validation_results.md').exists() else 'absent'}")
    A("")
    A("## Blockers")
    for b in gates.blocked_actions or ["(none)"]:
        A(f"- {b}")
    A("")
    A("## Hard stops (do NOT do these)")
    for hs in ["push", "history rewrite", "secret-content inspection",
               "unrestricted `git diff --cached`", "product-repo writes unless the job authorizes it",
               "`git add -A` in product repos"]:
        A(f"- {hs}")
    A("")
    A("## Allowed writes")
    for w in job.allowed_writes or ["(none declared)"]:
        A(f"- `{w}`")
    A("## Forbidden writes")
    for w in job.forbidden_writes or ["(none declared)"]:
        A(f"- `{w}`")
    A("")
    A("## Files the next agent SHOULD read")
    for f in [
        f"jobs/active/{job.job_id}/job.yaml",
        f"jobs/active/{job.job_id}/output/context_pack.md",
        f"jobs/active/{job.job_id}/output/compact_report.md",
        f"jobs/active/{job.job_id}/output/handoff/latest_handoff.md",
        f"jobs/active/{job.job_id}/output/handoff/resume_prompt.md",
    ]:
        A(f"- `{f}`")
    A("")
    A("## Files the next agent MUST NOT touch")
    A("- any product repo path (see forbidden_writes)")
    A("- `repo_control/` canonical truth (promotion is human-gated)")
    A("- prior job history under `jobs/completed/`, `jobs/failed/`")
    A("")
    A("## Compact continuation prompt")
    A(f"> Continue {job.job_id} as `{to_agent}`. Read the files listed above (do NOT rely on chat "
      f"history). Current state `{state.current_state}`. Next action: {gates.next_action} "
      f"Respect hard stops. Report compactly: status · next action · gates · changed files · "
      f"product repos touched · blockers · required human decision.")
    A("")
    return "\n".join(L)


def _resume_markdown(job: JobSpec, state: StateResult, gates: GateEvaluation, agent: str) -> str:
    role = _ROLE_INSTRUCTION.get(agent, _ROLE_INSTRUCTION["claude"])
    L: List[str] = []
    A = L.append
    A(f"# Resume Prompt — {job.job_id}  (agent: {agent})")
    A("")
    A("> **Do NOT rely on chat history.** All continuity is in the files below. MQAI owns memory,")
    A("> state, rules, gates, and handoff. Agents are temporary compute; Cray is final risk owner.")
    A("> Agents do not share memory with each other — read the files.")
    A("")
    A("## Your role")
    A(f"- {role}")
    A("")
    A("## Read these job files (do not paste them wholesale)")
    for f in [
        f"jobs/active/{job.job_id}/job.yaml",
        f"jobs/active/{job.job_id}/output/context_pack.md",
        f"jobs/active/{job.job_id}/output/compact_report.md",
        f"jobs/active/{job.job_id}/output/handoff/latest_handoff.md",
    ]:
        A(f"- `{f}`")
    A("")
    A("## Current state summary")
    A(f"- state: `{state.current_state}`  ·  tier: {gates.tier}  ·  next gate: {gates.next_gate}")
    A(f"- next allowed action: {gates.next_action}")
    A(f"- blocked: {', '.join(gates.blocked_actions) or '(none)'}")
    A("")
    A("## Hard stops")
    A("- no push · no history rewrite · no secret-content inspection · no unrestricted "
      "`git diff --cached` · no product-repo writes unless authorized · no `git add -A` in product repos")
    A("")
    A("## Reporting format (compact)")
    A("- status · next action · gates passed/pending · changed files · product repos touched · "
      "blockers · required human decision")
    A("")
    return "\n".join(L)


def build_handoff(job: JobSpec, state: StateResult, gates: GateEvaluation,
                  from_agent: str, to_agent: str, stop_reason: Optional[str] = None) -> List[Path]:
    stop = normalize_stop_reason(stop_reason)
    from_agent = (from_agent or "unknown").strip().lower()
    to_agent = (to_agent or "unknown").strip().lower()
    d = _handoff_dir(job)

    md = _handoff_markdown(job, state, gates, from_agent, to_agent, stop)
    latest = d / "latest_handoff.md"
    pair = d / f"{from_agent}_to_{to_agent}.md"
    resume = d / "resume_prompt.md"
    latest.write_text(md, encoding="utf-8")
    pair.write_text(md, encoding="utf-8")
    resume.write_text(_resume_markdown(job, state, gates, to_agent), encoding="utf-8")

    (d / "handoff_state.json").write_text(json.dumps({
        "job_id": job.job_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "recommended_next_agent": to_agent,
        "stop_reason": stop,
        "created": datetime.now().isoformat(timespec="seconds"),
        "current_state": state.current_state,
    }, indent=2), encoding="utf-8")

    return [latest, pair, resume, d / "handoff_state.json"]


def build_resume(job: JobSpec, state: StateResult, gates: GateEvaluation, agent: str) -> Path:
    agent = (agent or "claude").strip().lower()
    d = _handoff_dir(job)
    resume = d / "resume_prompt.md"
    resume.write_text(_resume_markdown(job, state, gates, agent), encoding="utf-8")
    return resume


def rel(path: Path) -> str:
    try:
        return path.relative_to(repo_root()).as_posix()
    except ValueError:
        return str(path)
