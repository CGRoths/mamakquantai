"""Load MQAI jobs from job.yaml into structured JobSpec objects.

Search order for a job id: jobs/active, jobs/completed, jobs/failed.
Fixtures (tests) load a job directory directly via `load_job_from_dir`.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from . import minimal_yaml
from .schemas import JobSpec


def repo_root() -> Path:
    # orchestrator/ lives directly under the MQAI repo root.
    return Path(__file__).resolve().parent.parent


def _as_list(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    return [str(value)]


def load_job_from_dir(job_dir: Path) -> JobSpec:
    job_dir = Path(job_dir)
    yaml_path = job_dir / "job.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"No job.yaml in {job_dir}")
    raw = minimal_yaml.load_path(yaml_path) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"job.yaml in {job_dir} did not parse to a mapping")

    parent = job_dir.parent.name  # active/completed/failed or fixture parent
    location = parent if parent in ("active", "completed", "failed") else "fixture"

    flag_keys = (
        "execution_authorized",
        "commit_authorized",
        "push_authorized",
        "product_repo_writes_allowed",
        "writes_gated",
    )
    flags = {k: raw.get(k) for k in flag_keys if k in raw}

    # target_repos may be a list of names or a list of maps with 'repo'.
    targets_raw = raw.get("target_repos", raw.get("targets", []))
    target_repos: List[str] = []
    if isinstance(targets_raw, list):
        for t in targets_raw:
            if isinstance(t, dict):
                target_repos.append(str(t.get("repo", t)))
            elif t is not None:
                target_repos.append(str(t))

    return JobSpec(
        job_id=str(raw.get("job_id", raw.get("id", job_dir.name))),
        title=str(raw.get("title", job_dir.name)),
        status=str(raw.get("status", "unknown")),
        risk_tier=str(raw.get("risk_tier", "UNKNOWN")).upper(),
        job_dir=job_dir,
        location=location,
        target_repos=target_repos,
        allowed_writes=_as_list(raw.get("allowed_writes")),
        forbidden_writes=_as_list(raw.get("forbidden_writes", raw.get("forbidden_actions"))),
        gates=_as_list(raw.get("gates")),
        objective=str(raw.get("objective", raw.get("title", ""))),
        success_criteria=_as_list(raw.get("success_criteria")),
        flags=flags,
        raw=raw,
    )


def find_job_dir(job_id: str, root: Optional[Path] = None) -> Path:
    root = root or repo_root()
    for loc in ("active", "completed", "failed"):
        candidate = root / "jobs" / loc / job_id
        if (candidate / "job.yaml").exists():
            return candidate
    raise FileNotFoundError(
        f"Job {job_id} not found under jobs/active|completed|failed of {root}"
    )


def load_job(job_id: str, root: Optional[Path] = None) -> JobSpec:
    return load_job_from_dir(find_job_dir(job_id, root))
