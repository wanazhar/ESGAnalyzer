import json
import requests
import numpy as np
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from transformers import pipeline

app = Flask(__name__)

# Sentiment Analysis Pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def fetch_historical_sentiment(company):
    """Fetch ESG sentiment scores over time (past 12 months)."""
    try:
        response = requests.get(f"http://localhost:5000/api/historical_sentiment?company={company}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def detect_sentiment_shifts(sentiment_data):
    """Identify major sentiment changes over time using statistical deviation."""
    if not sentiment_data or len(sentiment_data) < 6:
        return "Insufficient sentiment data for analysis"

    scores = [month["sentiment_score"] for month in sentiment_data if month["sentiment_score"] is not None]
    
    if len(scores) < 3:
        return "Not enough valid sentiment scores"

    mean_score = np.mean(scores)
    std_dev = np.std(scores)

    significant_shifts = []
    for month in sentiment_data:
        if abs(month["sentiment_score"] - mean_score) > std_dev * 1.5:
            significant_shifts.append(f"Major sentiment shift in {month['month']}: {month['sentiment_score']}")
    
    return significant_shifts if significant_shifts else "No major sentiment shifts detected"

@app.route("/api/sentiment_trend", methods=["GET"])
def get_sentiment_trend():
    """Analyze ESG sentiment shifts for a company."""
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company symbol required"}), 400
    
    sentiment_data = fetch_historical_sentiment(company)
    if not sentiment_data:
        return jsonify({"error": "Unable to retrieve sentiment data"}), 500

    sentiment_shifts = detect_sentiment_shifts(sentiment_data)

    return jsonify({
        "company": company,
        "sentiment_shifts": sentiment_shifts
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
