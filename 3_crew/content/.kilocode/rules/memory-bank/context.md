# Context

This document captures the current state of the Content Crew project, recent changes, and immediate next steps. It is short and factual.

Current focus
- Add an Instagram carousel generator pipeline integrated into the existing crewAI project.
- Generate 7-slide educational carousels, text-first with brand overlays and logo.
- Ensure outputs are persisted as task artifacts and exported to a deterministic folder.

Recent changes
- New pipeline integrated and runnable via crewAI:
  - Agents and tasks extended in:
    - [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml)
    - [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml)
  - Crew wiring updated:
    - [3_crew/content/src/content/crew.py](3_crew/content/src/content/crew.py)
  - Entrypoint inputs extended:
    - [3_crew/content/src/content/main.py](3_crew/content/src/content/main.py)
- Data models and tools added:
  - Types/schemas:
    - [3_crew/content/src/content/types.py](3_crew/content/src/content/types.py)
  - Templates/prompts:
    - [3_crew/content/src/content/tools/templates.py](3_crew/content/src/content/tools/templates.py)
  - Brand helpers:
    - [3_crew/content/src/content/tools/brand.py](3_crew/content/src/content/tools/brand.py)
  - IO utils:
    - [3_crew/content/src/content/tools/io_utils.py](3_crew/content/src/content/tools/io_utils.py)
  - OpenAI image generation tool (currently configured for DALL·E 3 with fallback placeholder):
    - [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py)
  - Slide compositor (Pillow-based overlays, InterVariable font, logo bottom-right):
    - [3_crew/content/src/content/tools/composer.py](3_crew/content/src/content/tools/composer.py)
  - Export metadata + caption writer:
    - [3_crew/content/src/content/tools/export_metadata.py](3_crew/content/src/content/tools/export_metadata.py)
  - Generic JSON saver utility tool:
    - [3_crew/content/src/content/tools/save_json.py](3_crew/content/src/content/tools/save_json.py)
- Execution plan documentation added:
  - [3_crew/content/docs/execution-plan.md](3_crew/content/docs/execution-plan.md)
- Project dependencies updated for new functionality:
  - [3_crew/content/pyproject.toml](3_crew/content/pyproject.toml)
    - Added: openai, pillow, pydantic, python-slugify

Key behaviors and decisions
- Output structure (per carousel slug):
  - Base: [3_crew/content/output/carousels/{slug}/](3_crew/content/output/carousels/{slug}/)
  - Raw images (1024x1024): [3_crew/content/output/carousels/{slug}/raw/](3_crew/content/output/carousels/{slug}/raw/)
  - Final slides (1080x1350): [3_crew/content/output/carousels/{slug}/slides/](3_crew/content/output/carousels/{slug}/slides/)
  - Prompts trace: [3_crew/content/output/carousels/{slug}/prompts.json](3_crew/content/output/carousels/{slug}/prompts.json)
  - Metadata: [3_crew/content/output/carousels/{slug}/metadata.json](3_crew/content/output/carousels/{slug}/metadata.json) (stored as task artifact)
- Brand style (defaults; override via inputs):
  - Primary #000000, Secondary #FFFFFF, font InterVariable, logo bottom-right
  - Brand assets paths:
    - [3_crew/content/assets/logo.png](3_crew/content/assets/logo.png)
    - [3_crew/content/assets/fonts/InterVariable.ttf](3_crew/content/assets/fonts/InterVariable.ttf)
- Image model configuration:
  - Default model set to DALL·E 3 in [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py)
  - If image API errors (e.g., org unverified), pipeline continues by producing valid placeholder PNGs to allow composition and export to complete
- Composition:
  - Canvas 1080x1350, safe margins, title top, body mid, optional CTA near bottom, logo bottom-right
  - High-contrast black/white overlays for readability

How to run
- Ensure .env has OPENAI_API_KEY (already present).
- From project root:
  - uv sync
  - crewai run
- Default inputs are defined in [3_crew/content/src/content/main.py](3_crew/content/src/content/main.py). To change topic/brand, edit those inputs (topic, colors, assets paths).

Immediate next steps
- Verify OpenAI organization for image usage; if authorized, optionally switch model to gpt-image-1 in [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py)
- Add/confirm brand assets:
  - [3_crew/content/assets/logo.png](3_crew/content/assets/logo.png)
  - [3_crew/content/assets/fonts/InterVariable.ttf](3_crew/content/assets/fonts/InterVariable.ttf)
- Write README usage updates (env, run commands, outputs) and add troubleshooting for image org verification
- Add tests or smoke checks to validate: 7 PNGs produced at 1080x1350, metadata.json and prompts.json present, caption.txt generated (export_metadata or save_json pathway)
- Optionally expose CLI flags for topic/brand overrides (or use environment variables)

Known constraints and notes
- Without org verification, images fallback to placeholders to keep the pipeline deterministic and end-to-end runnable
- Agents and tasks are configured for a 7-slide educational explainer; slide_count can be changed via inputs
- The project currently uses uv for dependency management; avoid pip install -e in local workflows

State summary
- The carousel generator is integrated, runnable, and produces outputs under output/carousels/{slug}
- The run succeeded end-to-end with the current configuration and persisted a task artifact (metadata.json)