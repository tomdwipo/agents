# Product

Why this project exists
- Automate creation of educational Instagram carousels, ensuring consistent brand styling and high readability.
- Reduce manual design time by generating outline, copy, image prompts, images, overlays, and export metadata in one pipeline.

Problems it solves
- Fragmented workflow across research, copywriting, image generation, and design.
- Inconsistent brand presence and slide readability.
- Non-deterministic storage of outputs, making content reuse and publication slower.

How it works
- The crew runs a sequential pipeline of agents configured in YAML and wired in Python:
  - Planner: produces a 7-slide outline.
  - Copywriter: writes concise, educational copy per slide.
  - Image Prompt Engineer: crafts visual prompts (including text) for the image model.
  - Compositor: generates images, applies brand overlays, exports final slides and metadata.
- Key orchestrations:
  - [class Content](3_crew/content/src/content/crew.py:13) wires agents and tasks sequentially
  - [def run()](3_crew/content/src/content/main.py:29) sets default inputs (topic, brand) and kicks off the crew

User experience goals
- Text-first carousel optimized for readability and scannability.
- Brand-consistent overlays:
  - Primary #000000 (text), Secondary #FFFFFF (background), Inter font
  - Logo at bottom-right with safe margins
- Deterministic outputs under a slugged path per topic, ready for review and posting.

Inputs
- topic (string): e.g., How Compound Interest Works
- slide_count (int): default 7
- primary_hex: default #000000 (text color)
- secondary_hex: default #FFFFFF (background color)
- brand_logo: default 3_crew/content/assets/logo.png
- brand_font: default 3_crew/content/assets/fonts/InterVariable.ttf
- output_base: default 3_crew/content/output/carousels
- slug: computed from topic

Outputs
- Output directory: output/carousels/{slug}/
  - raw/slide_XX.png (1024x1024 source images)
  - slides/slide_XX.png (1080x1350 final slides)
  - prompts.json (trace of prompts)
  - metadata.json (caption, hashtags, alt texts, file list)
- The metadata.json path is also stored as the task artifact via tasks.yaml configuration.

Brand rules
- Inter font, large readable title at top, concise body below, optional CTA on the last slide.
- High contrast black/white overlays for accessibility.
- Logo positioned bottom-right within a safe margin.

Technical notes (product-level)
- Image tool configured to "dall-e-3"; if API is unavailable or restricted, the pipeline writes placeholder images and continues to completion.
- Composition uses Pillow to enforce layout, word-wrap, and truncation.
- YAML-driven agents/tasks ensure repeatability; Python tools encapsulate side effects.

Key files (for product behavior)
- Agents config: [3_crew/content/src/content/config/agents.yaml](3_crew/content/src/content/config/agents.yaml)
- Tasks config: [3_crew/content/src/content/config/tasks.yaml](3_crew/content/src/content/config/tasks.yaml)
- Crew wiring: [class Content](3_crew/content/src/content/crew.py:13)
- Entrypoint: [def run()](3_crew/content/src/content/main.py:29)
- Tools:
  - Images: [class DallETool](https://github.com/crewAI/crewAI-tools/blob/main/src/crewai_tools/tools/dalle_image_generator_tool/dalle_image_generator_tool.py)
  - Composer: [class ComposeSlideTool](3_crew/content/src/content/tools/composer.py:86)
  - Export: [class ExportMetadataTool](3_crew/content/src/content/tools/export_metadata.py:28)
  - Templates: [def outline_prompt](3_crew/content/src/content/tools/templates.py:6), [def slide_copy_prompt](3_crew/content/src/content/tools/templates.py:34), [def image_prompt_prompt](3_crew/content/src/content/tools/templates.py:66), [def caption_hashtags_prompt](3_crew/content/src/content/tools/templates.py:98)

Success criteria
- A run produces:
  - 7 final slide PNGs at 1080x1350
  - metadata.json and prompts.json under the carousel slug folder
  - Task artifact recorded for metadata.json
- Slides meet readability, brand, and layout requirements consistently.

Future enhancements
- After OpenAI org verification for image usage, optionally switch model to gpt-image-1 in [3_crew/content/src/content/tools/openai_images.py](3_crew/content/src/content/tools/openai_images.py:13).
- CLI/environment overrides for inputs to avoid editing main.py.
- Automated validation of artifact counts and alt text presence before publishing.