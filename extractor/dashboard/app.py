from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_esg_trends/<year>")
def get_esg_trends(year):
    with open("backend/esg_trend_data.json") as f:
        trend_data = json.load(f)
    return jsonify(trend_data.get(year, []))

if __name__ == "__main__":
    app.run(debug=True)
