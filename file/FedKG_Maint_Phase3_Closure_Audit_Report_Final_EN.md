# FedKG-Maint — Phase 3 Closure Audit Report

**Audit status: PASS for the defined Phase 3 v3 integrity, privacy-accounting, and utility screens.** This conclusion is limited to the current benchmark and the stated threat model.

## 1. Scope

This is a post-run audit of `FedKG_Maint_Phase3_Privacy_Utility_Fix_v3.ipynb`. It does not retrain models or tune hyperparameters. The test set `test_site_full` represents held-out `factory_5`, but it was used in earlier project experiments; it is not a new untouched external evaluation.

## 2. Final test results

The test set contains **87,380 rows**, **20 machines**, and a positive-row prevalence of **0.016480 (1.6480%)**. The three seeds were 42, 43, and 44.

| Method | Seed 42 PR-AUC | Seed 43 PR-AUC | Seed 44 PR-AUC | Mean PR-AUC | Sample SD |
|---|---:|---:|---:|---:|---:|
| DP-FedAvg-CompactLinear | 0.3146 | 0.3589 | 0.3040 | **0.3258** | 0.0291 |
| ClippedFedAvg | 0.2981 | 0.2941 | 0.2939 | 0.2954 | 0.0024 |
| FedAvg | 0.2981 | 0.2941 | 0.2939 | 0.2954 | 0.0024 |
| CentralCompactLinear | 0.3787 | 0.3776 | 0.3771 | 0.3778 | 0.0008 |

The saved prediction scores were re-evaluated against the saved split. The largest absolute difference between recomputed and recorded per-seed PR-AUC was approximately `1.11e-16`; the summary mean/SD differences were also below `1.11e-16` due to floating-point precision.

## 3. Paired machine-cluster bootstrap

The primary comparison is `DP-FedAvg-CompactLinear - ClippedFedAvg`. The bootstrap resampled the 20 held-out machines as clusters, preserved all rows within each sampled machine, paired the methods on the same sampled machines, and used **2,000 replicates**.

| Statistic | Result |
|---|---:|
| Mean DP-FedAvg PR-AUC | 0.325846 |
| Mean ClippedFedAvg PR-AUC | 0.295369 |
| Mean paired difference (DP minus clipped) | **+0.030477** |
| 95% machine-cluster bootstrap CI | **[0.018166, 0.041067]** |
| Bootstrap fraction with mean difference <= 0 | 0.0000 |

The 95% bootstrap interval is entirely above zero, which is benchmark-specific evidence that the observed mean PR-AUC difference favors DP-FedAvg for this set of trained models and these held-out machines. The bootstrap tail fraction is descriptive and **is not a formal p-value**. This interval is conditional on the trained models and does not capture all sources of training randomness or establish performance on unseen factories.

## 4. Privacy accounting

Selected configuration: **3 communication rounds**, **1 local epoch per round**, `clip_norm = 0.1`, `noise_multiplier = 1.0`, and `delta = 1e-5`. The study's predeclared cap was `epsilon <= 10`.

| Accountant / order grid | Epsilon |
|---|---:|
| Manual RDP conversion, original v3 order grid | 9.837642 |
| Manual RDP conversion, dense order grid | 9.811291 |
| Google `dp-accounting`, original v3 order grid | 9.087862 |
| Google `dp-accounting`, dense order grid | 9.009883 |

The original v3 value (`epsilon = 9.837642`) reproduces from the saved selection lock and remains below the study cap. The independent library values differ because the RDP-to-`(epsilon, delta)` conversion is not numerically identical; the audit no longer requires exact equality. In the completed run, all four values met the cap and the library values were no larger than the corresponding manual bounds.

The first import of `dp-accounting` initially raised `ModuleNotFoundError`; the notebook then installed the pinned package and successfully re-imported it. This was a recoverable setup event, not a final accounting failure. The corrected notebook records the initial import failure separately from any actual installation error.

**Privacy claim boundary:** the reported epsilon covers only the clipped/noised client-update mechanism under add/remove-one-client adjacency, a trusted server, a fixed denominator, full participation, and no subsampling amplification. Validation-based model selection, preprocessing statistics, evaluator access to raw data, and external diagnostic release are outside this bound. This is not end-to-end differential privacy.

## 5. Integrity checks

All **11 of 11** critical audit checks passed in the completed run:

1. The Phase 3 v3 selection lock exists and is readable.
2. All 12 saved prediction files align with the `factory_5` held-out test rows.
3. Recomputed per-seed PR-AUC matches the saved Phase 3 v3 values.
4. Recomputed summary means and standard deviations match the saved summary.
5. The stored epsilon reproduces from the original v3 RDP order grid.
6. The dense-order manual RDP result meets the study epsilon cap.
7. The independent `dp-accounting` cross-check meets the specified consistency and cap checks.
8. The predeclared mean-utility screen passes.
9. The predeclared descriptive seed-stability screen passes.
10. The paired machine-cluster bootstrap completes and returns a confidence interval above zero.
11. The saved selection lock declares validation-only selection and that the test data were not loaded before locking the selected configuration. This is a check of the saved protocol declaration, not cryptographic proof of execution order.

## 6. Decision and limitations

**Decision:** the Phase 3 v3 utility screens and the current benchmark integrity/accounting checks pass. The paired machine-cluster bootstrap interval is above zero, showing an observed DP-vs-clipped PR-AUC advantage on this benchmark.

Do not interpret this as proof of end-to-end differential privacy, broad external generalization, or real cryptographic secure aggregation. The earlier `SecureAggSim` is an arithmetic simulation only. Three seeds and 20 machines provide useful but limited evidence; additional independently held-out factories would be needed for stronger generalization claims.

## 7. Files written by the audit notebook

The notebook writes its machine-readable and human-readable reports under `phase3_closure_audit_v1/`:

- `reports/phase3_closure_audit_report.md`
- `reports/phase3_closure_audit_report.json`
- `results/paired_machine_bootstrap_dp_vs_clipped.csv`
- `results/prediction_ap_reproducibility.csv`
- `results/recomputed_test_ap_by_seed.csv`
- `results/summary_ap_reproducibility.csv`
- `results/phase3_closure_audit_checks.csv`
