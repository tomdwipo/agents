from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import DallETool, SerperDevTool
from typing import List

# Tools for the carousel pipeline
from content.tools.openai_images import GenerateImageTool
from content.tools.composer import ComposeSlideTool
from content.tools.save_json import SaveJSONTool
from content.tools.image_utils import AddLogoToImageTool
from content.tools.text_utils import AddTextToImageTool


@CrewBase
class Content():
    """Content crew with Instagram carousel generation pipeline"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # New agents for the carousel pipeline
    @agent
    def carousel_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['carousel_planner'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['copywriter'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def image_prompt_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['image_prompt_engineer'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def compositor(self) -> Agent:
        # Attach tools needed to generate images, compose overlays, and export metadata
        return Agent(
            config=self.agents_config['compositor'],  # type: ignore[index]
            tools=[
                GenerateImageTool(),
                AddLogoToImageTool(),
                AddTextToImageTool(),
            ],
            verbose=True
        )  

    # Carousel pipeline tasks
    @task
    def plan_carousel_task(self) -> Task:
        return Task(
            config=self.tasks_config['plan_carousel'],  # type: ignore[index]
        )

    @task
    def write_copy_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_copy'],  # type: ignore[index]
        )

    @task
    def engineer_prompts_task(self) -> Task:
        return Task(
            config=self.tasks_config['engineer_prompts'],  # type: ignore[index]
        )

    @task
    def generate_images_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_image'],  # type: ignore[index]
        )
    
    @task
    def generate_images_logo_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_add_logo_to_image'],  # type: ignore[index]
        )
    @task
    def generate_text_to_image(self) -> Task:
        return Task(
            config=self.tasks_config['generate_text_to_image'],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Content crew with the Instagram carousel pipeline"""
        # Explicitly wire only the carousel pipeline agents and tasks in order      
        return Crew(
            agents=[
                self.carousel_planner(),
                self.copywriter(),
                self.image_prompt_engineer(),
                self.compositor(),
            ],
            tasks=[
                self.plan_carousel_task(),
                self.write_copy_task(),
                self.engineer_prompts_task(),
                self.generate_images_task(),
                self.generate_images_logo_task(),
                self.generate_text_to_image()
            ],
            process=Process.sequential,
            verbose=True,
        )
