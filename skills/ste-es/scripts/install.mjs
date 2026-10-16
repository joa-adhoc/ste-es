#!/usr/bin/env node
// Turns ste-es on for every session. A skill alone is loaded on demand, so this adds one
// marked, plain-text block to the global instructions of each agent it finds:
//   ~/.claude/CLAUDE.md (Claude Code), ~/.codex/AGENTS.md (Codex), ~/.gemini/GEMINI.md (Gemini CLI).
// It never adds hooks or anything that runs on its own. You run it, it shows what it will
// change, and it asks before writing. Each changed file is backed up first.
//
//   node install.mjs              show the plan, ask, then install
//   node install.mjs --dry-run    show the plan and exit
//   node install.mjs --yes        install without asking (for scripts)
//   node install.mjs --check      report what is installed in each agent
//   node install.mjs --uninstall  show the plan, ask, then remove everything this script added

import { copyFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { createInterface } from "node:readline/promises";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const SCRIPT = fileURLToPath(import.meta.url);
const SKILL_DIR = resolve(dirname(SCRIPT), "..");
const HOME = homedir();
if (!HOME || !isAbsolute(HOME)) {
  // An empty or relative HOME would make every path below relative to the current directory.
  console.error(`HOME is not an absolute path (${JSON.stringify(HOME)}). Nothing changed.`);
  process.exit(1);
}

const START = "<!-- ste-es:start -->";
const END = "<!-- ste-es:end -->";
const BLOCK_RE = new RegExp(`\\n*${START}[\\s\\S]*?${END}\\n*`, "g");
// Same text as version 1, so an existing block counts as installed and is not rewritten.
const MESSAGE =
  "ste-es is active: load the `ste-es` skill now and apply it to every chat answer. " +
  `If you cannot load skills, read ${join(SKILL_DIR, "SKILL.md")}.`;
const BLOCK = `${START}\n${MESSAGE}\n${END}\n`;

const NO_AGENT = "No agent found (~/.claude, ~/.codex or ~/.gemini).";
const AGENTS = [
  { agent: "Claude Code", path: join(HOME, ".claude", "CLAUDE.md") },
  { agent: "Codex", path: join(HOME, ".codex", "AGENTS.md") },
  { agent: "Gemini CLI", path: join(HOME, ".gemini", "GEMINI.md") },
].filter((a) => existsSync(dirname(a.path)));
// Version 1 added a SessionStart hook that ran `node ".../ste-es/scripts/install.mjs" --hook`.
// It is removed on install and uninstall. Only that exact shape matches.
const SETTINGS = join(HOME, ".claude", "settings.json");
const isLegacyHook = (h) => /ste-es[\\/]scripts[\\/]install\.mjs"?\s+--hook\b/.test(h?.command ?? "");

// Anything that could not be checked. Each one makes the script exit with 1.
const warnings = [];
function warn(text) {
  warnings.push(text);
  console.error(`Warning: ${text}`);
}

const read = (p) => (existsSync(p) ? readFileSync(p, "utf8") : "");

// Removes every block with the blank lines around it; the text on each side joins with one blank line.
function stripBlock(text) {
  const out = text.replace(BLOCK_RE, "\n\n");
  if (out === text) return text;
  const trimmed = out.replace(/^\n+/, "").replace(/\n*$/, "\n");
  return trimmed === "\n" ? "" : trimmed;
}

// "installed", "outdated", "missing", or "broken" when the markers do not pair up.
function blockState(text) {
  const starts = text.split(START).length - 1;
  if (starts !== text.split(END).length - 1) return "broken";
  if (!starts) return "missing";
  return starts === 1 && text.includes(BLOCK) ? "installed" : "outdated";
}

// settings.json without the version 1 hook, or null when there is nothing to remove or the
// file cannot be read (bad JSON or an unexpected shape).
function settingsWithoutLegacyHook(text) {
  try {
    const settings = JSON.parse(text || "{}");
    const groups = settings?.hooks?.SessionStart ?? [];
    if (!groups.some((g) => (g?.hooks ?? []).some(isLegacyHook))) return null;
    // Only the groups that held the old hook change; one left empty goes away.
    const kept = groups.flatMap((g) => {
      const hooks = g?.hooks ?? [];
      if (!hooks.some(isLegacyHook)) return [g];
      const rest = hooks.filter((h) => !isLegacyHook(h));
      return rest.length ? [{ ...g, hooks: rest }] : [];
    });
    if (kept.length) settings.hooks.SessionStart = kept;
    else delete settings.hooks.SessionStart;
    if (!Object.keys(settings.hooks).length) delete settings.hooks;
    return settings;
  } catch (err) {
    warn(`cannot read ${SETTINGS} (${err.message}), so the version 1 hook was not checked.`);
    return null;
  }
}

function plan(install) {
  const steps = [];
  for (const { agent, path } of AGENTS) {
    const before = read(path);
    const state = blockState(before);
    if (state === "broken") {
      warn(`${path} has a ste-es marker without its pair. Fix it by hand; this file was skipped.`);
      continue;
    }
    if (install ? state === "installed" : state === "missing") continue;
    const base = stripBlock(before);
    const after = install ? (base.trimEnd() ? base.trimEnd() + "\n\n" : "") + BLOCK : base;
    if (after !== before) steps.push({ agent, path, before, after, what: install ? "add the ste-es block" : "remove the ste-es block" });
  }
  const before = read(SETTINGS);
  const settings = settingsWithoutLegacyHook(before);
  if (settings) {
    const what = "remove the old ste-es hook (version 1); the whole file is rewritten with 2-space indentation";
    steps.push({ agent: "Claude Code", path: SETTINGS, before, after: JSON.stringify(settings, null, 2) + "\n", what });
  }
  return steps;
}

const STATE_TEXT = {
  installed: "installed",
  outdated: "outdated: run install again",
  missing: "not installed",
  broken: "a ste-es marker has no pair: fix it by hand",
};

// Returns true only when every agent has the current block and the version 1 hook is gone.
function check() {
  if (!AGENTS.length) console.log(NO_AGENT);
  let ok = AGENTS.length > 0;
  for (const { agent, path } of AGENTS) {
    const state = blockState(read(path));
    if (state !== "installed") ok = false;
    console.log(`${agent}: ${STATE_TEXT[state]} (${path})`);
  }
  if (settingsWithoutLegacyHook(read(SETTINGS))) {
    ok = false;
    console.log("Claude Code: old ste-es hook found (version 1): run install again to remove it.");
  }
  return ok;
}

function show(steps, install) {
  if (!steps.length) {
    if (!AGENTS.length) console.log(`${NO_AGENT} Nothing to change.`);
    else if (warnings.length) console.log("Nothing else to change, but see the warnings above.");
    else console.log(install ? "ste-es is installed. Nothing to change." : "ste-es is not installed. Nothing to change.");
    return;
  }
  console.log("This will change:");
  for (const s of steps) console.log(`  - ${s.agent}: ${s.what} in ${s.path}`);
  if (install) console.log(`\nThe block is plain text:\n\n${BLOCK}`);
  console.log("Each file is backed up next to itself (*.ste-es-backup-<time>) before it changes.");
}

async function confirm() {
  if (!process.stdin.isTTY) {
    // Without a terminal the caller is usually an agent: the plan goes to a person first.
    console.error("\nNo terminal to ask in. Show this plan to the user; apply it only with their approval.");
    return false;
  }
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  try {
    return /^y(es)?$/i.test((await rl.question("\nApply these changes? [y/N] ")).trim());
  } catch {
    return false; // Ctrl-D or Ctrl-C at the prompt
  } finally {
    rl.close();
  }
}

// Returns false when any file could not be written. A file that changed after the plan was
// shown is left alone, so the answer to the prompt never overwrites newer edits.
function apply(steps) {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  let ok = true;
  for (const s of steps) {
    try {
      if (read(s.path) !== s.before) throw new Error("it changed after the plan was shown; run the script again");
      if (existsSync(s.path)) copyFileSync(s.path, `${s.path}.ste-es-backup-${stamp}`);
      writeFileSync(s.path, s.after);
      console.log(`  done: ${s.path}`);
    } catch (err) {
      ok = false;
      console.error(`  failed: ${s.path} (${err.message})`);
    }
  }
  if (!ok) console.error("Some files did not change. The files marked done did; their backups are next to them.");
  return ok;
}

if (process.argv.includes("--hook")) {
  // The version 1 SessionStart hook still calls this. systemMessage goes to the person, not to the
  // model, and the script does nothing else.
  const text = `ste-es: the version 1 hook is still in ${SETTINGS}. To remove it, run: node "${SCRIPT}"`;
  console.log(JSON.stringify({ systemMessage: text }));
  process.exit(0);
}

let opts;
try {
  ({ values: opts } = parseArgs({
    strict: true,
    options: {
      "dry-run": { type: "boolean" },
      check: { type: "boolean" },
      yes: { type: "boolean" },
      uninstall: { type: "boolean" },
    },
  }));
  if (opts.check && (opts["dry-run"] || opts.yes || opts.uninstall)) throw new Error("--check goes alone.");
  if (opts["dry-run"] && opts.yes) throw new Error("--dry-run and --yes do not go together.");
} catch (err) {
  console.error(err.message);
  process.exit(1);
}

// Exit 1 tells a script or an agent that something was not installed, applied or checked.
if (opts.check) {
  process.exitCode = check() && !warnings.length ? 0 : 1;
} else {
  const install = !opts.uninstall;
  const steps = plan(install);
  show(steps, install);
  let ok = !(install && !AGENTS.length);
  if (steps.length && !opts["dry-run"]) {
    if (opts.yes || (await confirm())) ok = apply(steps) && ok;
    else {
      console.log("Nothing changed.");
      ok = false;
    }
  }
  process.exitCode = ok && !warnings.length ? 0 : 1;
}
