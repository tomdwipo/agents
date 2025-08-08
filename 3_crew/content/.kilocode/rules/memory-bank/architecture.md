# Architecture

System overview
- Multi-agent pipeline using crewAI to generate Instagram carousel content with brand overlays.
- Four primary agents wired sequentially via Crew and YAML-configured tasks.
- Image generation via OpenAI Images API (configured to "dall-e-3") with placeholder fallback to ensure deterministic runs when image API access is restricted.

Key components and relationships
- Crew and Agents
  - [class Content](3_crew/content/src/content/crew.py:13)
    - Agents:
      - [def carousel_planner(self) -> Agent](3_crew/content/src/content/crew.py:35)
      - [def copywriter(self) -> Agent](3_crew/content/src/content/crew.py:42)
      - [def image_prompt_engineer(self) -> Agent](3_crew/content/src/content/crew.py:49)
      - [def compositor(self) -> Agent](3_crew/content/src/content/crew.py:56)
    - Tasks:
      - [def plan_carousel_task(self) -> Task](3_crew/content/src/content/crew.py:84)
      - [def write_copy_task(self) -> Task](3_crew/content/src/content/crew.py:90)
      - [def engineer_prompts_task(self) -> Task](3_crew/content/src/content/crew.py:71)
      - [def generate_images_task(self) -> Task](3_crew/content/src/content/crew.py:77)

- Config (YAML)
  - Agents roles/goals: [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml)
  - Tasks definitions: [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml)

- Entrypoint and orchestration
  - [def run()](3_crew/content/src/content/main.py:29): sets default inputs (topic, slide_count, brand assets) and kicks off crew.
  - Uses [def _base_inputs(topic: str) -> dict](3_crew/content/src/content/main.py:20) to produce a slug and bundle inputs.

- Data models
  - [class BrandConfig(BaseModel)](3_crew/content/src/content/types.py:8)
  - [class SlideOutline(BaseModel)](3_crew/content/src/content/types.py:18)
  - [class SlideCopy(BaseModel)](3_crew/content/src/content/types.py:26)
  - [class CarouselPlan(BaseModel)](3_crew/content/src/content/types.py:34)
  - [class ImagePromptSpec(BaseModel)](3_crew/content/src/content/types.py:41)
  - [class GeneratedImage(BaseModel)](3_crew/content/src/content/types.py:46)
  - [class ExportMetadata(BaseModel)](3_crew/content/src/content/types.py:52)

- Tools
  - Image generation:
    - [class DallETool(BaseTool)](https://github.com/crewAI/crewAI-tools/blob/main/src/crewai_tools/tools/dalle_image_generator_tool/dalle_image_generator_tool.py)
  - Slide composition:
    - [class ComposeSlideTool(BaseTool)](3_crew/content/src/content/tools/composer.py:86)
  - Brand utilities:
    - [def load_brand(...)](3_crew/content/src/content/tools/brand.py:7)
    - [def load_font(...)](3_crew/content/src/content/tools/brand.py:20)
    - [def hex_to_rgb(...)](3_crew/content/src/content/tools/brand.py:27)
  - IO utilities:
    - [def ensure_dirs(...)](3_crew/content/src/content/tools/io_utils.py:9)
    - [def slugify_topic(...)](3_crew/content/src/content/tools/io_utils.py:18)
    - [def write_json(...)](3_crew/content/src/content/tools/io_utils.py:23)
    - [def write_text(...)](3_crew/content/src/content/tools/io_utils.py:29)
  - Metadata export:
    - [class ExportMetadataTool(BaseTool)](3_crew/content/src/content/tools/export_metadata.py:28)
  - Generic JSON persistence:
    - [class SaveJSONTool(BaseTool)](3_crew/content/src/content/tools/save_json.py:14)
  - Prompt templates:
    - [def outline_prompt(...)](3_crew/content/src/content/tools/templates.py:6)
    - [def slide_copy_prompt(...)](3_crew/content/src/content/tools/templates.py:34)
    - [def image_prompt_prompt(...)](3_crew/content/src/content/tools/templates.py:66)
    - [def caption_hashtags_prompt(...)](3_crew/content/src/content/tools/templates.py:98)

Critical flows
- Inputs:
  - topic (str), slide_count (int, default 7), primary_hex (#000000), secondary_hex (#FFFFFF), brand_logo, brand_font, output_base, slug.
- Pipeline (sequential):
  1) plan_carousel -> outline JSON (slides: title + bullets)
  2) write_copy -> final per-slide title/body (+ CTA on last)
  3) engineer_prompts -> visual prompt per slide (including text in image)
  4) generate_images -> calls DALL-E tool; saves raw/slide_XX.png (1024x1024)
- Output locations:
  - Base: output/carousels/{slug}/
  - Raw images: raw/slide_XX.png
  - Final slides: slides/slide_XX.png
  - Prompts: prompts.json
  - Metadata artifact: metadata.json

Key technical decisions
- Brand-first readability: high-contrast black/white overlays with InterVariable font and logo bottom-right.
- Image generation model set to "dall-e-3" in [DEFAULT_MODEL](3_crew/content/src/content/tools/openai_images.py:13).
- Resilience: if image API errors, pipeline continues; composition uses a valid placeholder image to avoid blocking downstream steps.
- Dimensions: raw 1024x1024; final composed 1080x1350 with containment fit and padding to maintain aspect ratio.

Source code paths
- Crew and orchestration:
  - [3_crew/content/src/content/crew.py](3_crew/content/src/content/crew.py)
  - [3_crew/content/src/content/main.py](3_crew/content/src/content/main.py)
- Config:
  - [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml)
  - [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml)
- Tools and types:
  - [3_crew/content/src/content/types.py](3_crew/content/src/content/types.py)
  - [3_crew/content/src/content/tools/](3_crew/content/src/content/tools/)
- Documentation:
  - [3_crew/content/docs/execution-plan.md](3_crew/content/docs/execution-plan.md)
  - Memory bank files under:
    - [3_crew/content/.kilocode/rules/memory-bank/](3_crew/content/.kilocode/rules/memory-bank/)

Important patterns and constraints
- YAML-driven prompts/tasks keep agents declarative; Python tools encapsulate side-effects (API calls, image I/O, composition).
- Safe margins and word-wrap with truncation in composer to enforce visual consistency.
- CrewAI task output_file used to persist metadata.json as the primary artifact.

Open questions / future improvements
- Switch back to gpt-image-1 once organization verification is complete.
- Add CLI/environment overrides for inputs to avoid editing main.py for non-default runs.
- Add tests/smoke checks to validate artifact counts and structure after each run.