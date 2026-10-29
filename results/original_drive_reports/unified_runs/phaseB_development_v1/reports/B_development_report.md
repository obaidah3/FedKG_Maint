# FedKG-Maint Plan B — Development-only report

## B1 HGB LOFO feature ablation

| variant             |   mean_pr_auc |   worst_factory_pr_auc |   std_pr_auc |   mean_roc_auc |
|:--------------------|--------------:|-----------------------:|-------------:|---------------:|
| full                |        0.9756 |                 0.9252 |       0.0339 |         0.9996 |
| no_maintenance      |        0.7767 |                 0.7059 |       0.0493 |         0.9947 |
| sensor_errors       |        0.7767 |                 0.7059 |       0.0493 |         0.9947 |
| sensor_history_only |        0.2442 |                 0.1943 |       0.0476 |         0.9642 |

## B2 Federated MLP vs LSTM

| architecture   |   mean_pr_auc |   worst_fold_pr_auc |   std_pr_auc |   mean_roc_auc |
|:---------------|--------------:|--------------------:|-------------:|---------------:|
| LSTM           |        0.5777 |              0.2129 |       0.2187 |         0.9838 |
| MLP            |        0.5737 |              0.4013 |       0.1229 |         0.9857 |

## Paired LSTM minus MLP

{
  "mean_delta_pr_auc_lstm_minus_mlp": 0.004020107277027243,
  "median_delta_pr_auc": 0.11170233655031869,
  "positive_pair_fraction": 0.75,
  "n_paired_folds_and_seeds": 8,
  "all_pairs_improved": false,
  "interpretation": "Exploratory development-only LOFO; no significance or external blind-site claim"
}

## Interpretation boundaries

- All model selection remains on development factories 1–4.
- This notebook intentionally does not load the historical factory_5 evaluation.
- The HGB feature ablation tests predictive dependence, not causality.
- Fixed alert thresholds are exploratory and may not represent calibrated probabilities.
- The MLP/LSTM runs do not provide a DP guarantee.
- NASA and Phase 5 LLM evaluation are not performed here.