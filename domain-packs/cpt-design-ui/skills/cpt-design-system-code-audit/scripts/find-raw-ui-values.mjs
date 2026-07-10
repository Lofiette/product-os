#!/usr/bin/env node
// Heuristic scanner for raw UI values: colors, pixel spacing, inline styles.
// Usage: node scripts/find-raw-ui-values.mjs [root] [--json] [--fail-on-hit]

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const root = args.find(a => !a.startsWith('--')) || 'src';
const asJson = args.includes('--json');
const failOnHit = args.includes('--fail-on-hit');

const exts = new Set(['.ts', '.tsx', '.js', '.jsx', '.css', '.scss', '.sass', '.less']);
const ignoreDirs = new Set(['node_modules', '.git', 'dist', 'build', '.next', 'coverage', 'vendor']);

const checks = [
  { id: 'hex-color', severity: 'warning', rx: /#[0-9a-fA-F]{3,8}\b/ },
  { id: 'rgb-color', severity: 'warning', rx: /\brgba?\s*\(/ },
  { id: 'hsl-color', severity: 'warning', rx: /\bhsla?\s*\(/ },
  { id: 'inline-style', severity: 'warning', rx: /style\s*=\s*\{\{/ },
  { id: 'pixel-value', severity: 'info', rx: /\b\d+(?:\.\d+)?px\b/ },
  { id: 'arbitrary-tailwind-value', severity: 'warning', rx: /\b(?:m|p|w|h|min-w|max-w|min-h|max-h|rounded|text|bg|border|shadow)-\[[^\]]+\]/ }
];

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const out = [];
  for (const ent of entries) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      if (!ignoreDirs.has(ent.name)) out.push(...walk(p));
    } else if (ent.isFile() && exts.has(path.extname(ent.name))) {
      out.push(p);
    }
  }
  return out;
}

const hits = [];
for (const file of walk(root)) {
  const text = fs.readFileSync(file, 'utf8');
  const lines = text.split(/\r?\n/);
  lines.forEach((line, idx) => {
    for (const check of checks) {
      if (check.rx.test(line)) {
        hits.push({ file, line: idx + 1, check: check.id, severity: check.severity, text: line.trim() });
      }
    }
  });
}

if (asJson) {
  console.log(JSON.stringify({ root, hits }, null, 2));
} else if (hits.length === 0) {
  console.log('No raw UI value hits found by heuristic scanner.');
} else {
  for (const h of hits) {
    console.log(`${h.severity.toUpperCase()} ${h.check} ${h.file}:${h.line}: ${h.text}`);
  }
  console.log(`\n${hits.length} raw UI value hit(s) found.`);
}

if (failOnHit && hits.length > 0) process.exit(1);
