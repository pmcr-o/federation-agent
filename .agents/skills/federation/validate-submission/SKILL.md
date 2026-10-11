---
name: validate-submission
description: "Validate one orchestrator competition submission against round identity, seed, budget, and evidence requirements without scoring it."
---
# validate-submission

Route: `@federation-agent /federation:validate-submission`.

Run: `python scripts/validate_submission.py --round <round.json> --submission <submission.json> --output <validation.json>`.

`federation-agent` owns competition state only. `governance-agent` controls admissibility/authority, `eval-agent` scores observed runs, and the independent checker/referee settles the round.
