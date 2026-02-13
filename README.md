# HASC-protocol
Human-AI Structural Compatibility Protocol (HASC)

MB-X.01 / Omniabase±
Massimiliano Brighindi
brighissimo@gmail.com

## What this is
HASC is a minimal, non-semantic protocol to keep human language and AI representations
parallel (or convergent) by aligning invariant structure, not words.

HASC defines:
- a standard packet: Human -> Structural Packet -> AI
- a single compatibility score: HASC-score
- an envelope with STOP / ESCALATE conditions (architecture-agnostic)

HASC does not:
- interpret meaning
- optimize models
- act as an agent
- replace OMNIA or Omega-method

HASC composes with:
- OMNIA (measurement core)
- omega-method (structural superposition, residue)
- omega-translator (post-semantic extraction)
- OMNIA-LIMIT / PDSG (hard boundary, GO/NO-GO)

## Core idea
Do not align tokens.
Align transformations over states:
- what changes
- how much it changes
- when it changes
- why it changes (causal constraints, when available)

## Protocol objects
- HASC Packet (input standard)
- HASC Report (output standard)

See SPEC.md for the formal definition.

## Quick start
Install (editable):
pip install -e .

Run example:
python examples/03_generate_report.py examples/02_packet_with_omnia_outputs.json

## Output
A HASC Report includes:
- hasc_score in [0,1]
- drift indicators
- invariance break flags
- STOP / ESCALATE recommendation (measurement only)

## License
Apache-2.0