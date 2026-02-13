from __future__ import annotations

import json
import sys
from hasc.score import compute_hasc_score
from hasc.envelope import evaluate_envelope


def main(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        packet = json.load(f)

    score, breakdown = compute_hasc_score(packet)
    env = evaluate_envelope(packet, score)

    report = {
        "packet_id": packet["packet_id"],
        "hasc_score": score,
        "components": breakdown.as_dict(),
        "recommendation": env.recommendation,
        "flags": env.flags
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python examples/03_generate_report.py <packet.json>")
        raise SystemExit(2)
    main(sys.argv[1])