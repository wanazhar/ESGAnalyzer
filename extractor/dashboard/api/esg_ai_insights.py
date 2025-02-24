import openai
import os
from flask import Flask, request, jsonify
from historical_anomaly_detection import detect_historical_anomalies

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_insight(company, year, issue):
    """Generate an AI-powered explanation for an ESG score drop."""
    try:
        prompt = f"""
        {company} experienced a decline in ESG score in {year}. 
        Key issue: {issue}. 
        Provide an analysis on potential reasons behind this drop.
        Consider company policies, industry trends, and external factors.
        Keep the response concise and data-driven.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an ESG analysis expert."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response["choices"][0]["message"]["content"]
    except Exception:
        return "AI analysis unavailable. Check company reports and recent news for details."

@app.route("/api/esg_ai_insights", methods=["GET"])
def get_esg_insights():
    """Fetch ESG AI insights for companies with ESG score changes."""
    company = request.args.get("company")
    year = request.args.get("year")

    anomalies = detect_historical_anomalies()
    for data in anomalies:
        if data["name"] == company:
            for issue in data["anomalies"]:
                if issue["year"] == int(year):
                    return jsonify({
                        "company": company,
                        "year": year,
                        "issue": issue["message"],
                        "ai_insight": generate_ai_insight(company, year, issue["message"])
                    })
    
    return jsonify({"error": "No insights available"}), 404

if __name__ == "__main__":
    app.run(debug=True)
