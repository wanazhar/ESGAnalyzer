import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def compare_sentiments(company_report, external_report):
    """AI comparison of company vs external ESG sentiment."""
    prompt = f"""
    Compare the ESG sentiment between the company's internal report and external sources. 
    Highlight any discrepancies. Here’s the data:

    Company ESG Report:
    {company_report}

    External ESG Sources:
    {external_report}

    Return JSON format: {{"summary": "...", "alignment": "Aligned/Not Aligned", "key_discrepancies": "..."}}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def analyze_discrepancies():
    """Analyze sentiment discrepancies between reports."""
    with open("backend/esg_sentiment_data.json") as f1, open("backend/esg_scraped_data.json") as f2:
        company_data = json.load(f1)
        external_data = json.load(f2)

    comparison_results = []

    for company in company_data:
        for external in external_data:
            if company["category"] == external["category"]:
                result = compare_sentiments(company["summary"], external["summary"])
                comparison_results.append({"company": company["file"], "result": result})

    with open("backend/esg_sentiment_comparison.json", "w") as f:
        json.dump(comparison_results, f, indent=4)

if __name__ == "__main__":
    analyze_discrepancies()
