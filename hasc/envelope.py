# MB-X.01 / Omniabase±
# Massimiliano Brighindi
# brighissimo@gmail.com

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class EnvelopeResult:
    recommendation: str  # OK | ESCALATE | STOP
    flags: Dict[str, bool]


def evaluate_envelope(packet: Dict[str, Any],
                      hasc_score: float,
                      ok_threshold: float = 0.80,
                      escalate_threshold: float = 0.60) -> EnvelopeResult:
    omnia = packet.get("omnia_metrics") or {}

    invariance_break = bool(omnia.get("invariance_break", False))
    snrc_candidate = bool(omnia.get("snrc_candidate", False))

    sei = float(omnia.get("sei", 0.0))
    iri = float(omnia.get("iri", 0.0))

    ice = omnia.get("ice") or {}
    impossibility = float(ice.get("impossibility", 0.0))

    stop = False
    if snrc_candidate:
        stop = True
    if impossibility >= 0.80:
        stop = True
    if invariance_break and iri >= 0.80:
        stop = True

    flags = {
        "invariance_break": invariance_break,
        "drift_risk": (sei >= 0.70),
        "saturation_risk": (sei >= 0.80),
        "irreversibility_risk": (iri >= 0.70),
        "snrc_candidate": snrc_candidate,
        "ice_high_impossibility": (impossibility >= 0.80),
    }

    if stop:
        return EnvelopeResult("STOP", flags)

    if hasc_score >= ok_threshold:
        return EnvelopeResult("OK", flags)

    if hasc_score >= escalate_threshold:
        return EnvelopeResult("ESCALATE", flags)

    return EnvelopeResult("ESCALATE", flags)