import os
import requests
import json
from bs4 import BeautifulSoup
from newspaper import Article

# Create a folder to store scraped ESG data
SCRAPED_DATA_FOLDER = "web_scraping"
os.makedirs(SCRAPED_DATA_FOLDER, exist_ok=True)

# Load ESG sources from external file
SOURCES_FILE = os.path.join(SCRAPED_DATA_FOLDER, "esg_sources.json")

def load_sources():
    """Load ESG news & company sources from JSON file."""
    if not os.path.exists(SOURCES_FILE):
        print(f"❌ Error: {SOURCES_FILE} not found!")
        return {"news_sources": [], "company_sources": []}

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_page_content(url):
    """Fetch and parse a webpage using BeautifulSoup."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_news_links(source_url):
    """Extract article links from an ESG news site."""
    soup = fetch_page_content(source_url)
    if not soup:
        return []

    links = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        if "article" in url and url.startswith("http"):  # Filter relevant links
            links.append(url)

    return list(set(links))  # Remove duplicates

def extract_article_content(article_url):
    """Extract text content from an article using newspaper3k."""
    try:
        article = Article(article_url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error extracting article {article_url}: {e}")
        return None

def scrape_esg_news():
    """Scrape ESG news and save content."""
    sources = load_sources()
    all_esg_articles = {}

    for source_url in sources["news_sources"]:
        print(f"🔍 Scraping source: {source_url}")
        article_links = extract_news_links(source_url)

        for link in article_links:
            content = extract_article_content(link)
            if content:
                all_esg_articles[link] = content

    # Save scraped articles
    output_path = os.path.join(SCRAPED_DATA_FOLDER, "esg_news.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_esg_articles, f, indent=4)

    print(f"✅ Scraped ESG news saved: {output_path}")

# Run the scraper
scrape_esg_news()
