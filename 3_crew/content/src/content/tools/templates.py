from __future__ import annotations

from typing import List


def outline_prompt(topic: str, slide_count: int = 7) -> str:
    """Builds the prompt to plan a multi-slide educational IG carousel outline."""
    return f"""
You are an expert social content strategist.

Task:
Design an educational Instagram carousel outline on the topic "{topic}" with exactly {slide_count} slides.

Requirements:
- Slide 1: Hook (attention-grabbing, sets context)
- Slides 2-{slide_count-1}: Value slides with concise bullets that teach progressively
- Slide {slide_count}: Clear CTA (what to do next)
- Titles: max 8 words
- Bullets per slide: 2-4 bullets
- Each bullet: max 12 words
- Tone: educational, clear, plain language, no jargon, no emojis, no hashtags
- Output: Valid JSON only. Do not include commentary or code fences.

JSON schema:
{{
  "slides": [
    {{ "index": 1, "title": "Title", "bullets": ["...", "..."] }},
    ...
    {{ "index": {slide_count}, "title": "Title", "bullets": ["...", "..."] }}
  ]
}}
""".strip()


def slide_copy_prompt(topic: str, outline_json: str) -> str:
    """Builds the prompt to produce final copy per slide from the outline."""
    return f"""
You are a senior social copywriter.

Topic:
{topic}

Given this outline JSON:
{outline_json}

Write final copy for each slide with:
- Fields: index, title (<= 8 words), body (<= 25 words, single paragraph), cta (only on last slide, else null)
- Tone: educational, clear, concise
- Avoid: emojis, hashtags, clickbait, jargon
- Output: Valid JSON only. No commentary or code fences.

JSON schema:
{{
  "slides": [
    {{"index": 1, "title": "Title", "body": "Short single paragraph", "cta": null}},
    ...,
    {{"index": 7, "title": "Title", "body": "Short single paragraph", "cta": "Short CTA"}}
  ]
}}
""".strip()


def image_prompt_prompt(topic: str, slides_copy_json: str) -> str:
    """Builds the prompt to engineer image prompts per slide."""
    return f"""
You are an image prompt engineer for educational carousels.

Topic:
{topic}

Given final copy JSON:
{slides_copy_json}

For each slide, craft a visual prompt for gpt-image-1 that supports the message without embedding any text.

Guidelines:
- Include: subject, setting, composition, style (e.g., modern, minimal), lighting, color mood
- Visuals must allow high-contrast black/white text overlay (avoid overly busy backgrounds)
- Explicitly prohibit text: "No text, no typography, no watermarks"
- Output: Valid JSON only. No commentary or code fences.

JSON schema:
{{
  "prompts": [
    {{"index": 1, "prompt": "..." }},
    ...,
    {{"index": 7, "prompt": "..." }}
  ]
}}
""".strip()


def caption_hashtags_prompt(topic: str, key_points: List[str]) -> str:
    """Builds the prompt to produce caption and hashtags."""
    bullets = "\\n".join(f"- {k}" for k in key_points[:6])
    return f"""
You are a social media strategist.

Create a concise caption and 8-12 relevant hashtags for an educational carousel on "{topic}".

Key points:
{bullets}

Constraints:
- Caption: 1-2 short sentences, plain language, no emojis
- Hashtags: lowercase, readable, niche + general mix, no spaces, no special characters
- Output: Valid JSON only. No commentary or code fences.

JSON schema:
{{
  "caption": "short caption text",
  "hashtags": ["tag1", "tag2", "..."]
}}
""".strip()