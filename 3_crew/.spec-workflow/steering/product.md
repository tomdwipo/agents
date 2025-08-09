# Product Steering

## Vision & Mission
- **What problem does this project solve?** This project is a monorepo of specialized AI-powered crews, each designed to automate a specific, complex task. It addresses the inefficiency of manual work in areas like content creation, financial research, coding, and software engineering, providing a collection of ready-to-use, autonomous agents.
- **Who are the target users?** The target users vary by crew, but generally include developers, content creators, financial analysts, and anyone looking to leverage AI to automate their workflows.
- **What is the long-term vision?** To build a comprehensive and extensible ecosystem of specialized AI crews that can be easily combined and customized to tackle a wide range of complex problems, effectively creating a 'workforce' of AI agents.

## User Experience Principles
- **Clarity and Focus:** Each crew has a single, well-defined purpose and produces a clear, understandable output.
- **Ease of Use:** All crews are designed to be run with a single command and sensible defaults, requiring minimal configuration for a standard run.
- **Transparency:** The logs and outputs of each crew are clear and easy to follow, allowing users to understand the agent's process.

## Feature Priorities

### Content Crew
- **Must-have features:**
  - A sequential pipeline of four distinct agents: `carousel_planner`, `copywriter`, `image_prompt_engineer`, and `compositor`.
  - Generation of a 7-slide carousel based on a default topic.
  - Application of brand assets, including a logo and specific fonts and colors.
  - Creation of a unique, slugified output directory for each run.
  - Generation of a final `metadata.json` file with caption, hashtags, and alt texts.

### Financial Researcher Crew
- **Must-have features:**
  - Takes a company name as input.
  - Conducts research on the specified company.
  - Generates a detailed financial report in `output/report.md`.

### Stock Picker Crew
- **Must-have features:**
  - Takes a stock market sector as input.
  - Researches and analyzes stocks within that sector.
  - Generates a report with a final decision on stock picks.

### Coder Crew
- **Must-have features:**
  - Takes a coding-related task or problem as input.
  - Generates a report or solution in `report.md`.

### A0 Crew
- **Must-have features:**
  - A general-purpose research crew.
  - Takes a topic as input.
  - Generates a research report in `report.md`.

### Debate Crew
- **Must-have features:**
  - Simulates a debate between two AI agents on a given topic.
  - Generates a transcript of the debate.

### Engineering Team Crew
- **Must-have features:**
  - Takes a set of software requirements as input.
  - Generates a Python module and class that implement the requirements.

## Success Metrics

### Content Crew
- A successful run must produce a complete set of artifacts: 7 raw images, 7 composed slides, `prompts.json`, and `metadata.json`.

### Financial Researcher Crew
- A successful run must generate a comprehensive and accurate financial report in `output/report.md`.

### Stock Picker Crew
- A successful run must generate a well-reasoned stock picking report with a clear final decision.

### Coder Crew
- A successful run must generate a relevant and accurate report or solution to the given coding task.

### A0 Crew
- A successful run must generate a comprehensive research report on the given topic.

### Debate Crew
- A successful run must generate a coherent and well-structured debate transcript.

### Engineering Team Crew
- A successful run must generate a Python module and class that correctly implement the provided software requirements.