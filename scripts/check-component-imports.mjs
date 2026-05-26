#!/usr/bin/env node
// Heuristic DS component contract scanner.
// Usage: node scripts/check-component-imports.mjs [root] [--manifest docs/design-system/DESIGN_SYSTEM_MANIFEST.json] [--json] [--fail-on-violation]

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const root = args.find(a => !a.startsWith('--')) || 'src';
const manifestArgIndex = args.indexOf('--manifest');
const manifestPath = manifestArgIndex >= 0 ? args[manifestArgIndex + 1] : 'docs/design-system/DESIGN_SYSTEM_MANIFEST.json';
const asJson = args.includes('--json');
const failOnViolation = args.includes('--fail-on-violation');

const exts = new Set(['.ts', '.tsx', '.js', '.jsx']);
const ignoreDirs = new Set(['node_modules', '.git', 'dist', 'build', '.next', 'coverage', 'vendor']);

function normalizeAllowed(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  return [v];
}

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      if (!ignoreDirs.has(ent.name)) out.push(...walk(p));
    } else if (ent.isFile() && exts.has(path.extname(ent.name))) {
      out.push(p);
    }
  }
  return out;
}

function lineNumber(text, index) {
  return text.slice(0, index).split(/\r?\n/).length;
}

if (!fs.existsSync(manifestPath)) {
  const msg = `No DS manifest found at ${manifestPath}. Run design-recon/design-system-manifest first.`;
  if (asJson) console.log(JSON.stringify({ manifestPath, violations: [], warnings: [{ message: msg }] }, null, 2));
  else console.log(msg);
  process.exit(0);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const componentImports = manifest.component_imports || {};
const components = Object.keys(componentImports);
const allowedByComponent = Object.fromEntries(components.map(name => [name, normalizeAllowed(componentImports[name])]));
const files = walk(root);
const violations = [];
const warnings = [];

for (const file of files) {
  const text = fs.readFileSync(file, 'utf8');

  // import { Button } from '...'; import Button from '...';
  const importRx = /import\s+(?:([A-Za-z0-9_]+)|\{([^}]+)\})\s+from\s+['"]([^'"]+)['"]/g;
  let match;
  while ((match = importRx.exec(text)) !== null) {
    const defaultName = match[1];
    const named = match[2] ? match[2].split(',').map(s => s.trim().split(/\s+as\s+/i)[0].trim()).filter(Boolean) : [];
    const source = match[3];
    const importedNames = [defaultName, ...named].filter(Boolean);
    for (const imported of importedNames) {
      if (components.includes(imported)) {
        const allowed = allowedByComponent[imported];
        if (allowed.length && !allowed.some(src => source === src || source.endsWith(src) || src.endsWith(source))) {
          violations.push({
            type: 'wrong-component-import-source',
            file,
            line: lineNumber(text, match.index),
            component: imported,
            source,
            allowed
          });
        }
      }
    }
  }

  // function Button(...) or const Button = ... outside allowed source paths.
  for (const name of components) {
    const declRx = new RegExp(`(?:function\\s+${name}\\s*\\(|const\\s+${name}\\s*=|class\\s+${name}\\s+)`, 'g');
    let d;
    while ((d = declRx.exec(text)) !== null) {
      const allowed = allowedByComponent[name];
      const normalizedFile = file.split(path.sep).join('/');
      const isAllowedFile = allowed.some(src => normalizedFile.includes(src.replace('@/', '').replace(/^\.\//, '')));
      if (!isAllowedFile) {
        violations.push({ type: 'duplicate-component-declaration', file, line: lineNumber(text, d.index), component: name, allowed });
      }
    }
  }

  // Native primitives when DS has equivalents. Warn, because sometimes DS components contain them.
  const primitiveMap = { Button: /<button\b/gi, Input: /<input\b/gi, TextArea: /<textarea\b/gi, Select: /<select\b/gi, Card: /className=['"][^'"]*\bcard\b/i };
  for (const [component, rx] of Object.entries(primitiveMap)) {
    if (!components.includes(component)) continue;
    let p;
    while ((p = rx.exec(text)) !== null) {
      warnings.push({ type: 'native-primitive-used-while-ds-component-exists', file, line: lineNumber(text, p.index), component });
    }
  }
}

const result = { manifestPath, root, violations, warnings };
if (asJson) {
  console.log(JSON.stringify(result, null, 2));
} else {
  if (!violations.length && !warnings.length) console.log('No component contract findings.');
  for (const v of violations) console.log(`VIOLATION ${v.type} ${v.file}:${v.line} ${v.component || ''}`.trim(), JSON.stringify(v));
  for (const w of warnings) console.log(`WARNING ${w.type} ${w.file}:${w.line} ${w.component || ''}`.trim(), JSON.stringify(w));
  console.log(`\n${violations.length} violation(s), ${warnings.length} warning(s).`);
}

if (failOnViolation && violations.length > 0) process.exit(1);
