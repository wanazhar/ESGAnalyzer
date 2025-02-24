import requests
import json
import time

API_SOURCES = {
    "FMP": "https://fmp.com/api/esg/",
    "Finhub": "https://finhub.com/api/esg/",
    "Refinitiv": "https://refinitiv.com/api/esg/"
}

def fetch_esg_data(company):
    """Retrieve ESG data from multiple sources with fallback handling."""
    aggregated_data = {}

    for source, url in API_SOURCES.items():
        try:
            response = requests.get(f"{url}{company}")
            if response.status_code == 200:
                aggregated_data[source] = response.json()
            else:
                print(f"⚠️ {source} API Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {source} API Error: {e}")

        time.sleep(1)  # Prevent rate-limiting issues

    return aggregated_data

def clean_esg_data(raw_data):
    """Standardize and remove duplicates from ESG data."""
    cleaned_data = {}
    categories = ["Environmental", "Social", "Governance"]

    for category in categories:
        values = []
        for source, data in raw_data.items():
            value = data.get(category, None)
            if value:
                values.append(value)

        if values:
            cleaned_data[category] = sum(values) / len(values)  # Averaging values across sources

    return cleaned_data

def aggregate_esg_data(company):
    """Main function to fetch, clean, and aggregate ESG data."""
    raw_data = fetch_esg_data(company)
    aggregated_data = clean_esg_data(raw_data)

    return {
        "company": company,
        "aggregated_esg_scores": aggregated_data,
        "raw_sources": raw_data
    }
