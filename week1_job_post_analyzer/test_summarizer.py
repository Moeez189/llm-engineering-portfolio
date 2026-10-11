from core.scraper import fetch_page_text
from core.extractor import extract_job_details
from core.summarizer import stream_job_summary

url = "https://www.jobleads.com/pk/job/flutter-developer-mid-level--lahore--e15652dba6735b55f7740711ba23fef59?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"

title, text = fetch_page_text(url)
details = extract_job_details(text)

if details is None:
    print("Extraction failed, so no summary can be written.")
else:
    for piece in stream_job_summary(text, details):
        print(piece, end="", flush=True)
    print()