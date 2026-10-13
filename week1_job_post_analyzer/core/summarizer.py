import json

from core.llm import client, MODEL

SUMMARY_SYSTEM_PROMPT = """You help software developers understand job posts quickly.
You receive verified job details as JSON, plus the original job post text.

Write ONLY these two sections in markdown:
## The Role - 2 or 3 sentences on what the job really involves day to day.
## Questions to Ask - 3 questions to ask in the interview that are specific to this job.

Rules:
- Treat the JSON as the source of truth for facts. Never change or add facts.
- Do not list skills, salary, location or working hours. They are shown separately.
- Avoid generic questions that could apply to any job.
- Keep both sections under 150 words in total.
- Write clearly and simply, without hype."""

FIELD_LABELS = {
    "company": "Company",
    "location": "Location",
    "work_type": "Work type",
    "employment_type": "Employment type",
    "working_hours": "Working hours",
    "experience_years": "Experience (years)",
}


def format_salary(salary):
    """Turn the salary dictionary into a readable line using code, not the model."""
    if not salary:
        return "Not mentioned in the post."

    low = salary.get("min")
    high = salary.get("max")
    currency = salary.get("currency") or ""
    period = salary.get("period")

    if low is None and high is None:
        return "Not mentioned in the post."

    if low is not None and high is not None:
        amount = f"{low:,} - {high:,}"
    else:
        amount = f"{low or high:,}"

    if period:
        period_text = f"per {period}"
    else:
        period_text = "(period not stated, so ask whether this is monthly or yearly)"

    return f"{currency} {amount} {period_text}".strip()


def build_key_facts(details):
    """Build the Key Facts section with code, and collect what's missing."""
    lines = ["## Key Facts"]
    missing = []

    for key, label in FIELD_LABELS.items():
        value = details.get(key)
        if value is None:
            missing.append(label)
        else:
            lines.append(f"- **{label}:** {value}")

    salary = details.get("salary") or {}
    lines.append(f"- **Salary:** {format_salary(salary)}")
    if salary.get("min") is None and salary.get("max") is None:
        missing.append("Salary")

    return "\n".join(lines), missing


def build_skills(details):
    """Build the skills sections with code, straight from the JSON."""
    lines = ["## Required Skills"]
    for skill in details.get("required_skills") or []:
        lines.append(f"- {skill}")

    nice_to_have = details.get("nice_to_have_skills") or []
    if nice_to_have:
        lines.append("\n## Nice to Have")
        for skill in nice_to_have:
            lines.append(f"- {skill}")

    return "\n".join(lines)


def stream_job_summary(page_text, details):
    """Stream the summary: facts from code first, then the model's writing."""
    key_facts, missing = build_key_facts(details)
    yield key_facts + "\n\n"
    yield build_skills(details) + "\n\n"

    if missing:
        yield "## Not Mentioned in the Post\n"
        yield "Ask about these in the interview: " + ", ".join(missing) + "\n\n"

    user_prompt = (
        "Verified job details (JSON):\n"
        f"{json.dumps(details, indent=2, ensure_ascii=False)}\n\n"
        "Original job post text:\n"
        f"{page_text}"
    )

    stream = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        stream=True,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        if text:
            yield text