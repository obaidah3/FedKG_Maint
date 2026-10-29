# Data layout (create locally; do not commit raw files)

The original Azure project uses five CSVs under `MyDrive/FedKG-Maint/data/raw/` in Colab:

```
PdM_telemetry.csv
PdM_errors.csv
PdM_maint.csv
PdM_failures.csv
PdM_machines.csv
```

The notebooks include their own local loading logic or KaggleHub fallback. Verify the source dataset license before redistribution. Large generated parquets, score `.npz`, per-factory RDF graphs, and fitted checkpoint files are excluded from this GitHub package by design.

NASA C-MAPSS RUL experiments are **not yet implemented**. Official reference: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
