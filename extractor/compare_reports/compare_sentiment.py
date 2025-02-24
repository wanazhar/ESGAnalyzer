import os
import json
import openai

# File paths
CONFIG_FILE = "config.json"
COMPANY_REPORTS_FOLDER = "company_reports"
SENTIMENT_FILE = "sentiment_analysis/esg_sentiment_llm.json"
OUTPUT_FILE = "compare_reports/esg_comparison.json"

# Load API key from config
def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Error: {CONFIG_FILE} not found!")
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
if config:
    openai.api_key = config.get("openai_api_key")
    llm_model = config.get("llm_model", "gpt-4")

if not openai.api_key:
    raise ValueError("❌ OpenAI API key is missing! Set it in config.json.")

# Load company reports
def load_company_reports():
    reports = {}
    for filename in os.listdir(COMPANY_REPORTS_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(COMPANY_REPORTS_FOLDER, filename), "r", encoding="utf-8") as f:
                reports[filename] = json.load(f)
    return reports

# Load sentiment analysis results
def load_sentiment_analysis():
    if not os.path.exists(SENTIMENT_FILE):
        print(f"❌ Error: {SENTIMENT_FILE} not found! Run sentiment analysis first.")
        return {}

    with open(SENTIMENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Ask LLM for opinion on ESG contradictions
def get_llm_opinion(company_name, category, claim, external_sentiment, news_source):
    """Send ESG contradiction to the LLM for analysis and reliability scoring."""
    
    prompt = f"""
    A company named "{company_name}" has made the following ESG claim:

    Category: {category}
    Company Claim: "{claim}"

    However, external news reports contradict this claim with the following information:

    Source: {news_source}
    External Sentiment Analysis: "{external_sentiment}"

    Please analyze the credibility of this ESG claim. Provide:
    - A reliability score (High, Medium, Low)
    - A short explanation of whether the company appears truthful or misleading.

    Format:
    Reliability Score: [High/Medium/Low]
    Explanation: [Short summary]
    """

    try:
        response = openai.ChatCompletion.create(
            model=llm_model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return "Reliability Score: Unknown\nExplanation: Error processing."

# Compare company ESG claims with external sentiment
def compare_esg_data():
    company_reports = load_company_reports()
    external_sentiment = load_sentiment_analysis()

    comparison_results = {}

    for filename, report in company_reports.items():
        company_name = report["company_name"]
        esg_claims = report.get("ESG_claims", {})

        comparison_results[company_name] = {"claims": esg_claims, "contradictions": []}

        for url, news_data in external_sentiment.items():
            news_sentiment = news_data["llm_sentiment"]

            for category, claim in esg_claims.items():
                if category in news_sentiment and "Negative" in news_sentiment:
                    llm_opinion = get_llm_opinion(company_name, category, claim, news_sentiment, url)

                    comparison_results[company_name]["contradictions"].append({
                        "category": category,
                        "company_claim": claim,
                        "external_sentiment": news_sentiment,
                        "news_source": url,
                        "llm_opinion": llm_opinion
                    })

    # Save comparison results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=4)

    print(f"✅ ESG comparison saved: {OUTPUT_FILE}")

# Run the comparison
compare_esg_data()
