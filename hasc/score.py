# MB-X.01 / Omniabase±
# Massimiliano Brighindi
# brighissimo@gmail.com

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass(frozen=True)
class ScoreBreakdown:
    invariance_preservation: float
    drift_penalty_complement: float
    ambiguity_penalty_complement: float
    boundary_safety: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "invariance_preservation": self.invariance_preservation,
            "drift_penalty_complement": self.drift_penalty_complement,
            "ambiguity_penalty_complement": self.ambiguity_penalty_complement,
            "boundary_safety": self.boundary_safety,
        }


def _clip01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def compute_hasc_score(packet: Dict[str, Any],
                       weights: Tuple[float, float, float, float] = (0.40, 0.20, 0.15, 0.25)
                       ) -> Tuple[float, ScoreBreakdown]:
    """
    HASC v0.1 scoring.
    Uses only structural signals (optionally OMNIA metrics if present).

    - invariance_preservation: from omega_score and invariance_break
    - drift_penalty_complement: from sei/iri (proxy) if present
    - ambiguity_penalty_complement: from claim confidences dispersion
    - boundary_safety: from ICE/SNRC flags
    """
    w1, w2, w3, w4 = weights
    s = w1 + w2 + w3 + w4
    if abs(s - 1.0) > 1e-6:
        raise ValueError("Weights must sum to 1.0")

    omnia = packet.get("omnia_metrics") or {}

    omega_score = float(omnia.get("omega_score", 0.5))
    invariance_break = bool(omnia.get("invariance_break", False))
    invariance_preservation = _clip01(omega_score * (0.0 if invariance_break else 1.0))

    sei = float(omnia.get("sei", 0.0))
    iri = float(omnia.get("iri", 0.0))
    # Higher SEI/IRI -> higher drift/lock risk -> lower complement
    drift_penalty_complement = _clip01(1.0 - max(sei, iri))

    claims = packet.get("structural_claims") or []
    confs = []
    for c in claims:
        if "confidence" in c and c["confidence"] is not None:
            try:
                confs.append(float(c["confidence"]))
            except Exception:
                pass
    if len(confs) == 0:
        # If no confidence provided, assume moderate ambiguity
        ambiguity_penalty_complement = 0.5
    else:
        # Dispersion proxy: low mean or high variance indicates ambiguity
        mean = sum(confs) / len(confs)
        var = sum((x - mean) ** 2 for x in confs) / len(confs)
        ambiguity_penalty_complement = _clip01(0.5 * mean + 0.5 * (1.0 - var))

    snrc_candidate = bool(omnia.get("snrc_candidate", False))
    ice = omnia.get("ice") or {}
    impossibility = float(ice.get("impossibility", 0.0))
    boundary_safety = _clip01(1.0 - max(impossibility, 1.0 if snrc_candidate else 0.0))

    breakdown = ScoreBreakdown(
        invariance_preservation=invariance_preservation,
        drift_penalty_complement=drift_penalty_complement,
        ambiguity_penalty_complement=ambiguity_penalty_complement,
        boundary_safety=boundary_safety,
    )

    score = _clip01(
        w1 * breakdown.invariance_preservation
        + w2 * breakdown.drift_penalty_complement
        + w3 * breakdown.ambiguity_penalty_complement
        + w4 * breakdown.boundary_safety
    )
    return score, breakdown