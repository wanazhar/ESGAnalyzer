import numpy as np
import json
from sklearn.ensemble import IsolationForest

def load_historical_esg_data():
    """Load multi-year ESG score data for anomaly detection."""
    with open("../output/esg_historical_results.json", "r", encoding="utf-8") as f:
        return json.load(f)

def detect_historical_anomalies():
    """Identifies ESG anomalies based on historical trends."""
    data = load_historical_esg_data()

    anomaly_results = []
    
    for company in data["companies"]:
        scores = np.array(company["historical_scores"]).reshape(-1, 1)

        if len(scores) < 2:
            continue  # Skip companies with insufficient data

        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(scores)

        predictions = model.predict(scores)  # -1 means anomaly, 1 means normal
        
        company_anomalies = {
            "name": company["name"],
            "anomalies": []
        }

        for i, year in enumerate(company["years"]):
            if predictions[i] == -1:
                company_anomalies["anomalies"].append({
                    "year": year,
                    "score": scores[i][0],
                    "message": f"⚠️ Unusual ESG drop detected in {year}."
                })

        if company_anomalies["anomalies"]:
            anomaly_results.append(company_anomalies)

    return anomaly_results
