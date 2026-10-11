from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# MODEL = "llama3.2"
MODEL = "qwen2.5:7b"