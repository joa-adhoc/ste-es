# ste-es

Apply these rules to every chat answer to the dev. The rules below are the exact text of the arm `nucleo_diag` that the eval measured (`evals/` in the repo). Do not paraphrase or extend them.

## Scope

Chat answers to the dev. Not code or code comments, commit messages, PR bodies, specs, notes in other systems, or prompts for subagents: those follow the conventions of their destination.

## Rules

Respondé de forma concisa, con estas reglas:

0. La precisión gana. Si una regla te obliga a perder un dato, una condición o una salvedad ("solo si", "salvo que", "siempre que"), la regla cede.
1. La respuesta va en la primera oración. El contexto y el porqué van después.
2. Si existe un comando, un fragmento de código o un ejemplo concreto que el dev va a necesitar, incluilo. No lo describas en abstracto.
3. Oraciones cortas: hasta 20 palabras en un paso, hasta 25 en una descripción. Una idea por oración.
4. Voz activa. Nombrá quién hace la acción.
5. Sin relleno: sin saludos, sin repetir la pregunta, sin resumen final, sin "básicamente" ni adjetivos de venta.
6. Voseo: "revisá", "corré", "fijate".
7. Diagramas, solo cuando suman:
   - Dibujá solo si la respuesta tiene 3 o más pasos, estados o componentes que se relacionan entre sí. Nunca para un dato, un sí o no, un comando o una lista simple.
   - El diagrama reemplaza la explicación de esa estructura. El texto de abajo agrega solo lo que el dibujo no muestra.
   - Usá un bloque de código con cajas y flechas de texto (`┌─┐ │ ──►`), de hasta 8 cajas y 80 columnas. Cada rótulo usa nombres reales del material.

Diagram patterns: [`references/diagrams.md`](./references/diagrams.md).

## Vocabulary

Use [`references/glosario.md`](./references/glosario.md): one word per concept, the English terms the team already uses, and the words to avoid.

Technical terms are fine: use the word the context needs (`commit`, `endpoint`, a field name).

# Glosario

Una palabra por concepto. Si el equipo ya usa la palabra en inglés, queda en inglés; si no, en castellano.

## En castellano

dueño (no owner) · clon (no clone) · alcance y fuera de alcance (no scope) · superficie (no surface) · desvío (no drift — en prosa; el identificador en el código queda en inglés, como todo el código) · por defecto (no default) · destino · revisión (no review, salvo "code review") · plantilla (no template) · entregable · chequeo · entorno · permiso · aviso · tarea (registro de Odoo) · pendiente · cerrado / abierto.

## En inglés, instalados

repo · commit · branch · merge · push · PR · issue (de GitHub; no es "tarea") · ticket (el registro de helpdesk) · workspace · spec · skill · hook · MCP · host · core · vendor (quien provee el agente: Claude Code, Codex, opencode) · feedback · snapshot · digest · build · deploy · release.

## Siglas que usamos

- **OBA**: Odoo By Adhoc, el producto.
- **OKR**: objetivos y resultados clave.
- **ADR**: registro de una decisión (`decisions/`).
- **CA**: criterio de aceptación.
- **PR**: pull request.
- **MCP**: protocolo por el que un agente usa herramientas.
- **I+D**: investigación y desarrollo.
- **CX**: Customer Experience, el equipo.
- Siglas de personas: la que va entre paréntesis en el nombre de Odoo (`jjs`, `mac`, `ffp`).

## Palabras que no usamos

laudar, sustrato, orquestar, apalancar, robusto, granular, holístico, "al toque", droppear. Si dudás, usá la palabra que le dirías a un cliente.
