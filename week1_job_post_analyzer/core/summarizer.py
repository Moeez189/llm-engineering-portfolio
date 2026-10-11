import json

from core.llm import client, MODEL

SUMMARY_SYSTEM_PROMPT = """You help software developers understand job posts quickly.
You receive verified job details as JSON, plus the original job post text.

Write a short summary in markdown with these sections:
## The Role - 2 or 3 sentences on what the job really involves.
## What You Need - the required skills and experience, then any nice-to-have skills marked as optional.
## Questions to Ask - 3 smart questions to ask in the interview.

Rules:
- Treat the JSON as the source of truth for facts. Never change or add facts.
- Do not mention the salary. It is shown separately.
- Never repeat the same point twice.
- At least one question must be about information that is null in the JSON, because that is what the post leaves unclear.
- Keep the whole summary under 200 words.
- Write clearly and simply, without hype."""


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


def stream_job_summary(page_text, details):
    """Stream a readable summary of the job post, piece by piece."""
    yield "## Salary\n"
    yield format_salary(details.get("salary")) + "\n\n"

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