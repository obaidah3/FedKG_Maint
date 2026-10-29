# FedKG-Maint — Master Research Integration Closure

**STATUS: Research artifacts integrated; unfinished phases remain transparently open.**

## Frozen model choice
**FedAvg MLP 25→32→8→1**, full 25 features, B4 pilot.

- Mean development LOFO PR-AUC: **0.7623**
- Worst development fold: **0.7421**
- Actionable event recall: **40/46**
- False alarms per machine-day: **0.00979**

## Verified integration
- B4 prediction rows verified: **66,160**
- Local KG cases prepared: **12**
- Balanced LLM prompts: **24** (not executed)

## Important limitations
- B4 single-seed pilot, exploratory development LOFO, no independent external factory
- Histories from synthetic Azure data may introduce operationally unrealistic predictive signals
- B4 stores scored folds, not a deployable four-client trained checkpoint
- No end-to-end DP or cryptographic Secure Aggregation is demonstrated
- LLM explanation quality not tested; human evaluation sheet is blank

## Remaining required work
- Execute and review Phase5 LLM pairwise experiment and human evaluation.
- Complete NASA C-MAPSS RUL benchmark if still required by project specification.
- A final B4 MLP global checkpoint is NOT in prior output; if an operational model or matched DP comparison is needed, one explicitly controlled final fit will be required. No new architecture search.

## Reproducibility
- Source files were read-only and verified by SHA256.
- Archived original notebooks remain separate as provenance, not primary notebooks.
- Master output directory is not a publication-safe DP release.