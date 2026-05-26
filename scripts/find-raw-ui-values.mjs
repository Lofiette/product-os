#!/usr/bin/env node
// Lightweight heuristic scanner for raw colors/spacing/inline styles.
// Usage: node scripts/find-raw-ui-values.mjs src
import fs from 'fs';
import path from 'path';
const root = process.argv[2] || 'src';
const exts = new Set(['.ts','.tsx','.js','.jsx','.css','.scss']);
const patterns = [/#(?:[0-9a-fA-F]{3}){1,2}/, /rgb\(/, /hsl\(/, /style=\{\{/, /\d+px/];
function walk(dir){
  if(!fs.existsSync(dir)) return [];
  const out=[];
  for(const ent of fs.readdirSync(dir,{withFileTypes:true})){
    const p=path.join(dir,ent.name);
    if(ent.isDirectory() && !['node_modules','.git','dist','build'].includes(ent.name)) out.push(...walk(p));
    if(ent.isFile() && exts.has(path.extname(ent.name))) out.push(p);
  }
  return out;
}
let hits=[];
for(const f of walk(root)){
  const s=fs.readFileSync(f,'utf8');
  s.split(/
/).forEach((line,i)=>{ if(patterns.some(rx=>rx.test(line))) hits.push(`${f}:${i+1}: ${line.trim()}`); });
}
console.log(hits.length ? hits.join('
') : 'No raw UI value hits found by heuristic scanner.');
process.exit(0);
