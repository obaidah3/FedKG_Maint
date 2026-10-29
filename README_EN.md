# FedKG-Maint — Azure Phases 1–5 (Research Repository)

Five-stage Azure PdM research repository: preprocessing, baselines, federated learning with conditional DP research comparisons, per-factory RDF knowledge graphs, and executed Groq API explanations with/without KG. Development model selection used B4 FedAvg MLP, which achieved mean PR-AUC 0.7623 (worst site 0.7421; pilot with one seed). The selected pilot has no unified all-client checkpoint and is not covered by the earlier v3 DP accounting.

Phase 5: 24/24 Groq explanations generated for 12 paired cases. Mean valid citation-ID coverage 99.24% with KG vs 93.93% without KG. A source-based AI-assisted review found numeric/date inaccuracies in several With-KG claims. Higher citation-ID coverage **does not** prove improved fidelity. Independent human evaluation is **not complete**. Raw responses and machine-history evidence are not in the GitHub package.

Main code: `notebooks/00_MASTER_Integration.ipynb`, `notebooks/core/01_Unified_v3_Phases_1_to_4.ipynb`, `notebooks/phase5/04_Phase5_Groq_KG_Explanations.ipynb`. B1–B4 stay under `notebooks/experiments/`.

NASA C-MAPSS RUL work remains unimplemented. Read `docs/RELEASE_STATUS.md`, `reports/PHASE5_FINAL_EXPLAINABILITY.md`, and `docs/PRIVACY_AND_PUBLICATION.md` before citing or publishing results.

**Original source evidence added:** 51 selected original small Drive reports and experiment configs, with per-file SHA-256 and verification script, under [`results/original_drive_reports/`](results/original_drive_reports/README.md). No raw source cases or full KG graphs are included.
