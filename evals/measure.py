"""Summarize a run: length, fidelity, conditions kept, rule violations, diagrams and preference.

    python3 measure.py --run-id piloto
"""

import argparse
import json
import random
from statistics import mean, median

from common import ARM_ORDER, JUDGE, REFERENCE, RESULTS, load_cases, tokens_to_understand
from lint import lint, per100


def bootstrap_ci(values, n=2000, seed=0):
    rnd = random.Random(seed)
    stats = sorted(median(rnd.choices(values, k=len(values))) for _ in range(n))
    return [round(stats[int(0.025 * n)], 3), round(stats[int(0.975 * n)], 3)]


def load_arm(run_id, model, arm, cases):
    rows = []
    for path in sorted((RESULTS / run_id / model / arm).glob("*.json")):
        ans = json.loads(path.read_text())
        case = cases[ans["case"]]
        fid_path = JUDGE / run_id / model / "fidelity" / arm / path.name
        fid = json.loads(fid_path.read_text()) if fid_path.exists() else None
        rd_path = JUDGE / run_id / model / "reader" / arm / path.name
        rd = json.loads(rd_path.read_text()) if rd_path.exists() else None
        cp_path = JUDGE / run_id / model / "comprehension" / arm / path.name
        comp = json.loads(cp_path.read_text()) if cp_path.exists() else None
        rows.append({"key": path.stem, "case": case, "ans": ans, "lint": lint(ans["result"]),
                     "fid": fid, "reader": rd, "comp": comp})
    return rows


def arm_summary(rows):
    facts = cond = facts_ok = cond_ok = contradicted = incorrect = diag_err = 0
    judged = 0
    for r in rows:
        if not r["fid"]:
            continue
        judged += 1
        status = {int(f["n"]): f.get("status") for f in r["fid"].get("facts", []) if str(f.get("n", "")).isdigit()}
        for i, f in enumerate(r["case"]["pass_criteria"], 1):
            ok = status.get(i) == "present"
            facts += 1
            facts_ok += ok
            contradicted += status.get(i) == "contradicted"
            if f.get("condition"):
                cond += 1
                cond_ok += ok
        incorrect += len(r["fid"].get("incorrect") or [])
        diag_err += ((r["fid"].get("diagram") or {}).get("errors") or 0)
    struct = [r for r in rows if r["case"].get("structure")]
    flat = [r for r in rows if not r["case"].get("structure")]
    read = [r for r in rows if r["reader"]]
    # A follow-up that was voted but never generated has no tokens; treat the row as unread.
    complete = [r for r in read if not r["reader"].get("needs_followup") or r["reader"].get("followup_usage")]
    full = len(complete) == len(rows)
    follow_types = {}
    for r in read:
        t = r["reader"].get("type") if r["reader"].get("needs_followup") else None
        if t:
            follow_types[t] = follow_types.get(t, 0) + 1

    def input_tokens(u):
        return u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)

    grade_score = {"correct": 1.0, "partial": 0.5, "wrong": 0.0, "not_stated": 0.0}
    grades = [g for r in rows if r["comp"] for g in r["comp"]["grades"]]

    vos = sum(r["lint"]["voseo"] for r in rows)
    tu = sum(r["lint"]["tuteo"] for r in rows)
    return {
        "n": len(rows),
        "judged": judged,
        "words_median": median(r["lint"]["words"] for r in rows),
        "words_total_median": median(r["lint"]["words_total"] for r in rows),
        "output_tokens_median": median(r["ans"]["usage"].get("output_tokens", 0) for r in rows),
        "input_tokens_median": median(input_tokens(r["ans"]["usage"]) for r in rows),
        "followup_rate": round(mean(bool(r["reader"].get("needs_followup")) for r in read), 2) if read else None,
        "followup_types": follow_types,
        "answer_first": round(mean(bool(r["reader"].get("first_sentence_answers")) for r in read), 2) if read else None,
        "reader_coverage": f"{len(complete)}/{len(rows)}",
        "tokens_to_understand_median": median(tokens_to_understand(r["ans"], r["reader"]) for r in rows) if full else None,
        "tokens_to_understand_total": sum(tokens_to_understand(r["ans"], r["reader"]) for r in rows) if full else None,
        "comprehension": round(mean(grade_score[g] for g in grades), 3) if grades else None,
        "comprehension_not_stated": round(grades.count("not_stated") / len(grades), 3) if grades else None,
        "reader_agreement": round(mean(r["reader"].get("unanimous_followup", True) for r in read), 2) if read else None,
        "facts_kept": round(facts_ok / facts, 3) if facts else None,
        "conditions_kept": round(cond_ok / cond, 3) if cond else None,
        "contradicted": contradicted,
        "incorrect": incorrect,
        "violations_per100": round(mean(per100(r["lint"]) for r in rows), 2),
        "voseo_share": round(vos / (vos + tu), 2) if vos + tu else None,
        "diagram_rate_structure": round(mean(r["lint"]["diagram"] for r in struct), 2) if struct else None,
        "diagram_rate_flat": round(mean(r["lint"]["diagram"] for r in flat), 2) if flat else None,
        "diagram_errors": diag_err,
    }


