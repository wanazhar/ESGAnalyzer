import requests

API_KEY = "YOUR_NEWS_API_KEY"

def fetch_news_articles(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
    response = requests.get(url).json()
    return [article["title"] for article in response.get("articles", [])[:5]]
