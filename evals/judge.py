"""Judge answers: fidelity per fact, wrong claims, diagram errors, and blind preference against `breve`.

    python3 judge.py --run-id piloto --judge-model sonnet
"""

import argparse
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import JUDGE, NO_TOOLS, REFERENCE, RESULTS, claude, is_cached, load_cases, parse_json_block, text_hash

FIDELITY = """Sos un evaluador. Compará una respuesta con una lista de hechos esperados.

PREGUNTA Y MATERIAL (la única fuente válida):
<<<
{prompt}
>>>

HECHOS ESPERADOS:
{facts}

RESPUESTA A EVALUAR:
<<<
{answer}
>>>

Para cada hecho, decidí:
- "present": la respuesta lo dice, con otras palabras sirve. Si el hecho es una condición o salvedad, tiene que estar la condición completa.
- "absent": no lo dice o lo dice incompleto.
- "contradicted": dice lo contrario.

Además:
- "incorrect": afirmaciones de la respuesta que el material contradice o que no tienen sustento en él. Ignorá consejos generales que no contradicen el material.
- "diagram": si la respuesta tiene un diagrama (texto con cajas o flechas), contá cuántos rótulos o flechas contradicen el material. Si no hay diagrama, null.

Devolvé solo JSON:
{{"facts": [{{"n": 1, "status": "present"}}], "incorrect": ["..."], "diagram": {{"errors": 0}} }}"""

PAIRWISE = """Sos un dev del equipo. Te llegan dos respuestas a la misma pregunta. Elegí la que preferirías recibir: la que entendés más rápido y mejor, sin perder información que necesitás.

PREGUNTA:
<<<
{prompt}
>>>

RESPUESTA A:
<<<
{a}
>>>

RESPUESTA B:
<<<
{b}
>>>

Devolvé solo JSON: {{"winner": "A" | "B" | "tie", "reason": "<una oración>"}}"""


def fidelity(run_id, model, judge_model, case, ans_path):
    out_path = JUDGE / run_id / model / "fidelity" / ans_path.parent.name / ans_path.name
    ans = json.loads(ans_path.read_text())
    key = {"judge_model": judge_model, "answer": text_hash(ans["result"])}
    if is_cached(out_path, **key):
        return "skip"
    facts = "\n".join(
        f"{i}. {f['fact']}" + (" [condición]" if f.get("condition") else "")
        for i, f in enumerate(case["pass_criteria"], 1)
    )
    out = claude(FIDELITY.format(prompt=case["prompt"], facts=facts, answer=ans["result"]),
                 model=judge_model, extra=NO_TOOLS)
    verdict = parse_json_block(out["result"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({**verdict, "key": key}, ensure_ascii=False, indent=1))
    return "ok"


def pairwise(run_id, model, judge_model, case, run, arm, reference=REFERENCE):
    """Blind comparison of `arm` against a reference arm, random A/B order."""
    folder = "pairwise" if reference == REFERENCE else f"pairwise_vs_{reference}"
    out_path = JUDGE / run_id / model / folder / arm / f"{case['id']}__r{run}.json"
    base = RESULTS / run_id / model
    mine = json.loads((base / arm / f"{case['id']}__r{run}.json").read_text())["result"]
    ref = json.loads((base / reference / f"{case['id']}__r{run}.json").read_text())["result"]
    key = {"judge_model": judge_model, "answers": text_hash(mine, ref)}
    if is_cached(out_path, **key):
        return "skip"
    swap = random.Random(f"{case['id']}{run}{arm}").random() < 0.5
    a, b = (ref, mine) if swap else (mine, ref)
    out = claude(PAIRWISE.format(prompt=case["prompt"], a=a, b=b), model=judge_model, extra=NO_TOOLS)
    verdict = parse_json_block(out["result"])
    w = {"a": "A", "b": "B", "tie": "tie", "empate": "tie"}.get(str(verdict.get("winner", "")).strip().lower())
    if w is None:
        raise RuntimeError(f"unexpected winner: {verdict.get('winner')!r}")
    winner = "tie" if w == "tie" else (arm if (w == "A") != swap else reference)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({**verdict, "swap": swap, "winner_arm": winner, "key": key},
                                   ensure_ascii=False, indent=1))
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--no-pairwise", action="store_true")
    ap.add_argument("--reference", default=REFERENCE, help="arm every other arm is compared against")
    ap.add_argument("--arms", nargs="*", help="only compare these arms against the reference")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    cases = {c["id"]: c for c in load_cases()}
    jobs = []
    for model_dir in (RESULTS / args.run_id).iterdir():
        if not model_dir.is_dir():
            continue
        model = model_dir.name
        arms = [p.name for p in model_dir.iterdir() if p.is_dir()]
        for ans_path in model_dir.glob("*/*.json"):
            cid = ans_path.stem.split("__")[0]
            jobs.append((fidelity, (args.run_id, model, args.judge_model, cases[cid], ans_path)))
        if args.no_pairwise or args.reference not in arms:
            continue
        for arm in arms:
            if arm == args.reference or (arm == "baseline" and args.reference == REFERENCE):
                continue
            if args.arms and arm not in args.arms:
                continue
            for ans_path in (model_dir / arm).glob("*.json"):
                cid, run = ans_path.stem.split("__r")
                if (model_dir / args.reference / ans_path.name).exists():
                    jobs.append((pairwise, (args.run_id, model, args.judge_model, cases[cid], int(run), arm,
                                            args.reference)))

    with ThreadPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(fn, *a): (fn.__name__, a) for fn, a in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            name, a = futures[fut]
            try:
                status = fut.result()
            except Exception as exc:
                status = f"error: {exc}"
            print(f"[{i}/{len(jobs)}] {name} {a[3]['id']}: {status}", flush=True)


if __name__ == "__main__":
    main()
