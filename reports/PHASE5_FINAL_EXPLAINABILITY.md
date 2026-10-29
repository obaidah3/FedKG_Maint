# Phase 5 — Groq API + RDF-KG Explanation Evaluation

**Executed study:** 12 paired development examples across four factories; **24/24 Groq responses saved**. Same sensor inputs, uncalibrated MLP risk score, same prompt schema; the With-KG condition additionally receives local historical RDF facts with time cutoffs. Model: `openai/gpt-oss-120b` via Groq API. No new FL training; no future failure labels sent to Groq.

## Results

| Indicator | Without KG | With KG |
|---|---:|---:|
| Mean mechanical citation-ID coverage | 93.93% | 99.24% |
| Invalid citation IDs | 0 | 0 |
| Unique KG source IDs used across the case outputs (sum of per-case distinct IDs) | 0 | 127 |
| AI-assisted faithfulness (1–5, NOT human) | 5.00 | 3.92 |
| AI-assisted actionability (1–5, NOT human) | 3.33 | 4.25 |
| AI-assisted uncertainty (1–5, NOT human) | 5.00 | 5.00 |
| Distinct materially unreliable source-based factual assertions flagged by AI-assisted review | 0 | 10 |
| Explicit unsafe-action flags in AI-assisted sample | 0 | 0 |

**Caution:** Citation-ID existence is not claim correctness. KG improved citation coverage and specificity of maintenance checks, but some answers misstated historical sensor ranges or cited error events when describing telemetry history. With-KG explanations also make more source-based claims, creating extra opportunities for error. Provisional AI scores are not independent human evidence. There is no statistically valid claim that KG generally improves faithfulness or operational outcomes based on these 12 examples.

The original `PHASE5_REPORT.json` status is **`human_review_complete: false`**. It must not be changed by substituting an AI-assessed score sheet for an independent human review. The review-assistance files were supplied privately in a separate ZIP, not committed here.

**Privacy:** The LLM service received case-specific operational/synthetic values through a third-party API. Raw prompts, private LLM outputs, human-review row texts, and factory KG Turtle files are NOT included in the public release. See `docs/PRIVACY_AND_PUBLICATION.md`.

**Model status:** B4 selected the FedAvg MLP architecture from four development LOFO folds; there is no single consolidated deployment checkpoint for the pilot, and earlier DP runs do not confer privacy guarantees on the B4 model or its transmitted scores. NASA C-MAPSS remains outside the completed work.
