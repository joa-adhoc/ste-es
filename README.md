# ste-es

A response style for coding agents (Claude Code, Codex, Gemini) that talk to developers in Spanish: direct, concise and with the concrete thing at hand, so the dev does not have to ask again for a summary or an example.

> **Status:** experiment. `ste-es` is a working name until the project settles. If the trial goes well, we decide where it goes next.

## What it is

The rules are the exact text of the `core_diagrams` arm measured by the eval: a small core taken from ASD-STE100 (the controlled English of aircraft maintenance manuals) and from the eval itself, plus text diagrams only when the answer has structure. Vocabulary comes from a [glossary](skills/ste-es/references/glossary.md) with one word per concept.

0. Precision wins: no rule justifies dropping a fact or a condition.
1. The answer goes in the first sentence.
2. Include the command or the concrete example.
3. Short sentences.
4. Active voice.
5. No filler.
6. Voseo (Rioplatense Spanish).
7. Diagrams only for 3 or more related parts, without repeating them in the text.

The rules themselves are in Spanish, because they shape Spanish answers. Details: [`skills/ste-es/SKILL.md`](skills/ste-es/SKILL.md).

## Install

```bash
npx skills add joa-adhoc/ste-es -g -y
node ~/.agents/skills/ste-es/scripts/install.mjs
```

This installs two skills: `ste-es` and `html-plan` (see [Plans](#plans)). To install only `ste-es`, add `--skill ste-es`.

A skill is loaded on demand, so installing it is not enough: in the eval, an installed but inactive skill was never loaded. `install.mjs` turns it on for every session:

- **Claude Code:** a `SessionStart` hook in `~/.claude/settings.json`, plus a block in `~/.claude/CLAUDE.md`.
- **Codex:** a block in `~/.codex/AGENTS.md`.
- **Gemini CLI:** a block in `~/.gemini/GEMINI.md`.

It only touches the agents it finds. It is idempotent and leaves the rest of those files alone.

```bash
node ~/.agents/skills/ste-es/scripts/install.mjs --check      # what is installed
node ~/.agents/skills/ste-es/scripts/install.mjs --uninstall  # remove everything
```

## Plans

`/html-plan <what to build>` writes an implementation plan as one interactive HTML page: a tree of claims, each shown by a mockup, state machine, call stack, schema or code, with the decisions placed where they matter. Its structure is used as is. Its prose follows the ste-es rules in Spanish instead of English STE, with a budget of about 500 words: see [`patches/html-plan-words.md`](patches/html-plan-words.md).

`skills/html-plan/` is a copy of [html-plan](https://github.com/anthropics/claude-plugins-community/tree/main/html-plan) by Thariq Shihipar (MIT), pinned to the commit in `skills/html-plan/UPSTREAM`. Only its "Words" section is replaced, by the patch above. To update it, run `node scripts/sync-html-plan.mjs`, review the diff and commit.

## What was measured

[`evals/`](evals/) compares plain Claude Code against several versions of the rules: 18 cases, 3 runs per case, isolated Claude Code. Reference run `local-03` (Sonnet):

| | No rules | Core | Core + diagrams | **This skill** (`skill_v2`) | STE-ES v1 (13 rules) |
|---|---|---|---|---|---|
| Answers in the first sentence | 31% | 94% | 91% | 89% | 46% |
| Follow-up questions | 69% | 52% | 59% | 54% | 57% |
| Tokens to understand | 92.5k | 70.8k | 78.7k | 78.1k | 82.1k |
| Conditions kept | 99.4% | 99.4% | 98.2% | 98.2% | 97.6% |
| Incorrect claims | 28 | 14 | 20 | **5** | 14 |
| Preferred over no rules | — | 35 to 19 | 37 to 17 | 31 to 23 | 24 to 30 |

The published skill is `core_diagrams` plus its scope and the glossary. It has the fewest incorrect claims of any arm. The trade-off: on flow cases the judge prefers plain Claude Code (17 to 10), while on cases without structure the skill wins 21 to 6. A variant that keeps step-by-step detail under each diagram (`skill_v3`) did not improve the overall result, so it was not adopted.

The current `SKILL.md` adds one line about html-plan; it does not change chat answers.

Limits: one model only, and the judge and the reader are Claude too.
