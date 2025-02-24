import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)

# AI NLP Model for News Sentiment Analysis
news_sentiment_pipeline = pipeline("sentiment-analysis")

REGULATORY_STANDARDS = {
    "GRI": ["GHG emissions", "biodiversity impact", "waste management"],
    "SASB": ["financial materiality", "supply chain sustainability"],
    "EU-Taxonomy": ["green investments", "climate risk disclosure"]
}

def fetch_esg_news(company):
    """Scrape ESG-related news headlines from a financial news aggregator."""
    try:
        url = f"https://news.google.com/search?q={company}+ESG+news"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = [h.text for h in soup.find_all("a") if "ESG" in h.text][:5]
        return headlines
    except:
        return ["No recent ESG news found."]

def analyze_news_sentiment(news_headlines):
    """Perform sentiment analysis on ESG news headlines."""
    sentiments = news_sentiment_pipeline(news_headlines)
    sentiment_summary = {"positive": 0, "neutral": 0, "negative": 0}

    for sentiment in sentiments:
        label = sentiment["label"].lower()
        sentiment_summary[label] = sentiment_summary.get(label, 0) + 1

    return sentiment_summary

def check_compliance_gaps(esg_report):
    """Cross-check ESG reports against global sustainability frameworks."""
    missing_disclosures = {}

    for standard, criteria in REGULATORY_STANDARDS.items():
        missing = [c for c in criteria if c.lower() not in esg_report.lower()]
        if missing:
            missing_disclosures[standard] = missing

    return missing_disclosures if missing_disclosures else "No compliance gaps detected."

@app.route("/api/news_compliance", methods=["GET"])
def get_news_compliance_analysis():
    """Analyze ESG news sentiment and compliance gaps for a company."""
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company symbol required"}), 400

    news_headlines = fetch_esg_news(company)
    sentiment_analysis = analyze_news_sentiment(news_headlines)
    esg_report = requests.get(f"http://localhost:5000/api/company_esg_report?company={company}").text
    compliance_gaps = check_compliance_gaps(esg_report)

    return jsonify({
        "company": company,
        "news_headlines": news_headlines,
        "news_sentiment": sentiment_analysis,
        "compliance_gaps": compliance_gaps
    })

if __name__ == "__main__":
    app.run(debug=True, port=5004)
