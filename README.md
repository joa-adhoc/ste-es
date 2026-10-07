# ste-es

A response style for coding agents (Claude Code, Codex, Gemini) that talk to developers in Spanish: direct, concise and with the concrete thing at hand, so the dev does not have to ask again for a summary or an example.

> **Status:** experiment. `ste-es` is a working name until the project settles. If the trial goes well, we decide where it goes next.

## What it is

The rules adapt ASD-STE100 (the controlled English of aircraft maintenance manuals) to Spanish, plus text diagrams only when the answer has structure. They are the exact text measured by the eval. Vocabulary comes from a [glossary](skills/ste-es/references/glossary.md) with one word per concept.

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

Plans use the Adhoc look: [`themes/adhoc.css`](themes/adhoc.css) holds the brand values and maps html-plan's variables to them. To go back to html-plan's own colors, run `node scripts/sync-html-plan.mjs --theme anthropic`.

`skills/html-plan/` is a copy of [html-plan](https://github.com/anthropics/claude-plugins-community/tree/main/html-plan) by Thariq Shihipar (MIT), pinned to the commit in `skills/html-plan/UPSTREAM`. Two changes on top: its "Words" section is replaced by the patch above, and the theme is appended to its CSS. To update it, run `node scripts/sync-html-plan.mjs`, review the diff and commit.

## What was measured

[`evals/`](evals/) compares plain Claude Code with this skill: 18 cases, 3 runs per case, isolated Claude Code, Sonnet.

| | Plain Claude Code | ste-es |
|---|---|---|
| Answers in the first sentence | 31% | 89% |
| Follow-up questions | 69% | 54% |
| Tokens to understand | 92.5k | 78.1k |
| Facts / conditions kept | 99.7% / 99.4% | 98.3% / 98.2% |
| Incorrect claims | 28 | 5 |
| Blind preference | 23 | 31 |

Limits: one model only, and the judge and the reader are Claude too. Earlier versions and their results are in the git history.
