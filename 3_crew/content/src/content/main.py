#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from content.crew import Content
from content.tools.io_utils import slugify_topic

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

DEFAULT_TOPIC = "fast"
DEFAULT_SLIDE_COUNT = 2
DEFAULT_PRIMARY = "#000000"
DEFAULT_SECONDARY = "#FFFFFF"
DEFAULT_BRAND_LOGO = "assets/logo.png"
DEFAULT_BRAND_FONT = "assets/fonts/Inter.ttf"
DEFAULT_OUTPUT_BASE = "content/output/carousels"


def _base_inputs(topic: str) -> dict:
    slug = slugify_topic(topic)
    return {
        "topic": topic,
        "slide_count": DEFAULT_SLIDE_COUNT,
        "primary_hex": DEFAULT_PRIMARY,
        "secondary_hex": DEFAULT_SECONDARY,
        "brand_logo": DEFAULT_BRAND_LOGO,
        "brand_font": DEFAULT_BRAND_FONT,
        "output_base": DEFAULT_OUTPUT_BASE,
        "slug": slug,
        # legacy/example input still present if used elsewhere
        "current_year": str(datetime.now().year),
    }


def run():
    """
    Run the crew to generate slides Instagram carousel.
    """
    inputs = _base_inputs(DEFAULT_TOPIC)
    try:
        Content().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

