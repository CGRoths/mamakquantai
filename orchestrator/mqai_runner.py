"""MQAI CLI entrypoint. Usage: python orchestrator/mqai_runner.py <command> <job_id> [args].

Works both as a script (`python orchestrator/mqai_runner.py ...`) and as a module
(`python -m orchestrator.mqai_runner ...`).
"""
from __future__ import annotations

import argparse
import os
import sys

try:
    from orchestrator import command_router as cr
except ImportError:  # run as a bare script: add repo root to sys.path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from orchestrator import command_router as cr


def _add(sub, name, help_):
    p = sub.add_parser(name, help=help_)
    p.add_argument("job_id")
    return p


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mqai", description="MQAI local control-plane runner (V1).")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_ in [
        ("status", "print compact job state"),
        ("next", "print next allowed action + blocked actions"),
        ("context", "generate output/context_pack.md"),
        ("report", "generate output/compact_report.md"),
        ("prompts", "generate output/prompts/*.md"),
        ("eval", "run local eval gates -> review/eval_results.json"),
    ]:
        _add(sub, name, help_)
    run_p = _add(sub, "run", "safe MQAI-local pass; stops before gate/product mutation")
    run_p.add_argument("--until-hard-stop", action="store_true", default=True)
    ap = _add(sub, "approve", "record an approval artifact for a gate")
    ap.add_argument("--gate", required=True)
    cl = _add(sub, "close", "close a job (dry-run by default)")
    cl.add_argument("--commit", action="store_true", default=False)
    ho = _add(sub, "handoff", "generate handoff artifacts from one agent to another")
    ho.add_argument("--from", dest="from_agent", required=True)
    ho.add_argument("--to", dest="to_agent", required=True)
    ho.add_argument("--stop-reason", dest="stop_reason", default=None)
    rs = _add(sub, "resume", "generate a resume prompt for an agent")
    rs.add_argument("--agent", required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "status":
            res = cr.cmd_status(args.job_id)
        elif args.command == "next":
            res = cr.cmd_next(args.job_id)
        elif args.command == "context":
            res = cr.cmd_context(args.job_id)
        elif args.command == "report":
            res = cr.cmd_report(args.job_id)
        elif args.command == "prompts":
            res = cr.cmd_prompts(args.job_id)
        elif args.command == "eval":
            res = cr.cmd_eval(args.job_id)
        elif args.command == "run":
            res = cr.cmd_run(args.job_id, until_hard_stop=args.until_hard_stop)
        elif args.command == "approve":
            res = cr.cmd_approve(args.job_id, args.gate)
        elif args.command == "close":
            res = cr.cmd_close(args.job_id, do_commit=args.commit)
        elif args.command == "handoff":
            res = cr.cmd_handoff(args.job_id, args.from_agent, args.to_agent, args.stop_reason)
        elif args.command == "resume":
            res = cr.cmd_resume(args.job_id, args.agent)
        else:
            print(f"unknown command {args.command}", file=sys.stderr)
            return 2
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3
    except Exception as e:  # fail safe, never partial-mutate
        print(f"ERROR ({type(e).__name__}): {e}", file=sys.stderr)
        return 1

    print(res.message)
    if res.artifacts:
        print("artifacts:")
        for a in res.artifacts:
            print(f"  - {a}")
    return 0 if res.ok else 4


if __name__ == "__main__":
    raise SystemExit(main())
