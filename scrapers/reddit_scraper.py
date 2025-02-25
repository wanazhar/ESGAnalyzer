import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API credentials
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ESGAnalyzer/1.0")

def fetch_reddit_posts(subreddit, query, limit=5):
    """
    Fetches Reddit posts related to a specific keyword from a subreddit.
    
    Args:
        subreddit (str): Subreddit to search in
        query (str): Search term
        limit (int): Maximum number of posts to return
        
    Returns:
        list: A list of post titles
    """
    try:
        if not CLIENT_ID or not CLIENT_SECRET:
            print("Warning: Reddit API credentials not configured")
            return ["Reddit API credentials not configured - add to .env file"]
            
        # Reddit API authentication
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        headers = {"User-Agent": USER_AGENT}
        
        # Search for posts
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&limit={limit}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return [f"Reddit API Error: {response.status_code}"]
            
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        return [post["data"]["title"] for post in posts]
    except Exception as e:
        return [f"Error fetching Reddit posts: {str(e)}"]
