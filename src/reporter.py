"""
HTML report generator for data quality results.
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
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f8f9fa; }
        .container { max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #1a365d; }
        h2 { color: #2d3748; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
        .pass { color: #38a169; font-weight: bold; }
        .fail { color: #e53e3e; font-weight: bold; }
        table { border-collapse: collapse; width: 100%; margin-top: 15px; }
        th, td { border: 1px solid #e2e8f0; padding: 12px; text-align: left; }
        th { background-color: #edf2f7; }
        .summary { background: #ebf8ff; padding: 15px; border-radius: 6px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Banking Data Quality & Reconciliation Report</h1>
        <p><strong>Generated:</strong> {{ timestamp }}</p>
        
        <div class="summary">
            <strong>Overall Status:</strong> 
            <span class="{{ 'pass' if overall_pass else 'fail' }}">
                {{ 'PASS' if overall_pass else 'FAIL' }}
            </span>
        </div>

        <h2>Reconciliation Summary</h2>
        <table>
            <tr><th>Check</th><th>Result</th><th>Details</th></tr>
            {% for check, result in results.items() %}
            <tr>
                <td>{{ check.replace('_', ' ').title() }}</td>
                <td class="{{ 'pass' if result.get('pass', result.get('match', False)) else 'fail' }}">
                    {{ 'PASS' if result.get('pass', result.get('match', False)) else 'FAIL' }}
                </td>
                <td>{{ result }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

def generate_report(results: dict, output_path="reports/data_quality_report.html"):
    os.makedirs("reports", exist_ok=True)
    overall_pass = all(
        r.get("pass", r.get("match", False)) 
        for r in results.values() 
        if isinstance(r, dict)
    )
    template = Template(HTML_TEMPLATE)
    html = template.render(
        results=results, 
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        overall_pass=overall_pass
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    from reconciler import reconcile_transactions
    from quality_checks import run_quality_checks
    
    results = reconcile_transactions()
    quality = run_quality_checks()
    
    # Flatten quality results for the report
    flat_quality = {}
    for check_name, check_result in quality.items():
        if isinstance(check_result, dict) and "pass" in check_result:
            flat_quality[check_name] = check_result
        else:
            # For nested results like null_checks
            all_pass = all(v.get("pass", False) for v in check_result.values() if isinstance(v, dict))
            flat_quality[check_name] = {"pass": all_pass, "details": check_result}
    
    combined = {**results, **flat_quality}
    generate_report(combined)