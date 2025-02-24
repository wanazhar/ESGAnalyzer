from caching_service import get_cached_data, cache_data

@app.route("/api/social_sentiment", methods=["GET"])
def get_social_sentiment():
    """API endpoint to fetch public sentiment on ESG topics."""
    keyword = request.args.get("keyword", "ESG")

    # Check cache first
    cached_data = get_cached_data(keyword)
    if cached_data:
        return jsonify(cached_data)

    # Fetch fresh data if not cached
    twitter_data = fetch_twitter_sentiment(keyword)
    reddit_data = fetch_reddit_sentiment(keyword)
    news_data = fetch_news_sentiment(keyword)

    overall_sentiment = (twitter_data["average_sentiment"] + reddit_data["average_sentiment"] + news_data["average_sentiment"]) / 3

    result = {
        "twitter": twitter_data,
        "reddit": reddit_data,
        "news": news_data,
        "overall_sentiment": overall_sentiment
    }

    # Cache the result
    cache_data(keyword, result)
    
    return jsonify(result)
