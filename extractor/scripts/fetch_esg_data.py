import requests
import json
import time

def load_api_keys():
    with open("data/external_esg_sources.json", "r") as file:
        return json.load(file)

def fetch_data_with_fallback(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Attempt {attempt + 1}: Failed to fetch data from {url} (Status Code: {response.status_code})")
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Error fetching data - {e}")
        time.sleep(delay)
    return "Not Available"

def fetch_fmp_esg(symbol, api_key):
    url = f"https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol={symbol}&apikey={api_key}"
    return fetch_data_with_fallback(url)

def fetch_finnhub_esg(symbol, api_key):
    url = f"https://finnhub.io/api/v1/stock/esg?symbol={symbol}&token={api_key}"
    return fetch_data_with_fallback(url)

def fetch_refinitiv_esg(symbol, api_key):
    url = f"https://refinitiv.com/api/v1/esg/{symbol}?apikey={api_key}"
    return fetch_data_with_fallback(url)

def fetch_all_esg(symbol):
    api_keys = load_api_keys()
    
    fmp_data = fetch_fmp_esg(symbol, api_keys["FMP"])
    finnhub_data = fetch_finnhub_esg(symbol, api_keys["Finnhub"])
    refinitiv_data = fetch_refinitiv_esg(symbol, api_keys["Refinitiv"])
    
    return {
        "FMP": fmp_data,
        "Finnhub": finnhub_data,
        "Refinitiv": refinitiv_data
    }

if __name__ == "__main__":
    symbol = "AAPL"  # Example company symbol
    esg_data = fetch_all_esg(symbol)
    print(json.dumps(esg_data, indent=4))
