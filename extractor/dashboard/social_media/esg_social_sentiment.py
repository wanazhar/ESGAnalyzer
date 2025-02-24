import requests
import praw
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API (Mock Example)
def fetch_twitter_sentiment(keyword):
    """Fetch tweets related to ESG and analyze sentiment."""
    # Mock data (Replace with Twitter API call)
    tweets = [
        f"{keyword} company is greenwashing again! Not happy. 😡",
        f"{keyword} just published their sustainability report, looks promising! 😊",
        f"More corporate ESG propaganda from {keyword}. 🤨"
    ]

    sentiments = [{"tweet": t, "score": analyzer.polarity_scores(t)} for t in tweets]
    return sentiments

# Reddit API (Using PRAW)
def fetch_reddit_sentiment(keyword):
    """Fetch ESG discussions from Reddit and analyze sentiment."""
    reddit = praw.Reddit(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        user_agent="esg-analyzer"
    )

    subreddit = reddit.subreddit("sustainability")
    comments = [comment.body for comment in subreddit.search(keyword, limit=5)]

    sentiments = [{"comment": c, "score": analyzer.polarity_scores(c)} for c in comments]
    return sentiments

# OpenAI GPT for News Sentiment
def fetch_news_sentiment(keyword):
    """Fetch ESG-related news and analyze sentiment."""
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey=YOUR_NEWSAPI_KEY"
    response = requests.get(url).json()

    articles = response.get("articles", [])
    news_analysis = []

    for article in articles[:5]:
        text = article["title"] + " " + article["description"]
        gpt_analysis = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "Analyze the ESG sentiment of this news."},
                      {"role": "user", "content": text}]
        )
        sentiment = gpt_analysis["choices"][0]["message"]["content"]
        news_analysis.append({"title": article["title"], "sentiment": sentiment})

    return news_analysis

# Example Run
company = "Tesla"
print("📢 Twitter Sentiment:", fetch_twitter_sentiment(company))
print("🗣️ Reddit Sentiment:", fetch_reddit_sentiment(company))
print("📰 News Sentiment:", fetch_news_sentiment(company))
