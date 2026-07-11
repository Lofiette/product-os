from pathlib import Path
root=Path(__file__).resolve().parents[1]
violations=[]
for path in (root/'src').rglob('*.tsx'):
    if 'design-system' in path.parts:
        continue
    text=path.read_text()
    if '<button' in text:
        violations.append(str(path.relative_to(root)))
if violations:
    raise SystemExit('raw buttons: '+', '.join(violations))
print('UI CHECK PASS')
