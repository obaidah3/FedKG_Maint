# Original Google Drive Research Reports — Source Evidence

This directory contains **51 selected small files** exported from the user's original `MyDrive/FedKG-Maint/` research run folders, plus `MANIFEST.json` listing the original Drive-relative paths, sizes and SHA-256. Files are stored **byte-for-byte unchanged**; generated copies of scientific results are not substituted for these originals.

**Source verification:** Run `python scripts/verify_original_drive_reports.py` at repository root. It checks all 51 hashes and that no manifest file is missing. This verifies against the supplied manifest, not independent provenance or scientific reproducibility.

## Folders

| Folder | Contents |
|---|---|
| `unified_runs/unified_v3_final_20261025/` | Unified v3 audit/report, preprocessing, centralized baseline and federated/conditional-DP summaries; local RDF KG ontology/schema and aggregate graph checks |
| `unified_runs/phaseB_development_v1/` | Original B1/B2/B3 development metrics and closure report |
| `unified_runs/phaseB4_generalization_pilot_v1/` | B4 LOFO experimental results, event alert metrics, selection decisions and experiment lock |
| `unified_runs/phase5_groq_grounded_v1/` | Actual Phase 5 Groq run report, mechanical citation metrics and experiment schema/lock; **not raw prompts or generated answer texts** |
| `unified_runs/fedkg_master_integration_v1/` | Integration closure report |

### What is intentionally absent

No raw Azure CSV, processed machine-level Parquet, per-factory KG graph (`factory_*.ttl`), B4 `.npz` scores, trained models, Groq API credentials, raw LLM case responses, private reviewer sheets or review mapping keys. Absolute `/content/drive/MyDrive/` paths in a few original report fields are preserved as recorded, and do **not** mean the runtime data is included.

### How to interpret the release

- B4 development selection is a **one-seed pilot**, not the final deployment model nor a DP-protected checkpoint.
- Source Phase 5 report correctly says **24/24 generated** but **human review pending**; separately published AI-assisted review results are provisional.
- Factory 5 is historically accessed, not a never-before-seen blind site.
- NASA C-MAPSS not implemented in this Azure release.

Not every report includes original data sufficient to recompute every score. Source filenames may not match the names of `results/reported/` tables, which are earlier publication summaries.
