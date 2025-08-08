from __future__ import annotations

from typing import Tuple
from PIL import ImageFont
from content.types import BrandConfig


def load_brand(
    primary_hex: str,
    secondary_hex: str,
    font_path: str,
    logo_path: str,
    margin_px: int = 96,
) -> BrandConfig:
    return BrandConfig(
        primary_hex=primary_hex,
        secondary_hex=secondary_hex,
        font_path=font_path,
        logo_path=logo_path,
        margin_px=margin_px,
    )


def load_font(font_path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(font_path, size=size)
    except Exception:
        # Fallback to default PIL font if Inter is unavailable
        return ImageFont.load_default()


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))