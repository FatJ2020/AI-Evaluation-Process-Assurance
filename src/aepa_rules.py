"""AEPA rule engine: evaluation-side risk flags, severity, recommendation."""

from __future__ import annotations
from typing import Any, Dict, List, Set

# Flags that indicate process-integrity problems (severity H)
HIGH_INTEGRITY_FLAGS: Set[str] = {
    "gate_threshold_unstable",
    "artifact_not_verified",
    "hard_fault_not_separated",
}


def detect_flags(session: Dict[str, Any]) -> List[str]:
    """Return evaluation-side risk flags for one synthetic review session."""
    flags: List[str] = []

    # Position bias: preferred_side stuck on A or B with no swap protocol
    preferred = session.get("preferred_side")
    swap_done = bool(session.get("position_swap_done", False))
    if preferred in {"A", "B"} and not swap_done and session.get("format") == "pairwise":
        if session.get("n_pairs", 0) >= 3:
            flags.append("position_bias_risk")

    # Length bias: explicit marker or longer always wins
    if session.get("longer_always_preferred") is True:
        flags.append("length_bias_risk")
    if session.get("length_controlled") is False and session.get("format") == "pairwise":
        if session.get("preference_correlated_with_length") is True:
            flags.append("length_bias_risk")

    # Hard fault not separated from preference
    if session.get("hard_fault_present") is True and session.get("hard_fault_tagged") is False:
        flags.append("hard_fault_not_separated")

    # Gate without stability review
    if session.get("uses_gate") is True and session.get("gate_fpr_fnr_reviewed") is False:
        flags.append("gate_threshold_unstable")

    # Spec version unclear / mixed
    versions = session.get("spec_versions_seen") or []
    if isinstance(versions, list) and len(set(versions)) > 1:
        flags.append("spec_version_drift")
    if session.get("spec_version_clear") is False:
        flags.append("spec_version_drift")

    # Agreement unknown on subjective task
    if session.get("subjective_dimensions") is True:
        if session.get("agreement_measured") is False and session.get("gold_check_present") is False:
            flags.append("agreement_unknown")

    # Artifact not verified (agent / coding style)
    if session.get("task_family") in {"agent", "visual_coding", "rollout"}:
        if session.get("artifact_verified") is False:
            flags.append("artifact_not_verified")

    # de-dupe preserving order
    seen = set()
    ordered = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            ordered.append(f)
    return ordered


def severity_band(flags: List[str]) -> str:
    """Severity-first band: H / M / L (not a numeric RPN product)."""
    if any(f in HIGH_INTEGRITY_FLAGS for f in flags):
        return "H"
    if flags:
        return "M"
    return "L"


def recommend(flags: List[str], severity: str) -> str:
    """ACCEPT | RE_REVIEW | HOLD_BATCH"""
    if "gate_threshold_unstable" in flags or "spec_version_drift" in flags:
        if severity == "H":
            return "HOLD_BATCH"
    if severity == "H":
        return "RE_REVIEW"
    if severity == "M":
        return "RE_REVIEW"
    return "ACCEPT"


def evaluate_session(session: Dict[str, Any]) -> Dict[str, Any]:
    flags = detect_flags(session)
    sev = severity_band(flags)
    rec = recommend(flags, sev)
    return {
        "session_id": session.get("session_id", "UNKNOWN"),
        "task_family": session.get("task_family", ""),
        "format": session.get("format", ""),
        "severity": sev,
        "flags": ";".join(flags) if flags else "none",
        "n_flags": len(flags),
        "recommendation": rec,
        "notes": session.get("notes", ""),
    }
