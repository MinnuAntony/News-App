import os
import requests

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_BASE = "https://newsapi.org/v2"

def fetch_top_headlines(country=None, category=None, q=None, pageSize=20):
    if not NEWSAPI_KEY:
        raise RuntimeError("NEWSAPI_KEY not set in environment variables")
    
    params = {
        "apiKey": NEWSAPI_KEY,
        "pageSize": pageSize
    }
    if country:
        params["country"] = country
    if category:
        params["category"] = category
    if q:
        params["q"] = q

    resp = requests.get(f"{NEWSAPI_BASE}/top-headlines", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
