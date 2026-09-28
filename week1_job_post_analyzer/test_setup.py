from openai import OpenAI

# Ollama exposes an OpenAI-compatible API, so the same client works for both
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Give me 3 skills a junior AI engineer needs."},
    ],
)
print(len(response.choices))
print(response.choices[0].message.content)