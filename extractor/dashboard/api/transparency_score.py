import json
import requests
import numpy as np

def fetch_external_esg_data(company):
    """Retrieve ESG data from external sources for comparison."""
    sources = [
        f"https://fmp.com/api/esg/{company}",
        f"https://finhub.com/api/esg/{company}",
        f"https://refinitiv.com/api/esg/{company}"
    ]
    
    external_data = {}
    for source in sources:
        try:
            response = requests.get(source)
            if response.status_code == 200:
                external_data[source] = response.json()
        except Exception as e:
            print(f"⚠️ API Error: {e}")
    
    return external_data

def compute_transparency_score(report_data, external_data):
    """Calculate ESG transparency score based on consistency and completeness."""
    
    categories = ["Environmental", "Social", "Governance"]
    scores = []
    
    for category in categories:
        reported_value = report_data.get(category, 0)
        external_values = [data.get(category, 0) for data in external_data.values()]
        
        if external_values:
            avg_external_value = np.mean(external_values)
            consistency_score = 1 - abs(reported_value - avg_external_value) / max(1, avg_external_value)
            scores.append(consistency_score)
    
    final_score = round(np.mean(scores) * 100, 2)
    return final_score

def analyze_transparency(company, report_data):
    """Compare company-reported ESG with external sources and generate score."""
    external_data = fetch_external_esg_data(company)
    score = compute_transparency_score(report_data, external_data)

    return {
        "company": company,
        "transparency_score": score,
        "external_sources": external_data
    }
