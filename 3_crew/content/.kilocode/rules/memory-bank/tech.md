# Tech

Technologies used
- Python 3.10–3.13 compatible
- crewAI framework for multi-agent orchestration
- uv for dependency management and execution
- OpenAI Python SDK for image generation
- Pillow (PIL) for image composition and typography
- Pydantic v2 for schemas
- python-slugify for safe output slugs

Development setup
- Project root: [3_crew/content/](3_crew/content/)
- Entry CLI:
  - [content.main:run](3_crew/content/src/content/main.py)
  - crew execution via [content.crew:Content.crew()](3_crew/content/src/content/crew.py)
- YAML configuration:
  - Agents: [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml)
  - Tasks: [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml)
- Execution plan: [3_crew/content/docs/execution-plan.md](3_crew/content/docs/execution-plan.md)
- Memory bank: [3_crew/content/.kilocode/rules/memory-bank/](3_crew/content/.kilocode/rules/memory-bank/)

Dependencies (declared)
- crewAI: pyproject dependency in [3_crew/content/pyproject.toml](3_crew/content/pyproject.toml)
- openai>=1.30.0
- pillow>=10.2.0
- pydantic>=2.7.0
- python-slugify>=8.0.0

Tool usage patterns
- Image generation tool:
  - [class GenerateImageTool(BaseTool)](3_crew/content/src/content/tools/openai_images.py:38)
  - Default model: "dall-e-3" (fallback placeholder if API blocked)
  - Generates 1024x1024 PNGs into output/carousels/{slug}/raw/slide_XX.png
- Composer tool:
  - [class ComposeSlideTool(BaseTool)](3_crew/content/src/content/tools/composer.py:86)
  - Builds 1080x1350 slides with Inter font and brand logo bottom-right
  - Wraps text and truncates for readability
- Export metadata tool:
  - [class ExportMetadataTool(BaseTool)](3_crew/content/src/content/tools/export_metadata.py:28)
  - Persists metadata.json and caption.txt and is wired as task artifact
- Save JSON tool:
  - [class SaveJSONTool(BaseTool)](3_crew/content/src/content/tools/save_json.py:14)

Environment variables
- OPENAI_API_KEY in [3_crew/content/.env](3_crew/content/.env) or root .env

Model selection strategy
- Default image model: "dall-e-3" in [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py:13)
- When org verification is available for gpt-image-1, update DEFAULT_MODEL accordingly
- On any image API error (403, unsupported), tool writes a white placeholder PNG of the requested size and proceeds

Fonts and assets
- Default font: InterVariable at [3_crew/content/assets/fonts/InterVariable.ttf](3_crew/content/assets/fonts/InterVariable.ttf)
- Default logo: [3_crew/content/assets/logo.png](3_crew/content/assets/logo.png)
- Composer loads Inter via PIL truetype, with fallback to PIL default if missing

Output paths
- Base: output/carousels/{slug}/
- Raw images (1024x1024): raw/slide_XX.png
- Final slides (1080x1350): slides/slide_XX.png
- Prompts: prompts.json
- Metadata: metadata.json (also set as task artifact)

Run commands
- From project root:
  - uv sync
  - crewai run

Troubleshooting
- Images 403 (org not verified) or unsupported parameter:
  - The pipeline continues with placeholder images; verify org at OpenAI and optionally switch model back to gpt-image-1
- Brand dict vs schema:
  - Composer coerces dict to BrandConfig; ensure keys match schema fields
- Ensure font and logo paths exist; missing fonts fall back to PIL default
- Use uv sync instead of pip install -e, per local workflow policy