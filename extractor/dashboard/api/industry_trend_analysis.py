import pandas as pd
from flask import Flask, request, jsonify
from data_fetcher import fetch_esg_data

app = Flask(__name__)

def analyze_industry_trends(year):
    """Analyze ESG trends across industries."""
    esg_data = fetch_esg_data(year)
    if not esg_data:
        return []

    df = pd.DataFrame(esg_data)

    # Calculate industry-wide ESG score changes
    industry_avg = df.groupby("industry")[["esg_score"]].mean().reset_index()
    prev_year_data = fetch_esg_data(str(int(year) - 1))
    
    if prev_year_data:
        prev_df = pd.DataFrame(prev_year_data)
        prev_industry_avg = prev_df.groupby("industry")[["esg_score"]].mean().reset_index()
        merged = industry_avg.merge(prev_industry_avg, on="industry", suffixes=("_current", "_previous"))
        merged["change"] = merged["esg_score_current"] - merged["esg_score_previous"]
    else:
        merged = industry_avg
        merged["change"] = 0

    return merged.sort_values(by="change", ascending=True).to_dict(orient="records")

@app.route("/api/industry_trends", methods=["GET"])
def get_industry_trends():
    """Fetch industry ESG trends."""
    year = request.args.get("year")
    trends = analyze_industry_trends(year)
    
    return jsonify(trends)

if __name__ == "__main__":
    app.run(debug=True)
