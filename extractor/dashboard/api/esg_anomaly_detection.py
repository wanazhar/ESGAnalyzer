import json
import requests
import numpy as np
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from transformers import pipeline

app = Flask(__name__)

# AI NLP Model for Sentiment & ESG Insights
sentiment_pipeline = pipeline("sentiment-analysis")

def fetch_sentiment_trends(company):
    """Fetch historical ESG sentiment trends for a company."""
    try:
        response = requests.get(f"http://localhost:5002/api/sentiment_trend?company={company}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def fetch_esg_report(company):
    """Fetch the company's official ESG report data."""
    try:
        response = requests.get(f"http://localhost:5000/api/company_esg_report?company={company}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def detect_anomalies(esg_report, sentiment_trends):
    """Detect inconsistencies between ESG reporting and public sentiment."""
    anomalies = []
    
    if not esg_report or not sentiment_trends:
        return ["Insufficient data for anomaly detection"]

    # Check for major sentiment shifts
    sentiment_shifts = sentiment_trends.get("sentiment_shifts", [])
    if sentiment_shifts and isinstance(sentiment_shifts, list):
        anomalies.append(f"Sentiment Shift Alerts: {', '.join(sentiment_shifts)}")

    # Compare ESG reporting with sentiment
    for category in ["Environmental", "Social", "Governance"]:
        reported_score = esg_report.get(category, {}).get("score")
        public_sentiment = esg_report.get(category, {}).get("public_sentiment")

        if reported_score and public_sentiment:
            diff = abs(reported_score - public_sentiment)
            if diff > 1.5:  # Threshold for anomaly detection
                anomalies.append(f"Discrepancy detected in {category}: Reported {reported_score}, Public Sentiment {public_sentiment}")

    return anomalies if anomalies else ["No significant anomalies detected"]

@app.route("/api/anomaly_detection", methods=["GET"])
def get_anomaly_analysis():
    """Analyze ESG anomalies for a company."""
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company symbol required"}), 400

    esg_report = fetch_esg_report(company)
    sentiment_trends = fetch_sentiment_trends(company)

    anomalies = detect_anomalies(esg_report, sentiment_trends)

    return jsonify({
        "company": company,
        "anomalies": anomalies
    })

if __name__ == "__main__":
    app.run(debug=True, port=5003)
