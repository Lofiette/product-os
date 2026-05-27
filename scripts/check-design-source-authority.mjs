#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const root = process.cwd();
const candidates = [
  'docs/design-system/DESIGN_SYSTEM_MANIFEST.json',
  'docs/design-system/design-system-manifest.json',
  'docs/DESIGN_SYSTEM_MANIFEST.json',
  'DESIGN_SYSTEM_MANIFEST.json'
];

function exists(p) { return fs.existsSync(path.join(root, p)); }
function gitTracked(p) {
  try { execSync(`git ls-files --error-unmatch "${p}"`, {stdio:'pipe'}); return true; }
  catch { return false; }
}
function gitChanged(p) {
  try {
    const out = execSync(`git status --porcelain -- "${p}"`, {encoding:'utf8'}).trim();
    return out.length > 0;
  } catch { return false; }
}

let found = false;
let reports = [];
for (const p of candidates) {
  if (!exists(p)) continue;
  found = true;
  const tracked = gitTracked(p);
  const changed = gitChanged(p);
  let authority = 'unknown';
  if (tracked && !changed) authority = 'authoritative_candidate';
  if (tracked && changed) authority = 'changed_during_task';
  if (!tracked) authority = 'untracked_or_generated';
  reports.push({path:p, tracked, changed, authority, can_prove_compliance: authority === 'authoritative_candidate'});
}

console.log(JSON.stringify({found, manifests: reports, note: 'Generated or changed manifests cannot prove same-task DS compliance without user approval.'}, null, 2));
if (reports.some(r => r.authority !== 'authoritative_candidate')) process.exitCode = 2;
