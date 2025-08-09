from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from video_generation_crew.tools.video_tool import VideoGenerationTool

@CrewBase
class VideoGenerationCrew():
	"""VideoGenerationCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def video_producer(self) -> Agent:
		return Agent(
			config=self.agents_config['video_producer'],
			tools=[VideoGenerationTool()],
			verbose=True
		)

	@task
	def generate_video_task(self) -> Task:
		return Task(
			config=self.tasks_config['generate_video_task'],
			agent=self.video_producer()
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the VideoGenerationCrew crew"""
		return Crew(
			agents=self.agents, # Automatically resolves the agents in your crew
			tasks=self.tasks, # Automatically resolves the tasks in your crew
			process=Process.sequential,
			verbose=True
		)
