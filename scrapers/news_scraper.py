import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("NEWS_API_KEY", "")

def fetch_news_articles(keyword):
    """
    Fetches news articles related to a specific keyword using the News API.
    
    Args:
        keyword (str): The search term to find articles for
        
    Returns:
        list: A list of article titles (up to 5)
    """
    try:
        if not API_KEY:
            print("Warning: NEWS_API_KEY environment variable not set")
            return ["API key not configured - add NEWS_API_KEY to .env file"]
            
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return [f"API Error: {response.status_code} - {response.text}"]
            
        data = response.json()
        return [article["title"] for article in data.get("articles", [])[:5]]
    except Exception as e:
        return [f"Error fetching news: {str(e)}"]
