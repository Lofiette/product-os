#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const errors = [];
const warnings = [];
const exists = p => fs.existsSync(path.join(root, p));
const read = p => fs.readFileSync(path.join(root, p), 'utf8');

for (const p of ['CURRENT.md','TASK_INDEX.md','TASK.md','CHRONICLE.md']) {
  if (!exists(p)) errors.push(`Missing ${p}`);
}

if (exists('TASK.md')) {
  const task = read('TASK.md');
  if (!/Deprecated Compatibility Pointer/i.test(task)) errors.push('TASK.md is not marked as deprecated compatibility pointer');
  if (task.length > 1600) errors.push(`TASK.md too large for shim: ${task.length} chars`);
  for (const phrase of ['## Scope', '## Acceptance criteria', '## Role-skill plan', '## Verification plan']) {
    if (task.includes(phrase)) errors.push(`TASK.md contains legacy working section: ${phrase}`);
  }
}

let activeTicket = null;
if (exists('CURRENT.md')) {
  const current = read('CURRENT.md');
  const m = current.match(/Current ticket:\s*`?([A-Z]+-\d+)`?/);
  if (m) activeTicket = m[1]; else errors.push('CURRENT.md does not declare Current ticket');
  if (!/Do not load by default/i.test(current)) warnings.push('CURRENT.md missing explicit do-not-load guidance');
}

if (activeTicket) {
  const taskPath = `tasks/${activeTicket.toUpperCase()}-`;
  const matches = fs.existsSync(path.join(root,'tasks')) ? fs.readdirSync(path.join(root,'tasks')).filter(n => n.startsWith(`${activeTicket}-`) && n.endsWith('.md')) : [];
  if (matches.length === 0) errors.push(`Active ticket ${activeTicket} has no tasks/${activeTicket}-*.md file`);
  if (exists('TASK_INDEX.md') && !read('TASK_INDEX.md').includes(activeTicket)) errors.push(`TASK_INDEX.md does not list active ticket ${activeTicket}`);
}

if (exists('TASK_INDEX.md')) {
  const idx = read('TASK_INDEX.md');
  const currentCount = (idx.match(/\|[^\n]*\|\s*yes\s*\|/gi) || []).length;
  if (currentCount > 1) errors.push(`TASK_INDEX.md has multiple current=yes rows: ${currentCount}`);
  if (currentCount === 0) warnings.push('TASK_INDEX.md has no current=yes row');
}

if (exists('CHRONICLE.md')) {
  const chron = read('CHRONICLE.md');
  if (chron.length > 3000) warnings.push(`CHRONICLE.md may be too large for compact rescue summary: ${chron.length} chars`);
}

if (errors.length) {
  console.log('MEMORY INTEGRITY FAILED');
  for (const e of errors) console.log('-', e);
  for (const w of warnings) console.log('WARN:', w);
  process.exit(1);
}
console.log(`MEMORY INTEGRITY PASSED${warnings.length ? ' WITH WARNINGS' : ''}`);
for (const w of warnings) console.log('WARN:', w);
