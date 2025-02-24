import json
from flask import Flask, request, jsonify
from historical_anomaly_detection import detect_historical_anomalies

app = Flask(__name__)

@app.route("/api/esg_trend_alerts", methods=["GET"])
def get_trend_alerts():
    """Fetch filtered ESG trend alerts based on company or industry."""
    anomalies = detect_historical_anomalies()
    
    company_filter = request.args.get("company")
    industry_filter = request.args.get("industry")

    filtered_alerts = []
    
    for company in anomalies:
        for issue in company["anomalies"]:
            if (not company_filter or company["name"] == company_filter) and \
               (not industry_filter or company.get("industry") == industry_filter):
                filtered_alerts.append({
                    "company": company["name"],
                    "industry": company.get("industry", "Unknown"),
                    "year": issue["year"],
                    "score": issue["score"],
                    "message": issue["message"]
                })

    return jsonify(filtered_alerts)

if __name__ == "__main__":
    app.run(debug=True)
