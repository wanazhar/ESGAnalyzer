from flask import Flask, request, jsonify
from esg_sentiment_analysis import analyze_sentiment
from reddit_scraper import fetch_reddit_comments
from twitter_scraper import fetch_tweets
from news_scraper import fetch_news_articles

app = Flask(__name__)

@app.route("/api/social_sentiment", methods=["POST"])
def get_social_sentiment():
    data = request.json
    company = data.get("company")

    twitter_sentiments = [analyze_sentiment(t) for t in fetch_tweets(company)]
    reddit_sentiments = [analyze_sentiment(r) for r in fetch_reddit_comments(company)]
    news_sentiments = [analyze_sentiment(n) for n in fetch_news_articles(company)]

    return jsonify({
        "Twitter": twitter_sentiments,
        "Reddit": reddit_sentiments,
        "News": news_sentiments
    })

if __name__ == "__main__":
    app.run(port=5020)
