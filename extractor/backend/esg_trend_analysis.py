import json
import pandas as pd

def load_esg_data():
    with open("backend/esg_parsed_data.json") as f1, open("backend/esg_scraped_data.json") as f2:
        company_data = json.load(f1)
        external_data = json.load(f2)
    return company_data, external_data

def extract_esg_trends():
    company_data, external_data = load_esg_data()
    
    esg_metrics = ["CO2 Emissions", "Water Usage", "Diversity Score"]
    trend_data = {}

    for year in range(2020, 2024):
        trend_data[str(year)] = []

        for metric in esg_metrics:
            company_values = [
                entry.get(metric, 0) for entry in company_data if entry.get("year") == year
            ]
            external_values = [
                entry.get(metric, 0) for entry in external_data if entry.get("year") == year
            ]

            trend_data[str(year)].append({
                "metric": metric,
                "company": sum(company_values) / len(company_values) if company_values else 0,
                "external": sum(external_values) / len(external_values) if external_values else 0
            })

    with open("backend/esg_trend_data.json", "w") as f:
        json.dump(trend_data, f, indent=4)

if __name__ == "__main__":
    extract_esg_trends()
