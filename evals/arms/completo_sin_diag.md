Respondé de forma concisa.

## Cómo responderle al dev: STE-ES + diagramas

POC (oct-2026), basada en el [hilo de Karpathy del 2-oct-2026](https://x.com/karpathy/status/2105819303471976479):
pedirle al modelo un lenguaje controlado (ASD-STE100) y diagramas en vez de
texto cuando la respuesta tiene estructura. ASD-STE100 existe solo en inglés.
STE-ES es nuestra adaptación al español, al "80%" que sugiere Karpathy.

**Alcance:** las respuestas al dev en el chat. No aplica al código ni a sus
comentarios (van en inglés), a los mensajes de commit ni a los docs del
producto. Tampoco aplica a prompts para subagentes ni a texto que va a archivos
o registros (specs, PRs, notas de Odoo): ahí manda la convención de cada lugar.

Las reglas de abajo aplican siempre. El detalle vive en dos skills del
workspace, en `.agents/skills/` (con symlinks en `.claude/skills/`). Si tu
agente no carga skills, leé el archivo directo.

| Skill | Qué trae |
|---|---|
| [`ste-es`](./.agents/skills/ste-es/SKILL.md) | Ejemplos de antes y después, revisión antes de enviar y el [glosario](./.agents/skills/ste-es/references/glosario.md) |

### Escritura (STE-ES)

**Regla 0: la precisión gana.** Si una regla te obliga a perder un dato, una
condición o una salvedad ("solo si", "salvo que", "siempre que"), la regla
cede. Las reglas que siguen acortan la forma, nunca el contenido.

1. Oraciones cortas: hasta 20 palabras si es un paso, hasta 25 si es una
   descripción.
2. Una instrucción por oración. Los pasos van en lista numerada.
3. Un tema por párrafo, hasta 6 oraciones.
4. Voz activa. Nombrá quién hace la acción: "el cron borra la fila", no "la
   fila se borra" ni "la fila fue borrada".
5. Tiempos simples: presente, pretérito o futuro simple. Sin perífrasis como
   "se va a proceder a".
6. Sin gerundios ("teniendo en cuenta", "verificando").
7. Verbos simples y sin nominalizar: "usar", no "utilizar"; "migrar", no
   "realizar la migración".
8. Hasta 3 eslabones de "de" seguidos. Si hay más, partí la frase.
9. No omitas artículos ni conectores.
10. Una palabra, un significado. Usá el término del glosario y no rotes
    sinónimos. Los nombres técnicos (archivos, funciones, tablas, campos) van
    tal cual, entre backticks.
11. Sin relleno: sin "básicamente", "cabe destacar" ni adjetivos de venta. Sin
    punto y coma.
12. Voseo: "revisá", "corré", "fijate".
13. Ante un riesgo, la orden va primero: "No pushees ahora: un push con un run
    en curso cancela el job `test`."

Hay dos modos. En pasos e instrucciones aplicá todas las reglas. En
explicaciones aplicá las reglas 1 a 10 y usá el vocabulario con más libertad.

---
name: ste-es
description: |
  STE-ES: the Spanish adaptation of ASD-STE100 that agents in this workspace use to answer the dev.
  The 13 rules live in AGENTS.md ("Cómo responderle al dev"); this skill holds before/after examples, a pre-send check, and the glossary.
  Use it when writing a long answer or one with steps, when unsure which term to use for a Tuqui or workflow concept, or when the dev says "más claro", "más corto", "no se entiende".
---

# STE-ES: examples, check, and glossary

The rules live in `AGENTS.md`, section "Cómo responderle al dev: STE-ES + diagramas". This skill does not repeat them. It adds three things:

1. Before/after examples, per rule.
2. A check to run before sending.
3. The glossary: [`references/glosario.md`](./references/glosario.md). It is in Spanish because the answers are.

## Examples per rule

| Rule | Before | After |
|---|---|---|
| 1. Short sentences | El job falla porque la migración que agregaste ayer en staging no corre en el preview, ya que las migraciones destructivas se saltean ahí y la base es compartida. | El job falla en el preview. El preview no corre migraciones destructivas. Tu migración de ayer es destructiva. |
| 2. One instruction per sentence | Rebaseá contra staging, corré pre-commit y pusheá. | 1. Rebaseá contra `staging`. 2. Corré pre-commit. 3. Pusheá la rama. |
| 4. Active voice | La fila se borra cuando la carpeta queda vacía. | El re-sync borra la fila cuando la carpeta queda vacía. |
| 5. Simple tenses | Se va a proceder a revisar el deploy. | Reviso el deploy. |
| 6. No gerunds | Revisé el log, encontrando que el token vencía. | Revisé el log. El token vencía. |
| 7. No nominalizations | Realicé la actualización de la migración. | Actualicé la migración. |
| 8. At most 3 "de" | El valor del campo de la cuota de la factura del proveedor. | El valor del campo `amount` en la cuota. La cuota es de la factura del proveedor. |
| 10. One meaning | Abrí el PR... el pull request... la MR. | Abrí el PR... el PR... el PR. |
| 11. No filler | Básicamente, cabe destacar que el cambio es bastante simple. | El cambio toca un archivo. |
| 13. Command first | Como hay un run en curso y el push lo cancelaría, mejor no pushear todavía. | No pushees todavía. Un push con un run en curso cancela el job `test`. |

## Full example

**Before:**

> Básicamente lo que está pasando es que, al haberse agregado la columna nueva sin una policy, y teniendo en cuenta que RLS se habilita automáticamente en las bases de Tuqui, la tabla termina devolviendo cero filas, cosa que el CI no detecta dado que corre como postgres.

**After:**

> La tabla devuelve cero filas. Tuqui habilita RLS en cada tabla nueva. Tu tabla no tiene policy, así que RLS bloquea todas las lecturas. El CI no ve el problema: corre como `postgres`, y `postgres` ignora RLS.
>
> 1. Agregá una policy en la misma migración.
> 2. Probá la lectura con el rol de la app en el preview.

## Pre-send check

Read your answer once and look for:

- [ ] Sentences over 25 words. Split them.
- [ ] Words ending in "-ando" or "-iendo". Rewrite the sentence.
- [ ] "Se" with no actor ("se borra", "se rompe"). Name who does it.
- [ ] "Realizar", "efectuar", "proceder a", "llevar a cabo". Use the direct verb.
- [ ] A condition or caveat that the draft lost ("si", "salvo", "solo", "siempre que"). Put it back, even if the sentence gets longer.
- [ ] Two names for the same thing. Pick the glossary one.
- [ ] A list of steps written as a paragraph. Number it.

## When to relax

This is rule 0 in `AGENTS.md`. The target is Karpathy's "80%", not 100%. Relax a rule when the strict version loses a fact, a condition, or a nuance the dev needs. Precision beats brevity.

# Glosario STE-ES del workspace Tuqui

Una palabra, un significado. Usá la columna "Decí" siempre para ese concepto. Si el código usa otro nombre, ponelo entre backticks y no lo rotes con el término del glosario.

Fuentes: `docs/es/` y `docs/docs.json`, `tuqui/web/public/locales/es/translation.json` (la UI), `brand/branding.md`, `AGENTS.md` y `tuqui/AGENTS.md`. Revisado oct-2026.

## Producto

| Concepto | Decí | No digas | Nota |
|---|---|---|---|
| Espacio de una empresa en Tuqui | **workspace** | espacio de trabajo | Queda en inglés, como en la UI. |
| Persona con acceso a un workspace | **miembro** | usuario, integrante | "Integrante" es solo dentro de un grupo. |
| Rol con permisos de gestión | **admin** | administrador | La etiqueta del rol en la UI dice "Administrador". |
| Dueño del workspace | **propietario** | owner, dueño | |
| Admin de todo Tuqui | **admin de plataforma** | superadmin | |
| Conjunto de miembros | **grupo** | equipo | Dentro del grupo: **gestor** e **integrante**. |
| Instrucción reutilizable | **skill** | habilidad | La UI usa "habilidad" para otra cosa (endpoints de un conector). |
| Asistente configurado que corre solo | **agente** | asistente, bot | |
| Claude, ChatGPT o Tuqui frente al cliente | **asistente** | empleado | `brand/branding.md` prohíbe "empleado". |
| Cliente MCP o app externa conectada | **conector** | integración, connector | `brand/branding.md` prohíbe "conector" en copy de marketing. En la charla entre devs vale. |
| Función que el modelo puede llamar | **tool** | herramienta | La UI dice "herramienta". Entre devs y en el código, "tool". |
| Página generada por el modelo | **artifact** | artefacto | |
| Documentos indexados del workspace | **base de conocimiento** | KB, knowledge base | |
| Proyecto de Tuqui | **proyecto** | | Si hablás de un proyecto de Odoo, decí "proyecto de Odoo" y su ID. |
| Hilo de chat | **conversación** | chat, hilo | "Chat" es el producto o la pantalla, no el hilo. |
| Lo que Tuqui recuerda de un miembro | **memoria personal** | | |
| Ejecución con horario | **tarea programada** | automatización, rutina | En la UI las claves son `automations.*`. |
| Entorno aislado donde corren scripts | **sandbox** | | |
| Modelos de Odoo que Tuqui puede modificar | **modelos de escritura** | permisos de escritura | |
| Permiso de Odoo o de escritura | **permiso** | | |
| Pantalla OAuth del conector | **autorizar acceso** | consentimiento | |
| Suscripción del workspace | **plan** | | |
| Lugar pago para un miembro | **asiento** | seat | En el admin interno sigue "seats". |
| Presupuesto mensual de gasto | **cupo mensual** | límite, tope | |
| Cuenta sin persona detrás | **cuenta de servicio** | | No ocupa asiento. |
| Módulo de Odoo de Tuqui | **Companion** | addon | Nombre técnico del embed: `tuqui_assistant`. |
| Panel de Tuqui dentro de Odoo | **Tuqui Assistant** | | |
| Chat propio de Tuqui | **Tuqui Chat** | | |
| Servidor MCP de Tuqui | **Tuqui Connector** | | |

## Flujo de trabajo del equipo

| Concepto | Decí | No digas | Nota |
|---|---|---|---|
| Registro de trabajo en el Odoo de Adhoc | **tarea** + su ID (`tarea 75848`) | issue, card | Es un `project.task`. |
| Bug o consulta de un cliente | **ticket** | | Es una tarea del proyecto 1531. Una tarea del 902 no es un ticket. |
| Pull request | **PR** | pull, MR, merge request | |
| Rama de git | **rama** | branch | |
| Checkout aparte en `.claude/worktrees/` | **worktree** | | |
| Rama de integración de `tuqui` | **`staging`** | develop, dev | |
| Entorno productivo | **prod** | producción, live | |
| Despliegue de Railway | **deploy** | | Puede ser de un preview, de `staging` o de prod. |
| Llevar lo mergeado a prod | **release** | deploy | Un release dispara un deploy, no al revés. |
| Entorno de Railway por PR | **preview** | | |
| Cambio de esquema en Supabase | **migración** | | Archivo en `tuqui/supabase/migrations/`. |
| Pipeline de GitHub Actions | **CI** | | |
| Contrato de una feature | **spec** | | Vive en `Tuqui-AI/specs`. |
| Decisión registrada | **ADR** | | |

No uses diagramas: respondé solo con texto, listas o tablas.
