# Research closure — Phases B1–B4 (development-only)

**Scope:** Azure Synthetic Predictive Maintenance. Five logical factories in the original v3 manifest, four development factories used for B1–B4. All numerical values below are from Colab outputs shared by the project owner. The private raw scored rows were not included in this public package.

## B1 — HGB feature ablation (4 development LOFO folds)

| Features | Mean PR-AUC | Minimum factory PR-AUC |
|---|---:|---:|
| Full (25) | 0.975604 | 0.925217 |
| Without maintenance recency | 0.776686 | 0.705921 |
| Sensors + error features | 0.776686 | 0.705921 |
| Sensor/history only | 0.244210 | 0.194293 |

**Caution:** “Without maintenance” and “Sensors + error features” are identical code feature sets, not independent experiments. Historical errors/maintenance add substantial predictive information; their presence does not automatically imply leakage, but may reflect synthetic maintenance-cycle patterns.

## B2 — Federated MLP versus LSTM

| Model | Mean PR-AUC | Worst fold | Standard deviation (8 values = 4 folds × 2 seeds) |
|---|---:|---:|---:|
| MLP | 0.573715 | 0.401261 | 0.122851 |
| LSTM | 0.577736 | 0.212891 | 0.218746 |

The LSTM improved PR-AUC for held-out factories 1–3 and suffered on factory 4. Fixed threshold 0.50 early-warning comparisons in this run are **not threshold-calibrated comparisons**.

## B4 — Federated MLP selected for integration (pilot only)

| Full-feature model | Mean PR-AUC | Worst fold | Standard deviation |
|---|---:|---:|---:|
| FedAvg MLP | **0.762308** | **0.742111** | **0.024211** |
| FedAvg LSTM | 0.730323 | 0.529216 | 0.137890 |

B4 pilot conditions: 4 development folds; train on 3 other factories each fold; 8 communication rounds, 6,000 training endpoints/client, seed 42, 25 features. Model selection follows robustness and early-warning performance, not average PR-AUC only.

At min 12-hour lead time with per-fold threshold chosen from other development folds under a predeclared 0.10 false alarms/machine-day budget on calibration folds:

| Metric | Full MLP | Full LSTM |
|---|---:|---:|
| Eligible events | 46 | 46 |
| Detected events | **40** | 36 |
| Event recall | **0.869565** | 0.782609 |
| False alerts | **27** | 55 |
| Observed false alarms/machine-day | **0.009794** | 0.019952 |

These are development metrics, **not a truly blind new site**. The folds used overlapping train sets and B4 had one seed. Cross-fold alert thresholds are not calibrated probabilities.

## Final engineering choice

Keep `Federated MLP (25→32→8→1), FedAvg, full 25 features` as the **frozen prediction architecture for integration**. Retain LSTM/HGB as explicit baselines. Do not attribute old v3 DP privacy accounting to B4. Current B4 records contain four separate out-of-factory predicted score sets; **no single global final checkpoint** was saved for B4.
