# Tools

This document provides a detailed description of the custom tools used in the Content Crew project.

## Image Generation

### DallETool

-   **Source:** `crewai_tools.tools.dalle_image_generator_tool.dalle_image_generator_tool.DallETool`
-   **Purpose:** Generates an image using the OpenAI DALL-E 3 model.
-   **Inputs:**
    -   `prompt` (str): The text prompt for generating the image.
-   **Outputs:**
    -   `path` (str): The path to the generated image file.

## Slide Composition

### ComposeSlideTool

-   **Source:** `3_crew/content/src/content/tools/composer.py`
-   **Purpose:** Composes a branded slide by adding a logo and text to a base image.
-   **Inputs:**
    -   `image_path` (str): The path to the base image.
    -   `slide_copy` (SlideCopy): A Pydantic model containing the title and body text for the slide.
    -   `brand_config` (BrandConfig): A Pydantic model containing brand information like logo path, font, and colors.
-   **Outputs:**
    -   `path` (str): The path to the final composed slide.

## Brand Utilities

### load_brand

-   **Source:** `3_crew/content/src/content/tools/brand.py`
-   **Purpose:** Loads brand configuration from a dictionary.
-   **Inputs:**
    -   `brand_dict` (dict): A dictionary containing brand information.
-   **Outputs:**
    -   `BrandConfig`: A Pydantic model instance.

### load_font

-   **Source:** `3_crew/content/src/content/tools/brand.py`
-   **Purpose:** Loads a font file using Pillow.
-   **Inputs:**
    -   `font_path` (str): The path to the font file.
    -   `font_size` (int): The desired font size.
-   **Outputs:**
    -   `ImageFont`: A Pillow font object.

### hex_to_rgb

-   **Source:** `3_crew/content/src/content/tools/brand.py`
-   **Purpose:** Converts a hex color string to an RGB tuple.
-   **Inputs:**
    -   `hex_color` (str): The hex color string (e.g., "#FFFFFF").
-   **Outputs:**
    -   `tuple`: An RGB tuple (e.g., (255, 255, 255)).

## I/O Utilities

### ensure_dirs

-   **Source:** `3_crew/content/src/content/tools/io_utils.py`
-   **Purpose:** Ensures that a directory exists, creating it if necessary.
-   **Inputs:**
    -   `path` (str): The directory path.

### slugify_topic

-   **Source:** `3_crew/content/src/content/tools/io_utils.py`
-   **Purpose:** Converts a topic string into a URL-friendly slug.
-   **Inputs:**
    -   `topic` (str): The topic string.
-   **Outputs:**
    -   `str`: The slugified string.

### write_json

-   **Source:** `3_crew/content/src/content/tools/io_utils.py`
-   **Purpose:** Writes a dictionary to a JSON file.
-   **Inputs:**
    -   `data` (dict): The dictionary to write.
    -   `path` (str): The output file path.

### write_text

-   **Source:** `3_crew/content/src/content/tools/io_utils.py`
-   **Purpose:** Writes text to a file.
-   **Inputs:**
    -   `text` (str): The text to write.
    -   `path` (str): The output file path.

## Metadata Export

### ExportMetadataTool

-   **Source:** `3_crew/content/src/content/tools/export_metadata.py`
-   **Purpose:** Exports carousel metadata to a JSON file and generates a caption.
-   **Inputs:**
    -   `carousel_plan` (CarouselPlan): The plan for the carousel.
    -   `generated_images` (list[GeneratedImage]): A list of generated images.
-   **Outputs:**
    -   `str`: A confirmation message.

## Generic JSON Persistence

### SaveJSONTool

-   **Source:** `3_crew/content/src/content/tools/save_json.py`
-   **Purpose:** Saves a Pydantic model as a JSON file.
-   **Inputs:**
    -   `model` (BaseModel): The Pydantic model to save.
    -   `filename` (str): The output filename.
-   **Outputs:**
    -   `str`: The path to the saved file.

## Prompt Templates

-   **Source:** `3_crew/content/src/content/tools/templates.py`
-   **Purpose:** These functions generate prompts for the various agents in the crew.
-   **Functions:**
    -   `outline_prompt`
    -   `slide_copy_prompt`
    -   `image_prompt_prompt`
    -   `caption_hashtags_prompt`