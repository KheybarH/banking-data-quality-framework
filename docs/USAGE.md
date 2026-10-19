# Banking Data Quality Framework

## Quick Start

See the main [README.md](../README.md) for full instructions.

## Running Reconciliation

```bash
python src/data_generator.py
python src/reconciler.py
python src/quality_checks.py
pytest tests/ -v
```
