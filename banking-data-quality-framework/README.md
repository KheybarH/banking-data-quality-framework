# Banking Data Quality & Reconciliation Framework

Personal portfolio project demonstrating data quality engineering practices for financial / banking data.

This project shows how to build reliable data validation and reconciliation checks between source and target systems — a critical skill when moving from QA automation into Data Engineering.

## Why this project?

Data quality issues are one of the most common causes of production incidents in data pipelines. Coming from a QA background, I built this framework to apply testing rigor to data pipelines: row-count reconciliation, checksum validation, business rule checks, and schema drift detection.

## What it does

- Generates realistic synthetic banking data (customers, accounts, transactions)
- Performs reconciliation between source and target datasets
- Runs data quality checks (nulls, duplicates, business rules, schema consistency)
- Generates an HTML report with pass/fail results
- Designed to be easily extended with Great Expectations or integrated into Airflow

## Key Features

- **Row count reconciliation** between source and target
- **Checksum / hash validation** for data integrity
- **Business rule checks** (e.g., transaction amount > 0, valid account status)
- **Schema drift detection**
- **HTML quality report**
- Modular and testable design (Pytest)

## Technologies

- Python
- Pandas
- Faker (synthetic data)
- Pytest
- Jinja2 (HTML reports)
- (Optional) Great Expectations

## Project Structure

```
src/
  data_generator.py      # Synthetic banking data generator
  reconciler.py          # Core reconciliation logic
  quality_checks.py      # Data quality rules
  reporter.py            # HTML report generator
tests/
  test_reconciler.py
  test_quality_checks.py
data/
  raw/                   # Source data
  processed/             # Target / cleaned data
reports/                 # Generated HTML reports
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic data and run reconciliation
python src/data_generator.py
python src/reconciler.py

# Run tests
pytest tests/ -v

# View report
open reports/data_quality_report.html
```

## Example Results

The framework detects:
- Row count mismatches
- Checksum differences
- Invalid transaction amounts
- Missing required fields
- Schema changes between source and target

## Future Improvements

- Integrate with Apache Airflow as a data quality task
- Add Great Expectations suite
- Support incremental reconciliation
- Connect to real databases (Postgres / DuckDB)

## Author

Built as a portfolio project to demonstrate the combination of QA testing practices and Data Engineering data quality skills.
