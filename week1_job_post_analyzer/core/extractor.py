import json

from core.llm import client, MODEL

EXTRACT_SYSTEM_PROMPT = """You extract facts from job posts.
Reply ONLY with JSON using exactly these keys:
{
  "title": string,
  "company": string or null,
  "location": string or null,
  "work_type": "Remote", "Onsite", "Hybrid" or null,
  "salary": {
    "min": number or null,
    "max": number or null,
    "currency": string or null,
    "period": "month", "year" or null
  },
  "experience_years": number or null,
  "required_skills": list of strings,
  "nice_to_have_skills": list of strings
}

Rules:
- Use only information written in the job post. Never guess or invent anything.
- If something is not mentioned, use null. Use an empty list if there are no skills.
- Skills described as "nice to have", "a plus" or "bonus" go in nice_to_have_skills only.
- Write salary numbers without commas, for example 15000.
- "company" is the organization that is hiring. It is often named in sentences like "X is seeking" or "X is hiring".
- Only fill "period" if the post clearly says per month or per year.
- Ignore website text that is not part of the job, such as buttons, ads and menus."""


def extract_job_details(page_text):
    """Send the job post text to the model and return its details as a dictionary."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": EXTRACT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the job post:\n\n{page_text}"},
        ],
    )

    raw_text = response.choices[0].message.content

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return None