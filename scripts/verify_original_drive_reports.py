#!/usr/bin/env python3
"""Verify original Drive report files match the user-supplied collection manifest."""
from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parents[1]
folder=root/'results'/'original_drive_reports'
manifest=json.loads((folder/'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest.get('file_count')==len(manifest['files'])==51, 'Unexpected manifest count'
seen=set()
for entry in manifest['files']:
    rel=Path(entry['path'])
    assert not rel.is_absolute() and '..' not in rel.parts, f'Unsafe path {rel}'
    assert str(rel) not in seen, f'Duplicate path {rel}'
    seen.add(str(rel))
    data=(folder/rel).read_bytes()
    assert len(data)==entry['bytes'], f'Size mismatch: {rel}'
    assert hashlib.sha256(data).hexdigest()==entry['sha256'], f'SHA256 mismatch: {rel}'
assert sum(p.is_file() for p in folder.rglob('*'))==53,'Unexpected extra files in original report collection'
print(f'PASS: {len(seen)} unchanged original report/config files, SHA256 and sizes verified.')
print('This checks source-package integrity, not accuracy of research claims.')
