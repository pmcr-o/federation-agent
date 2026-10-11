import argparse, json, pathlib

p = argparse.ArgumentParser()
p.add_argument('--round', required=True)
p.add_argument('--submission', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
round_doc = json.loads(pathlib.Path(a.round).read_text())
submission = json.loads(pathlib.Path(a.submission).read_text())

if round_doc.get('schema') != 'pmcro.federation-round/v1':
    raise SystemExit('invalid round schema')
required = ['roundId', 'contestant', 'seedDigest', 'runId', 'resultRef', 'budgetUsed']
for key in required:
    if key not in submission:
        raise SystemExit('missing submission field: ' + key)
if submission['roundId'] != round_doc['roundId']:
    raise SystemExit('roundId mismatch')
if submission['contestant'] not in round_doc['contestants']:
    raise SystemExit('contestant is not admitted to this round')
if submission['seedDigest'] != round_doc['seedDigest']:
    raise SystemExit('submission does not use the shared round seed')

used = submission['budgetUsed']
for key in ['runs', 'costUsd']:
    if key not in used:
        raise SystemExit('missing budgetUsed field: ' + key)
if int(used['runs']) < 1 or int(used['runs']) > int(round_doc['budget']['maxRunsPerContestant']):
    raise SystemExit('submission exceeds run budget')
if float(used['costUsd']) < 0 or float(used['costUsd']) > float(round_doc['budget']['maxTotalCostUsd']):
    raise SystemExit('submission exceeds total round cost budget')

out = {
    'schema': 'pmcro.federation-submission-validation/v1',
    'roundId': round_doc['roundId'],
    'contestant': submission['contestant'],
    'runId': submission['runId'],
    'verdict': 'PASS',
    'scoringRoute': '@eval-agent /eval:rank-model-runs',
    'identityStatement': submission.get('identityStatement', ''),
    'identityStatementGrantsAuthority': False,
    'resultRef': submission['resultRef'],
    'budgetUsed': used,
}
pathlib.Path(a.output).write_text(json.dumps(out, indent=2) + '\n')
print(a.output)
