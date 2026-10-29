# FedKG-Maint — Azure-Only Requirements and Pipeline Audit

**Audit scope:** the user's approved Azure-only scope; NASA C-MAPSS is excluded from this implementation plan. This report reviews the four uploaded notebooks and their recorded execution outputs. It does not claim to have independently accessed the user's Google Drive or rerun the original data pipeline in this runtime.

## Executive decision

The uploaded preparation notebook records successful data-quality, target-construction, partition, split, scaler-source, and leakage/integrity checks. The Phase 2 notebook records successful baseline checks and includes both global and per-factory local-normalization comparisons. The Phase 3 v3 privacy repair and its closure audit reproduce the previously reported results.

**Blocking compliance gap:** the selected Phase 3 privacy-utility run loads train, validation, and test data with `policy="global"`. The project specification says normalization statistics must be computed locally inside each factory. Therefore, the existing Phase 3 v3 and its closure audit are internally reproducible for the *global-scaler experiment*, but they do not yet establish final compliance of the primary federated privacy result with the local-normalization requirement.

A separate local-normalization run is prepared as a new experiment. Its results must be generated in Colab before they can replace or supplement the global-scaler results in the final report. No results are asserted for that new run here.

## 1. Data preparation findings

### Verified in the recorded Phase 1 v3 run

- Raw Azure file counts: telemetry 876,100; errors 3,919; failures 761; maintenance 3,286; machines 100. Raw SHA-256 fingerprints matched the stored reference manifest.
- The recorded data-quality checks passed: no missing values or duplicate rows in the five tables; 100 machines with 8,761 hourly rows each; failure events aligned with telemetry; identifiers were consistent.
- The 24-hour target was compared across three implementations. The recorded checks passed, and the last 24 rows per machine (2,400 rows total) were dropped because their full future horizon was not observable.
- After this horizon exclusion: 873,700 candidate rows, 17,184 positive rows, and a positive-row rate of 1.9668%.
- The primary simulated partition has five factories and 20 machines per factory. Its per-client model counts are:

| Factory | model1 | model2 | model3 | model4 | mean machine age |
|---|---:|---:|---:|---:|---:|
| factory_1 | 8 | 4 | 4 | 4 | 13.4 |
| factory_2 | 4 | 7 | 5 | 4 | 10.8 |
| factory_3 | 2 | 3 | 10 | 5 | 10.8 |
| factory_4 | 1 | 2 | 8 | 9 | 10.2 |
| factory_5 | 1 | 1 | 8 | 10 | 11.4 |

The model-mix is intentionally non-IID, while every primary client has multiple machine models. The notebook also saves a model-blocked stress-test manifest.
- The recorded scaler-source checks passed for six scalers: one pooled global scaler, one local scaler for each of factories 1–4, and a factory_5 scaler fitted only to 87,360 earlier feature-only calibration rows. Those rows had no target column and did not overlap the site-evaluation rows.
- The recorded leakage/integrity tests passed: future perturbations did not change sampled past feature vectors; past perturbations changed features in the positive control; scaler statistics matched permitted source rows; and all splits shared the expected schema without IDs or target leakage into the feature matrix.

### Important caveats

1. The factory partition is simulated from one Azure dataset, not collected from five physically separate factories. The Phase 1 notebook explicitly notes that raw data are centralized in the preprocessing process. The simulation is useful for methodology, but it is not evidence of enforced data isolation in a deployed distributed system.
2. The primary `test_site_full` contains 87,380 rows / 20 held-out machines / 60 distinct failure events and begins at 2015-07-02. The training data for factories 1–4 extend to 2015-10-18. Therefore, `test_site_full` tests held-out-site generalization but is not strictly forward-in-time across factories. The stricter site-plus-time subset `test_site_late` has only 17,480 rows and 16 distinct failure events, so its metrics are statistically fragile.
3. Maintenance records often coincide with replacement events: the Phase 1 run records same-component maintenance at the failure timestamp for 97.63% of failure rows. The maintenance-recency feature is strictly past-only, so it is not a direct future leak, but it can act as a proxy for elapsed time since a prior failure. Document this interpretation in the report.
4. For factory_5, the local scaler uses the first half of the site's timeline as **unlabeled calibration**. This is unsupervised site adaptation, not strict zero-shot deployment. Keep that distinction explicit.

## 2. Normalization compliance

Phase 1 creates both policies:

- `global`: one `StandardScaler` fitted on pooled supervised training rows from factories 1–4.
- `local`: a distinct scaler fitted on each of factories 1–4's own training rows, while factory_5 uses its earlier feature-only calibration window.

Phase 2 evaluates both policies and correctly stores centralized references per feature set and policy. In its recorded primary `test_site_full` readout, `hgb|full|global` reached PR-AUC 0.925 [0.799, 0.993], whereas `hgb|full|local` reached 0.396 [0.282, 0.510]. These are policy-specific baselines and should not be mixed as if they were the same preprocessing protocol.

**However, Phase 3 Privacy Utility Fix v3 loads all three splits with `policy="global"`.** The Phase 3 closure audit then audits predictions created by that global-scaler experiment. Its 11/11 checks validate reproducibility, the configured scoped epsilon calculation, and utility comparisons; they do not check that the primary federated run used local normalization.

**Required corrective action:** run a separate Phase 3 privacy/utility experiment using `policy="local"` for train, validation, and test; save to a separate output directory; lock hyperparameters on validation only; then report the resulting numbers separately. Do not overwrite or relabel the existing global-policy results. Do not choose settings using the already-reused test set.

A local-normalization variant notebook is provided separately. It is a code change only; it has not been run on the user's Google Drive data, and its outputs must not be treated as results until it is run.

