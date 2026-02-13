# HASC Protocol Spec v0.1

## 0. Boundary
HASC is a measurement protocol.
It emits diagnostics and certificates.
It does not decide policy or produce semantic interpretations.

## 1. Entities
- Packet: the standard input container
- Report: the standard output container

## 2. HASC Packet (conceptual fields)
Required:
- packet_id (string)
- created_at (ISO-8601)
- source (human|system)
- human_surface (string) : original human text
- structural_claims (list) : minimal structured assertions
- constraints (list) : explicit constraints (time, quantity, causality, limits)
- transformations (list) : allowed rewrites (paraphrase, translate, compress, permute)

Optional:
- omnia_metrics: { omega_score, omega_set, sei, iri, pbii, ice, snrc_candidate }
- external_refs: list of links or ids

## 3. HASC Score
Goal: quantify compatibility between:
- the packet's structural claims
- invariants measured by OMNIA / omega-method
- stability under allowed transformations

HASC-score is defined as a weighted aggregation:
score = w1 * invariance_preservation
      + w2 * drift_penalty_complement
      + w3 * ambiguity_penalty_complement
      + w4 * boundary_safety

All components are in [0,1].
Weights sum to 1.

## 4. Envelope
HASC emits:
- OK: score >= ok_threshold and no STOP flags
- ESCALATE: score in mid band or warning flags
- STOP: SNRC/ICE indicate structural impossibility or irreversible collapse

Default thresholds (v0.1):
- ok_threshold = 0.80
- escalate_threshold = 0.60
- stop_condition if:
  - snrc_candidate == true
  - ice.impossibility >= 0.80
  - or invariance_break == true AND iri >= 0.80

## 5. Output (Report)
Report contains:
- hasc_score
- components breakdown
- flags (invariance_break, drift_risk, saturation_risk, irreversibility_risk)
- recommendation (OK|ESCALATE|STOP)
- notes (non-semantic, structural)