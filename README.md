# FedKG-Maint — Federated Predictive Maintenance + Knowledge Graph Explanations

**Azure research release through Phases 1–5 (28 October 2026).**

This repository combines Azure PdM preprocessing, centralized baselines, federated learning and conditional DP studies, local RDF knowledge graphs, B1–B4 model-selection experiments, and a completed **Groq API comparison of 12 matched cases with/without knowledge-graph context**.

> **Research rather than production software.** Architecture selection was based on development data. No final four-client retrained deployment checkpoint exists for B4, earlier DP guarantees do not apply to its MLP, and NASA C-MAPSS required by the original brief is not implemented here.

## Main notebooks

| Notebook | Purpose | Re-run for documentation? |
|---|---|---|
| [`00_MASTER_Integration`](notebooks/00_MASTER_Integration.ipynb) | Read-only merge of v3 and B4, KG evidence preparation | Not necessary if prior run outputs exist |
| [`01_Unified_v3_Phases_1_to_4`](notebooks/core/01_Unified_v3_Phases_1_to_4.ipynb) | Original executed Azure/FL/DP/KG source | No |
| [`02_B1_B3_Feature_and_Temporal_FL`](notebooks/experiments/02_B1_B3_Feature_and_Temporal_FL.ipynb) | Feature ablation and federated MLP/LSTM comparison | No |
| [`03_B4_Generalization_Pilot`](notebooks/experiments/03_B4_Generalization_Pilot.ipynb) | Pilot selection of robust MLP | No |
| [`04_Phase5_Groq_KG_Explanations`](notebooks/phase5/04_Phase5_Groq_KG_Explanations.ipynb) | Groq LLM paired explanations, automated citation checks | No: 24/24 calls already saved to Drive |

Only the `04_Phase5_...` notebook needs Groq API access **when generating new answers**. It reads `GROQ_API_KEY` from environment / Colab Secrets or a hidden prompt, never a committed literal. Keep the old response files on Drive if continuing an interrupted run: it resumes cached responses.

## Documented results (development experiments)

| Study | Metric | Reported result |
|---|---|---:|
| B1 HGB full-feature Centralized baseline | Mean PR-AUC | 0.975604 |
| B4 FedAvg MLP full-feature, one seed | Mean PR-AUC | 0.762308 |
| B4 MLP across development factories | Worst-factory PR-AUC | 0.742111 |
| B4 early warning, 12h minimum lead | Events detected | 40/46 |
| Phase 5, without KG | Citation-ID coverage | 93.93% |
| Phase 5, with KG | Citation-ID coverage | 99.24% |

The 12-case explainability audit also found **source-level numeric/date errors** in some With-KG responses, despite syntactically valid citation IDs. An independent human assessment is still missing. See [`reports/PHASE5_FINAL_EXPLAINABILITY.md`](reports/PHASE5_FINAL_EXPLAINABILITY.md).

## Repository folders

`notebooks/` — main code, archived variants in `archive/legacy_notebooks/`.  
`results/reported/` — prior research summary tables.  
`results/original_drive_reports/` — **51 original Drive research reports/configs**, preserved byte-for-byte with SHA-256 manifest; excludes private individual records and large artifacts.  
`reports/` — model selection and Phase 5 evaluation.  
`docs/` — architecture, original requirements, reproducibility, and publication limitations.  
`scripts/` and `tests/` — static validation.

### Data and reproducibility

The notebooks read prior Colab runtime files in `/content/drive/MyDrive/FedKG-Maint/`. GitHub includes **51 original small research report/config files** but **no 1+ GB Google Drive runtime data**, factory-level graphs, raw Groq response payloads, or saved internal predictions. Original dataset access and saved v3/B4 runtime artifacts are necessary to reproduce individual outputs. Static tests confirm package integrity, not research reproducibility. Original report integrity is checked with `python scripts/verify_original_drive_reports.py`; see [`source report README`](results/original_drive_reports/README.md).

**Remaining scope:** NASA C-MAPSS RUL benchmark; independent human evaluation if required by course; new consolidated B4 model/private deployment if deployment is later required. These limitations are documented and should not be silently marked complete.

See [`docs/RELEASE_STATUS.md`](docs/RELEASE_STATUS.md), [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) and [`UPLOAD_TO_GITHUB_AR.md`](UPLOAD_TO_GITHUB_AR.md). This archive is ready for manual inspection and GitHub upload; no GitHub upload action has been performed by the assistant.
