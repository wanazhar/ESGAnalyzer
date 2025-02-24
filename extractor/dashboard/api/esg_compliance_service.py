from flask import Flask, request, jsonify
import json
from compliance.esg_compliance_checker import check_compliance

app = Flask(__name__)

@app.route("/api/check_compliance", methods=["POST"])
def api_check_compliance():
    """API endpoint for checking ESG compliance."""
    report_data = request.json.get("report_data")
    if not report_data:
        return jsonify({"error": "Invalid report data"}), 400

    compliance_result = check_compliance(report_data)
    return jsonify({"compliance_result": compliance_result})

if __name__ == "__main__":
    app.run(debug=True, port=5010)
