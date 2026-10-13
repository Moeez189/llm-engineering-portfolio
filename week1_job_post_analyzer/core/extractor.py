import json

from core.llm import client, MODEL

EXTRACT_SYSTEM_PROMPT = """You extract facts from job posts.
Reply ONLY with JSON using exactly these keys:
{
  "title": string,
  "company": string or null,
  "location": string or null,
  "work_type": "Remote", "Onsite", "Hybrid" or null,
  "employment_type": string or null,
  "working_hours": string or null,
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
- "company" is the organization that is hiring. It is often named in sentences like "X is seeking" or "X is hiring".
- "employment_type" is the type of contract, such as Full-time, Part-time or Contract. Copy what the post says.
- "working_hours" is the shift or timings exactly as written, for example "4 pm to 12 am, Monday to Friday".
- Check every skill line on its own. If a line says "nice to have", "a plus", "bonus" or "preferred", put it in nice_to_have_skills only, even if it appears under a "Required" heading.
- When the post offers a choice, like "Flutter or React Native", keep the choice together as one skill, written exactly like "Flutter or React Native". Never split a choice into separate skills.
- Keep each skill short, for example "RAG" instead of "Knowledge of Retrieval-Augmented Generation (RAG)".
- Write salary numbers without commas, for example 15000.
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
        details = json.loads(raw_text)
    except json.JSONDecodeError:
        return None

    for key in ["required_skills", "nice_to_have_skills"]:
        skills = details.get(key) or []
        details[key] = list(dict.fromkeys(skills))

    return details