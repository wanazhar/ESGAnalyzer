import openai
import json
from flask import Flask, request, jsonify
from industry_trend_analysis import analyze_industry_trends
from config import OPENAI_API_KEY

app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

def generate_ai_insights(year):
    """Use AI to generate ESG insights for industry-wide trends."""
    industry_trends = analyze_industry_trends(year)
    
    if not industry_trends:
        return "No available data for analysis."

    prompt = f"""
    Analyze the following industry-wide ESG score changes for {year} and generate insights:
    
    {json.dumps(industry_trends, indent=2)}

    Provide key takeaways in simple bullet points.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an ESG financial analyst."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"

@app.route("/api/industry_ai_insights", methods=["GET"])
def get_industry_ai_insights():
    """Fetch AI-generated ESG insights per industry."""
    year = request.args.get("year")
    insights = generate_ai_insights(year)
    
    return jsonify({"year": year, "insights": insights})

if __name__ == "__main__":
    app.run(debug=True)
