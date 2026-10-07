## Words

The exhibits are the plan. Words only name them.

**Write all prose in Spanish, with the `ste-es` rules (voseo, short sentences, active voice, no filler) and its glossary. Do not write the plan in English.** This applies to claims, captions, pins, questions, options and notes. Set `<html lang="es">`.

- **Claims at levels 1 and 2 are sentences that can be true or false, 12 words at most.** Count the words. A level-3 claim is only a place: `file:line · symbol`.
- **A caption is one sentence: what to notice.** A pin is a clause. An option's `<small>` is 12 words at most.
- **No paragraph between a claim and its exhibit.** If the exhibit needs explaining, pick a better exhibit.
- **Budget: about 500 words of prose in the whole plan**, outside code, schemas and mockup text. If the plan is longer, cut claims, not exhibits.
- **"tiene que" for a rule, "puede" for what is possible.** No "debería" or "podría".
- **Technical names stay as they are**: names from the code, product names, UI labels and units. Use the same name for the same thing each time.

The words of the user in a `doc-quote`, the code and the text on a UI mockup stay in their own language.

`pack.mjs` warns about English STE errors: unapproved English words, contractions, *has/have* tenses, *-ing* words and the English passive voice. These warnings do not apply to Spanish text: ignore them. Fix every structure error it reports.

