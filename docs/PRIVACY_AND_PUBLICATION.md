# Privacy, safe publication, and honest threat model

**Before setting this repository to public:** inspect the entire diff with `git status` / `git diff --cached --stat`; never commit raw machine records, API keys, access tokens, Google Drive exports, detailed internal model scores, or fitted RDF graphs unless you explicitly verified permission and release scope.

### Differential Privacy boundary

Unified v3 contains a **conditional record-level DP-SGD experiment** applied to a preprocessed feature table with a declared noise mechanism/accountant. The transformation from raw telemetry into the fixed table, local normalization, private labels, non-DP baselines, KG generation, and raw diagnostics are *outside that guarantee*. B4's newly trained FedAvg MLP/LSTM models are **not DP-protected**. A DP metric from another version cannot be attached to B4 results.

### Federated simulation boundary

The experiments run simulated clients in Colab memory; data are split into logical client partitions rather than isolated real factory computers. Do not claim production-grade secure aggregation or network-level data confidentiality.

### Evaluation boundary

- Factory 5 was examined in historical v1/v2/v3 experiments, so it is not a never-before-seen blind site.
- B1–B4 selection and evaluation use development factories 1–4, with non-IID mixes of machine models.
- Historical event features (errors and maintenance) may be especially informative in synthetic Azure. Strong scores must not be equated with causality or generality to real factories.
- One B4 seed and cross-fold evaluation do not measure industrial utility or statistical superiority.
- Event warning thresholds and observed FAR/recall belong to the specific evaluation protocol.

### Files intentionally excluded

`data/raw/`, raw Colab logs, `unified_runs`, actual score `.npz`, model checkpoints, scaler `.joblib`, raw experiment privacy diagnostics, full KG `.ttl` outputs, `.env`, credentials, original course handout PDF. Only publication-cleaned notebook code, reported summary tables and **51 selected small original report/config files** (including the shared ontology schema, NOT individual factory graphs) are included. Review the selected original reports before setting the repo public: some preserve Colab Drive paths and machine/model-level aggregate metrics.

### Copyright and licensing

This package does not assign a software license on the owner's behalf. If you want other people to reuse, modify, or redistribute your project, decide on a license and commit an appropriate `LICENSE` file. Dataset licenses and course handout rights are separate.
