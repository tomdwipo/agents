from __future__ import annotations

import os
from typing import Optional, Tuple, Type

from PIL import Image, ImageDraw, ImageFont
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from content.types import BrandConfig
from content.tools.brand import load_font, hex_to_rgb


CANVAS_W = 1080
CANVAS_H = 1350


def _fit_on_canvas(img: Image.Image, bg_color: Tuple[int, int, int]) -> Image.Image:
    """
    Contain-fit the given image onto a 1080x1350 canvas with padding,
    preserving aspect ratio and filling background with bg_color.
    """
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), bg_color)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Compute scale to fit
    scale = min(CANVAS_W / img.width, CANVAS_H / img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Center
    x = (CANVAS_W - new_w) // 2
    y = (CANVAS_H - new_h) // 2
    canvas.paste(resized, (x, y))
    return canvas


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    """
    Naive word-wrap text to fit within max_width.
    """
    words = text.split()
    if not words:
        return ""
    lines = []
    cur = words[0]
    for w in words[1:]:
        test = f"{cur} {w}"
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return "\n".join(lines)


def _truncate_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int, max_lines: int) -> str:
    """
    Truncate wrapped text to max_lines and add ellipsis if needed.
    """
    lines = text.split("\n")
    if len(lines) <= max_lines:
        return text
    kept = lines[:max_lines]
    # Add ellipsis to last line if space permits
    last = kept[-1]
    ellipsis = "…"
    if draw.textlength(last + ellipsis, font=font) <= max_width:
        kept[-1] = last + ellipsis
    return "\n".join(kept)


class ComposeSlideInput(BaseModel):
    image_path: str = Field(..., description="Path to the raw image to be composed on canvas.")
    title: str = Field(..., description="Slide title text (short).")
    body: str = Field(..., description="Slide body text (short paragraph).")
    cta: Optional[str] = Field(None, description="CTA text (only on last slide).")
    index: int = Field(..., description="Slide index (1-based).")
    brand: BrandConfig = Field(..., description="Brand configuration.")
    save_path: str = Field(..., description="Where to save the composed PNG.")


class ComposeSlideTool(BaseTool):
    name: str = "compose_slide"
    description: str = (
        "Compose a final 1024x1024 Instagram slide with brand overlays (title, body, optional CTA, logo). "
        "Will fit the base image to canvas with padding, draw text with Inter font if available, and place logo bottom-right."
    )
    args_schema: Type[BaseModel] = ComposeSlideInput

    def _run(
        self,
        image_path: str,
        title: str,
        body: str,
        cta: Optional[str],
        index: int,
        brand: BrandConfig,
        save_path: str,
    ) -> str:
        # Ensure brand is a BrandConfig instance even if a dict was passed through tooling
        if isinstance(brand, dict):
            brand = BrandConfig(**brand)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Colors and fonts
        primary = hex_to_rgb(brand.primary_hex)    # text color primary
        secondary = hex_to_rgb(brand.secondary_hex)  # background color (or vice versa depending on contrast)
        bg_color = secondary

        try:
            base = Image.open(image_path)
        except Exception:
            # Fallback to blank background if raw image missing
            base = Image.new("RGB", (1024, 1024), bg_color)

        canvas = _fit_on_canvas(base, bg_color)
        draw = ImageDraw.Draw(canvas)

        # Font sizes tuned for IG portrait
        title_font = load_font(brand.font_path, size=72)
        body_font = load_font(brand.font_path, size=44)
        cta_font = load_font(brand.font_path, size=40)

        margin = brand.margin_px
        text_area_w = CANVAS_W - margin * 2

        # Title block near top
        title_wrapped = _wrap_text(draw, title, title_font, text_area_w)
        title_bbox = draw.multiline_textbbox((0, 0), title_wrapped, font=title_font, spacing=6)
        title_h = title_bbox[3] - title_bbox[1]
        y_cursor = margin

        draw.multiline_text(
            (margin, y_cursor),
            title_wrapped,
            font=title_font,
            fill=primary,
            spacing=6,
            align="left",
        )
        y_cursor += title_h + 32

        # Body block
        body_wrapped = _wrap_text(draw, body, body_font, text_area_w)
        # Limit body to ~8 lines for readability
        body_wrapped = _truncate_lines(draw, body_wrapped, body_font, text_area_w, max_lines=8)
        body_bbox = draw.multiline_textbbox((0, 0), body_wrapped, font=body_font, spacing=6)
        body_h = body_bbox[3] - body_bbox[1]

        draw.multiline_text(
            (margin, y_cursor),
            body_wrapped,
            font=body_font,
            fill=primary,
            spacing=6,
            align="left",
        )

        # CTA near bottom if provided
        if cta:
            cta_text = cta.strip()
            cta_wrapped = _wrap_text(draw, cta_text, cta_font, text_area_w)
            cta_bbox = draw.multiline_textbbox((0, 0), cta_wrapped, font=cta_font, spacing=4)
            cta_w = cta_bbox[2] - cta_bbox[0]
            cta_h = cta_bbox[3] - cta_bbox[1]
            cta_x = margin
            cta_y = CANVAS_H - margin - cta_h - 8  # leave room for logo line above

            draw.multiline_text(
                (cta_x, cta_y),
                cta_wrapped,
                font=cta_font,
                fill=primary,
                spacing=4,
                align="left",
            )

        # Logo bottom-right
        try:
            from content.tools.image_utils import AddLogoToImageTool
            add_logo_tool = AddLogoToImageTool()
            add_logo_tool._run(
                base_image_path=save_path,
                logo_path=brand.logo_path,
                output_path=save_path,
                position='bottom-right',
                margin=margin
            )
        except Exception:
            # No logo available, ignore
            pass

        # Save
        canvas.save(save_path, format="PNG")
        return save_path