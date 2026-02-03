import os

# 🔥 FORCE a valid LiteLLM log level (this fixes the crash)
os.environ["LITELLM_LOG"] = "ERROR"

# 🔕 Optional LiteLLM noise reduction (safe)
os.environ["LITELLM_DISABLE_TELEMETRY"] = "true"
os.environ["LITELLM_DISABLE_COLD_STORAGE"] = "true"
os.environ["LITELLM_DISABLE_SPEND_LOGGING"] = "true"

# 🚫 DO NOT SET THESE (they cause issues)
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("XAI_API_KEY", None)



# ======================= ENV SETUP ===================================
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# 🚫 HARD BLOCK ALL CLOUD FALLBACKS
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("XAI_API_KEY", None)

# ======================= IMPORTS =====================================
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from guide_generation_flow.llms import writing_llm  # ✅ Ollama ONLY

# ======================= CREW ========================================
@CrewBase
class WritingCrew:
    """Writing Crew — Ollama only (local, unlimited, stable)"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # -------------------- AGENTS -------------------------------------
    @agent
    def technical_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_writer"],
            llm=writing_llm
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["content_editor"],
            llm=writing_llm
        )

    # -------------------- TASKS --------------------------------------
    @task
    def write_getting_started_guide(self) -> Task:
        return Task(
            config=self.tasks_config["write_getting_started_guide"]
        )

    @task
    def review_and_polish_guide(self) -> Task:
        return Task(
            config=self.tasks_config["review_and_polish_guide"]
        )

    # -------------------- CREW ---------------------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.technical_writer(),
                self.content_editor()
            ],
            tasks=[
                self.write_getting_started_guide(),
                self.review_and_polish_guide()
            ],
            process=Process.sequential,
            verbose=True
        )

