# FedKG-Maint Unified v3 — Final research run

Run ID: `unified_v3_final_20261025`
## Selection protocol
Four development-factory LOFO folds. Historical factory_5 is EXPLORATORY, not blind.

## LOFO Federated selection
| method   |   rounds |   mean_ap |   worst_factory_ap |    std_ap |   mean_brier |   robust_selection_score |
|:---------|---------:|----------:|-------------------:|----------:|-------------:|-------------------------:|
| FedAdam  |        6 |  0.371153 |           0.206601 | 0.129637  |    0.0500025 |                 0.305332 |
| FedAdam  |       12 |  0.542254 |           0.376632 | 0.164167  |    0.0249708 |                 0.476005 |
| FedAdam  |       18 |  0.550513 |           0.136484 | 0.307676  |    0.026803  |                 0.384901 |
| FedAvg   |        6 |  0.603238 |           0.520229 | 0.0725737 |    0.170605  |                 0.570035 |
| FedAvg   |       12 |  0.735465 |           0.70437  | 0.0476032 |    0.0563922 |                 0.723027 |
| FedAvg   |       18 |  0.776852 |           0.732529 | 0.047573  |    0.0258075 |                 0.759123 |
| FedProx  |        6 |  0.603438 |           0.515794 | 0.0806335 |    0.172849  |                 0.568381 |
| FedProx  |       12 |  0.729492 |           0.698413 | 0.0489156 |    0.0588495 |                 0.71706  |
| FedProx  |       18 |  0.775735 |           0.728331 | 0.0497933 |    0.0265677 |                 0.756773 |

Chosen: **FedAvg**, 18 rounds, OOF threshold 0.920404
## Classical HGB / LR LOFO diagnostics
| method    | feature_set         |   mean_ap |    std_ap |   worst_factory_ap |   mean_brier |   robust_score |
|:----------|:--------------------|----------:|----------:|-------------------:|-------------:|---------------:|
| hgb_local | full                |  0.938437 | 0.0405866 |           0.886833 |   0.00261401 |       0.920375 |
| hgb_local | no_maintenance      |  0.770449 | 0.0785643 |           0.702322 |   0.0056771  |       0.746605 |
| hgb_raw   | full                |  0.974883 | 0.0391851 |           0.916301 |   0.00128425 |       0.954379 |
| hgb_raw   | no_maintenance      |  0.805995 | 0.0672946 |           0.766965 |   0.00520345 |       0.792335 |
| hgb_raw   | sensor_errors       |  0.805995 | 0.0672946 |           0.766965 |   0.00520345 |       0.792335 |
| hgb_raw   | sensor_history_only |  0.249655 | 0.059866  |           0.185443 |   0.0139939  |       0.227181 |
| lr_local  | full                |  0.740853 | 0.0467891 |           0.674819 |   0.0300276  |       0.717741 |

## Historical exploratory factory_5
| model                                   |       ap |   pr_auc_ci_low |   pr_auc_ci_high |   event_recall |   false_alarms_per_machine_day |   alert_precision |
|:----------------------------------------|---------:|----------------:|-----------------:|---------------:|-------------------------------:|------------------:|
| HGB_PhysicalUnits_Robust                | 0.917152 |        0.787891 |         0.987652 |       1        |                    0.0043946   |          0.789474 |
| HGB_PhysicalUnits_Full                  | 0.917152 |        0.787891 |         0.987652 |       1        |                    0.0043946   |          0.789474 |
| MLP_FedAvg_seed42                       | 0.778693 |        0.685322 |         0.880691 |       0.983333 |                    0.0115358   |          0.58     |
| CentralizedMatchedMLP                   | 0.768539 |        0.67544  |         0.872002 |       0.9      |                    0.00631724  |          0.697368 |
| MLP_FedAvg_seed44                       | 0.761183 |        0.657773 |         0.871656 |       0.983333 |                    0.0145571   |          0.518182 |
| MLP_FedAvg_seed43                       | 0.76053  |        0.674868 |         0.853624 |       0.983333 |                    0.0140078   |          0.53211  |
| HGB_PhysicalUnits_NoMaintenance         | 0.680419 |        0.577426 |         0.82758  |       1        |                    0.0131838   |          0.555556 |
| LocalOnlyLR_Ensemble                    | 0.659176 |        0.546973 |         0.784974 |       0.983333 |                    0.0156558   |          0.504348 |
| record_dp_sgd_federated_mlp_one_release | 0.656414 |        0.537774 |         0.778281 |       0.966667 |                    0.0214237   |          0.413534 |
| LR_LocalScaled_Full                     | 0.63759  |        0.522373 |         0.773521 |       0.983333 |                    0.0167544   |          0.487395 |
| HGB_LocalScaled_Full                    | 0.548999 |        0.435183 |         0.657776 |       0.05     |                    0.000274662 |          0.75     |

