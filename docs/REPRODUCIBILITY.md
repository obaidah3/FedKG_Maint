# Reproducibility and Google Colab run order

## Zero-new-training reuse

1. Confirm the following folders exist in **your Google Drive** (not automatically downloadable from this GitHub repo):
   - `MyDrive/FedKG-Maint/unified_runs/unified_v3_final_20261025/`
   - `MyDrive/FedKG-Maint/unified_runs/phaseB4_generalization_pilot_v1/`
2. Open `notebooks/00_MASTER_Integration.ipynb` in Google Colab; connect Drive and run cells in order. It expects the original v3 `prep_v3/processed/*.parquet`, factory manifests, `v3_federated`, KG RDF graph files, and B4 `predictions/*.npz` / locks.
3. Output destination: `MyDrive/FedKG-Maint/unified_runs/fedkg_master_integration_v1/`.
4. The master **does not** retrain the selected FL model, does not spend API tokens, and does not claim newly evaluated KG explanations. It prepares 12 scored-evidence cases/24 paired prompts for later Phase 5.

## Historical code reproduction (expensive; OPTIONAL)

`notebooks/core/01_Unified_v3_Phases_1_to_4.ipynb` is the standalone original Azure implementation. It expects the five Azure CSVs under `MyDrive/FedKG-Maint/data/raw/`, or its documented KaggleHub fallback. Historical B1/B4 notebooks depend on v3 generated features and scalers. Do not execute historical notebooks merely to check this repository or to publish the reported results.

## Dataset availability

- Azure Predictive Maintenance: get the five source CSVs from their original publicly hosted dataset provider; do not commit them unless you check redistribution rights. Expected names: `PdM_telemetry.csv`, `PdM_errors.csv`, `PdM_maint.csv`, `PdM_failures.csv`, `PdM_machines.csv`.
- NASA C-MAPSS: official NASA PCoE repository (<https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/>). **No NASA RUL evaluation in this release.**

## Integrity and provenance

Notebooks in GitHub are **cleaned for publication**: code and Markdown are retained, saved execution counts and stdout/outputs removed. `docs/NOTEBOOK_INVENTORY.md` and `notebook_source_manifest.json` contain paths and SHA256 of originals and published variants. This stripping makes files easier to review and prevents accidental publication of private Colab outputs. It does **not** alter algorithmic source code.

`python scripts/validate_repo.py` checks notebook JSON/nbformat, missing notebooks, publication outputs, and indicative credential patterns. It does not establish numerical correctness of the scientific results. `python scripts/show_results.py` prints included summaries.

## Original Drive result provenance (release addition)

`results/original_drive_reports/` preserves 51 user-exported original small reports/configs unchanged, with byte count and SHA-256 in `MANIFEST.json`. Run `python scripts/verify_original_drive_reports.py` to verify this release against that manifest. The original reports are research evidence but **do not** substitute for the private Drive datasets, `.npz` prediction arrays or experiment environments needed for full numerical reproduction.
