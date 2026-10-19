"""
Simple HTML report generator for data quality results.
"""

from jinja2 import Template
from datetime import datetime
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Quality Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #1a365d; }
        .pass { color: green; font-weight: bold; }
        .fail { color: red; font-weight: bold; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Banking Data Quality & Reconciliation Report</h1>
    <p>Generated: {{ timestamp }}</p>
    <h2>Reconciliation Summary</h2>
    <table>
        <tr><th>Check</th><th>Result</th><th>Details</th></tr>
        {% for check, result in results.items() %}
        <tr>
            <td>{{ check }}</td>
            <td class="{{ 'pass' if result.get('pass', result.get('match', False)) else 'fail' }}">
                {{ 'PASS' if result.get('pass', result.get('match', False)) else 'FAIL' }}
            </td>
            <td>{{ result }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def generate_report(results: dict, output_path="reports/data_quality_report.html"):
    os.makedirs("reports", exist_ok=True)
    template = Template(HTML_TEMPLATE)
    html = template.render(results=results, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    sample = {
        "row_count": {"source": 10000, "target": 9980, "match": False, "difference": 20},
        "key_uniqueness": {"pass": True}
    }
    generate_report(sample)
