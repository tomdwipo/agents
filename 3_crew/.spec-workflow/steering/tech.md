# Technical Steering

## Architecture Overview
- **System Architecture**: The project is a monorepo of specialized, self-contained AI-powered crews built with the crewAI framework. Each crew operates as an independent multi-agent system designed for a specific task.
- **Technology Stack**: The core technology stack across all crews is Python, crewAI, and Pydantic. Specific crews leverage additional libraries like Pillow for image manipulation and the OpenAI SDK for interacting with language models.
- **Integration Patterns**: Crews are designed to be modular and independent. They are invoked via a `main.py` entry point and do not directly interact with each other.
- **Data Flow**: Each crew defines its own data flow, typically starting with a set of inputs, processing them through a series of agent-led tasks, and producing a final output, such as a report or a set of generated files.

## Development Standards
- **Coding Conventions**: All Python code should adhere to the PEP 8 style guide. Pydantic is used for data validation and creating clear data schemas.
- **Testing Requirements**: While not yet implemented, each crew should have its own set of unit tests for its tools and agents, and integration tests for the overall crew execution.
- **Security Guidelines**: API keys and other sensitive information must be managed through environment variables (`.env` files) and should never be hardcoded.
- **Performance Standards**: Each crew should be optimized for its specific task. For crews involving external API calls, resilience and error handling (e.g., fallbacks, retries) are important.

## Technology Choices
- **Programming Language**: Python 3.10+
- **Frameworks and Libraries**: 
  - **Core:** crewAI, Pydantic, `uv` (for dependency management).
  - **Content Crew:** Pillow, OpenAI Python SDK.
  - **Other Crews:** The specific dependencies for each crew are defined in their respective `pyproject.toml` files.
- **Development Tools**: `uv` is the standard tool for dependency management across all crews.
- **Deployment Infrastructure**: All crews are designed to be run locally from the command line.

## Patterns & Best Practices
- **YAML-driven Configuration**: Each crew's agents and tasks are defined in YAML files, separating configuration from the core logic.
- **Tool Abstraction**: Complex or reusable logic is encapsulated in custom crewAI tools.
- **Modularity and Independence**: Each crew is a self-contained project within the monorepo, with its own source code, dependencies, and entry point. This promotes separation of concerns and makes it easy to work on individual crews without affecting others.