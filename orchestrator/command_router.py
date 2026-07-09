"""Dispatch MQAI CLI commands. Default posture: safe / read-only / dry-run.

Commands: status, next, context, report, prompts, eval, run (--until-hard-stop),
approve --gate <name>, close [--commit].
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import List, Optional

from . import (agent_prompt_builder, compact_report, context_pack, eval_runner, gate_policy,
               handoff, job_state)
from .job_loader import load_job, repo_root
from .schemas import CommandResult, JobSpec

APPROVABLE_GATES = {"plan", "execution", "validation", "executed_diff_review",
                    "synthesis", "final_commit", "push", "closeout"}


def _load(job_id: str) -> JobSpec:
    return load_job(job_id)


def _eval_and_gates(job: JobSpec):
    state = job_state.infer_state(job)
    gates = gate_policy.evaluate(job, state)
    return state, gates


def cmd_status(job_id: str) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    msg = (f"{job.job_id} | tier={gates.tier} | state={state.current_state} | "
           f"next={gates.next_action}")
    return CommandResult(True, msg, data={
        "state": state.current_state, "tier": gates.tier,
        "gates": [(g.name, g.status) for g in gates.gates],
    })


def cmd_next(job_id: str) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    lines = [f"next gate: {gates.next_gate}", f"action: {gates.next_action}",
             f"human approval required: {gates.human_required}", "blocked actions:"]
    lines += [f"  - {b}" for b in gates.blocked_actions]
    return CommandResult(True, "\n".join(lines))


def cmd_context(job_id: str) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    dest = context_pack.build(job, state, gates)
    return CommandResult(True, f"context pack written: {dest}", [str(dest)])


def cmd_report(job_id: str, changed_files: Optional[List[str]] = None) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    dest = compact_report.build(job, state, gates, changed_files)
    return CommandResult(True, f"compact report written: {dest}", [str(dest)])


def cmd_prompts(job_id: str) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    written = agent_prompt_builder.build(job, state, gates)
    return CommandResult(True, f"{len(written)} prompt files written",
                         [str(p) for p in written])


def cmd_eval(job_id: str) -> CommandResult:
    job = _load(job_id)
    dest = eval_runner.run_and_write(job)
    payload = json.loads(dest.read_text(encoding="utf-8"))
    summary = ", ".join(f"{r['gate']}={r['status']}" for r in payload)
    return CommandResult(True, f"eval_results.json written ({summary})", [str(dest)])


def cmd_run(job_id: str, until_hard_stop: bool = True) -> CommandResult:
    """Safe MQAI-local pass: no product writes, no approvals, stop before any gate mutation."""
    job = _load(job_id)
    artifacts: List[str] = []
    state, gates = _eval_and_gates(job)
    artifacts.append(str(context_pack.build(job, state, gates)))
    for p in agent_prompt_builder.build(job, state, gates):
        artifacts.append(str(p))
    artifacts.append(str(eval_runner.run_and_write(job)))
    changed = [Path(a).relative_to(repo_root()).as_posix() for a in artifacts]
    artifacts.append(str(compact_report.build(job, state, gates, changed)))
    stop_reason = ("reached next gate '%s' (%s) -> MQAI stops before approval/product mutation"
                   % (gates.next_gate, gates.next_action)) if gates.next_gate else "job complete"
    msg = (f"run --until-hard-stop complete for {job.job_id}\n"
           f"state={state.current_state} tier={gates.tier}\n"
           f"STOP: {stop_reason}")
    return CommandResult(True, msg, artifacts, {"stop_reason": stop_reason})


def cmd_approve(job_id: str, gate: str) -> CommandResult:
    if gate not in APPROVABLE_GATES:
        return CommandResult(False, f"unknown gate '{gate}'. Known: {sorted(APPROVABLE_GATES)}")
    job = _load(job_id)
    job.review_dir.mkdir(parents=True, exist_ok=True)
    # Generic, auditable approval artifact.
    artifact = job.review_dir / f"approved_{gate}.md"
    artifact.write_text(
        f"# MQAI approval — {job.job_id}\n\n"
        f"DECISION: approve_gate\nGATE: {gate}\nDATE: {date.today().isoformat()}\n"
        f"APPROVED_BY: Cray (via mqai approve)\n\n"
        f"Note: `push` is never implied by any other gate. This artifact approves ONLY '{gate}'.\n",
        encoding="utf-8",
    )
    # Reflect known gates into job.yaml flags conservatively (text-level, additive; no product writes).
    note = ""
    if gate in ("execution", "final_commit", "push"):
        note = (" NOTE: job.yaml flag not auto-flipped by MVP to avoid unsafe YAML rewrites; "
                "set the flag manually or via the governance artifact.")
    return CommandResult(True, f"approval artifact written for gate '{gate}': {artifact}.{note}",
                         [str(artifact)])


def cmd_handoff(job_id: str, from_agent: str, to_agent: str,
                stop_reason: Optional[str] = None) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    written = handoff.build_handoff(job, state, gates, from_agent, to_agent, stop_reason)
    sr = handoff.normalize_stop_reason(stop_reason)
    # Refresh compact report so handoff_ready surfaces immediately.
    state2 = job_state.infer_state(job)
    compact_report.build(job, state2, gate_policy.evaluate(job, state2))
    return CommandResult(True, f"handoff {from_agent}->{to_agent} written (stop_reason={sr})",
                         [str(p) for p in written])


def cmd_resume(job_id: str, agent: str) -> CommandResult:
    if agent not in handoff.AGENTS:
        return CommandResult(False, f"unknown agent '{agent}'. Known: {sorted(handoff.AGENTS)}")
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    dest = handoff.build_resume(job, state, gates, agent)
    return CommandResult(True, f"resume prompt for '{agent}' written: {dest}", [str(dest)])


def cmd_close(job_id: str, do_commit: bool = False) -> CommandResult:
    job = _load(job_id)
    state, gates = _eval_and_gates(job)
    required_done = all(g.status in ("done", "na") for g in gates.gates if g.name != "push")
    if not required_done:
        pending = [g.name for g in gates.gates if g.status not in ("done", "na") and g.name != "push"]
        return CommandResult(False, f"cannot close: pending gates {pending}")
    if not do_commit:
        return CommandResult(True, "DRY-RUN close: all required gates satisfied. "
                                   "Re-run with --commit to move job to jobs/completed/ "
                                   "(MVP keeps close as dry-run by default; see docs/known_limits.md).")
    # Real close intentionally not automated in MVP (avoids clobbering job history). Documented limit.
    return CommandResult(False, "real close not automated in MVP; perform move + memory update via a "
                                "governed closeout step. See docs/known_limits.md.")
