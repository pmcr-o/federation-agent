import argparse, json, pathlib

p = argparse.ArgumentParser()
p.add_argument('--round', required=True)
p.add_argument('--ranking', required=True)
p.add_argument('--referee-verdict', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
round_doc = json.loads(pathlib.Path(a.round).read_text())
ranking = json.loads(pathlib.Path(a.ranking).read_text())
referee = json.loads(pathlib.Path(a.referee_verdict).read_text())

if round_doc.get('schema') != 'pmcro.federation-round/v1':
    raise SystemExit('invalid round schema')
if ranking.get('schema') != 'pmcro.model-ranking/v1':
    raise SystemExit('ranking must come from eval:rank-model-runs')
if referee.get('kind') != 'checker.verdict' or referee.get('verdict') != 'PASS':
    raise SystemExit('independent referee PASS is required')
referee_agent = referee.get('checker', '')
if referee_agent in round_doc['contestants']:
    raise SystemExit('referee must not be a contestant')
winner = ranking.get('winner')
if winner not in round_doc['contestants']:
    raise SystemExit('ranked winner is not an admitted contestant')
if referee.get('winner') and referee['winner'] != winner:
    raise SystemExit('referee winner disagrees with ranking winner')

summary = str(referee.get('winnerSummary', '')).strip()
if not summary:
    summary = 'Winner selected from checker-passed evidence under the declared round policy.'

out = {
    'schema': 'pmcro.federation-settlement/v1',
    'roundId': round_doc['roundId'],
    'winner': winner,
    'winnerRunId': ranking.get('winnerRunId', ''),
    'referee': referee_agent,
    'refereeVerdict': 'PASS',
    'winningSummary': summary,
    'privateInternalReasoningRequired': False,
    'rankingRule': ranking.get('rule', ''),
    'budgetMayWidenAuthority': False,
    'status': 'SETTLED',
    'next': 'Reflect may reuse the winning checked strategy as a candidate procedure or seed another round.'
}
pathlib.Path(a.output).write_text(json.dumps(out, indent=2) + '\n')
print(a.output)
