import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

def fetch_tweets(keyword, count=5):
    """
    Fetches tweets related to a specific keyword using the Twitter API.
    
    Args:
        keyword (str): Search term for tweets
        count (int): Maximum number of tweets to return
        
    Returns:
        list: A list of tweet texts
    """
    try:
        if not TWITTER_BEARER_TOKEN:
            print("Warning: Twitter API credentials not configured")
            return ["Twitter API credentials not configured - add TWITTER_BEARER_TOKEN to .env file"]
            
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Twitter API v2 endpoint for searching recent tweets
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results={count}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return [f"Twitter API Error: {response.status_code} - {response.text}"]
            
        data = response.json()
        tweets = data.get("data", [])
        return [tweet["text"] for tweet in tweets]
    except Exception as e:
        return [f"Error fetching tweets: {str(e)}"]
