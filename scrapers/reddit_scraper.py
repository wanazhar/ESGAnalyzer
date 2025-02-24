import praw

def fetch_reddit_comments(keyword):
    reddit = praw.Reddit(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        user_agent="esg-analyzer"
    )
    subreddit = reddit.subreddit("sustainability")
    return [comment.body for comment in subreddit.search(keyword, limit=5)]
