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

A skill is loaded on demand, so installing it is not enough: in the eval, an installed but inactive skill was never loaded. `install.mjs` turns it on for every session:

- **Claude Code:** a `SessionStart` hook in `~/.claude/settings.json`, plus a block in `~/.claude/CLAUDE.md`.
- **Codex:** a block in `~/.codex/AGENTS.md`.
- **Gemini CLI:** a block in `~/.gemini/GEMINI.md`.

It only touches the agents it finds. It is idempotent and leaves the rest of those files alone.

```bash
node ~/.agents/skills/ste-es/scripts/install.mjs --check      # what is installed
node ~/.agents/skills/ste-es/scripts/install.mjs --uninstall  # remove everything
```

## What was measured

[`evals/`](evals/) compares plain Claude Code against several versions of the rules: 18 cases, 3 runs per case, isolated Claude Code. Reference run `local-03` (Sonnet):

| | No rules | Core | Core + diagrams | STE-ES v1 (13 rules) |
|---|---|---|---|---|
| Answers in the first sentence | 31% | 94% | 91% | 46% |
| Follow-up questions | 69% | 52% | 59% | 57% |
| Tokens to understand | 92.5k | 70.8k | 78.7k | 82.1k |
| Conditions kept | 99.4% | 99.4% | 98.2% | 97.6% |
| Incorrect claims | 28 | 14 | 20 | 14 |
| Preferred over no rules | — | 35 to 19 | 37 to 17 | 24 to 30 |

Limits: one model only, and the judge and the reader are Claude too. The published skill (`skill_v2`) has no run of its own yet.
