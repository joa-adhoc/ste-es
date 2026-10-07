"""Simulated dev reader, several reads per answer: does it need a follow-up? If so, generate it with the same arm.

    python3 reader.py --run-id local-02 --reader-model sonnet
"""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from collections import Counter

from common import JUDGE, NO_TOOLS, RESULTS, arm_hash, arm_text, claude, is_cached, load_cases, parse_json_block, text_hash

READER = """Sos un dev del equipo. Hiciste esta pregunta y recibiste esta respuesta. No tenés otro material.

PREGUNTA:
<<<
{question}
>>>

RESPUESTA:
<<<
{answer}
>>>

Decidí, siendo exigente pero realista:
- "first_sentence_answers": ¿la primera oración ya responde lo que preguntaste?
- "needs_followup": ¿necesitás pedir algo más antes de poder actuar o quedarte tranquilo?
- "type": si necesitás algo, qué pedirías:
  "resumen" (es largo o difícil de seguir), "ejemplo" (es abstracto, falta el comando o el caso concreto),
  "aclaracion" (algo es ambiguo o no se entiende), "dato" (falta información). Si no necesitás nada, null.
- "followup": la repregunta exacta que harías, o null.

Devolvé solo JSON:
{{"first_sentence_answers": true, "needs_followup": false, "type": null, "followup": null}}"""

FOLLOWUP = """{prompt}

Tu respuesta anterior fue:
<<<
{answer}
>>>

Repregunta del dev: {followup}"""


def question_of(prompt):
    return prompt.split("Material:")[0].strip()


def majority(values):
    return sum(bool(v) for v in values) * 2 > len(values)


def read_one(run_id, model, reader_model, case, ans_path, reads):
    """Several independent reads; the verdict is the majority, and agreement is recorded."""
    arm = ans_path.parent.name
    out_path = JUDGE / run_id / model / "reader" / arm / ans_path.name
    ans = json.loads(ans_path.read_text())
    key = {"reader_model": reader_model, "reads": reads, "answer": text_hash(ans["result"])}
    if is_cached(out_path, **key):
        return "skip"
    if ans.get("arm_hash") != arm_hash(arm):
        raise RuntimeError("the arm changed since this answer was generated; the follow-up would use other rules")
    prompt = READER.format(question=question_of(case["prompt"]), answer=ans["result"])
    votes = [parse_json_block(claude(prompt, model=reader_model, extra=NO_TOOLS)["result"]) for _ in range(reads)]
    follow_votes = [bool(v.get("needs_followup")) for v in votes]
    first_votes = [bool(v.get("first_sentence_answers")) for v in votes]
    verdict = {
        "reads": votes,
        "needs_followup": majority(follow_votes),
        "first_sentence_answers": majority(first_votes),
        "unanimous_followup": len(set(follow_votes)) == 1,
        "unanimous_first": len(set(first_votes)) == 1,
        "type": None,
        "followup": None,
    }
    if verdict["needs_followup"]:
        asked = [v for v in votes if v.get("needs_followup") and v.get("followup")]
        types = [v["type"] for v in asked if v.get("type")]
        # most_common keeps first-seen order on ties, so the choice is deterministic.
        verdict["type"] = Counter(types).most_common(1)[0][0] if types else None
        chosen = next((v for v in asked if v.get("type") == verdict["type"]), asked[0] if asked else None)
        if chosen:
            verdict["followup"] = chosen["followup"]
            follow = claude(FOLLOWUP.format(prompt=case["prompt"], answer=ans["result"],
                                            followup=chosen["followup"]),
                            append_system=arm_text(arm), model=model)
            verdict["followup_answer"] = follow.get("result", "")
            verdict["followup_usage"] = follow.get("usage", {})
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({**verdict, "key": key}, ensure_ascii=False, indent=1))
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--reader-model", default="sonnet")
    ap.add_argument("--reads", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    cases = {c["id"]: c for c in load_cases()}
    jobs = []
    for model_dir in (p for p in (RESULTS / args.run_id).iterdir() if p.is_dir()):
        for ans_path in model_dir.glob("*/*.json"):
            cid = ans_path.stem.split("__")[0]
            jobs.append((args.run_id, model_dir.name, args.reader_model, cases[cid], ans_path, args.reads))

    with ThreadPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(read_one, *j): j for j in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            j = futures[fut]
            try:
                status = fut.result()
            except Exception as exc:
                status = f"error: {exc}"
            print(f"[{i}/{len(jobs)}] reader {j[4].parent.name} {j[3]['id']}: {status}", flush=True)


if __name__ == "__main__":
    main()
