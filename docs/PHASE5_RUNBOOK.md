# Phase 5 operating notes

**Do not rerun API calls for documentation.** All 24 calls succeeded on the previously run Colab output and were persisted under `MyDrive/FedKG-Maint/unified_runs/phase5_groq_grounded_v1/responses/`.

If reproducing from source: open `notebooks/phase5/04_Phase5_Groq_KG_Explanations.ipynb`, attach prior Unified v3/B4 runtime artifacts, and supply the API key via Colab Secrets `GROQ_API_KEY` (grant access), environment variable, or secure getpass fallback. The notebook will reuse completed response files when the protocol hash and prompts match. It will not access Factory 5 or train ML.

**Review protocol:** The original `reports/human_review_blinded.csv` on Drive remains unrated. AI-assisted provisional ratings are in a separate private package and MUST NOT be submitted as actual independent human ratings. To close independent human evaluation, a human reviewer must grade and validate the 24 responses against the evidence, then rerun only the last two report-generating cells (no API calls).

For GitHub include only `results/reported` and `reports/PHASE5_FINAL_EXPLAINABILITY.md`, not full prompts or raw responses. The repository intentionally does not include runtime data or private detailed review sheet.
