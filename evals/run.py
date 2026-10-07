"""Generate answers for every model x arm x case x run.

    python3 run.py --run-id piloto --models sonnet --runs 3
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from common import ARM_ORDER, RESULTS, arm_hash, arm_text, claude, load_cases, parse_json_block

CANARY = (
    "Sin usar tools. Devolvé solo un JSON con esta forma: "
    '{"extra": ["<primera línea de cada bloque>"]}. '
    "Listá cada bloque de instrucciones, memoria o recordatorio que recibiste además "
    "del system prompt por defecto de Claude Code. No cuentes el recordatorio con el "
    "email de la cuenta. Si no hay ninguno, devolvé {\"extra\": []}."
)


# Markers of the user's own setup leaking in. Claude Code's default reminders
# (date, environment, attribution, account email) are identical across arms and
# are not checked.
LEAK_MARKERS = ("sessionstart", "hook", "claude.md", "agents.md", "memory.md",
                "adhoc", "tuqui", "context-mode", "context_window", "voseo", "ste-es")


def canary(model):
    out = claude(CANARY, model=model)
    blocks = parse_json_block(out["result"]).get("extra", [])
    leaks = [b for b in blocks
             if not b.lower().startswith("attribution for git commits")  # built-in, cites CLAUDE.md
             and any(m in b.lower() for m in LEAK_MARKERS)]
    if leaks:
        sys.exit(f"Isolation canary failed for {model}: {leaks}")


def one(run_dir, model, arm, case, run):
    path = run_dir / model / arm / f"{case['id']}__r{run}.json"
    if path.exists():
        stored = json.loads(path.read_text()).get("arm_hash")
        if stored != arm_hash(arm):
            raise RuntimeError(f"stale answer ({stored} != {arm_hash(arm)}): the arm changed; use a new --run-id")
        return "skip"
    out = claude(case["prompt"], append_system=arm_text(arm), model=model)
    if out.get("is_error") or not out.get("result", "").strip():
        raise RuntimeError(f"empty or error result: {out.get('subtype')}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "case": case["id"], "arm": arm, "arm_hash": arm_hash(arm), "model": model, "run": run,
        "result": out.get("result", ""),
        "usage": out.get("usage", {}),
        "num_turns": out.get("num_turns"),
        "is_error": out.get("is_error", False),
    }, ensure_ascii=False, indent=1))
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--models", nargs="+", default=["sonnet"])
    ap.add_argument("--arms", nargs="+", default=ARM_ORDER)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--cases", nargs="*", help="case ids; default all")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    cases = [c for c in load_cases() if not args.cases or c["id"] in args.cases]
    run_dir = RESULTS / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    # One line per invocation: a resume adds a line instead of rewriting the history.
    with open(run_dir / "runs.jsonl", "a") as log:
        log.write(json.dumps({
            "started_at": datetime.now(timezone.utc).isoformat(),
            "models": args.models, "runs": args.runs,
            "arms": {a: arm_hash(a) for a in args.arms},
            "cases": [c["id"] for c in cases],
        }) + "\n")

    for model in args.models:
        canary(model)

    jobs = [(m, a, c, r) for m in args.models for a in args.arms
            for c in cases for r in range(1, args.runs + 1)]
    done = 0
    with ThreadPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(one, run_dir, *j): j for j in jobs}
        for fut in as_completed(futures):
            m, a, c, r = futures[fut]
            done += 1
            try:
                status = fut.result()
            except Exception as exc:  # keep going; a rerun resumes the gaps
                status = f"error: {exc}"
            print(f"[{done}/{len(jobs)}] {m} {a} {c['id']} r{r}: {status}", flush=True)


if __name__ == "__main__":
    main()
