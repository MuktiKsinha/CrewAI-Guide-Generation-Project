from guide_generation_flow.llms import research_llm, writing_llm

print("Groq:", research_llm.call("One line about AI"))
print("Ollama:", writing_llm.call("One line about data science"))