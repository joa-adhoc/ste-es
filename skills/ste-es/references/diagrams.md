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
