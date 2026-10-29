# FedKG-Maint · Phase 5 Groq Explanation Study

- Model: `openai/gpt-oss-120b`
- Successful calls: **24/24**
- Evidence-bearing KG cases: **12/12**
- Generation status: **COMPLETE**
- Human evaluation status: **PENDING — fill human_review_blinded.csv**

## Mechanical citation audit (does not prove factual correctness)

| condition   |   number_of_explanations |   mean_citation_id_coverage |   invalid_id_total |   kg_ids_cited_total |
|:------------|-------------------------:|----------------------------:|-------------------:|---------------------:|
| with_kg     |                       12 |                    0.992424 |                  0 |                  127 |
| without_kg  |                       12 |                    0.939286 |                  0 |                    0 |

## Human review

Pending: score faithfulness, actionability, uncertainty, safety, unsupported claims for each response.

## Interpretation boundaries

- Only 12 selected development cases; nonrandom engineering evaluation, no statistical superiority claim.
- Valid citation IDs verify references exist, NOT that all generated assertions follow from them.
- KG historical co-occurrence is not causal model attribution.
- B4 predictions derive from four LOFO models, not one production-grade checkpoint.
- Groq is a third-party API receiving synthetic/operational evidence; review data-sharing authorization.

## Next phase
Merge this report and sanitized tables into GitHub final release; proceed to NASA benchmark if required.