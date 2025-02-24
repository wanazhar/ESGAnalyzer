import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    """Scrapes text data from an ESG-related webpage."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    paragraphs = soup.find_all("p")
    extracted_text = " ".join([p.text for p in paragraphs])
    
    return extracted_text

def scrape_sources():
    """Reads external sources from JSON file and scrapes ESG data."""
    with open("config.json") as config_file:
        config = json.load(config_file)
    
    esg_sources = config.get("esg_sources", [])
    scraped_data = {}

    for source in esg_sources:
        scraped_data[source] = scrape_website(source)
    
    with open("backend/esg_scraped_data.json", "w") as f:
        json.dump(scraped_data, f, indent=4)

    print("✅ ESG external sources scraped and saved!")

if __name__ == "__main__":
    scrape_sources()
