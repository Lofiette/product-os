#!/usr/bin/env node
// Placeholder heuristic: compare imports with docs/design-system/DESIGN_SYSTEM_MANIFEST.json if present.
import fs from 'fs';
const manifestPath='docs/design-system/DESIGN_SYSTEM_MANIFEST.json';
if(!fs.existsSync(manifestPath)) { console.log('No DESIGN_SYSTEM_MANIFEST.json found. Run design-recon first.'); process.exit(0); }
const m=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
console.log('Known DS components:', Object.keys(m.component_imports||{}).join(', ') || 'none');
console.log('Use this manifest to review component imports manually or extend this script for your stack.');
