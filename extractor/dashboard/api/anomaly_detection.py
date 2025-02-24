import numpy as np
import json
from sklearn.ensemble import IsolationForest

def load_esg_data():
    """Load ESG score data for anomaly detection."""
    with open("../output/esg_results.json", "r", encoding="utf-8") as f:
        return json.load(f)

def detect_anomalies():
    """Identifies anomalies in ESG trends using Isolation Forest."""
    data = load_esg_data()
    
    # Convert ESG scores to NumPy array
    scores = np.array([[company["score"]] for company in data["companies"]])

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(scores)
    
    predictions = model.predict(scores)  # -1 means anomaly, 1 means normal
    
    # Attach anomaly flag to ESG data
    for i, company in enumerate(data["companies"]):
        company["anomaly"] = "Yes" if predictions[i] == -1 else "No"

    return data
