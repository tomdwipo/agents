from __future__ import annotations
from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from PIL import Image, ImageEnhance
import os

class AddLogoToImageInput(BaseModel):
    """Input schema for AddLogoToImageTool."""
    base_image_path: str = Field(..., description="Path to the base image.")
    logo_path: str = Field(..., description="Path to the logo image.")
    output_path: Optional[str] = Field(None, description="Path to save the result. If None, returns PIL Image object.")
    position: str = Field('bottom-right', description="Logo position - 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'.")
    logo_size: Optional[tuple] = Field(None, description="Resize logo to (width, height). If None, keeps original size.")
    opacity: float = Field(1.0, description="Logo opacity (0.0 to 1.0).")
    margin: int = Field(20, description="Margin from edges in pixels.")

class AddLogoToImageTool(BaseTool):
    name: str = "add_logo_to_image"
    description: str = "Add a logo image to a base image."
    args_schema: Type[BaseModel] = AddLogoToImageInput

    def _run(
        self,
        base_image_path: str,
        logo_path: str,
        output_path: Optional[str] = None,
        position: str = 'bottom-right',
        logo_size: Optional[tuple] = (150, 120) ,
        opacity: float = 1.0,
        margin: int = 0,
    ) -> str:
        """
        Add a logo image to a base image.
        """
        try:
            base_image = Image.open(base_image_path).convert('RGBA')
            logo = Image.open(logo_path).convert('RGBA')
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Image file not found: {e}")
        except Exception as e:
            raise Exception(f"Error opening images: {e}")

        if logo_size:
            logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

        if opacity < 1.0:
            alpha = logo.split()[-1]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            logo.putalpha(alpha)

        base_width, base_height = base_image.size
        logo_width, logo_height = logo.size

        position_map = {
            'top-left': (margin, margin),
            'top-right': (base_width - logo_width - margin, margin),
            'bottom-left': (margin, base_height - logo_height - margin),
            'bottom-right': (base_width - logo_width - margin, base_height - logo_height - margin),
            'center': ((base_width - logo_width) // 2, (base_height - logo_height) // 2),
            'bottom-bellow-center': ((base_width - logo_width) // 2, base_height - logo_height - 200)

        }

        if position not in position_map:
            raise ValueError(f"Invalid position. Choose from: {list(position_map.keys())}")

        logo_position = position_map[position]

        transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        transparent.paste(logo, logo_position, logo)

        result = Image.alpha_composite(base_image, transparent)

        if output_path and not output_path.lower().endswith('.png'):
            result = result.convert('RGB')

        if output_path:
            result.save(output_path, quality=95)
            return f"Image with logo saved to: {output_path}"
        
        return "Logo added to image in memory."