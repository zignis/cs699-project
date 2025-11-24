import requests
import time
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

CACHE_TTL = 3 * 60 * 60 # 3 hours
__SEARCH_CACHE__ = {}

def duckduckgo_search(query, limit=10):
    url = f"https://duckduckgo.com/html/?q={query.replace(' ', '%20')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    results = []

    for r in soup.select(".result")[:limit]:
        link = r.select_one(".result__url")
        title = r.select_one(".result__title")
        snippet = r.select_one(".result__snippet")
        if title and link:
            results.append({
                "title": title.text.strip(),
                "url": link.get("href", ""),
                "snippet": snippet.text.strip() if snippet else ""
            })
    return results

def brave_search(query, limit=10):
    url = f"https://search.brave.com/search?q={query.replace(' ', '%20')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    results = []

    for r in soup.select(".snippet")[:limit]:
        title = r.select_one(".snippet-title")
        link = r.select_one("a")
        snippet = r.select_one(".snippet-content")
        if title and link:
            results.append({
                "title": title.text.strip(),
                "url": link.get("href", ""),
                "snippet": snippet.text.strip() if snippet else ""
            })
    return results

def reddit_search(query, limit=10):
    url = f"https://old.reddit.com/search/?q={query.replace(' ', '%20')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    results = []

    for post in soup.select(".search-result")[:limit]:
        title = post.select_one("a.search-title")
        snippet = post.select_one(".search-result-meta")
        if title:
            results.append({
                "title": title.text.strip(),
                "url": title.get("href", ""),
                "snippet": snippet.text.strip() if snippet else ""
            })
    return results

def wikipedia_search(query, limit=10):
    url = f"https://en.wikipedia.org/w/index.php?search={query.replace(' ', '%20')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=5).text, "html.parser")
    results = []

    for r in soup.select(".mw-search-result")[:limit]:
        title = r.select_one(".mw-search-result-heading a")
        snippet = r.select_one(".searchresult")
        if title:
            results.append({
                "title": title.text.strip(),
                "url": f"https://en.wikipedia.org{title.get('href')}",
                "snippet": snippet.text.strip() if snippet else ""
            })
    return results


def aggregated_search(query):
    now = time.time()
    key = query.lower().strip()

    if key in __SEARCH_CACHE__:
        timestamp, cached_results = __SEARCH_CACHE__[key]
        if now - timestamp < CACHE_TTL:
            return cached_results

    results = []

    try:
        results.extend(duckduckgo_search(query))
    except:
        pass

    try:
        results.extend(brave_search(query))
    except:
        pass

    try:
        results.extend(reddit_search(query))
    except:
        pass

    try:
        results.extend(wikipedia_search(query))
    except:
        pass

    results = results[:10]
    __SEARCH_CACHE__[key] = (now, results)

    return results
