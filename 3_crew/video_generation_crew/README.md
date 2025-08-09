# Video Generation Crew

Welcome to the Video Generation Crew project, powered by [crewAI](https://crewai.com). This crew is designed to generate a short, iconography-based video from a given topic.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

First, install uv:

```bash
pip install uv
```

Next, install the dependencies:

```bash
uv sync
```

## Customizing

- **Add your `OPENAI_API_KEY` into the `.env` file.**
- Modify `src/video_generation_crew/config/agents.yaml` to define your agents.
- Modify `src/video_generation_crew/config/tasks.yaml` to define your tasks.
- Modify `src/video_generation_crew/crew.py` to add your own logic and tools.
- Modify `src/video_generation_crew/main.py` to add custom inputs.

## Running the Project

To run the crew, use the following command from the `3_crew/video_generation_crew` directory:

```bash
crewai run
```

This will generate a video in the `output` directory based on the default topic "Daily Improvement".
