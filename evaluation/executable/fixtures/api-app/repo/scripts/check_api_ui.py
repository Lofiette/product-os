from pathlib import Path
text=(Path(__file__).resolve().parents[1]/'src/features/account/AccountForm.tsx').read_text()
assert 'Something went wrong' not in text
assert 'aria-live="polite"' in text
print('API UI CHECK PASS')
