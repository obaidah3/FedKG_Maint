# Implemented / planned architecture

```mermaid
flowchart TD
  A[Azure PdM telemetry/errors/maintenance/failures] --> B[Temporal feature generation and 24h failure label]
  B --> C[Simulated non-IID factory clients x5]
  C --> D[Federated prediction development: FedAvg MLP]
  D --> E[Per-factory out-of-fold risk scores, B4 pilot]
  C --> F[Local RDF Knowledge Graphs: one per factory]
  E --> G[MASTER joins score to machine/time and retrieves as-of evidence]
  F --> G
  G --> H[Paired WITH-KG vs WITHOUT-KG prompts — prepared, NOT yet evaluated]
  I[Unified v3 conditional DP-SGD research branch] -. separate, not protection for B4 .-> D
  J[NASA C-MAPSS RUL branch — NOT implemented] -. later .-> C
```

The Azure pipeline targets: failure occurring strictly in `(t, t + 24 hours]`. Measured PR-AUC is *average precision*, not accuracy. The reported B4 architecture uses 25 current-row features, local StandardScaler per development factory, 25→32→8→1 MLP, FedAvg, and four leave-one-development-factory-out folds (three training clients each). The selected B4 scores are fold-specific; a new general-purpose unseen-client checkpoint has not been trained/saved in this package.

The KG retrieval is as-of; graph evidence represents documented historical observations, not causal proof. The LLM layer is a prepared next-stage **experiment**, not a validated system feature.
