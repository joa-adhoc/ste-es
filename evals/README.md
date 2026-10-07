# ste-es eval

Measures whether the ste-es rules meet their goal: an answer that is simple, concise and direct, so the dev does not have to ask again ("resumime", "dame un ejemplo"), without losing facts and without spending more tokens.

## Arms

Every arm keeps Claude Code's default system prompt. Only the text added with `--append-system-prompt` changes. Each arm is a frozen file in `arms/`: editing the skill never changes an arm that already has answers. To measure a new version, add a new arm.

| Arm | Added text |
|---|---|
| `baseline` | none: plain Claude Code |
| `terse` | "Respondé de forma concisa." The reference for blind preference. |
| `core` | rule 0 and 4 rules |
| `core_plus` | `core` + answer in the first sentence + concrete example |
| `core_diagrams` | `core_plus` + diagrams only for 3 or more related parts, not repeated in the text |
| `core_vocab` | `core_plus` + one word per concept + simple verbs |
| `full_v1` | snapshot of STE-ES v1 (13 rules, glossary and diagrams) from 2026-10-06 |
| `full_v1_no_diagrams` | `full_v1` without the diagram part. Known flaw: it still mentions diagrams in its intro and ends with "No uses diagramas", so its instructions contradict each other. Only in `local-02`. |
| `skill_v2` | snapshot of the published skill: the body of `SKILL.md` (the `core_diagrams` rules unchanged, plus scope) and the glossary. Not measured yet. |

Each answer stores the hash of its arm. Each verdict stores the model, the settings and the hash of the text it judged: if any of them changes, the verdict is redone instead of reused.

Arm texts, cases and the judge, reader and grader prompts are in Spanish, because the answers being measured are in Spanish.

## Isolation

Each answer runs with `claude -p` in an empty directory, with no user settings (hooks, plugins), no MCP servers, no claude.ai connectors and no web access. Native tools stay on: they are the same in every arm, and the material is inside the prompt. Before a run, a canary asks the model which extra instructions it received, and the run stops if anything from the user's own setup shows up.

## Run

```bash
python3 run.py --run-id local-03 --models sonnet --runs 3
python3 judge.py --run-id local-03 --judge-model sonnet
python3 judge.py --run-id local-03 --judge-model sonnet --reference baseline
python3 reader.py --run-id local-03 --reader-model sonnet
python3 comprehension.py --run-id local-03 --model sonnet
python3 measure.py --run-id local-03
```

Runs resume: whatever exists is skipped. Each `run.py` call appends a line to `results/<run>/runs.jsonl`. `results/` and `judge/` are committed as the source of the numbers.

## Metrics

**Goal:**

| Metric | Source |
|---|---|
| Comprehension: 3 control questions per case, answered from the answer alone and graded against a key | `comprehension.py` |
| Follow-up rate, by type (summary, example, clarification, missing fact) | `reader.py`: a reader sees only the question and the answer, 3 times; the majority decides and agreement is reported |
| Answer in the first sentence | `reader.py` |
| Tokens to understand: the answer plus the follow-up answer from the same arm. Reported only when every answer of the arm has a complete reading. | `reader.py`, Claude usage |
| Input tokens: what the rules add to each call | Claude usage |

**Guard** (an arm does not win if it makes these worse):

| Metric | Source |
|---|---|
| Facts and conditions kept, incorrect claims | `judge.py` |
| Blind preference of each arm against `terse` and against `baseline` | `judge.py`, random A/B order |

**Diagnostics** (`lint.py`, deterministic): total and prose words, violations per 100 words (sentences over 25 words, semicolons, gerunds, filler, nominalizations, tuteo), voseo, and diagrams in cases with and without structure.

## Limits

- The linter checks the ste-es rules, so it favors arms with rules by design.
- The voseo and gerund heuristics are approximate.
- The judge, the reader and the generator are all Claude models. The reader simulates a dev; it does not replace one.
- The cases were written by the people who wrote the rules.
