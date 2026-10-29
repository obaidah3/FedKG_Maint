#!/usr/bin/env python3
"""Static publication integrity checker; does not run expensive Colab models."""
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'notebook_source_manifest.json').read_text(encoding='utf-8'))
assert manifest['outputs_stripped'] is True
assert len(manifest['files'])>=8
risks={
 'OpenAI key':re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
 'GitHub classic token':re.compile(r'gh[pousr]_[a-zA-Z0-9]{25,}'),
 'GitHub fine-grained token':re.compile(r'github_pat_[a-zA-Z0-9_]{30,}'),
 'Google API key':re.compile(r'AIza[A-Za-z0-9_-]{30,}'),
 'private key':re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),
}
seen=set();count=0
for e in manifest['files']:
 p=ROOT/e['path']
 assert p.is_file(),f'Missing: {p}'
 assert e['path'] not in seen
 seen.add(e['path'])
 raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e['publication_sha256'],f'Manifest checksum mismatch: {p}'
 note=json.loads(raw)
 assert note['nbformat']==4 and isinstance(note['cells'],list)
 for c in note['cells']:
  if c['cell_type']=='code':
   assert c.get('outputs',[])==[],f'Output still committed in {p}'
   assert c.get('execution_count') is None,f'Executed code cell committed: {p}'
 for desc,rx in risks.items():
  assert not rx.search(raw.decode('utf-8')),f'{desc} in {p}'
 count+=1
for rel in ['README.md','docs/PRIVACY_AND_PUBLICATION.md','reports/PHASE_B_FINDINGS.md','results/reported/B4_model_performance_reported.csv']:
 assert (ROOT/rel).exists(),f'Missing referenced file: {rel}'
for forbidden in ['data/raw','unified_runs','secrets']:
 assert not (ROOT/forbidden).exists(),f'Private directory unexpectedly present: {forbidden}'

# Original research evidence package must be present and valid.
import subprocess
subprocess.run([sys.executable, str(ROOT/'scripts'/'verify_original_drive_reports.py')],check=True)
print(f'PASS: {count} notebooks, SHA256, clean outputs, obvious credential-pattern checks, main docs and 51 original Drive research files.')
print('Reminder: this is a static packaging check, NOT a scientific or secret-scanning guarantee.')
