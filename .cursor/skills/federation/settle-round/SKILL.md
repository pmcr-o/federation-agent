---
name: settle-round
description: "Settle an orchestrator competition only from an independent referee verdict and checked evaluation evidence; emit a winner summary without private internal reasoning."
---
# settle-round

Route: `@federation-agent /federation:settle-round`.

Run: `python scripts/settle.py --round <round.json> --ranking <ranking.json> --referee-verdict <verdict.json> --output <settlement.json>`.

`federation-agent` owns competition state only. `governance-agent` controls admissibility/authority, `eval-agent` scores observed runs, and the independent checker/referee settles the round.
