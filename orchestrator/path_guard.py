"""Write-scope guard: is a path allowed to be written under a job's policy?

Pure-Python, glob-based. Used to keep MQAI honest about write scope and to flag any
product-repo path. Does not touch the filesystem beyond normalization.
"""
from __future__ import annotations

import fnmatch
from typing import List

from .schemas import JobSpec

# Known product-repo path prefixes (forward-slash, lowercased) — always product, never MQAI.
PRODUCT_PREFIXES = (
    "c:/mamakquant/mqnode_test2",
    "c:/mamakquant/mqnode_cloud",
    "c:/mamakquant/mqengine_lib_full",
    "c:/mamakquant/mamakquantchain",
)


def _norm(p: str) -> str:
    return p.replace("\\", "/").strip().lower()


def is_product_path(path: str) -> bool:
    n = _norm(path)
    return any(n.startswith(pref) for pref in PRODUCT_PREFIXES)


def matches_globs(path: str, globs: List[str]) -> bool:
    n = _norm(path)
    for g in globs:
        gg = _norm(g)
        if fnmatch.fnmatch(n, gg) or n.startswith(gg.rstrip("*").rstrip("/")):
            return True
    return False


def check_path(job: JobSpec, path: str) -> dict:
    """Return {allowed, reason} for writing `path` under job policy."""
    n = _norm(path)
    if matches_globs(path, [_norm(g) for g in job.forbidden_writes]):
        return {"allowed": False, "reason": "matches forbidden_writes"}
    if is_product_path(path) and not job.flags.get("product_repo_writes_allowed", False):
        return {"allowed": False, "reason": "product-repo path; product writes not allowed by job"}
    if job.allowed_writes and not matches_globs(path, job.allowed_writes):
        return {"allowed": False, "reason": "not within allowed_writes"}
    return {"allowed": True, "reason": "within allowed_writes"}


def check_paths(job: JobSpec, paths: List[str]) -> dict:
    results = {p: check_path(job, p) for p in paths}
    offending = [p for p, r in results.items() if not r["allowed"]]
    return {"ok": not offending, "offending": offending, "results": results}
