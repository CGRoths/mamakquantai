"""Structured return objects for the MQAI orchestrator."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class JobSpec:
    job_id: str
    title: str
    status: str
    risk_tier: str
    job_dir: Path
    location: str  # active | completed | failed | fixture
    target_repos: List[str] = field(default_factory=list)
    allowed_writes: List[str] = field(default_factory=list)
    forbidden_writes: List[str] = field(default_factory=list)
    gates: List[str] = field(default_factory=list)
    objective: str = ""
    success_criteria: List[str] = field(default_factory=list)
    flags: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def output_dir(self) -> Path:
        return self.job_dir / "output"

    @property
    def review_dir(self) -> Path:
        return self.job_dir / "review"


@dataclass
class StateResult:
    current_state: str
    signals: Dict[str, Any] = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)


@dataclass
class GateStatus:
    name: str
    status: str  # done | pending | awaiting_approval | na | blocked
    human_required: bool = False
    detail: str = ""


@dataclass
class GateEvaluation:
    tier: str
    gates: List[GateStatus] = field(default_factory=list)
    next_action: str = ""
    next_gate: Optional[str] = None
    human_required: bool = False
    blocked_actions: List[str] = field(default_factory=list)


@dataclass
class EvalGateResult:
    gate: str
    status: str  # pass | fail | skipped
    detail: str = ""
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandResult:
    ok: bool
    message: str
    artifacts: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
