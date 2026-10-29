# FedKG-Maint — Phase 4/5 Runbook

## Current decision
Phase 3 LocalNorm implementation checks passed (9/9); mean utility and the declared three-seed stability screens passed. Report epsilon only for the client-update channel (epsilon≈9.8376, delta=1e-5), not as end-to-end DP. DP seed spread remains high, and a paired significance test has not been run.

## Run order
1. Open `FedKG_Maint_Phase4_Local_Knowledge_Graphs_v1.ipynb` in Google Colab. It reads `MyDrive/FedKG-Maint/data/raw/` and the authoritative Phase 1 client mapping in `prep_v3/fedkg_data.py`. Run all cells.
2. Inspect `phase4_local_knowledge_graphs_v1/reports/phase4_kg_build_report.md` and confirm every structural check passed. Main deliverable: `ontology/fedkg_shared_ontology.ttl` plus `graphs/factory_1.ttl` through `graphs/factory_5.ttl`.
3. Open `FedKG_Maint_Phase5_KG_Grounded_LLM_Explanations_v1.ipynb`. It expects Phase 3 seed-42 predictions and Phase 4 graphs. Run all cells with `RUN_LLM_EXPERIMENT=False` first to validate case construction and time-filtered evidence packs.
4. To actually call an LLM, add `OPENAI_API_KEY` using Colab Secrets (never paste the key into the notebook), optionally set `OPENAI_MODEL` and `OPENAI_BASE_URL`, and change `RUN_LLM_EXPERIMENT = True` in the API-config cell. It will make up to 24 calls (12 cases with and without KG). Confirm API access/cost first.
5. Review `phase5_kg_llm_explanations_v1/reports/human_evaluation_template.csv`; citation-ID validity alone is not a semantic factuality score.

## Interpretation cautions
- KG facts represent source records and temporal co-occurrence, not proven causation.
- Phase 4 simulates five logically separated local graphs in one Colab process; this does not prove physical raw-data isolation.
- Phase 5 filters event facts at or before each prediction timestamp and uses only completed prior-day telemetry aggregates to avoid same-day aggregation leakage.
- The local-normalization held-out site uses earlier unlabeled calibration data, so it is unsupervised site adaptation, not strict zero-shot normalization.
- The benchmark test set was used in earlier project experiments; do not call it a new untouched external replication.
