

```markdown
# Banking Data Quality & Reconciliation Framework

Personal portfolio project demonstrating data quality engineering practices for financial / banking data.

This project shows how to build reliable data validation and reconciliation checks between source and target systems — a critical skill when moving from QA automation into Data Engineering.

## Why this project?

Data quality issues are one of the most common causes of production incidents in data pipelines. Coming from a QA background, I built this framework to apply testing rigor to data pipelines: row-count reconciliation, checksum validation, business rule checks, and schema drift detection.

## What it does

- Generates realistic synthetic banking data (customers, accounts, transactions)
- Performs reconciliation between source and target datasets
- Runs data quality checks (nulls, duplicates, business rules, schema consistency)
- Generates a clean HTML report with pass/fail results
- Designed to be easily extended with Great Expectations or integrated into Airflow

## Key Features

- Row count reconciliation between source and target
- Key uniqueness and missing key detection
- Null checks on critical columns
- Business rule validation (transaction amounts, status values)
- Schema drift detection
- HTML quality report with overall status

## Technologies

- Python
- Pandas
- Faker (synthetic data)
- Pytest
- Jinja2 (HTML reports)

## Project Structure

```
src/
  data_generator.py      # Synthetic banking data generator
  reconciler.py          # Core reconciliation logic
  quality_checks.py      # Data quality rules
  reporter.py            # HTML report generator
tests/
  test_quality_checks.py
data/
  raw/                   # Source data
  processed/             # Target data
reports/                 # Generated HTML reports
```

## How to Run

```bash
pip install -r requirements.txt

# Generate data and run full pipeline
python src/data_generator.py
python src/reporter.py

# Run tests
pytest tests/ -v
```

## Example Output

The framework detects real issues such as:
- Row count mismatches
- Missing keys
- Null values in critical fields
- Invalid transaction amounts

## Author

Built as a portfolio project to demonstrate the combination of QA testing practices and Data Engineering data quality skills.
```


