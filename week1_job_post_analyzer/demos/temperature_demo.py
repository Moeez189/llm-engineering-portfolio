from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

question = "Give me one catchy name for a job-post analyzer app. Reply with the name only."

for temp in [0, 0.7, 1.5]:
    print(f"=== Temperature {temp} ===")
    for attempt in range(3):
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[{"role": "user", "content": question}],
            temperature=temp,
        )
        print(response.choices[0].message.content.strip())
    print()