#!/usr/bin/env node
// Turns ste-es on for every session. A skill alone is loaded on demand, so this adds:
//   - a SessionStart hook in ~/.claude/settings.json (Claude Code);
//   - a short marked block in the global instructions of each agent found
//     (~/.claude/CLAUDE.md, ~/.codex/AGENTS.md, ~/.gemini/GEMINI.md).
//
//   node install.mjs              install (idempotent)
//   node install.mjs --check      report what is installed
//   node install.mjs --uninstall  remove everything this script added
//   node install.mjs --hook       print the SessionStart message (used by the hook)

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(import.meta.url);
const SKILL_DIR = resolve(dirname(SCRIPT), "..");
const HOME = homedir();
const START = "<!-- ste-es:start -->";
const END = "<!-- ste-es:end -->";
const MESSAGE =
  "ste-es is active: load the `ste-es` skill now and apply it to every chat answer. " +
  `If you cannot load skills, read ${join(SKILL_DIR, "SKILL.md")}.`;
const HOOK_COMMAND = `node "${SCRIPT}" --hook`;

const INSTRUCTION_FILES = [
  { agent: "Claude Code", dir: join(HOME, ".claude"), file: "CLAUDE.md" },
  { agent: "Codex", dir: join(HOME, ".codex"), file: "AGENTS.md" },
  { agent: "Gemini CLI", dir: join(HOME, ".gemini"), file: "GEMINI.md" },
];
const SETTINGS = join(HOME, ".claude", "settings.json");

const read = (p) => (existsSync(p) ? readFileSync(p, "utf8") : "");
const block = `${START}\n${MESSAGE}\n${END}\n`;
const stripBlock = (text) =>
  text.replace(new RegExp(`\\n?${START}[\\s\\S]*?${END}\\n?`, "g"), "\n").replace(/\n{3,}$/, "\n\n");

function hookEntries(settings) {
  return (settings.hooks?.SessionStart ?? []).filter((g) =>
    (g.hooks ?? []).some((h) => h.command === HOOK_COMMAND),
  );
}

function setHook(install) {
  if (!existsSync(dirname(SETTINGS))) return "Claude Code not found, hook skipped";
  const settings = existsSync(SETTINGS) ? JSON.parse(read(SETTINGS)) : {};
  const groups = settings.hooks?.SessionStart ?? [];
  const others = groups.filter((g) => !(g.hooks ?? []).some((h) => h.command === HOOK_COMMAND));
  const next = install ? [...others, { hooks: [{ type: "command", command: HOOK_COMMAND }] }] : others;
  settings.hooks = { ...(settings.hooks ?? {}), SessionStart: next };
  if (!next.length) delete settings.hooks.SessionStart;
  writeFileSync(SETTINGS, JSON.stringify(settings, null, 2) + "\n");
  return install ? "hook installed" : "hook removed";
}

function setInstructions(install) {
  const out = [];
  for (const { agent, dir, file } of INSTRUCTION_FILES) {
    if (!existsSync(dir)) continue;
    const path = join(dir, file);
    let text = stripBlock(read(path));
    if (install) text = (text.trimEnd() ? text.trimEnd() + "\n\n" : "") + block;
    mkdirSync(dir, { recursive: true });
    writeFileSync(path, text);
    out.push(`${agent}: ${install ? "block added to" : "block removed from"} ${path}`);
  }
  return out;
}

function check() {
  const settings = existsSync(SETTINGS) ? JSON.parse(read(SETTINGS)) : {};
  console.log(`Claude Code hook: ${hookEntries(settings).length ? "installed" : "missing"}`);
  for (const { agent, dir, file } of INSTRUCTION_FILES) {
    if (!existsSync(dir)) continue;
    console.log(`${agent} instructions: ${read(join(dir, file)).includes(START) ? "installed" : "missing"}`);
  }
}

const arg = process.argv[2];
if (arg === "--hook") {
  console.log(MESSAGE);
} else if (arg === "--check") {
  check();
} else if (arg === "--uninstall" || !arg) {
  const install = !arg;
  console.log(setHook(install));
  for (const line of setInstructions(install)) console.log(line);
} else {
  console.error(`Unknown option: ${arg}`);
  process.exit(1);
}
