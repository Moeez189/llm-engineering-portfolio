from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = "ollama"  # "ollama" for free local models, "openai" for frontier models

if PROVIDER == "openai":
    client = OpenAI()
    MODEL = "gpt-4.1-mini"
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    MODEL = "qwen2.5:14b"