# ste-es

Estilo de respuesta para agentes (Claude Code, Codex, Gemini) que le hablan a un dev en español: directo, conciso y con lo concreto a mano, para que no haga falta repreguntar "resumime" o "dame un ejemplo".

> **Estado:** experimento. `ste-es` es el nombre del proyecto hasta que quede definido. Si la prueba sale bien, la convención pasa a [adhoc-way](https://github.com/ingadhoc/adhoc-way) y este repo se archiva.

## Qué es

Las reglas son el texto exacto del brazo `nucleo_diag` que midió el eval: un núcleo sacado de ASD-STE100 (el inglés controlado de los manuales de aviones) y del propio eval, más diagramas de texto solo cuando la respuesta tiene estructura. El vocabulario es el [glosario de adhoc-way](https://github.com/ingadhoc/adhoc-way/blob/main/templates/glosario.md).

0. La precisión gana: ninguna regla justifica perder un dato o una condición.
1. La respuesta va en la primera oración.
2. Incluir el comando o el ejemplo concreto.
3. Oraciones cortas.
4. Voz activa.
5. Sin relleno.
6. Voseo.
7. Diagramas solo con 3 o más partes relacionadas, sin repetir en el texto.

El detalle está en [`skills/ste-es/SKILL.md`](skills/ste-es/SKILL.md).

## Instalar

```bash
npx skills add joa-adhoc/ste-es -g -y
node ~/.agents/skills/ste-es/scripts/install.mjs
```

Una skill se carga a demanda, así que sola no alcanza: en el eval, instalada sin más, no se cargó nunca. `install.mjs` la activa en cada sesión:

- **Claude Code:** un hook `SessionStart` en `~/.claude/settings.json`, más un bloque en `~/.claude/CLAUDE.md`.
- **Codex:** un bloque en `~/.codex/AGENTS.md`.
- **Gemini CLI:** un bloque en `~/.gemini/GEMINI.md`.

Solo toca los agentes que encuentra instalados. Es idempotente, y no modifica el resto de esos archivos.

```bash
node ~/.agents/skills/ste-es/scripts/install.mjs --check      # qué está instalado
node ~/.agents/skills/ste-es/scripts/install.mjs --uninstall  # sacar todo
```

## Qué se midió

[`evals/`](evals/) compara Claude Code sin nada contra varias versiones de las reglas: 18 casos, 3 corridas por caso, Claude Code aislado. Corrida de referencia `local-03` (Sonnet):

| | Sin reglas | Núcleo | Núcleo + diagramas | STE-ES v1 (13 reglas) |
|---|---|---|---|---|
| Responde en la 1.ª oración | 31% | 94% | 91% | 46% |
| Repreguntas | 69% | 52% | 59% | 57% |
| Tokens hasta entender | 92,5k | 70,8k | 78,7k | 82,1k |
| Condiciones conservadas | 99,4% | 99,4% | 98,2% | 97,6% |
| Afirmaciones incorrectas | 28 | 14 | 20 | 14 |
| Preferencia contra sin reglas | — | 35 a 19 | 37 a 17 | 24 a 30 |

Límites: un solo modelo, y el juez y el lector también son Claude. La skill publicada (`skill_v2`) todavía no tiene corrida propia.
