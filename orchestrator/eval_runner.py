"""Local eval-gate runner (Python-native, deterministic, no network).

V1 runs Python-native equivalents of the deterministic gates so results are reliable in
tests and CLI. The PowerShell scripts under evals/scripts/ remain available as an
alternative surface. Never fakes a pass: gates without required inputs are `skipped`.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List

from .path_guard import check_paths, is_product_path
from .schemas import EvalGateResult, JobSpec

_SECRET_PATTERNS = {
    "private_key_block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
}


def _risk_tier_assignment(job: JobSpec) -> EvalGateResult:
    tier = job.risk_tier
    if tier in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
        return EvalGateResult("risk_tier_assignment", "pass", f"tier={tier}", {"tier": tier})
    return EvalGateResult("risk_tier_assignment", "skipped", "risk_tier missing/unknown", {"tier": tier})


def _write_scope_check(job: JobSpec) -> EvalGateResult:
    if not job.allowed_writes:
        return EvalGateResult("write_scope_check", "skipped", "no allowed_writes declared")
    # Any product path present in allowed_writes without product authorization is a scope smell.
    product_in_allowed = [w for w in job.allowed_writes if is_product_path(w)]
    if product_in_allowed and not job.flags.get("product_repo_writes_allowed"):
        return EvalGateResult(
            "write_scope_check", "fail",
            "allowed_writes contains product paths but product writes not authorized",
            {"product_in_allowed": product_in_allowed},
        )
    return EvalGateResult("write_scope_check", "pass",
                          "allowed_writes present; no unauthorized product paths",
                          {"allowed_writes": job.allowed_writes})


def _secret_scan(job: JobSpec) -> EvalGateResult:
    scan_dirs = [job.output_dir, job.review_dir]
    hits: List[dict] = []
    for d in scan_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if not f.is_file() or f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".pdf"):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for name, pat in _SECRET_PATTERNS.items():
                if pat.search(text):
                    hits.append({"file": str(f.name), "pattern": name})
    status = "pass" if not hits else "fail"
    return EvalGateResult("secret_scan", status,
                          "no secret-shape values in job output/review" if not hits
                          else "secret-shape values detected (values NOT logged)",
                          {"hit_count": len(hits), "hits": hits})


def _touched_path_check(job: JobSpec) -> EvalGateResult:
    tp = job.output_dir / "touched_paths.txt"
    if not tp.exists():
        return EvalGateResult("touched_path_check", "skipped", "no output/touched_paths.txt")
    paths = [ln.strip() for ln in tp.read_text(encoding="utf-8").splitlines()
             if ln.strip() and not ln.startswith("#") and not ln.startswith("###")]
    res = check_paths(job, paths)
    status = "pass" if res["ok"] else "fail"
    return EvalGateResult("touched_path_check", status,
                          "touched paths within allowed_writes" if res["ok"]
                          else "touched paths outside allowed_writes",
                          {"offending": res["offending"]})


def _git_status_capture(job: JobSpec) -> EvalGateResult:
    if not job.target_repos:
        return EvalGateResult("git_status_capture", "skipped", "no target_repos to capture")
    return EvalGateResult("git_status_capture", "skipped",
                          "live git capture deferred to product-repo execution job (V1 does not shell git here)",
                          {"target_repos": job.target_repos})


def run(job: JobSpec) -> List[EvalGateResult]:
    return [
        _risk_tier_assignment(job),
        _write_scope_check(job),
        _secret_scan(job),
        _touched_path_check(job),
        _git_status_capture(job),
    ]


def run_and_write(job: JobSpec) -> Path:
    results = run(job)
    job.review_dir.mkdir(parents=True, exist_ok=True)
    dest = job.review_dir / "eval_results.json"
    payload = [
        {"gate": r.gate, "status": r.status, "detail": r.detail, "data": r.data}
        for r in results
    ]
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return dest
