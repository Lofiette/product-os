#!/usr/bin/env python3
from pathlib import Path
import ast, json, sys
root=Path(__file__).resolve().parents[1]
required=[
 'tools/cpt_migrate.py','migration/README.md','migration/schemas/migration-plan.schema.json',
 'migration/schemas/migration-receipt.schema.json','migration/LEGACY_DETECTION_RULES.json',
 'docs/MIGRATION_3X_TO_4X.md','docs/INSTALL_UPDATE_ROLLBACK.md','docs/PLATFORM_SUPPORT.md',
 'docs/TROUBLESHOOTING.md','tests/test_migration.py'
]
errors=[]
for rel in required:
 p=root/rel
 if not p.exists(): errors.append('missing '+rel)
for rel in ['tools/cpt_migrate.py','tests/test_migration.py']:
 p=root/rel
 if p.exists():
  try: ast.parse(p.read_text(encoding='utf-8'))
  except SyntaxError as e: errors.append(f'{rel}: {e}')
for rel in ['migration/schemas/migration-plan.schema.json','migration/schemas/migration-receipt.schema.json','migration/LEGACY_DETECTION_RULES.json']:
 p=root/rel
 if p.exists():
  try: json.loads(p.read_text(encoding='utf-8'))
  except Exception as e: errors.append(f'{rel}: {e}')
text='\n'.join((root/r).read_text(encoding='utf-8',errors='ignore') for r in required if (root/r).exists()).lower()
for forbidden in ['sova_design_system_kit','ai-web','платформа око']:
 if forbidden in text: errors.append('product-specific term: '+forbidden)
if errors:
 print('MIGRATION ASSET VALIDATION FAILED')
 print('\n'.join('- '+x for x in errors)); sys.exit(1)
print('MIGRATION ASSET VALIDATION PASSED')
