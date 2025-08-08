from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Optional, Type
from dotenv import load_dotenv

from openai import OpenAI
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from PIL import Image


DEFAULT_MODEL = "imagen-3.0-generate-002"
DEFAULT_SIZE = "1024x1024"


@dataclass
class _ClientHolder:
    client: Optional[OpenAI] = None


_client_holder = _ClientHolder()


def _get_client() -> OpenAI:
    # OPENAI_API_KEY should be set in environment or .env
    if _client_holder.client is None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        _client_holder.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
      
)
    return _client_holder.client


class GenerateImageInput(BaseModel):
    prompt: str = Field(..., description="Detailed visual prompt for the image model.")
    save_path: str = Field(..., description="Absolute or relative path to save the PNG image.")
    size: str = Field(DEFAULT_SIZE, description="Image size e.g., '1024x1024'.")


class GenerateImageTool(BaseTool):
    name: str = "generate_image"
    description: str = (
        "Generate a PNG image from a visual prompt and save it to disk."
    )
    args_schema: Type[BaseModel] = GenerateImageInput

    def _run(self, prompt: str, save_path: str, size: str = DEFAULT_SIZE) -> str:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        client = _get_client()
        
        result = client.images.generate(
             model=DEFAULT_MODEL,
             prompt=prompt,
             size=size,
             response_format='b64_json',
             n=1
        )
        for image_data in result.data:
            b64 = image_data.b64_json

        img_bytes = base64.b64decode(b64) 
        with open(save_path, "wb") as f:
            f.write(img_bytes)

        return save_path 