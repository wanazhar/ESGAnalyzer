import json
import pandas as pd

def load_company_esg_report(file_path):
    """Load parsed ESG data from company reports."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_external_esg_data(file_path):
    """Load fetched ESG scores from external sources."""
    with open(file_path, "r") as file:
        return json.load(file)

def compare_esg_scores(company_data, external_data):
    """Compare ESG data from company reports and external sources."""
    comparison_matrix = []
    
    esg_categories = ["Environmental", "Social", "Governance"]
    sources = ["FMP", "Finnhub", "Refinitiv"]
    
    for category in esg_categories:
        company_score = company_data.get(category, "Not Available")
        external_scores = {source: external_data.get(source, {}).get(category, "Not Available") for source in sources}
        
        comparison_matrix.append({
            "Category": category,
            "Company Report": company_score,
            "FMP": external_scores["FMP"],
            "Finnhub": external_scores["Finnhub"],
            "Refinitiv": external_scores["Refinitiv"]
        })
    
    return pd.DataFrame(comparison_matrix)

def main():
    company_esg_path = "data/company_esg_report.json"
    external_esg_path = "data/external_esg_data.json"
    
    company_data = load_company_esg_report(company_esg_path)
    external_data = load_external_esg_data(external_esg_path)
    
    comparison_df = compare_esg_scores(company_data, external_data)
    print(comparison_df)
    comparison_df.to_csv("data/esg_comparison_matrix.csv", index=False)

if __name__ == "__main__":
    main()
