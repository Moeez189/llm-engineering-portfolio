from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

system_prompt = "Classify the job post as Remote, Onsite, or Hybrid."

job_post = "Flutter developer needed. Work from our Riyadh office Sunday to Tuesday, rest from home."

# Zero-shot: no examples
zero_shot = client.chat.completions.create(
    model="llama3.2",
    temperature=0,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": job_post},
    ],
)
print("=== Zero-shot ===")
print(zero_shot.choices[0].message.content)

# Few-shot: we show examples first
few_shot = client.chat.completions.create(
    model="llama3.2",
    temperature=0,
    messages=[
        {"role": "system", "content": system_prompt + " Reply with one word only."},
        {"role": "user", "content": "React developer, fully remote, work from anywhere."},
        {"role": "assistant", "content": "Remote"},
        {"role": "user", "content": "Backend engineer, must be in our Lahore office every day."},
        {"role": "assistant", "content": "Onsite"},
        {"role": "user", "content": "Designer, 2 days in the Dubai office, 3 days from home."},
        {"role": "assistant", "content": "Hybrid"},
        {"role": "user", "content": job_post},
    ],
)
print("\n=== Few-shot ===")
print(few_shot.choices[0].message.content)