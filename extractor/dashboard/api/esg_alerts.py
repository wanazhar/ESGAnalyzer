import json
from anomaly_detection import detect_anomalies

def generate_alerts():
    """Generates alerts for detected ESG anomalies."""
    anomalies = detect_anomalies()
    flagged = [c for c in anomalies["companies"] if c["anomaly"] == "Yes"]

    alerts = []
    for company in flagged:
        alerts.append({
            "company": company["name"],
            "message": f"⚠️ Unusual ESG reporting detected for {company['name']}. Review necessary.",
            "score": company["score"]
        })
    
    return alerts
