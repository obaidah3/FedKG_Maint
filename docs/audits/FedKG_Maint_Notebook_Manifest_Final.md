# FedKG-Maint — Canonical Notebook Manifest for Reporting and Submission

This manifest separates the current reproducible workflow from historical experiments. Do not merge results from superseded notebooks into the final results table unless they are clearly labelled as earlier experiments.

## A. Canonical notebooks to base the main report on

Run / cite these in this order:

1. **Phase 1 — Data Preparation**  
   File: `FedKG_Maint_Data_Preparation_v3_Revised.ipynb`  
   Role: prepare and validate data, labels, feature groups, client/site splits, and leakage checks.

2. **Phase 2 — Centralized Baselines**  
   File: `FedKG_Maint_Phase2_Baselines_v3_Revised.ipynb`  
   Role: train/evaluate centralized reference models and provide the baseline comparison. Preserve the report's documented temporal/test-split caveats.

3. **Phase 3 — Federated Learning and Initial Privacy Trade-off Experiments**  
   File: `FedKG_Maint_Phase3_Federated_Learning_v2_Privacy_Tradeoff.ipynb`  
   Role: primary original federated-learning experiment, comparisons of FedAvg/FedProx/DP and simulated secure aggregation, and diagnosis of the initial privacy–utility problem.

4. **Phase 3 — Current Compact DP Repair (v3)**  
   File: `FedKG_Maint_Phase3_Privacy_Utility_Fix_v3.ipynb`  
   Role: latest repair experiment. Report the actual results obtained from this run: selected local epochs = 1, clipping norm = 0.1, noise multiplier = 1.0, reported update-channel bound epsilon ≈ 9.8376 at delta = 1e-5; mean held-out PR-AUC across three seeds = 0.3258 for DP-FedAvg, 0.2954 for ClippedFedAvg, and 0.3778 for Central Compact Linear. State that the privacy accountant's scope is the clipped/noised client-update channel only; it is not end-to-end DP.

5. **Phase 3 — Final Closure Audit**  
   File: `FedKG_Maint_Phase3_Closure_Audit_v1.ipynb`  
   Role: audit the saved outputs without retraining or retuning: paired machine-level uncertainty comparison and independent privacy-accounting check. This notebook must be run in the user's Colab/Drive environment before claiming the audit is complete; merely having the file or passing structural checks is not an executed audit.

## B. Supporting experiment notebooks (appendix / research trail)

These explain why v3 was needed. Keep them as supporting evidence, not as the latest final model:

- `FedKG_Maint_Phase3_Privacy_Closure_v1.ipynb` — earlier noise sweep showing poor utility under its selected privacy cap.
- `FedKG_Maint_Phase3_Privacy_Utility_Fix_v2.ipynb` — intermediate 8-parameter repair; superseded by v3 because it remained unstable across seeds.

They can be cited in a development-history/ablation section but should not replace v3 in the final results table.

## C. Superseded — do not use as the final source of truth

- `FedKG_Maint_Data_Preparation_v2 (1).ipynb`
- `FedKG_Maint_Phase2_Baselines (1).ipynb`
- `FedKG_Maint_Phase3_Federated_Learning_v1.ipynb`

These are older versions and should not be mixed with the revised v3/v2 workflow above.

## D. Suggested final submission structure

- Main reproducible notebooks: Phase 1 v3, Phase 2 v3, Phase 3 federated/privacy v2, Phase 3 repair v3, Phase 3 closure audit v1.
- Optional appendix / experiment history: Privacy Closure v1 and Privacy Utility Fix v2.
- Exclude superseded notebooks from the final submission bundle unless the instructor specifically requests version history.
- Before final submission, run the closure audit on the saved Phase 3 v3 artifacts and archive its generated report/results with the other outputs.

## E. Scope reminder

The current notebook set does not itself complete the planned Knowledge Graph and LLM explainability phases. If those remain requirements in the project specification, their implementation, evaluation, and notebooks are still separate work. Also, `SecureAggSim` in Phase 3 is an arithmetic simulation, not cryptographic secure aggregation.
