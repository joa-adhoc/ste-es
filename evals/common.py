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

ARM_ORDER = ["baseline", "terse", "core", "core_plus", "core_diagrams", "core_vocab", "full_v1_no_diagrams", "full_v1", "skill_v2"]

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
REFERENCE = "terse"


def load_cases():
    return yaml.safe_load(CASES.read_text())["cases"]


def arm_text(arm):
    """Arms are frozen snapshots in arms/<arm>.md, so editing AGENTS.md or the skills never
    silently changes an arm that already has answers. To measure a new version, add a new arm."""
    if arm == "baseline":
        return ""
    return (HERE / "arms" / f"{arm}.md").read_text().strip()


def arm_hash(arm):
    return hashlib.sha1(arm_text(arm).encode()).hexdigest()[:10]


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


def claude(prompt, append_system="", model=None, extra=(), timeout=600):
    """Run `claude -p` in a fresh empty directory. Returns the parsed JSON result."""
    cmd = ["claude", "-p", *ISOLATION_FLAGS, *extra]
    if model:
        cmd += ["--model", model]
    if append_system:
        cmd += ["--append-system-prompt", append_system]
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