## Research-scoped record-level DP-SGD
{
  "dp_validation_ap": 0.6808836661040643,
  "nonprivate_selected_development_temporal_ap": 0.8158960729764572,
  "dp_relative_utility": 0.8345225435638435,
  "illustrative_relative_utility_gate": 0.8,
  "meets_gate": true,
  "private_epsilon_max": 0.6226875671831649,
  "private_epsilon_cap": 10.0,
  "scope_note": "conditional preprocessed row privacy ONLY, not raw-record or client-level DP"
}
Privacy manifest: `v3_federated/reports/dp_release_manifest.json`.
**No end-to-end DP of Azure raw rows or local scaler stats. No client-level DP claim.**

## Type-shift stress (same Azure data)
{
  "experiment": "type_blocked_simulated_factory",
  "predeclared_manifest": "factory_manifest_type_shift_stress.csv",
  "result_status": "EXPLORATORY_SYNTHETIC_MODEL_TYPE_SHIFT",
  "features": [
    "volt",
    "rotate",
    "pressure",
    "vibration",
    "volt_past_mean_24h",
    "volt_past_std_24h",
    "volt_past_mean_7d",
    "volt_past_std_7d",
    "rotate_past_mean_24h",
    "rotate_past_std_24h",
    "rotate_past_mean_7d",
    "rotate_past_std_7d",
    "pressure_past_mean_24h",
    "pressure_past_std_24h",
    "pressure_past_mean_7d",
    "pressure_past_std_7d",
    "vibration_past_mean_24h",
    "vibration_past_std_24h",
    "vibration_past_mean_7d",
    "vibration_past_std_7d",
    "hours_since_last_error_log1p",
    "has_prior_error",
    "hours_since_last_maintenance_log1p",
    "past_observation_count_24h",
    "past_observation_count_7d"
  ],
  "hgb_params": {
    "max_iter": 90,
    "max_depth": 3,
    "learning_rate": 0.08,
    "l2_regularization": 0.2
  },
  "n_training": 557200,
  "n_validation": 68000,
  "n_test": 87380,
  "test_machine_models": {
    "model4": 20
  },
  "validation_ap": 0.9495744177849,
  "threshold": 0.43196983447890736,
  "heldout_results": {
    "prevalence": 0.016479743648432136,
    "ap": 0.9724452738238005,
    "roc_auc": 0.9997068206500659,
    "precision": 0.9455511288180611,
    "recall": 0.9888888888888889,
    "f1": 0.96673455532926,
    "fpr": 0.0009541540609727717,
    "event_recall": 1.0
  },
  "operational_metrics": {
    "alerts_total": 75,
    "true_alerts": 60,
    "false_alerts": 15,
    "alert_precision": 0.8,
    "false_alarms_per_machine_day": 0.004119935912108034,
    "median_true_alert_lead_time_hours": 24.0,
    "cooldown_hours": 24,
    "horizon_hours": 24
  },
  "limitations": [
    "Same underlying Azure source",
    "Not a new untouched physical site",
    "Not a fully federated stress comparison"
  ]
}

## RDF graph local partitions
| factory   |   machines |   daily_telemetry_nodes |   error_occurrences |   maintenance_events |   failure_records |   rdf_triples |   ttl_size_mb | graph_path                                                                                                                      |
|:----------|-----------:|------------------------:|--------------------:|---------------------:|------------------:|--------------:|--------------:|:--------------------------------------------------------------------------------------------------------------------------------|
| factory_1 |         20 |                    7320 |                 797 |                  650 |               191 |        162111 |         9.224 | /content/drive/MyDrive/FedKG-Maint/unified_runs/unified_v3_final_20261025/phase4_local_knowledge_graphs_v1/graphs/factory_1.ttl |
| factory_2 |         20 |                    7320 |                 796 |                  650 |               161 |        161956 |         9.21  | /content/drive/MyDrive/FedKG-Maint/unified_runs/unified_v3_final_20261025/phase4_local_knowledge_graphs_v1/graphs/factory_2.ttl |
| factory_3 |         20 |                    7320 |                 789 |                  655 |               147 |        161876 |         9.202 | /content/drive/MyDrive/FedKG-Maint/unified_runs/unified_v3_final_20261025/phase4_local_knowledge_graphs_v1/graphs/factory_3.ttl |
| factory_4 |         20 |                    7320 |                 717 |                  657 |               130 |        161441 |         9.16  | /content/drive/MyDrive/FedKG-Maint/unified_runs/unified_v3_final_20261025/phase4_local_knowledge_graphs_v1/graphs/factory_4.ttl |
| factory_5 |         20 |                    7320 |                 820 |                  674 |               132 |        162051 |         9.217 | /content/drive/MyDrive/FedKG-Maint/unified_runs/unified_v3_final_20261025/phase4_local_knowledge_graphs_v1/graphs/factory_5.ttl |

Graph checks: 8; risk-to-graph bindings: 16.

## Audit / limitations
19/19 integrity checks passed.
Private-mechanism epsilon cap: PASS.
Privacy utility gate: PASS.
- one simulated source dataset
- only four contributing silos
- factory_5 examined in previous experiments
- no true cryptographic secure aggregation
- no end-to-end differential privacy of raw preprocessing, feature normalizers or graphs
- NASA C-MAPSS remains outside Azure-only pipeline
- tuning and nonprivate baselines not included in private release