"""Comprehension check: a reader answers the case's control questions from the answer alone,
and a grader scores those answers against the key.

    python3 comprehension.py --run-id local-03 --model sonnet
"""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import JUDGE, NO_TOOLS, RESULTS, claude, is_cached, load_cases, parse_json_block, text_hash

ANSWERER = """Leíste solo este texto. No tenés otra fuente.

TEXTO:
<<<
{answer}
>>>

Contestá cada pregunta usando solo lo que dice el texto. Si el texto no lo dice, contestá "no lo dice". No completes con conocimiento propio.

{questions}

Devolvé solo JSON: {{"answers": ["...", "...", "..."]}}"""

GRADER = """Corregí respuestas contra una clave.

{items}

Para cada ítem, decidí:
- "correct": coincide con la clave en lo esencial, incluida cualquier condición que la clave mencione.
- "partial": coincide en parte, o le falta la condición.
- "wrong": contradice la clave.
- "not_stated": la respuesta dice que el texto no lo dice.

Devolvé solo JSON: {{"grades": ["correct", "partial", "wrong"]}}"""


def check_one(run_id, model, judge_model, case, ans_path):
    arm = ans_path.parent.name
    out_path = JUDGE / run_id / model / "comprehension" / arm / ans_path.name
    control = case["control"]
    ans = json.loads(ans_path.read_text())
    key = {"model": judge_model, "answer": text_hash(ans["result"]),
           "control": text_hash(*(c["q"] + c["a"] for c in control))}
    if is_cached(out_path, **key):
        return "skip"
    questions = "\n".join(f"{i}. {c['q']}" for i, c in enumerate(control, 1))
    given = parse_json_block(claude(ANSWERER.format(answer=ans["result"], questions=questions),
                                    model=judge_model, extra=NO_TOOLS)["result"])["answers"]
    if len(given) != len(control):
        raise RuntimeError(f"expected {len(control)} answers, got {len(given)}")
    items = "\n\n".join(f"Ítem {i}\nPregunta: {c['q']}\nClave: {c['a']}\nRespuesta: {g}"
                        for i, (c, g) in enumerate(zip(control, given), 1))
    grades = parse_json_block(claude(GRADER.format(items=items), model=judge_model, extra=NO_TOOLS)["result"])["grades"]
    if len(grades) != len(control) or not set(grades) <= {"correct", "partial", "wrong", "not_stated"}:
        raise RuntimeError(f"bad grades: {grades}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"answers": given, "grades": grades, "key": key}, ensure_ascii=False, indent=1))
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--model", default="sonnet", help="model for the answerer and the grader")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    cases = {c["id"]: c for c in load_cases()}
    jobs = []
    for model_dir in (p for p in (RESULTS / args.run_id).iterdir() if p.is_dir()):
        for ans_path in model_dir.glob("*/*.json"):
            case = cases[ans_path.stem.split("__")[0]]
            if case.get("control"):
                jobs.append((args.run_id, model_dir.name, args.model, case, ans_path))

    with ThreadPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(check_one, *j): j for j in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            j = futures[fut]
            try:
                status = fut.result()
            except Exception as exc:
                status = f"error: {exc}"
            print(f"[{i}/{len(jobs)}] comprehension {j[4].parent.name} {j[3]['id']}: {status}", flush=True)


if __name__ == "__main__":
    main()
