#!/usr/bin/env python3
"""Print the reported comparison snapshots included with the public repo."""
from pathlib import Path
import csv
root=Path(__file__).resolve().parents[1]/'results'/'reported'
for path in sorted(root.glob('*.csv')):
 print('\n###',path.name)
 with path.open(encoding='utf-8',newline='') as f:
  rows=list(csv.DictReader(f))
  for row in rows[:12]:
   print(' | '.join(f'{k}={v}' for k,v in row.items() if k not in {'validation_rows_sha256'}))
 if len(rows)>12:print(f'... ({len(rows)} total rows)')
