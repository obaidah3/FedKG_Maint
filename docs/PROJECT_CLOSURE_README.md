# FedKG-Maint — Research Closure & Integration Decision

**Date:** 27 October 2026  
**Selected model:** Federated **MLP (25→32→8→1)**, `full` 25 features, FedAvg.  
**Selection evidence:** Phase B4 **pilot**, eight rounds, seed 42; four development-factory LOFO folds, each trained on the other three factories. Selection is an engineering closure for this project, **not** statistical evidence of global model supremacy.

## Frozen model choice (from actual user-provided B4 Colab run)

| Metric | Value | Scope |
|---|---:|---|
| Mean PR-AUC | **0.762308** | Development LOFO |
| Worst factory PR-AUC | **0.742111** | Development LOFO |
| Worst factory (LSTM comparator) | 0.529216 | Development LOFO |
| Actionable events detected | **40/46** | 12–24 h lead condition |
| False alarms per machine-day | **0.009794** | Cross-fold threshold procedure |
| HGB full features PR-AUC | 0.975604 | B1 centralized LOFO; not federated |

The final architecture choice is MLP because it has a higher worst-factory PR-AUC and fewer false alerts than LSTM at the reported cross-fold threshold procedure. This does not prove industrial deployment readiness. Azure is a synthetic factory partition benchmark.

## What has actually been merged

- Unified v3's **data schema, splits, feature and machine manifests, local RDF graph artifacts** are the canonical foundational source.
- The B4 **full-feature MLP out-of-factory scored folds** are treated as the canonical selected prediction evidence, not scores from earlier v3 models.
- The master notebook reconstructs validation endpoints, checks per-fold **SHA256 metadata hashes** and **PR-AUC**, and joins B4 scores to each machine and timestamp.
- It retrieves historical evidence from the four **actual per-factory RDF graphs**, applying strict as-of and completed-day guards.
- It prepares **12 paired explanation cases / 24 prompts** under WITH-KG and WITHOUT-KG conditions, with the same base context and no offline outcome labels.
- All source Notebooks are preserved as an **archive** rather than run as separate submission targets.

## Honest research boundaries

1. B4 is a **one-seed pilot**; the model is selected for engineering closure, not called globally optimal.
2. B4 saved **prediction arrays, not one final fitted checkpoint for a four-client combined model**. A new unseen-factory inference deployment would require a single final fit and associated testing. The integrated notebook does not fabricate that checkpoint.
3. Unified v3's **record-level conditional DP-SGD** result protects that separate experiment's declared mechanism, **not** the chosen B4 MLP predictions, model, or KG.
4. Factory 5 was used in earlier work, and is **not** a fresh external blind test. Phase B purposely excludes it.
5. No real LLM evaluation or NASA RUL model has yet been executed; original course specification mentioned both.
6. PR-AUC is not classification accuracy, and synthetic maintenance histories may encode benchmark-specific correlations. No root cause is established from KG co-occurrence.

## Submission strategy

The file `FedKG_Maint_MASTER_Integration_v1.ipynb` is the **single integration entry point**. The `source_archive/` contains immutable source code provenance to reproduce the earlier costly trainings **only if specifically required**. It should **not** be treated as 4 separate primary submissions. The final presentation/report should use the closure tables and identify unexecuted scope accurately.

### Remaining work without more architecture search

**Next: Phase 5 paired LLM experiment and human evaluation** using the prepared score+KG evidence cases. Separately complete the **NASA C-MAPSS RUL benchmark if required**. If you need a deployable B4 MLP or formally match DP to the selected architecture, there is **one controlled final-model fit** to make; it is not another architecture search.
