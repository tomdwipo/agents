# Structure Steering

## Project Organization
- **Directory Structure**: The `3_crew` directory is a monorepo containing multiple, independent crew projects. Each crew has its own subdirectory (e.g., `content`, `coder`, `financial_researcher`) and follows a standardized structure:
  - `src/<crew_name>`: Contains the core source code for the crew.
    - `config`: Holds `agents.yaml` and `tasks.yaml` for defining the crew's agents and their tasks.
    - `tools`: Contains custom tools developed specifically for the crew.
    - `crew.py`: Defines the crew, its agents, and the overall workflow.
    - `main.py`: Serves as the entry point for running the crew with default inputs.
  - `knowledge`: Optional directory for storing knowledge base files for the agents.
  - `output`: The default directory where the crew's output (e.g., reports, generated files) is saved.
  - `pyproject.toml`: Defines the project metadata and dependencies for the specific crew.
  - `.env`: For storing environment variables, such as API keys.
- **File Naming Conventions**: Python files are named using snake_case (e.g., `crew.py`).
- **Configuration Management**: All crews are configured using YAML files for agents and tasks, promoting a clear separation of configuration from code.

## Development Workflow
- **Git Branching Strategy**: A feature-branch workflow is recommended. Each new feature or bug fix should be developed in its own branch.
- **Code Review Process**: All code changes should be submitted as pull requests and reviewed by at least one other developer before being merged.
- **Testing Workflow**: Each crew should have its own suite of tests. New features should be accompanied by unit and integration tests.
- **Deployment Process**: All crews are designed to be run locally from the command line. There is no standardized deployment process.

## Documentation Structure
- **Where to find what**:
  - Crew-specific source code: `src/<crew_name>`
  - Crew-specific configuration: `src/<crew_name>/config`
  - Shared project documentation: `docs`
  - Memory bank: `.kilocode/rules/memory-bank`
  - Specifications: `.spec-workflow/specs`
- **How to update docs**: Documentation should be updated in conjunction with any relevant code changes.

## Team Conventions
- **Communication Guidelines**: (Not yet defined)
- **Meeting Structures**: (Not yet defined)
- **Decision-making Process**: (Not yet defined)
- **Knowledge Sharing**: The memory bank and the steering documents serve as the primary sources of truth for the project.