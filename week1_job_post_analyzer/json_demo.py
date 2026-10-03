import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

system_prompt = """You extract information from job posts.
Reply ONLY with JSON using exactly these keys:
"title" (string), "location" (string), "salary" (string or null), "skills" (list of strings).
If information is not in the post, use null. Never invent information."""

job_post = """We are hiring a Senior Flutter Developer in Jeddah.
You must know Dart, Firebase, and REST APIs. Experience with Riverpod is a plus.
Salary: 15,000 - 20,000 SAR per month."""

response = client.chat.completions.create(
    model="llama3.2",
    temperature=0,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": job_post},
    ],
)

raw_text = response.choices[0].message.content
print("Raw text from model:")
print(raw_text)

try:
    data = json.loads(raw_text)
    print("\nTitle:", data.get("title"))
    print("Location:", data.get("location"))
    print("Salary:", data.get("salary"))
    for skill in data.get("skills", []):
        print(" -", skill)
except json.JSONDecodeError:
    print("The model did not return valid JSON.")