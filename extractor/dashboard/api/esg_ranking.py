from flask import Flask, request, jsonify
import requests
import numpy as np
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Dummy company sector & region mapping
COMPANY_DETAILS = {
    "AAPL": {"sector": "Technology", "region": "North America"},
    "TSLA": {"sector": "Technology", "region": "North America"},
    "MSFT": {"sector": "Technology", "region": "North America"},
    "GOOGL": {"sector": "Technology", "region": "North America"},
    "AMZN": {"sector": "Technology", "region": "North America"},
}

def fetch_esg_scores():
    """Fetches ESG transparency scores"""
    scores = {}
    for company in COMPANY_DETAILS.keys():
        try:
            response = requests.get(f"http://localhost:5005/api/esg_transparency?company={company}")
            data = response.json()
            scores[company] = data.get("transparency_score", 50)  # Default 50 if missing
        except:
            scores[company] = 50  # Fallback default score
    return scores

@app.route("/api/esg_ranking", methods=["GET"])
def get_esg_ranking():
    """Provides AI-ranked ESG transparency scores with filtering"""
    sector_filter = request.args.get("sector", "All")
    region_filter = request.args.get("region", "All")

    all_scores = fetch_esg_scores()

    # Apply filters
    filtered_scores = {
        company: score
        for company, score in all_scores.items()
        if (sector_filter == "All" or COMPANY_DETAILS[company]["sector"] == sector_filter)
        and (region_filter == "All" or COMPANY_DETAILS[company]["region"] == region_filter)
    }

    # Normalize scores between 0-100
    scores_array = np.array(list(filtered_scores.values())).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 100))
    ranked_scores = scaler.fit_transform(scores_array).flatten()

    ranked_data = {
        list(filtered_scores.keys())[i]: round(ranked_scores[i], 2)
        for i in range(len(filtered_scores))
    }

    return jsonify({"ranked_esg_scores": ranked_data})

if __name__ == "__main__":
    app.run(debug=True, port=5006)
