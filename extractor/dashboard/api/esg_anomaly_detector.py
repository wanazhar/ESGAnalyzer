import json
import numpy as np
import requests
from flask import Flask, request, jsonify
from transformers import pipeline
from config import OPENAI_API_KEY

app = Flask(__name__)

# AI Sentiment & ESG Analysis Pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def fetch_esg_data(company):
    """Fetch latest ESG data from the aggregation API."""
    try:
        response = requests.get(f"http://localhost:5000/api/esg_data?company={company}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def detect_anomalies(esg_data):
    """AI-powered anomaly detection using statistical deviation."""
    scores = []
    for source in ["FMP", "Finhub", "Refinitiv"]:
        if esg_data[source] != "Not Available":
            scores.append(esg_data[source].get("esgScore", np.nan))
    
    if len(scores) < 2:
        return "Insufficient data for anomaly detection"
    
    mean_score = np.nanmean(scores)
    std_dev = np.nanstd(scores)
    
    anomalies = []
    for source, score in zip(["FMP", "Finhub", "Refinitiv"], scores):
        if abs(score - mean_score) > std_dev * 1.5:  # Flag scores outside 1.5 std dev
            anomalies.append(f"Anomalous score in {source}: {score}")
    
    return anomalies if anomalies else "No anomalies detected"

def ai_analysis(company):
    """AI-powered insights using ESG-related LLM analysis."""
    prompt = f"Analyze the ESG performance of {company}. Identify discrepancies in ESG reports and highlight potential risks."
    
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]}
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return "AI analysis unavailable"
    except:
        return "AI analysis unavailable"

@app.route("/api/esg_anomaly", methods=["GET"])
def get_esg_anomalies():
    """Fetch ESG anomalies and AI analysis for a given company."""
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company symbol required"}), 400
    
    esg_data = fetch_esg_data(company)
    if not esg_data:
        return jsonify({"error": "Unable to retrieve ESG data"}), 500

    anomalies = detect_anomalies(esg_data)
    ai_insights = ai_analysis(company)

    return jsonify({
        "company": company,
        "anomalies": anomalies,
        "ai_insights": ai_insights
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
