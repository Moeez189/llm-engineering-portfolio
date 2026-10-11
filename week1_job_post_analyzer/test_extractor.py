import json

from core.scraper import fetch_page_text
from core.extractor import extract_job_details

url = "https://www.jobleads.com/pk/job/flutter-developer-mid-level--lahore--e15652dba6735b55f7740711ba23fef59?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
# url= "https://www.linkedin.com/jobs/view/4448906837/?alternateChannel=search&eBP=NOT_ELIGIBLE_FOR_CHARGING&refId=mz0r183FhuKPlXcSpZ8HLA%3D%3D&trackingId=Ny1%2B7UmtrOzNRnUw696xLA%3D%3D"
title, text = fetch_page_text(url)
details = extract_job_details(text)

if details is None:
    print("The model did not return valid JSON.")
else:
    print(json.dumps(details, indent=2, ensure_ascii=False))