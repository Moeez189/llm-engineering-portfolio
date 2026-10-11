import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

NOISE_TAGS = ["script", "style", "nav", "footer", "header", "img", "input", "svg"]


def fetch_page_text(url, max_chars=8000):
    """Download a webpage and return its title and clean text."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(NOISE_TAGS):
        tag.decompose()

    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = "No title found"

    text = soup.get_text(separator="\n", strip=True)

    return title, text[:max_chars]