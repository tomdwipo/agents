# Tasks

## Instagram Carousel Generation Pipeline
Last performed: 2025-08-08

Purpose
- Generate a 7-slide educational Instagram carousel with text-first overlays, brand styling (primary #000000, secondary #FFFFFF, Inter font), and logo bottom-right.
- Persist outputs as a CrewAI task artifact and export deterministic files under output/carousels/{slug}/.

Files to modify or review
- Agents and tasks configuration:
  - [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml)
  - [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml)
- Crew wiring and entrypoint:
  - [class Content](3_crew/content/src/content/crew.py:13)
  - [def run()](3_crew/content/src/content/main.py:29)
  - [def _base_inputs(topic: str) -> dict](3_crew/content/src/content/main.py:20)
- Data models and tools:
  - [class BrandConfig(BaseModel)](3_crew/content/src/content/types.py:8)
  - [class ComposeSlideTool(BaseTool)](3_crew/content/src/content/tools/composer.py:86)
  - [class GenerateImageTool(BaseTool)](3_crew/content/src/content/tools/openai_images.py:38)
  - [class ExportMetadataTool(BaseTool)](3_crew/content/src/content/tools/export_metadata.py:28)
  - [class SaveJSONTool(BaseTool)](3_crew/content/src/content/tools/save_json.py:14)
  - [def outline_prompt(...)](3_crew/content/src/content/tools/templates.py:6)
  - [def slide_copy_prompt(...)](3_crew/content/src/content/tools/templates.py:34)
  - [def image_prompt_prompt(...)](3_crew/content/src/content/tools/templates.py:66)
  - [def caption_hashtags_prompt(...)](3_crew/content/src/content/tools/templates.py:98)
  - [def ensure_dirs(...)](3_crew/content/src/content/tools/io_utils.py:9)
  - [def slugify_topic(...)](3_crew/content/src/content/tools/io_utils.py:18)
  - [def write_json(...)](3_crew/content/src/content/tools/io_utils.py:23)
  - [def write_text(...)](3_crew/content/src/content/tools/io_utils.py:29)
  - [def load_font(...)](3_crew/content/src/content/tools/brand.py:20)
  - [def hex_to_rgb(...)](3_crew/content/src/content/tools/brand.py:27)

Inputs and environment
- topic: string; default defined in [3_crew/content/src/content/main.py](3_crew/content/src/content/main.py)
- slide_count: default 7
- Colors: primary_hex #000000, secondary_hex #FFFFFF
- Brand assets:
  - [3_crew/content/assets/logo.png](3_crew/content/assets/logo.png)
  - [3_crew/content/assets/fonts/InterVariable.ttf](3_crew/content/assets/fonts/InterVariable.ttf)
- OPENAI_API_KEY in [.env](3_crew/content/.env)
- Dependency management with uv (not pip install -e)

Output structure
- Base: [3_crew/content/output/carousels/{slug}/](3_crew/content/output/carousels/{slug}/)
  - Raw images (1024x1024): raw/slide_XX.png
  - Slides (1080x1350): slides/slide_XX.png
  - Prompts trace: prompts.json
  - Metadata artifact: metadata.json

Step-by-step workflow
1) Dependencies
   - Ensure pyproject lists:
     - openai, pillow, pydantic, python-slugify (see [3_crew/content/pyproject.toml](3_crew/content/pyproject.toml))
   - Run:
     - uv sync

2) Data models
   - Confirm required Pydantic models in [3_crew/content/src/content/types.py](3_crew/content/src/content/types.py).

3) Agent and task configuration
   - Add/verify agents in [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml):
     - carousel_planner, copywriter, image_prompt_engineer, compositor
   - Add/verify tasks in [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml):
     - plan_carousel, write_copy, engineer_prompts, generate_images, compose_slides, export_metadata
   - Ensure export_metadata sets output_file to output/carousels/{slug}/metadata.json for task artifact storage.

4) Crew wiring
   - Wire agents/tasks sequentially in [class Content.crew(self) -> Crew](3_crew/content/src/content/crew.py:122).

5) Prompt templates
   - Outline, copy, image prompts, and caption/hashtags builders in [3_crew/content/src/content/tools/templates.py](3_crew/content/src/content/tools/templates.py).

6) Image generation tool
   - Model default set to "dall-e-3" with placeholder fallback in [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py:13).
   - On image API errors (e.g., org verification required), a white placeholder PNG is created to keep pipeline running.

7) Composition tool
   - Compose overlays with Inter font, safe margins, logo bottom-right via [ComposeSlideTool._run(...)](3_crew/content/src/content/tools/composer.py:94).
   - If brand arrives as dict, it is coerced to BrandConfig (guard added).

8) IO utilities
   - Use [ensure_dirs(...)](3_crew/content/src/content/tools/io_utils.py:9) before writes.
   - Save artifacts with [write_json(...)](3_crew/content/src/content/tools/io_utils.py:23) or [class SaveJSONTool(BaseTool)](3_crew/content/src/content/tools/save_json.py:14).

9) Entrypoint inputs
   - Default inputs and slug computed in [def _base_inputs(...)](3_crew/content/src/content/main.py:20).
   - Run with:
     - uv sync
     - crewai run

10) Execution and verification
   - Verify outputs:
     - 7 PNGs under slides/
     - 7 raw images under raw/
     - prompts.json and metadata.json present
   - Confirm Crew task artifact: output/carousels/{slug}/metadata.json

11) Brand checks
   - Confirm InterVariable.ttf and logo.png are present at expected paths.

12) Optional: Switch to gpt-image-1 later
   - After OpenAI org verification for images, update DEFAULT_MODEL in [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py:13) to "gpt-image-1".

Important considerations and gotchas
- Use uv sync instead of pip install -e.
- If images API returns 403 for unverified orgs, composition proceeds with placeholder images; the pipeline remains deterministic and completes.
- Composition enforces 1080x1350 canvas, word-wrapping, and truncation for readability.
- Agents.yaml llm field defaults to gpt-4o-mini; adjust as needed.

Example of completed implementation
- Example run (topic in main.py): How Compound Interest Works
- Outputs:
  - [3_crew/content/output/carousels/how-compound-interest-works/slides/slide_01.png](3_crew/content/output/carousels/how-compound-interest-works/slides/slide_01.png)
  - [3_crew/content/output/carousels/how-compound-interest-works/slides/slide_07.png](3_crew/content/output/carousels/how-compound-interest-works/slides/slide_07.png)
  - [3_crew/content/output/carousels/how-compound-interest-works/metadata.json](3_crew/content/output/carousels/how-compound-interest-works/metadata.json)
  - [3_crew/content/output/carousels/how-compound-interest-works/prompts.json](3_crew/content/output/carousels/how-compound-interest-works/prompts.json)