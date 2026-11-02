<<<<<<< HEAD


```markdown
=======
>>>>>>> fa14fa5 (Upgrade to PostgreSQL + SQL reconciliation + CI)
# Banking Data Quality & Reconciliation Framework

Personal portfolio project demonstrating production-style data quality engineering for financial / banking data.

This project shows how to build reliable validation and reconciliation checks between source and target systems — a critical skill when moving from QA automation into Data Engineering.

![CI](https://github.com/KheybarH/banking-data-quality-framework/actions/workflows/ci.yml/badge.svg)

## Why this project?

Data quality issues are one of the most common causes of production incidents in data pipelines. Coming from a QA background, I built this framework to apply testing rigor to data pipelines using **PostgreSQL + SQL reconciliation**, controlled fault injection, and structured checks.

## What it does

- Generates realistic synthetic banking data (customers, accounts, transactions)
- Loads data into **PostgreSQL** with separate `source` and `target` schemas
- Runs **SQL-based reconciliation** (row counts, amount sums, missing/extra keys, referential integrity)
- Introduces controlled data quality issues in the target for demonstration
- Designed to be extended with Great Expectations, dbt tests, or Airflow

## Technologies

- Python
- PostgreSQL (Docker Compose)
- SQLAlchemy / psycopg2
- Pandas + Faker
- Pytest
- GitHub Actions

## Project Structure

```
.
├── docker-compose.yml
├── Makefile
├── sql/
│   ├── init.sql              # Schemas and tables
│   └── reconciliation.sql    # Example SQL checks
├── src/
│   ├── data_generator.py     # Synthetic data + fault injection
│   ├── load_to_postgres.py   # Load CSVs into Postgres
│   └── sql_reconciler.py     # Run SQL reconciliation
├── tests/
├── .github/workflows/ci.yml
└── LICENSE
```

## Quick Start

```bash
# 1. Start PostgreSQL
make up

# 2. Generate data and load into Postgres
make generate
make load

# 3. Run reconciliation
make reconcile

# Or all at once
make run
```

## Example Reconciliation Output

The SQL reconciler detects issues such as:
- Row count mismatches
- Amount sum differences
- Missing / extra transaction keys
- Orphan transactions (broken referential integrity)

## License

MIT
