import os
from crewai import LLM

# 🔍 Research LLM — Groq (short, fast, cheap)
research_llm = LLM(
    provider="groq",
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=350,
)

# ✍️ Writing LLM — Ollama (local, unlimited)
writing_llm = LLM(
    provider="ollama",
    model="llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.2,
)