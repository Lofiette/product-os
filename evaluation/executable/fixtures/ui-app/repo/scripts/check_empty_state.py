from pathlib import Path
root=Path(__file__).resolve().parents[1]
text=(root/'src/features/editor/EmptyState.tsx').read_text()
assert 'from "../../design-system/Button"' in text
assert '<Button' in text
assert '<button' not in text
print('EMPTY STATE DS CHECK PASS')
