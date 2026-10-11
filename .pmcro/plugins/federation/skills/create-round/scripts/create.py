import argparse, hashlib, json, pathlib, re

p = argparse.ArgumentParser()
p.add_argument('--input', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
d = json.loads(pathlib.Path(a.input).read_text())

required = ['roundId', 'seed', 'contestants', 'budget']
for key in required:
    if key not in d:
        raise SystemExit('missing field: ' + key)

round_id = str(d['roundId'])
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,127}', round_id):
    raise SystemExit('invalid roundId')
contestants = list(d['contestants'])
if len(contestants) < 2 or len(set(contestants)) != len(contestants):
    raise SystemExit('contestants must contain at least two unique orchestrator IDs')
if any(not isinstance(x, str) or not x.endswith('-agent') for x in contestants):
    raise SystemExit('contestants must be agent IDs ending in -agent')

budget = d['budget']
for key in ['maxCandidates', 'maxRunsPerContestant', 'maxTotalCostUsd']:
    if key not in budget:
        raise SystemExit('missing budget field: ' + key)
if int(budget['maxCandidates']) < len(contestants):
    raise SystemExit('budget maxCandidates is smaller than contestant count')
if int(budget['maxRunsPerContestant']) < 1 or float(budget['maxTotalCostUsd']) < 0:
    raise SystemExit('invalid budget values')

seed = str(d['seed'])
seed_digest = hashlib.sha256(seed.encode()).hexdigest()
out = {
    'schema': 'pmcro.federation-round/v1',
    'roundId': round_id,
    'seed': seed,
    'seedDigest': seed_digest,
    'contestants': contestants,
    'sharedConstraints': d.get('sharedConstraints', []),
    'budget': budget,
    'governance': {
        'admissionRoute': '@governance-agent /pmcro-governance:agt-governance',
        'scoringRoute': '@eval-agent /eval:rank-model-runs',
        'refereeMustBeIndependent': True,
        'budgetMayWidenAuthority': False,
        'sameSeedForAllContestants': True,
        'sameSharedConstraintsForAllContestants': True,
    },
    'status': 'OPEN',
}
pathlib.Path(a.output).write_text(json.dumps(out, indent=2) + '\n')
print(a.output)
