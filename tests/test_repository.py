import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestPublication(unittest.TestCase):
 def test_manifest_and_main_entry(self):
  meta=json.loads((ROOT/'notebook_source_manifest.json').read_text())
  paths={row['path'] for row in meta['files']}
  self.assertIn('notebooks/00_MASTER_Integration.ipynb',paths)
  self.assertIn('notebooks/core/01_Unified_v3_Phases_1_to_4.ipynb',paths)
  self.assertIn('notebooks/experiments/03_B4_Generalization_Pilot.ipynb',paths)
 def test_outputs_are_empty(self):
  meta=json.loads((ROOT/'notebook_source_manifest.json').read_text())
  for e in meta['files']:
   note=json.loads((ROOT/e['path']).read_text())
   for c in note['cells']:
    if c['cell_type']=='code':
     self.assertFalse(c.get('outputs',[]))
     self.assertIsNone(c.get('execution_count'))
if __name__=='__main__':unittest.main()
