# FedKG-Maint — Data preparation v3 final report

Generated (UTC): 2026-10-25T20:09:31+00:00

## Checklist

| Check | Status | Detail |
|---|---|---|
| DATA-1 raw files present with expected row counts | PASS | telemetry=876,100, errors=3,919, failures=761, maint=3,286, machines=100 |
| DATA-2 initial raw fingerprint baseline created | PASS | No earlier checksum manifest existed; subsequent runs will fail if any hash changes. |
| DQ-1 no missing values and no duplicate rows | PASS |  |
| DQ-2 hourly grid, identical coverage for all machines | PASS | 100 machines x 8,761 rows, 2015-01-01 06:00:00 -> 2016-01-01 06:00:00 |
| DQ-3 failure events align with telemetry timestamps | PASS | 761 failure rows |
| DQ-4 machine identifiers consistent across tables | PASS | 100 machines |
| L-1 label identical across three independent implementations | PASS | searchsorted == merge_asof on 876,100 rows; == brute force on 3,000 sampled rows |
| L-2 last 24 rows of every machine dropped (unobservable horizon) | PASS | 2,400 rows dropped in total |
| C-0 fixed partition quotas match the raw machine-model counts | PASS | observed={'model3': 35, 'model4': 32, 'model2': 17, 'model1': 16}; quota totals={'model1': 16, 'model2': 17, 'model3': 35, 'model4': 32} |
| C-1 five mixed-model factories x 20 machines; each machine assigned once | PASS | primary clients contain multiple models; factory_5 has at least three model types |
| S-1 24h purge gaps: no label window crosses train/validation/test boundary | PASS | train end + 24h=2015-10-19 10:00:00 < val start=2015-10-19 11:00:00; validation end + 24h=2015-11-24 20:00:00 < test start=2015-11-24 21:00: |
| S-2 held-out machines never appear in supervised development splits | PASS | 20 held-out machines isolated from train/validation/time-test rows |
| S-3 no duplicate (machine, timestamp) rows inside any evaluation split | PASS |  |
| S-4 late site test is a subset of post-calibration site test; all evaluation splits contain positives | PASS | test_site_full rows=87,380; late subset rows=17,480 |
| S-5 held-out calibration is earlier than and disjoint from all site-evaluation rows | PASS | calibration rows=87,360; eval starts=2015-07-02 06:00:00 |
| S-5 event table produced | PASS | 19 rows saved to split_event_table.csv |
| D-2 maintenance time semantics measured and documented | PASS | 97.6% of failure rows have a same-timestamp replacement of the same component |
| FE-0 every telemetry row has a prior maintenance record (has_prior_maintenance is constant, excluded) | PASS |  |
| FE-1 all 25 features finite, none constant in training | PASS | constant features: none |
| N-0 calibration artifact contains no target and no evaluation rows | PASS | 87,360 feature-only calibration rows; evaluation starts 2015-07-02 06:00:00 |
| N-1 six scalers fitted from allowed sources and saved | PASS | global + 4 local training factories + local held-out feature-only calibration |
| N-2 loader works for every split x policy x feature set; scaling behaves as specified | PASS | {'train': 557200, 'validation': 68000, 'test_time_late': 69920, 'test_site_late': 17480, 'test_site_full': 87380} |
| F-1 future perturbation leaves every tested feature vector unchanged | PASS | 1000 rows tested (200 per split), 0 changed |
| F-2 positive control: perturbing the past does change the features | PASS | 10/10 rows changed |
| F-3 scaler stats match permitted source rows; held-out calibration is label-free and disjoint | PASS | 6 scalers checked; calibration rows=87,360; overlap rows=0 |
| F-4 identical schema in every split; features match feature_groups.json; no id/target leaks into features | PASS | 25 features; no_maintenance set has 24 |

## Final evaluation splits

| Split | Rows | Machines | Positive rows | Positive rate % | Failure events |
|---|---:|---:|---:|---:|---:|
| train | 557,200 | 80 | 11,664 | 2.0933 | 491 |
| validation | 68,000 | 80 | 1,133 | 1.6662 | 48 |
| test_time_late | 69,920 | 80 | 1,377 | 1.9694 | 58 |
| test_site_late | 17,480 | 20 | 384 | 2.1968 | 16 |
| test_site_full | 87,380 | 20 | 1,440 | 1.648 | 60 |

## Held-out calibration

- Calibration cutoff: `2015-07-02 06:00:00`
- Rows: 87,360
- Target column present: `False`
- The held-out local scaler uses this feature-only file; evaluation rows begin at/after the cutoff.

## Problem → change → evidence

| Problem | Change | Evidence |
|---|---|---|
| Raw-data reproducibility | Compare SHA-256, byte size and row count with an immutable prior manifest; fail on mismatch | DATA-1, DATA-2 |
| Held-out calibration overlaps old site test | Use a feature-only calibration artifact and start site evaluation after the calibration cutoff | S-5, N-0, F-3 |
| Site/type confounding | Use mixed-model quotas for primary clients and save a separate model-blocked stress-test manifest | C-0, C-1, factory_partition_config.json |
| Label construction | Recompute the 24-hour label independently and test boundary handling | L-1, L-2 |
| Temporal leakage | Use 24-hour purge gaps, past-only features, future perturbation and a past-perturbation positive control | S-1, F-1, F-2 |
| Feature/schema integrity | Validate finite values, scaler source statistics, consistent schemas and exclusion of labels/IDs from features | FE-1, F-3, F-4 |
| Machine-type stress generalization | Save a model-blocked alternate manifest; it must be run as a separate evaluation scenario | factory_manifest_type_shift_stress.csv |

## Known limitations

1. The factories are simulated clients, not real factory records; this preprocessing notebook centralizes the raw tables to simulate the partition.
2. The primary partition uses mixed machine types with different quotas, reducing the old single-model held-out confounding but not proving generalization to a real site. A model-blocked stress-test manifest is saved separately and must be evaluated in a separate experiment.
3. The first 50% of the held-out timeline is used only for unsupervised local-scaler calibration. The feature-only artifact omits labels, and all site-evaluation rows are later than the calibration cutoff.
4. test_site_late is a subset of test_site_full; these results are nested, not independent samples. Confidence intervals should be computed by machine or distinct failure event, not by treating hourly rows as independent.
5. The data cover one year and each temporal split has a limited number of distinct failure events; per-factory and late-window metrics can be statistically fragile.
6. Positive rows are not independent: one failure can produce up to 24 consecutive positive rows. The effective sample size is closer to the number of distinct failure events.
7. Maintenance recency partly encodes time since the last failure because replacements may coincide with failures. It is past-only, included in 'full', and should be ablated using 'no_maintenance'.
8. Rolling windows are row-count based and rely on the verified regular hourly grid (DQ-2).
9. A global scaler is a centralized reference. The local scaler is an unsupervised adaptation policy; neither alone implements secure federated learning or a formal privacy guarantee.