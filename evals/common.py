"""Shared helpers: paths, arms and the isolated Claude Code call."""

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CASES = HERE / "cases.yml"
RESULTS = HERE / "results"
JUDGE = HERE / "judge"

ARM_ORDER = ["baseline", "ste_es", "ste_es_v3", "concise", "conventions", "conventions_v3", "conventions_concise", "conventions_v4", "conventions_v5", "conventions_v6"]

# Flags that keep the user's setup out of the run: no user/local settings
# (hooks, plugins), no CLAUDE.md outside the empty cwd, no MCP servers, no
# claude.ai connectors, no web access.
ISOLATION_FLAGS = [
    "--setting-sources", "project",
    "--strict-mcp-config",
    "--disable-slash-commands",
    "--no-session-persistence",
    "--disallowedTools", "WebSearch", "WebFetch",
    "--output-format", "json",
]
ISOLATION_ENV = {"ENABLE_CLAUDEAI_MCP_SERVERS": "false"}
NO_TOOLS = ("--tools=",)
REFERENCE = "baseline"


# Who reads and judges an answer. Functional profiles do not know code, models or field names, and an
# LLM told to play them still understands everything, so the jargon rule makes that limit explicit.
PERSONAS = {
    None: "un dev del equipo.",
    "soporte": "una persona de soporte funcional del equipo: usás Odoo desde la pantalla (menús, botones, documentos) y no sabés de código, modelos ni nombres técnicos de campos.",
    "actualizacion": "una persona del equipo de actualizaciones de versión: conocés Odoo desde la pantalla y los procesos del cliente, no el código, los modelos ni los nombres técnicos de campos.",
    "consultoria": "una persona de consultoría funcional del equipo: conocés los procesos del cliente y Odoo desde la pantalla, no el código ni los nombres técnicos de campos.",
    "comercial": "una persona del equipo comercial: hablás con clientes y no conocés Odoo por dentro.",
}
JARGON_RULE = (" Un nombre técnico (campo, modelo, método, módulo) que no conocés y que la respuesta no explica"
               " cuenta como algo que no entendés.")


def persona(case):
    profile = case.get("perfil")
    return PERSONAS[profile] + (JARGON_RULE if profile else "")


def persona_key(case):
    """Added to a verdict's cache key only for functional cases, so dev verdicts stay valid."""
    return {"persona": case["perfil"]} if case.get("perfil") else {}


def load_cases():
    return yaml.safe_load(CASES.read_text())["cases"]


def arm_text(arm):
    """Arms are frozen snapshots in arms/<arm>.md, so editing AGENTS.md or the skills never
    silently changes an arm that already has answers. To measure a new version, add a new arm.
    An arm made only of settings (arms/<arm>.settings.json) needs no .md."""
    path = HERE / "arms" / f"{arm}.md"
    if path.exists():
        return path.read_text().strip()
    if arm == "baseline" or arm_settings(arm):
        return ""
    raise FileNotFoundError(f"arm {arm!r} has neither arms/{arm}.md nor arms/{arm}.settings.json")


def arm_settings(arm):
    """Optional Claude Code settings for an arm (arms/<arm>.settings.json), e.g. a built-in output style."""
    path = HERE / "arms" / f"{arm}.settings.json"
    return path.read_text().strip() if path.exists() else ""


def arm_hash(arm):
    return hashlib.sha1((arm_text(arm) + arm_settings(arm)).encode()).hexdigest()[:10]


def text_hash(*texts):
    return hashlib.sha1("\x00".join(texts).encode()).hexdigest()[:10]


def is_cached(path, **key):
    """A verdict is reused only if it was made with the same model, settings and answer text."""
    if not path.exists():
        return False
    stored = json.loads(path.read_text()).get("key", {})
    return stored == key


def tokens_to_understand(answer, reader):
    """Output tokens of the answer plus the follow-up answer, when the reader needed one."""
    extra = (reader or {}).get("followup_usage", {}).get("output_tokens", 0)
    return answer["usage"].get("output_tokens", 0) + extra


def claude(prompt, arm=None, model=None, extra=(), timeout=600):
    """Run `claude -p` in a fresh empty directory, with the arm's text and settings if one is given.
    Returns the parsed JSON result."""
    cmd = ["claude", "-p", *ISOLATION_FLAGS, *extra]
    if model:
        cmd += ["--model", model]
    if arm and arm_text(arm):
        cmd += ["--append-system-prompt", arm_text(arm)]
    if arm and arm_settings(arm):
        cmd += ["--settings", arm_settings(arm)]
    env = {**os.environ, **ISOLATION_ENV}
    with tempfile.TemporaryDirectory(prefix="ste-es-eval-") as cwd:
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True,
            cwd=cwd, env=env, timeout=timeout,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"claude failed ({proc.returncode}): {proc.stderr[-500:]}")
    return json.loads(proc.stdout)


def parse_json_block(text):
    """Extract the first JSON object from a model answer (fenced or bare)."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fenced:
        return json.loads(fenced.group(1))
    # raw_decode stops at the end of the first object, so trailing prose or a second object is ignored.
    return json.JSONDecoder().raw_decode(text[text.find("{"):])[0]
