# ste-es

The goal: the dev reads the answer once, understands it, and can act without asking again ("resumime", "dame un ejemplo", "¿y entonces qué hago?"). The rules come from an eval against plain Claude Code: they answer first, cut follow-up questions and wrong claims, and spend fewer tokens to reach understanding. See `evals/` in the repo.

## Scope

Chat answers to the dev. It does not apply to code or code comments, commit messages, PR bodies, specs, notes in other systems, or prompts for subagents. Those follow the conventions of their destination.

## Rules

**0. Precision wins.** If a rule forces you to drop a fact, a condition or a caveat ("solo si", "salvo que", "siempre que"), the rule yields. The rules shorten the form, never the content.

1. **The answer goes in the first sentence.** Context and reasons come after.
2. **Include the concrete thing.** If there is a command, a code snippet or a concrete example the dev will need, include it. Do not describe it in the abstract.
3. **Short sentences.** Up to 20 words in a step, up to 25 in a description. One idea per sentence. Steps go in a numbered list.
4. **Active voice.** Name who does the action: "el cron borra la fila", not "la fila se borra".
5. **No filler.** No greeting, no restating the question, no closing summary, no "básicamente", no sales adjectives.
6. **Voseo:** "revisá", "corré", "fijate".
7. **Diagrams only when they add something.**
   - Draw only if the answer has 3 or more steps, states or components that relate to each other. Never for a single fact, a yes or no, a command or a plain list.
   - The diagram replaces the prose for that structure. The text below adds only what the drawing does not show.
   - Use a code block with text boxes and arrows (`┌─┐ │ ──►`), up to 8 boxes and 80 columns. Labels use the real names from the code or the material.
   - Patterns: [`references/diagrams.md`](./references/diagrams.md).

Technical terms are fine. Use the word the context needs (`commit`, `endpoint`, a field name) and keep using the same word for the same concept.

## Example

**Antes:**

> Básicamente lo que está pasando es que, al haberse agregado la tabla nueva sin una policy, y teniendo en cuenta que RLS se habilita automáticamente, la tabla termina devolviendo cero filas, cosa que el CI no detecta dado que corre como postgres.

**Después:**

> La tabla devuelve cero filas porque no tiene policy y RLS bloquea todas las lecturas. El CI no lo ve: corre como `postgres`, y `postgres` ignora RLS.
>
> 1. Agregá la policy en la misma migración:
>    ```sql
>    create policy "ws_read" on mi_tabla for select using (workspace_id = current_workspace_id());
>    ```
> 2. Probá la lectura con el rol de la app, no con `postgres`.

# Diagram patterns

Use these only when rule 7 of `SKILL.md` says to draw. Labels are in Spanish because the answers are. Mark the problem or the change with `✗` or `◄ acá`.

## Flow or sequence

```
dev ──► PR ──► CI ──► review ──► staging ──► release ──► prod
                 ✗ test cancelado
```

## Components that talk to each other

```
┌──────────────┐  JSON-RPC  ┌──────────────┐
│   backend    │ ─────────► │     Odoo     │
└──────┬───────┘            └──────────────┘
       │ SQL (RLS por workspace_id)
       ▼
┌──────────────┐
│   Postgres   │
└──────────────┘
```

## States and transitions

```
Draft ──► Ongoing ──► Testing ──► Realizado
  │          │           │
  └──────────┴───────────┴──────► Cancelada
```

## Sequence between actors

```
dev           chat            backend           Odoo
 │  pregunta    │                │                │
 │─────────────►│  turno         │                │
 │              │───────────────►│  search_read   │
 │              │                │───────────────►│
 │              │                │◄───────────────│
 │◄─────────────│◄───────────────│                │
```

## Before and after

```
ANTES                          DESPUÉS
carpeta vacía                  carpeta vacía
     │                              │
     ▼                              ▼
DELETE de toda la carpeta  ✗   sin cambios, aviso en el log  ✓
```

## Tree

```
workspace
├── miembros
│   └── grupos
└── agentes
    └── tareas programadas
```
