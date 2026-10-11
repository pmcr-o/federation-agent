---
name: create-round
description: "Create a bounded orchestrator competition round with one seed, shared constraints, explicit contestants, and a fixed budget policy."
---
# create-round

Route: `@federation-agent /federation:create-round`.

Run: `python scripts/create.py --input <round-request.json> --output <round.json>`.

`federation-agent` owns competition state only. `governance-agent` controls admissibility/authority, `eval-agent` scores observed runs, and the independent checker/referee settles the round.
