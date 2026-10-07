# ste-es eval

Evidence for the published skill: does it give a direct answer the dev does not have to follow up on, without losing facts or spending more tokens? It compares two arms, each a frozen file in `arms/` added with `--append-system-prompt`:

| Arm | Added text |
|---|---|
| `baseline` | none: plain Claude Code |
| `ste_es` | the published skill: the body of `SKILL.md` and the glossary |

Earlier versions and arms are in the git history.

## Isolation

`claude -p` in an empty directory, with no user settings (hooks, plugins), no MCP servers, no claude.ai connectors and no web access. The material is inside each case. A canary stops the run if anything from the user's own setup shows up.

## Run

```bash
python3 run.py --run-id local-03 --models sonnet --runs 3
python3 judge.py --run-id local-03 --judge-model sonnet
python3 reader.py --run-id local-03 --reader-model sonnet
python3 comprehension.py --run-id local-03 --model sonnet
python3 measure.py --run-id local-03
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

One model (Sonnet). The judge, the reader and the generator are all Claude. The cases were written by the people who wrote the rules.
