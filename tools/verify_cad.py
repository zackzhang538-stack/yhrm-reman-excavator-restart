"""Verify that the retained STEP bytes match the source audit."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
audit = json.loads((ROOT / 'evidence/cad-origin-and-native-match.json').read_text())
parts = audit['source_parts']
assert len(parts) == 7
for part in parts:
    path = ROOT / part['asset']
    assert sha256(path.read_bytes()).hexdigest() == part['sha256'], path
    print('OK', path.name)
