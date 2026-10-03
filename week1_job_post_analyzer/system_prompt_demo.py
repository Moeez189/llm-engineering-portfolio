from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def ask(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


question = "What is Flutter?"

print("=== Teacher for kids ===")
print(ask("You explain things to a 10-year-old in 2 simple sentences.", question))

print("\n=== Senior interviewer ===")
print(ask("You are a strict technical interviewer. Answer in 3 precise technical bullet points.", question))

print("\n=== Pirate ===")
print(ask("You are a pirate. Always talk like a pirate, in 2 sentences.", question))