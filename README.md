# ste-es

A response style for coding agents (Claude Code, Codex, Gemini) that talk to developers in Spanish: direct, concise and with the concrete thing at hand, so the dev does not have to ask again for a summary or an example.

> **Status:** experiment. `ste-es` is a working name until the project settles. If the trial goes well, we decide where it goes next.

## What it is

The rules adapt ASD-STE100 (the controlled English of aircraft maintenance manuals) to Spanish, plus text diagrams only when the answer has structure. They are the exact text measured by the eval.

0. Precision wins: no rule justifies dropping a fact or a condition. An error, a failing test, a security warning and what a destructive action loses arrive whole.
1. The answer goes in the first sentence.
2. Include the command or the concrete example.
3. Short sentences.
4. Active voice.
5. Start with the fact and stop when the dev can act, shown with two examples.
6. Voseo (Rioplatense Spanish).
7. Diagrams only for 3 or more related parts, never for an answer that depends on conditions, and without repeating them in the text.

The rules themselves are in Spanish, because they shape Spanish answers. Details: [`skills/ste-es/SKILL.md`](skills/ste-es/SKILL.md).

## Install

```bash
npx skills add joa-adhoc/ste-es -g -y
node ~/.agents/skills/ste-es/scripts/install.mjs
```

Earlier versions also installed `html-plan`. It is no longer part of this repo: if you got it from here, remove it with `npx skills remove html-plan -g -y`, or install it from its own plugin.

A skill is loaded on demand, so installing it is not enough: in the eval, an installed but inactive skill was never loaded. `install.mjs` turns it on for every session by adding one plain-text block to the global instructions of each agent it finds:

- **Claude Code:** `~/.claude/CLAUDE.md`
- **Codex:** `~/.codex/AGENTS.md`
- **Gemini CLI:** `~/.gemini/GEMINI.md`

It shows what it will change and asks before writing. It backs up each file first (`*.ste-es-backup-<time>`) and never deletes those backups. It is idempotent and leaves the rest of those files alone. It exits with 1 when you decline, when there is no terminal to ask in, when a write fails, or when a file could not be checked.

```bash
node ~/.agents/skills/ste-es/scripts/install.mjs --dry-run    # only show the plan
node ~/.agents/skills/ste-es/scripts/install.mjs --yes        # apply without asking
node ~/.agents/skills/ste-es/scripts/install.mjs --check      # what is installed in each agent (exit 1 if anything is missing)
node ~/.agents/skills/ste-es/scripts/install.mjs --uninstall  # remove the block and the old hook (backups stay)
```

## Security

Skill scanners can flag a skill whose script writes to an agent's global configuration, because it is how a persistent prompt injection works. This is what `install.mjs` does and does not do:

- **It writes only the block shown above**, between `<!-- ste-es:start -->` and `<!-- ste-es:end -->`. The block is text: it asks the agent to load the skill.
- **It never runs on its own.** It adds no hooks, so nothing from this repo executes when a session starts. Updating the skill changes text, not code that runs by itself.
- **You run it, see the plan, and confirm.** Without a terminal (for example, when an agent runs it) it only shows the plan; `--yes` is for scripts you control.

Version 1 added a `SessionStart` hook that ran this script in every session. **If you installed version 1, run `install.mjs` again**: it removes that hook. Until then the hook still starts `node` in each session, but it only shows you a message with that command. The message goes to you, not to the model.

To skip the script, paste the block into the files above by hand. The skill works the same.

## What was measured

[`evals/`](evals/) compares plain Claude Code with this skill and with the alternatives: 29 cases, 3 runs per case, isolated Claude Code, Sonnet (run `local-04`, 2026-11-18).

| | Plain Claude Code | `Concise` output style | ste-es (this version) | ste-es (previous) |
|---|---|---|---|---|
| Answers in the first sentence | 55% | 76% | 97% | 89% |
| Follow-up questions | 48% | 44% | 45% | 48% |
| Tokens to understand | 130k | 91k | 105k | 106k |
| Facts / conditions kept | 98.4% / 98.8% | 96.8% / 97.5% | 97.5% / 97.9% | 95.9% / 97.1% |
| Incorrect claims | 47 | 32 | 22 | 13 |
| Voseo | 85% | 86% | 100% | 100% |
| Blind preference against plain | — | 65 to 22 | 60 to 27 | 54 to 33 |

This version beats the previous one 47 to 40, and wins back the flow cases (18 to 9) that the previous one lost against plain Claude Code. It pays for that with more incorrect claims (22 against 13), it loses the work reports to the previous one (3 to 9), and it drops an unasked caveat in 2 of 9 conditional answers.

Against the built-in `Concise` style it ties (44 to 42): in Claude Code, `Concise` gives about the same with fewer tokens, and ste-es adds voseo, the answer first and fewer incorrect claims.

On top of adhoc-way's `conventions.md`, the rules beat the conventions alone (56 to 31) but tie with the conventions plus `Concise` (44 to 42), which uses fewer tokens and loses less in the precision cases (the rules lose them 3 to 9). The rules also raise follow-ups against the conventions alone (0.54 to 0.61).

### Functional cases and today's model (2026-11-26)

Eight cases from real follow-ups of support, upgrade, consulting and sales people in Tuqui Work (run `local-05`), and the 29 dev cases again with `claude-sonnet-5-5` (run `local-06`). All arms load adhoc-way's `conventions.md`; `conventions_v4` rewrites rule 2 for someone who does not code.

| | Functional: preference | Functional: follow-ups | Dev: preference against `Concise` | Dev: follow-ups |
|---|---|---|---|---|
| `conventions` + `Concise` | — | 100% | — | 37% |
| `conventions_v3` | 11 to 13 against `Concise` | 100% | 25 to 62 | 37% |
| `conventions_v4` | 15 to 9 against `Concise` | 88% | 30 to 57 | 31% |
| `conventions_v5` | 15 to 9 against `Concise` | 92% | 50 to 36 | 32% |
| `conventions_v6` | 15 to 9 against `Concise` | 100% | 45 to 40 | 36% |

- With today's model, `Concise` beats the rules in the dev cases. On 2026-11-18 they tied (44 to 42); v4 and v3 tie with each other (42 to 44), so the change comes from the model, not from v4.
- `conventions_v5` writes `Concise` as text, in our words, so it works in any agent, and adds rule 2 for someone who does not code. It beats `Concise` in Claude Code, but in the functional cases it keeps only 57% of the conditions. `conventions_v6` adds one sentence ("lo que no verificaste o no probaste se dice siempre") and keeps 68% of them, like v4, while it still beats `Concise` (45 to 40 in dev, 15 to 9 in functional cases).
- In the functional cases no arm answers in functional language: answers have about 540 words, keep 73% to 76% of the facts, and the reader asks again almost every time. v4 helps a little.

Limits: one model only, and the judge and the reader are Claude too. Codex and opencode are not measured. Earlier versions and their results are in the git history.
