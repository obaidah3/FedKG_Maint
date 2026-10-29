# How to use the integrated release

1. Keep your existing Google Drive `MyDrive/FedKG-Maint/` folder unchanged: `unified_runs/unified_v3_final_20261025/`, `unified_runs/phaseB_development_v1/` (optional reports), and `unified_runs/phaseB4_generalization_pilot_v1/` (24 saved experiments and predictions).
2. Upload `FedKG_Maint_MASTER_Integration_v1.ipynb` to Colab, mount Drive, and **Run all**. This does **not train any new ML model**, does not call an LLM, and does not modify the original run folders.
3. The integrated output appears under `MyDrive/FedKG-Maint/unified_runs/fedkg_master_integration_v1/`, specifically `reports/MASTER_CLOSURE.md` and `phase5_inputs/selected_MLP_KG_evidence_12_cases.json` and `phase5_inputs/matched_24_prompts_internal.jsonl`.
4. Review these outputs. The **next unfinished work is actual LLM evaluation** and, if required, NASA. No research-mode B4 rerun is required to merge the previous work.
5. Keep `source_archive/` as provenance only. There is no replacement of any original Notebook in Drive, nor a new blind test, nor a privacy release.

**Source artifact requirement:** The master links to generated v3 and B4 output **files** (parquet, CSV, `.npz`, TTL), not just original notebooks. It will stop with a descriptive assertion if any required output is absent. The package includes a small snapshot of the published B4 metrics for reading offline, **not** the scored observations themselves; those remain on your Drive.