def paired_delta(rows_a, rows_b, fn, needs_reader=False):
    if needs_reader and not all(r["reader"] for r in rows_a + rows_b):
        return None
    b = {r["key"]: fn(r) for r in rows_b}
    deltas = [(fn(r) - b[r["key"]]) / b[r["key"]] for r in rows_a if b.get(r["key"])]
    if not deltas:
        return None
    return {"median": round(median(deltas), 3), "ci95": bootstrap_ci(deltas), "n": len(deltas)}


def pairwise(run_id, model, reference=REFERENCE):
    out = {}
    folder = "pairwise" if reference == REFERENCE else f"pairwise_vs_{reference}"
    base = JUDGE / run_id / model / folder
    if not base.exists():
        return out
    for other_dir in base.iterdir():
        wins = [json.loads(p.read_text())["winner_arm"] for p in other_dir.glob("*.json")]
        arm = other_dir.name
        out[arm] = {arm: wins.count(arm), "tie": wins.count("tie"), reference: wins.count(reference), "n": len(wins)}
    return out


def table(summary):
    cols = ["n", "reader_coverage", "comprehension", "comprehension_not_stated", "followup_rate", "reader_agreement",
            "followup_types", "answer_first", "tokens_to_understand_total", "tokens_to_understand_median",
            "output_tokens_median", "input_tokens_median", "words_total_median", "words_median", "facts_kept", "conditions_kept",
            "contradicted", "incorrect", "violations_per100", "voseo_share",
            "diagram_rate_structure", "diagram_rate_flat", "diagram_errors"]
    arms = [a for a in ARM_ORDER if a in summary]
    lines = ["| metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for c in cols:
        lines.append(f"| {c} | " + " | ".join(str(summary[a][c]) for a in arms) + " |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    cases = {c["id"]: c for c in load_cases()}
    report = {}
    md = []
    for model_dir in sorted(p for p in (RESULTS / args.run_id).iterdir() if p.is_dir()):
        model = model_dir.name
        rows = {a: load_arm(args.run_id, model, a, cases) for a in ARM_ORDER if (model_dir / a).exists()}
        summary = {a: arm_summary(r) for a, r in rows.items()}
        deltas = {}
        if REFERENCE in rows:
            for a in rows:
                if a in (REFERENCE, "baseline"):
                    continue
                deltas[f"{a}_vs_{REFERENCE}"] = {
                    "tokens_to_understand": paired_delta(rows[a], rows[REFERENCE],
                                                         lambda r: tokens_to_understand(r["ans"], r["reader"]),
                                                         needs_reader=True),
                    "words_total": paired_delta(rows[a], rows[REFERENCE], lambda r: r["lint"]["words_total"]),
                }
        report[model] = {"arms": summary, "deltas": deltas, "pairwise": pairwise(args.run_id, model),
                         "pairwise_vs_baseline": pairwise(args.run_id, model, "baseline")}
        md += [f"## {model}", "", table(summary), "",
               f"Change vs `{REFERENCE}` (per-case median, 95% CI):", ""]
        md += [f"- {k}: {v}" for k, v in deltas.items()]
        md += ["", f"Blind preference (each arm vs `{REFERENCE}`):", ""]
        md += [f"- {k}: {v}" for k, v in report[model]["pairwise"].items()]
        if report[model]["pairwise_vs_baseline"]:
            md += ["", "Blind preference (each arm vs `baseline`, plain Claude Code):", ""]
            md += [f"- {k}: {v}" for k, v in report[model]["pairwise_vs_baseline"].items()]
        md.append("")
    out = RESULTS / args.run_id
    (out / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    (out / "summary.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
