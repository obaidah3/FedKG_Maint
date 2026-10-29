# FedKG-Maint · B4 Cross-Factory Generalization Report

**Experiment mode:** pilot · **Model runs:** 24
**Factory 5:** NOT read or used. **Privacy:** new models are non-DP.

## Model performance (development LOFO)
| variant             | architecture   |   mean_ap |   worst_fold_ap |   sd_ap |   mean_roc_auc |   robust_score |
|:--------------------|:---------------|----------:|----------------:|--------:|---------------:|---------------:|
| full                | LSTM           |    0.7303 |          0.5292 |  0.1379 |         0.9935 |         0.6499 |
| full                | MLP            |    0.7623 |          0.7421 |  0.0242 |         0.9938 |         0.7542 |
| no_maintenance      | LSTM           |    0.6057 |          0.3670 |  0.1611 |         0.9894 |         0.5102 |
| no_maintenance      | MLP            |    0.6136 |          0.5686 |  0.0409 |         0.9894 |         0.5956 |
| sensor_history_only | LSTM           |    0.2425 |          0.1271 |  0.1147 |         0.9677 |         0.1964 |
| sensor_history_only | MLP            |    0.2812 |          0.1856 |  0.0783 |         0.9654 |         0.2429 |

## Paired improvement (LSTM minus MLP)
| fold      | variant             |   seed |   LSTM |    MLP |   LSTM_minus_MLP |
|:----------|:--------------------|-------:|-------:|-------:|-----------------:|
| factory_1 | full                |     42 | 0.8422 | 0.7964 |           0.0459 |
| factory_1 | no_maintenance      |     42 | 0.7119 | 0.6564 |           0.0555 |
| factory_1 | sensor_history_only |     42 | 0.3167 | 0.3741 |          -0.0574 |
| factory_2 | full                |     42 | 0.7680 | 0.7421 |           0.0259 |
| factory_2 | no_maintenance      |     42 | 0.6524 | 0.5686 |           0.0838 |
| factory_2 | sensor_history_only |     42 | 0.3627 | 0.3002 |           0.0624 |
| factory_3 | full                |     42 | 0.7818 | 0.7623 |           0.0195 |
| factory_3 | no_maintenance      |     42 | 0.6915 | 0.5908 |           0.1007 |
| factory_3 | sensor_history_only |     42 | 0.1637 | 0.1856 |          -0.0220 |
| factory_4 | full                |     42 | 0.5292 | 0.7485 |          -0.2192 |
| factory_4 | no_maintenance      |     42 | 0.3670 | 0.6388 |          -0.2718 |
| factory_4 | sensor_history_only |     42 | 0.1271 | 0.2647 |          -0.1376 |

## Event recall at cross-fold budgeted false alarms
| variant             | architecture   |   mean_test_far |   mean_test_event_recall |   min_test_event_recall |   total_detected_events |   total_eligible_events |   total_false_alerts |   total_machine_days |   pooled_event_recall |   pooled_far |
|:--------------------|:---------------|----------------:|-------------------------:|------------------------:|------------------------:|------------------------:|---------------------:|---------------------:|----------------------:|-------------:|
| full                | LSTM           |          0.0200 |                   0.7740 |                  0.7143 |                      36 |                      46 |                   55 |            2756.6667 |                0.7826 |       0.0200 |
| full                | MLP            |          0.0098 |                   0.8990 |                  0.7500 |                      40 |                      46 |                   27 |            2756.6667 |                0.8696 |       0.0098 |
| no_maintenance      | LSTM           |          0.0341 |                   0.8437 |                  0.7143 |                      40 |                      46 |                   94 |            2756.6667 |                0.8696 |       0.0341 |
| no_maintenance      | MLP            |          0.0116 |                   0.8954 |                  0.7692 |                      40 |                      46 |                   32 |            2756.6667 |                0.8696 |       0.0116 |
| sensor_history_only | LSTM           |          0.0649 |                   0.4385 |                  0.3077 |                      19 |                      46 |                  179 |            2756.6667 |                0.4130 |       0.0649 |
| sensor_history_only | MLP            |          0.0802 |                   0.3484 |                  0.2857 |                      17 |                      46 |                  221 |            2756.6667 |                0.3696 |       0.0802 |

## Factory profiles
| factory   |   machines |   train_rows |   val_rows |   train_failure_24h_prevalence |   val_failure_24h_prevalence |   distinct_failure_events_all_source_period |   model_mix_model1 |   model_mix_model2 |   model_mix_model3 |   model_mix_model4 |
|:----------|-----------:|-------------:|-----------:|-------------------------------:|-----------------------------:|--------------------------------------------:|-------------------:|-------------------:|-------------------:|-------------------:|
| factory_1 |         20 |       139300 |      17000 |                         0.0248 |                       0.0226 |                                         178 |             0.4000 |             0.2000 |             0.2000 |             0.2000 |
| factory_2 |         20 |       139300 |      17000 |                         0.0212 |                       0.0195 |                                         152 |             0.2000 |             0.3500 |             0.2500 |             0.2000 |
| factory_3 |         20 |       139300 |      17000 |                         0.0202 |                       0.0141 |                                         144 |             0.1000 |             0.1500 |             0.5000 |             0.2500 |
| factory_4 |         20 |       139300 |      17000 |                         0.0176 |                       0.0105 |                                         123 |             0.0500 |             0.1000 |             0.4000 |             0.4500 |

## Limitations
- All evaluation is development-only; no new independent test site is evaluated.
- Candidate comparison uses shared validation data across model selection and reporting; outcome is exploratory.
- Thresholds are cross-fold but folds use overlapping training datasets.
- This study does not supply any new differential privacy guarantee.
- Pilot/smoke mode is not final research-grade seed-stability evidence.
- Historical event features may encode synthetic data-generating patterns.
- No model is automatically released or marked as a winner.