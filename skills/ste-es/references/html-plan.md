# ste-es on top of html-plan

`html-plan` (the sibling skill in this repo, copied unchanged from its author) writes an implementation plan as one interactive HTML page. Use it as it is, with one change: the language of its prose.

## What stays as html-plan says

Everything about structure: the tree of claims (why › what › how › where), one exhibit per claim, at most 5 children and 3 levels, decisions on the claim they change, the `aux="shared"` and `aux="scope"` claims, the title rules, real paths and lines, packing with `pack.mjs`, and the Respond flow.

## What changes: the "Words" section

Its "Words" section asks for ASD-STE100 English and says "use no other style". For this team, write the prose of the plan in **Spanish, with the ste-es rules** instead:

- Rules 0 to 6 and rule 7 of `SKILL.md` apply to claims, captions, pins, questions, options and notes.
- Use the glossary in `glossary.md`.
- Keep html-plan's sentence limits: a level 1 or 2 claim is a sentence that can be true or false, about 12 words at most. An option's `<small>` is 12 words at most.
- Where html-plan says *must* and *can*, write "tiene que" and "puede".
- Set `<html lang="es">`.

Code, technical names, the user's own words in a `doc-quote` and the text on a UI mockup stay as they are.

## pack.mjs warnings

`pack.mjs` checks structure and some English STE errors. Fix every structure error: levels, exhibit count, decisions, the closing `aux` claims and the title. Ignore its English vocabulary, contraction, *-ing*, *has/have* and passive-voice warnings: they do not apply to Spanish text.
