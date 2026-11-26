# ste-es eval

Evidence for the published skill: does it give a direct answer the dev does not have to follow up on, without losing facts or spending more tokens? Each arm is a frozen file in `arms/` added with `--append-system-prompt`, plus optional Claude Code settings in `arms/<arm>.settings.json`:

| Arm | Added text |
|---|---|
| `baseline` | none: plain Claude Code |
| `ste_es` | the skill published until local-03: rules, scope and glossary |
| `ste_es_v3` | the candidate: rules only, rule 0 with the cases that must arrive whole, rule 5 as examples, no diagram for conditional answers, no glossary |
| `concise` | no text: Claude Code's built-in `Concise` output style (`--settings`) |
| `conventions` | adhoc-way's `templates/conventions.md` as it is (commit `29a520c`) |
| `conventions_v3` | the same file with rules 0 to 6 of `ste_es_v3` as a section, the way they would land in adhoc-way |
| `conventions_concise` | adhoc-way's `conventions.md` as it is, plus the `Concise` output style: the cheap option in Claude Code |
| `conventions_v4` | `conventions_v3` with rule 2 for any person: what to do and where, the command for someone who codes, screen names and what to tell the customer for someone who does not |
| `conventions_v5` | Claude Code's `Concise` rules written in our words as a `conventions.md` section, so any agent can follow them, plus rule 2 of v4 |
| `conventions_v6` | `conventions_v5` plus one sentence: what was not verified or tested is always said |

Earlier versions and arms are in the git history.

## Cases

37 cases in `cases.yml`, in six groups that `measure.py` also reports apart, so a loss in one kind of case does not hide in the average:

| Group | Cases | What it checks |
|---|---|---|
| `flow` | 9 | answers with 3 or more related steps or parts: where a diagram may help |
| `precision` | 4 | an error, a failing test, a leaked secret and a destructive command: what rule 0 must keep whole |
| `conditional` | 3 | the answer depends on conditions: no diagram, and no condition lost |
| `report` | 4 | the agent tells what it did, from a session log |
| `functional` | 8 | support, upgrade, consulting and sales people, from real follow-ups in Tuqui Work (anonymized); F05 to F07 take part of their material from an agent answer |
| `other` | 9 | facts, procedures, explanations, diagnoses and comparisons |

## Isolation

`claude -p` in an empty directory, with no user settings (hooks, plugins), no MCP servers, no claude.ai connectors and no web access. The material is inside each case. A canary stops the run if anything from the user's own setup shows up.

## Run

```bash
python3 run.py --run-id local-04 --models sonnet --runs 3 --arms baseline ste_es ste_es_v3 concise conventions conventions_v3 conventions_concise
python3 judge.py --run-id local-04 --judge-model sonnet
python3 judge.py --run-id local-04 --judge-model sonnet --reference ste_es --arms ste_es_v3
python3 judge.py --run-id local-04 --judge-model sonnet --reference conventions --arms conventions_v3
python3 judge.py --run-id local-04 --judge-model sonnet --reference concise --arms ste_es_v3
python3 judge.py --run-id local-04 --judge-model sonnet --reference conventions_concise --arms conventions_v3
python3 reader.py --run-id local-04 --reader-model sonnet
python3 comprehension.py --run-id local-04 --model sonnet
python3 measure.py --run-id local-04
```

Runs resume, and each verdict is reused only if the model, the settings and the judged text are the same.

## Metrics

| Metric | Source |
|---|---|
| Comprehension: 3 control questions per case, graded against a key | `comprehension.py` |
| Follow-up rate and answer in the first sentence: a reader sees only the question and the answer, 3 times, majority decides | `reader.py` |
| Tokens to understand: the answer plus a follow-up answer when the reader needs one | `reader.py` |
| Facts and conditions kept, incorrect claims | `judge.py` |
| Blind preference against `baseline` | `judge.py` |
| Rule violations, voseo, diagrams | `lint.py` (deterministic) |

Arm texts, cases and prompts are in Spanish, because the answers are.

## Limits

One model (Sonnet). The judge, the reader and the generator are all Claude: a reader from another family is still pending. The cases were written by the people who wrote the rules.

In the `functional` cases the reader and the judge play that profile, and a technical name the answer does not explain counts as something they do not understand: an LLM told to play a person who does not code still understands everything unless the limit is explicit.