## 3. Phase 2 and Phase 3 evaluation findings

### Phase 2

- The recorded Phase 2 notebook completed with its internal checks passing.
- It includes both global and local normalization policies, `full` and `no_maintenance` feature sets, centralized references, heuristic references, validation-based threshold/model selection, confidence intervals, and paired comparisons.
- The main site test and its subsets are not independent replications: `test_site_post` and `test_site_late` are nested subsets of `test_site_full`.
- The Phase 2 notebook records 40 paired comparisons without multiplicity correction. Treat individual comparison flags as exploratory and emphasize predeclared contrasts.

### Phase 3 v3 and its closure audit

The uploaded Phase 3 privacy repair records the selected configuration as `local_epochs=1`, `clip_norm=0.1`, `noise_multiplier=1.0`, and 3 rounds. It uses 7 compact features / 8 parameters and uses `policy="global"` for train, validation, and test.

The recorded closure-audit results are reproducible: 87,380 test rows, 20 held-out machines, and all 12 saved prediction files aligned to the same test rows. Mean test PR-AUC is 0.325846 for DP-FedAvg-CompactLinear, 0.295369 for ClippedFedAvg, and 0.377797 for CentralCompactLinear. The paired machine-cluster bootstrap difference is +0.030477 with 95% CI [0.018166, 0.041067]. This is benchmark-specific evidence conditional on the trained models and the 20 machines, not a proof of generalization to new factories.

Privacy-accounting values recorded by the audit are:

| Calculation | Epsilon at delta = 1e-5 |
|---|---:|
| Manual RDP, v3 order grid | 9.837642 |
| Manual RDP, dense order grid | 9.811291 |
| `dp-accounting`, v3 order grid | 9.087862 |
| `dp-accounting`, dense order grid | 9.009883 |

All four values are below the project's experimental cap of epsilon <= 10. The declared bound covers only the clipped/noised client-update channel under add/remove-one client adjacency, a trusted server, a fixed denominator, full participation, and no subsampling amplification. It excludes preprocessing statistics, validation-based model selection, raw-data access by the evaluator, and external diagnostics. It is not end-to-end DP. The audit's 11/11 PASS result applies to the existing global-normalization run; it does not close the local-normalization compliance gap above.

The simulated `SecureAggSim` from prior work is arithmetic cancellation, not cryptographic Secure Aggregation. The uploaded project brief only requires at least one privacy mechanism, and DP has been implemented; real cryptographic secure aggregation is an additional requirement only if the supervisor explicitly requires it.

## 4. Requirements status for the Azure-only scope

| Requirement | Current evidence | Status |
|---|---|---|
| Azure data cleaning, target, feature construction, and integrity checks | Phase 1 recorded checks passed | **Pass, based on recorded run** |
| Non-IID factory simulation and held-out factory | Five 20-machine clients, model quotas, held-out factory_5 | **Pass as simulation; limited external validity** |
| Local normalization for the primary federated privacy model | Phase 1 supports local; Phase 3 v3 uses global | **Open / blocking** |
| Centralized baseline comparisons | Phase 2 runs global and local policies; compact v3 central baseline is policy-matched to global | **Partial; rerun matched comparison under local policy** |
| Two FL strategies vs local-only and centralized references | Prior Phase 3 contains FedAvg/FedProx and LocalOnly, but the compact privacy repair is a different 7-feature architecture | **Needs a consolidated, like-for-like results table** |
| Privacy-utility analysis | DP vs clipped baseline and scoped accountant audited | **Pass for existing global-policy experiment; repeat under local policy** |
| Communication cost and effects of client count / heterogeneity | Not demonstrated by the uploaded repair/audit notebooks | **Open** |
| Maintenance Knowledge Graph and local graphs with shared ontology | Not present in uploaded notebooks | **Not started** |
| LLM-grounded explanations and comparison with/without KG | Not present in uploaded notebooks | **Not started** |
| Explanation correctness / hallucination evaluation | Not present | **Not started** |
| Ablations without privacy, without KG, without LLM; multi-run/statistical analysis | Some privacy/maintenance ablations and a paired bootstrap exist, but no KG/LLM ablations yet | **Partial** |
| Integrated system, final report and reproducibility package | Component notebooks and audit reports exist | **Open** |

## 5. Recommended execution order

1. Run the prepared local-normalization Phase 3 experiment in Colab; preserve the existing global-policy run as a separate baseline and do not use test results for tuning.
2. Compare the local-normalized DP, clipped/no-noise, ordinary FedAvg, centralized compact, and the existing local-only baseline where architectures/features permit. Make comparison groups explicit; do not compare unmatched architectures as if they were controlled ablations.
3. Freeze the Azure preprocessing protocol and split definitions, and include both `test_site_full` and the small strict site-time subset with the event-count caveat.
4. Build the shared maintenance ontology and one local graph per simulated factory, with provenance/timestamps and no future failure facts in explanations.
5. Build the LLM retrieval/explanation layer, then evaluate grounded vs ungrounded explanations for factual correctness and hallucination.
6. Run required ablations, communication-cost and heterogeneity experiments, followed by integrated evaluation and report preparation.

## Final conclusion

Phase 1's recorded preprocessing checks and Phase 2's recorded baseline checks passed. Phase 3 v3's current closure audit also passed, but it audits a global-normalization experiment. Because the project requires local normalization, **the main remaining technical gate before treating the privacy result as fully aligned to the stated federated protocol is a validation-selected local-normalization Phase 3 run and policy-matched comparison**. After that, the major unimplemented requirements are the Maintenance Knowledge Graph, LLM-based grounded explanations, and their evaluation/ablations.
