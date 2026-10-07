# Eval de ste-es

Mide si las reglas de ste-es cumplen el objetivo: que la respuesta sea sencilla, concisa y directa, para que el dev no tenga que repreguntar ("resumime", "dame un ejemplo"), sin perder hechos y sin gastar más tokens. Nació en el harness de Tuqui ([workspace#24](https://github.com/Tuqui-AI/workspace/pull/24), tarea [77063](https://www.adhoc.inc/odoo/project.task/77063)), con casos sacados de la documentación de Tuqui. El material viaja dentro de cada caso, así que no depende de ese repo.

## Brazos

Todos usan el system prompt por defecto de Claude Code. Solo cambia el texto que se suma con `--append-system-prompt`. Cada brazo es un archivo congelado en `arms/`: editar la skill no cambia un brazo que ya tiene respuestas. Para medir una versión nueva, se agrega un brazo nuevo.

| Brazo | Texto agregado |
|---|---|
| `baseline` | ninguno: Claude Code sin nada |
| `breve` | "Respondé de forma concisa." Es la referencia de la preferencia a ciegas. |
| `nucleo` | regla 0 y 4 reglas |
| `nucleo_plus` | `nucleo` + respuesta en la primera oración + ejemplo concreto |
| `nucleo_diag` | `nucleo_plus` + diagramas solo con 3 o más partes relacionadas, sin repetir en el texto |
| `nucleo_ste` | `nucleo_plus` + una palabra un significado + verbos simples |
| `completo` | foto de STE-ES v1 (13 reglas, glosario y diagramas) del 6-oct-2026 |
| `skill_v2` | foto de la skill publicada (`skills/ste-es/SKILL.md` + `references/diagrams.md`). Todavía sin medir. |
| `completo_sin_diag` | `completo` sin la parte de diagramas. Defecto conocido: todavía menciona diagramas en la introducción y termina con "No uses diagramas", así que da instrucciones contradictorias. Solo está en `local-02`. |

Cada respuesta guarda el hash de su brazo. Cada veredicto guarda el modelo, la configuración y el hash del texto que juzgó: si alguno cambia, se rehace en vez de reutilizarse.

## Aislamiento

Cada respuesta corre con `claude -p` en un directorio vacío, sin settings de usuario (hooks, plugins), sin MCP, sin conectores de claude.ai y sin web. Las tools nativas quedan prendidas: son iguales en todos los brazos y el material va dentro del prompt. Antes de empezar, un canario le pide al modelo las instrucciones extra que recibió, y la corrida se corta si aparece algo del entorno del usuario.

## Correr

```bash
python3 run.py --run-id local-03 --models sonnet --runs 3
python3 judge.py --run-id local-03 --judge-model sonnet
python3 judge.py --run-id local-03 --judge-model sonnet --reference baseline
python3 reader.py --run-id local-03 --reader-model sonnet
python3 comprehension.py --run-id local-03 --model sonnet
python3 measure.py --run-id local-03
```

Las corridas se retoman: lo que ya existe se saltea. Cada invocación de `run.py` agrega una línea a `results/<run>/runs.jsonl`. `results/` y `judge/` se commitean como fuente de los números.

## Métricas

**Objetivo:**

| Métrica | Fuente |
|---|---|
| Comprensión: 3 preguntas de control por caso, contestadas solo con la respuesta y corregidas contra una clave | `comprehension.py` |
| Tasa de repregunta, por tipo (resumen, ejemplo, aclaración, dato) | `reader.py`: un lector lee solo la pregunta y la respuesta, 3 veces; decide la mayoría y se informa el acuerdo |
| Respuesta en la primera oración | `reader.py` |
| Tokens hasta entender: respuesta + repregunta generada con el mismo brazo. Se informa solo si todas las respuestas del brazo tienen lectura completa. | `reader.py`, uso de Claude |
| Tokens de entrada: lo que las reglas suman a cada llamada | uso de Claude |

**Guarda** (un brazo no gana si las empeora):

| Métrica | Fuente |
|---|---|
| Hechos y condiciones conservados, afirmaciones incorrectas | `judge.py` |
| Preferencia a ciegas de cada brazo contra `breve` y contra `baseline` | `judge.py`, orden A/B al azar |

**Diagnóstico** (`lint.py`, determinístico): palabras totales y de prosa, violaciones cada 100 palabras (oraciones de más de 25 palabras, punto y coma, gerundios, relleno, nominalizaciones, tuteo), voseo y diagramas en casos con estructura y sin ella.

## Límites

- El linter mide las reglas de STE-ES, así que favorece a los brazos con reglas por diseño.
- Las heurísticas de voseo y gerundio son aproximadas.
- El juez, el lector y el generador son modelos de Claude. El lector simula a un dev, no lo reemplaza.
- Los casos los escribió quien arma las reglas.
- El glosario no se mide: se rehace a partir del de adhoc-way.
