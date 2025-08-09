# Architecture

## System Overview
- The `3_crew` project is a monorepo containing a collection of specialized, multi-agent AI systems built with the crewAI framework.
- Each subdirectory in `3_crew` represents a self-contained crew designed to automate a specific, complex task.
- The crews are designed to be independent and are run via their own `main.py` entry points.

## Key Components and Relationships

### Content Crew
- **Purpose:** Generates Instagram carousel content with brand overlays.
- **Agents:** `carousel_planner`, `copywriter`, `image_prompt_engineer`, `compositor`.
- **Key Tools:** `DallETool`, `ComposeSlideTool`, `ExportMetadataTool`.
- **Source:** `3_crew/content/`

### Financial Researcher Crew
- **Purpose:** Conducts financial research on a given company and generates a report.
- **Source:** `3_crew/financial_researcher/`

### Stock Picker Crew
- **Purpose:** Researches and analyzes stocks within a given sector and provides recommendations.
- **Source:** `3_crew/stock_picker/`

### Coder Crew
- **Purpose:** A general-purpose crew that takes a coding task and generates a report or solution.
- **Source:** `3_crew/coder/`

### A0 Crew
- **Purpose:** A general-purpose research crew that takes a topic and generates a report.
- **Source:** `3_crew/a0/`

### Debate Crew
- **Purpose:** Simulates a debate between two AI agents on a given topic.
- **Source:** `3_crew/debate/`

### Engineering Team Crew
- **Purpose:** Takes a set of software requirements and generates a Python module and class.
- **Source:** `3_crew/engineering_team/`

## Common Patterns
- **YAML Configuration:** All crews use `agents.yaml` and `tasks.yaml` to define their agents and tasks.
- **Pydantic Models:** Data structures are defined using Pydantic models for type safety and validation.
- **`uv` for Dependencies:** `uv` is used for dependency management across all crews.