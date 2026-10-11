from core.scraper import fetch_page_text

url = "https://www.jobleads.com/pk/job/flutter-developer-mid-level--lahore--e15652dba6735b55f7740711ba23fef59?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"

title, text = fetch_page_text(url)

print("Title:", title)
print("Characters:", len(text))
print("-" * 50)
print(text[:1500])