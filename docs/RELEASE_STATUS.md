# FedKG-Maint status — 28 October 2026

| Component | Status | Research boundary |
|---|---|---|
| Azure data prep and features | Executed (Unified v3) | Simulated non-IID factory splits |
| Centralized HGB baselines | Executed | Not a federated predictor |
| Federated FedAvg/FedProx/FedAdam | Executed in v3 | Versions have different protocols |
| Earlier DP-SGD / privacy analyses | Executed research comparators | Fixed preprocessed-row-level conditional scope; NOT B4 privacy |
| Local RDF KGs, 5 factories | Built & tested | Large raw TTL artifacts on Drive, not public ZIP |
| B1–B3 | Executed | Development experiments |
| B4 pilot | Executed 24 runs | One seed, 4 held-out dev factories |
| Model architecture selection | FedAvg MLP engineering choice | No consolidated B4 all-factory checkpoint |
| Master integration | Run outputs evidenced on Drive tree | Not a fresh trained/deployed model |
| Groq Phase 5 generation | **Complete: 24/24 outputs** | 12 matched development cases only |
| Phase 5 mechanical citation audit | **Complete** | ID validity != factual fidelity |
| Phase 5 AI-assisted source review | **Complete, provisional** | Not an independent human assessor |
| Independent human ratings | **Pending / not supplied** | Original report lists 0/24 reviewed |
| NASA C-MAPSS RUL | **Not implemented** | Original assignment requirement remains open |

Primary Phase 5 report: `reports/PHASE5_FINAL_EXPLAINABILITY.md`; source result aggregates: `results/reported/`.

This is a publishable **research-code snapshot**, not a fully compliant NASA-inclusive graduation submission or industrially deployed private AI product.

**Evidence package update (29 October 2026):** 51 original Drive report/config files have been added under `results/original_drive_reports/`, alongside their original SHA-256 manifest. This does not change model results or incomplete-work statuses listed above.
