from __future__ import annotations
from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw, ImageFont
import os

class AddTextToImageInput(BaseModel):
    """Input schema for AddTextToImageTool."""
    image_path: str = Field(..., description="Path to the input image.")
    text: str = Field(..., description="Text to add to the image.")
    output_path: Optional[str] = Field(None, description="Path to save result. If None, returns PIL Image.")
    position: str | tuple = Field('center', description="Text position - 'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', or (x, y) coordinates.")
    font_size: int = Field(40, description="Font size in pixels.")
    font_color: str | tuple = Field('white', description="Text color - color name, hex, or RGB tuple.")
    font_path: Optional[str] = Field(None, description="Path to custom font file (.ttf, .otf).")
    background_color: Optional[str | tuple] = Field(None, description="Background color for text box.")
    padding: int = Field(10, description="Padding around text when using background color.")
    opacity: int = Field(255, description="Text opacity (0-255, where 255 is fully opaque).")

class AddTextToImageTool(BaseTool):
    name: str = "add_text_to_image"
    description: str = "Add text to an image with customizable styling and positioning."
    args_schema: Type[BaseModel] = AddTextToImageInput

    def _run(
        self,
        image_path: str,
        text: str,
        output_path: Optional[str] = None,
        position: str | tuple = 'bottom-bellow-center',
        font_size: int = 12,
        font_color: str | tuple = 'white',
        font_path: Optional[str] = None,
        background_color: Optional[str | tuple] = None,
        padding: int = 10,
        opacity: int = 255,
    ) -> str:
        """
        Add text to an image with customizable styling and positioning.
        """
        try:
            image = Image.open(image_path).convert('RGBA')
            txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                        except:
                            font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            img_width, img_height = image.size

            if isinstance(position, tuple):
                x, y = position
            else:
                position_map = {
                    'bottom-bellow-center': ((img_width - text_width) // 2, (img_height - text_height) // 2),
                    'top-left': (20, 20),
                    'top-right': (img_width - text_width - 20, 20),
                    'bottom-left': (20, img_height - text_height - 20),
                    'bottom-right': (img_width - text_width - 20, img_height - text_height - 20),
                    'top-center': ((img_width - text_width) // 2, 20),
                    'bottom-center': ((img_width - text_width) // 2, img_height - text_height - 20),
                    'center': ((img_width - text_width) // 2, img_height - text_height - 170)
                }
                if position not in position_map:
                    raise ValueError(f"Invalid position. Choose from: {list(position_map.keys())} or use (x, y) coordinates")
                x, y = position_map[position]

            if isinstance(font_color, str):
                if font_color.startswith('#'):
                    font_color = tuple(int(font_color[i:i+2], 16) for i in (1, 3, 5))

            if isinstance(font_color, tuple) and len(font_color) == 3:
                font_color = font_color + (opacity,)
            
            if background_color:
                bg_x1 = x - padding
                bg_y1 = y - padding
                bg_x2 = x + text_width + padding
                bg_y2 = y + text_height + padding
                
                if isinstance(background_color, tuple) and len(background_color) == 3:
                    background_color = background_color + (opacity,)
                
                draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=background_color)

            draw.text((x, y), text, font=font, fill=font_color)
            result = Image.alpha_composite(image, txt_layer)

            if output_path and not output_path.lower().endswith('.png'):
                result = result.convert('RGB')

            if output_path:
                result.save(output_path, quality=95)
                return f"Image with text saved to: {output_path}"
            
            return "Text added to image in memory."
            
        except Exception as e:
            raise Exception(f"Error adding text to image: {e}")