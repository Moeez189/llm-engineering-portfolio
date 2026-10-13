import requests

from core.scraper import fetch_page_text
from core.extractor import extract_job_details
from core.summarizer import stream_job_summary

MAX_CHARS = 8000


def get_text_from_url():
    """Ask for a URL, scrape it, and return the text, or None if it fails."""
    url = input("Paste the job post URL: ").strip()

    try:
        title, text = fetch_page_text(url, max_chars=MAX_CHARS)
    except requests.exceptions.HTTPError as error:
        print(f"\nThis site refused the request (error {error.response.status_code}).")
        print("Many job sites block automated access. Try option 2 and paste the text instead.")
        return None
    except requests.exceptions.RequestException:
        print("\nCould not reach this URL. Check the link and your internet connection.")
        return None

    if len(text) < 300:
        print("\nThis page has almost no text. It may be built with JavaScript.")
        print("Try option 2 and paste the text instead.")
        return None

    return text


def get_pasted_text():
    """Let the user paste a job post across many lines, ending with END."""
    print("Paste the job post text. When you're done, type END on a new line and press Enter.")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    return "\n".join(lines)[:MAX_CHARS]


def get_job_text():
    """Ask the user how they want to provide the job post."""
    choice = input("Analyze (1) a URL or (2) pasted text? Enter 1 or 2: ").strip()

    if choice == "1":
        return get_text_from_url()
    elif choice == "2":
        return get_pasted_text()
    else:
        print("Please run the program again and enter 1 or 2.")
        return None


def main():
    text = get_job_text()
    if not text:
        return

    print("\nExtracting job details...")
    details = extract_job_details(text)

    if details is None:
        print("Sorry, the model couldn't read this job post. Please try again.")
        return
    print()
    for piece in stream_job_summary(text, details):
        print(piece, end="", flush=True)
    print()


if __name__ == "__main__":
    main()