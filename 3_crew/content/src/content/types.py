from __future__ import annotations

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class BrandConfig(BaseModel):
    """Brand styling configuration for composing slides."""
    primary_hex: str = Field("#000000", description="Primary color in hex, e.g., #000000")
    secondary_hex: str = Field("#FFFFFF", description="Secondary color in hex, e.g., #FFFFFF")
    font_path: str = Field(..., description="Path to InterVariable.ttf")
    logo_path: str = Field(..., description="Path to logo PNG")
    margin_px: int = Field(96, description="Safe margin for text and logo placement")


class SlideOutline(BaseModel):
    """Outline for a single slide during planning stage."""
    index: int
    title: str
    bullets: List[str]


class SlideCopy(BaseModel):
    """Final copy for a slide after copywriting stage."""
    index: int
    title: str
    body: str
    cta: Optional[str] = None


class CarouselPlan(BaseModel):
    """Structured plan for the full carousel."""
    topic: str
    slide_count: int = 7
    slides: List[SlideOutline]


class ImagePromptSpec(BaseModel):
    """Engineered image prompt for one slide."""
    index: int
    prompt: str


class GeneratedImage(BaseModel):
    """Reference to a generated image asset on disk."""
    index: int
    path: str


class ExportMetadata(BaseModel):
    """Final export metadata written to metadata.json."""
    slug: str
    topic: str
    slide_count: int
    caption: str
    hashtags: List[str]
    alt_texts: Dict[int, str]
    files: Dict[str, str]
    slides: List[GeneratedImage]