#!/usr/bin/env node
/**
 * check-versions.mjs — Universal npm dependency version checker
 *
 * Reports the latest stable version within the same major for every
 * dependency in package.json, plus flags when a newer major exists.
 *
 * Usage:  node check-versions.mjs [--all]
 *   --all   Also check peerDependencies and optionalDependencies
 *
 * Works with any npm-based project. Just drop it in and run.
 */
import { execSync } from "child_process";
import { readFileSync } from "fs";

const showAll = process.argv.includes("--all");

const pkg = JSON.parse(readFileSync("package.json", "utf8"));

const PRERELEASE_RE =
  /-(alpha|beta|rc|next|canary|dev|pre|snapshot|experimental|unstable)/i;

function parseVersion(spec) {
  // Strip range operators: ^, ~, >=, <=, >, <, =, ||, spaces
  const cleaned = spec
    .replace(/\|\|/g, " ")
    .trim()
    .split(/\s+/)
    .pop() // take the last segment for ">=1.0.0 <2.0.0" style ranges
    .replace(/[\^~>=<]/g, "")
    .trim();
  return cleaned;
}

function getLatestInMajor(name, currentSpec) {
  // Handle npm: aliases like "npm:xstate@4.38.3"
  if (currentSpec.startsWith("npm:")) {
    const inner = currentSpec.slice(4);
    // Scoped: npm:@scope/pkg@ver  or  Unscoped: npm:pkg@ver
    const lastAt = inner.lastIndexOf("@");
    const aliasName = inner.slice(0, lastAt);
    const aliasVer = inner.slice(lastAt + 1);
    return {
      isAlias: true,
      note: `alias → ${aliasName}@${aliasVer}`,
    };
  }

  // Skip workspace, file, link, git protocols
  if (/^(workspace:|file:|link:|git[+:]|https?:)/.test(currentSpec)) {
    return { isAlias: true, note: currentSpec };
  }

  const clean = parseVersion(currentSpec);
  if (!/^\d+\.\d+/.test(clean)) {
    return { isAlias: true, note: `unparseable: ${currentSpec}` };
  }

  const major = parseInt(clean.split(".")[0]);

  try {
    const raw = execSync(`npm view ${name} versions --json 2>/dev/null`, {
      encoding: "utf8",
    });
    const allVersions = JSON.parse(raw);
    // npm view returns a string for single-version packages
    const versions = Array.isArray(allVersions)
      ? allVersions
      : [allVersions];

    const sameMajor = versions.filter((v) => {
      const m = parseInt(v.split(".")[0]);
      return m === major && !PRERELEASE_RE.test(v);
    });
    const latestSameMajor = sameMajor[sameMajor.length - 1] || clean;

    const latestAll = execSync(`npm view ${name} version 2>/dev/null`, {
      encoding: "utf8",
    }).trim();
    const latestMajor = parseInt(latestAll.split(".")[0]);

    return {
      currentClean: clean,
      latestSameMajor,
      latestAbsolute: latestAll,
      needsUpdate: clean !== latestSameMajor,
      majorAvailable: latestMajor > major ? latestAll : null,
    };
  } catch {
    return { error: true };
  }
}

// Sections to check
const sections = ["dependencies", "devDependencies"];
if (showAll) sections.push("peerDependencies", "optionalDependencies");

let totalOk = 0;
let totalUpdate = 0;
let totalMajor = 0;
let totalError = 0;

console.log("=== DEPENDENCY VERSION REPORT ===");

for (const section of sections) {
  const deps = pkg[section];
  if (!deps || Object.keys(deps).length === 0) continue;

  console.log(`\n--- ${section} ---\n`);
  console.log(
    `${"Package".padEnd(45)} ${"Current".padEnd(16)} ${"Latest(same maj)".padEnd(18)} ${"Latest(abs)".padEnd(15)} Status`
  );
  console.log("-".repeat(120));

  for (const [name, spec] of Object.entries(deps)) {
    const info = getLatestInMajor(name, spec);

    if (info.isAlias) {
      console.log(
        `${name.padEnd(45)} ${spec.padEnd(16)} ${"—".padEnd(18)} ${"—".padEnd(15)} ${info.note}`
      );
      continue;
    }
    if (info.error) {
      totalError++;
      console.log(
        `${name.padEnd(45)} ${spec.padEnd(16)} ${"ERROR".padEnd(18)}`
      );
      continue;
    }

    const status = [];
    if (info.needsUpdate) {
      totalUpdate++;
      status.push("⬆️  UPDATE");
    } else {
      totalOk++;
      status.push("✅ OK");
    }
    if (info.majorAvailable) {
      totalMajor++;
      status.push(`🆕 major ${info.majorAvailable}`);
    }

    console.log(
      `${name.padEnd(45)} ${spec.padEnd(16)} ${info.latestSameMajor.padEnd(18)} ${info.latestAbsolute.padEnd(15)} ${status.join(" | ")}`
    );
  }
}

console.log("\n=== SUMMARY ===");
console.log(`  ✅ Up to date:     ${totalOk}`);
console.log(`  ⬆️  Needs update:   ${totalUpdate}`);
console.log(`  🆕 Major available: ${totalMajor}`);
if (totalError) console.log(`  ❌ Errors:          ${totalError}`);
console.log();
