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

load_dotenv()

# 🚫 HARD DISABLE OPENAI
os.environ.pop("OPENAI_API_KEY", None)

# ======================= IMPORTS =====================================
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from guide_generation_flow.llms import research_llm  # ✅ FIXED IMPORT

from crewai_tools import (
    ScrapeWebsiteTool,
    SeleniumScrapingTool,
    ArxivPaperTool,
    FileReadTool,
    DirectoryReadTool
)

from typing import List

# ======================= VALIDATE GROQ ===============================
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("❌ GROQ_API_KEY not found. Check your .env")

# ======================= TOOLS (OPENAI-FREE) =========================
web_scraping_tool = ScrapeWebsiteTool()
selenium_scraping_tool = SeleniumScrapingTool()
arxiv_tool = ArxivPaperTool(download_pdfs=True)

file_reader_tool = FileReadTool()
directory_read_tool = DirectoryReadTool()

# ======================= CREW ========================================
@CrewBase
class ResearchCrew:
    """Research Crew — Groq only, stable, OpenAI-free"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # -------------------- AGENTS -------------------------------------
    @agent
    def research_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["research_manager"],
            llm=research_llm
        )

    @agent
    def web_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["web_specialist"],
            tools=[web_scraping_tool, selenium_scraping_tool],
            llm=research_llm
        )

    @agent
    def arxiv_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["arxiv_specialist"],
            tools=[arxiv_tool],
            llm=research_llm
        )

    @agent
    def document_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["document_specialist"],
            tools=[file_reader_tool, directory_read_tool],
            llm=research_llm
        )

    # -------------------- TASK ---------------------------------------
    @task
    def research_compilation(self) -> Task:
        return Task(
            config=self.tasks_config["research_compilation"]
        )

    # -------------------- CREW ---------------------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.web_specialist(),
                self.arxiv_specialist(),
                self.document_specialist()
            ],
            tasks=[self.research_compilation()],
            process=Process.hierarchical,
            manager_agent=self.research_manager(),
            manager_llm=research_llm,
            planning=False,   # ✅ avoids OpenAI planner
            verbose=True
        )



