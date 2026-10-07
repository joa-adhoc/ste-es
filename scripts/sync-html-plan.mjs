#!/usr/bin/env node
// Copies the html-plan skill from anthropics/claude-plugins-community into skills/html-plan/
// at a fixed commit, and records where it came from in skills/html-plan/UPSTREAM.
// Two changes on top: the "## Words" section of SKILL.md (English STE) is replaced by
// patches/html-plan-words.md (Spanish, ste-es), and themes/<theme>.css is appended to
// runtime/htmlplan.css (its @import lines go first). Everything else stays unchanged.
// Updates are manual: run this, review the diff, commit.
//
//   node scripts/sync-html-plan.mjs                     latest commit, theme "adhoc"
//   node scripts/sync-html-plan.mjs <commit-sha>        a specific commit
//   node scripts/sync-html-plan.mjs --theme anthropic   another theme from themes/
//
// Set GITHUB_TOKEN to avoid the unauthenticated API rate limit.

import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const REPO = "anthropics/claude-plugins-community";
const SRC = "html-plan/skills/html-plan";
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const DEST = join(ROOT, "skills", "html-plan");
const WORDS = join(ROOT, "patches", "html-plan-words.md");
const args = process.argv.slice(2);
const themeAt = args.indexOf("--theme");
const THEME = themeAt === -1 ? "adhoc" : args[themeAt + 1];
const positional = args.filter((a, i) => !a.startsWith("--") && i !== themeAt + 1);
const headers = { "User-Agent": "ste-es-sync", ...(process.env.GITHUB_TOKEN && { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` }) };

async function get(url, as = "json") {
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  return as === "json" ? res.json() : Buffer.from(await res.arrayBuffer());
}

const ref = positional[0]
  ?? (await get(`https://api.github.com/repos/${REPO}/commits?path=html-plan&per_page=1`))[0].sha;
const tree = await get(`https://api.github.com/repos/${REPO}/git/trees/${ref}?recursive=1`);
const files = tree.tree.filter((n) => n.type === "blob" && n.path.startsWith(`${SRC}/`));
if (!files.length) throw new Error(`no files under ${SRC} at ${ref}`);

rmSync(DEST, { recursive: true, force: true });
for (const f of files) {
  const out = join(DEST, f.path.slice(SRC.length + 1));
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, await get(`https://raw.githubusercontent.com/${REPO}/${ref}/${f.path}`, "bytes"));
}
// The upstream "Words" section asks for English STE and "no other style"; it arrives with
// /html-plan after ste-es, so it wins unless the copy itself says otherwise.
const skillPath = join(DEST, "SKILL.md");
const skill = readFileSync(skillPath, "utf8");
const start = skill.indexOf("## Words\n");
const end = skill.indexOf("\n## ", start + 1);
if (start === -1 || end === -1) throw new Error("upstream SKILL.md has no '## Words' section: review the patch by hand");
writeFileSync(skillPath, skill.slice(0, start) + readFileSync(WORDS, "utf8").trimEnd() + "\n" + skill.slice(end));
// pack.mjs only looks for htmlplan.css in runtime/, so the theme goes inside it. Its variables
// come after html-plan's and win; @import has to be the first rule of a stylesheet.
const cssPath = join(DEST, "runtime", "htmlplan.css");
const theme = readFileSync(join(ROOT, "themes", `${THEME}.css`), "utf8");
const imports = theme.split("\n").filter((l) => l.startsWith("@import")).join("\n");
const rules = theme.split("\n").filter((l) => !l.startsWith("@import")).join("\n").trim();
writeFileSync(cssPath, (imports ? imports + "\n" : "") + readFileSync(cssPath, "utf8") + `\n/* theme: ${THEME} */\n` + rules + "\n");

const plugin = await get(`https://raw.githubusercontent.com/${REPO}/${ref}/html-plan/.claude-plugin/plugin.json`);
writeFileSync(join(DEST, "LICENSE.upstream"), await get(`https://raw.githubusercontent.com/${REPO}/${ref}/LICENSE`, "bytes"));
writeFileSync(join(DEST, "UPSTREAM"), [
  `Source:  https://github.com/${REPO}/tree/${ref}/${SRC}`,
  `Commit:  ${ref}`,
  `Author:  ${plugin.author?.name ?? "unknown"}`,
  `License: ${plugin.license ?? "see LICENSE.upstream"} (plugin.json); repository license in LICENSE.upstream`,
  `Theme:   ${THEME} (themes/${THEME}.css, appended to runtime/htmlplan.css)`,
  `Copied by scripts/sync-html-plan.mjs. Two changes: the "## Words" section of SKILL.md is replaced by`,
  `patches/html-plan-words.md (Spanish prose with ste-es), and the theme is appended to runtime/htmlplan.css.`,
  `Do not edit these files by hand.`,
  "",
].join("\n"));
console.log(`html-plan synced at ${ref}: ${files.length} files, theme ${THEME}`);
