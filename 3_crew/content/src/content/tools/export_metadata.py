from __future__ import annotations

import os
from typing import Dict, List, Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from content.types import ExportMetadata, GeneratedImage
from content.tools.io_utils import ensure_dirs, write_json, write_text


class ExportMetadataInput(BaseModel):
    slug: str = Field(..., description="Slug for the carousel directory name.")
    topic: str = Field(..., description="Topic of the carousel.")
    slide_count: int = Field(..., description="Number of slides.")
    caption: str = Field(..., description="Caption text for Instagram post.")
    hashtags: List[str] = Field(..., description="List of hashtags.")
    alt_texts: Dict[int, str] = Field(..., description="Alt text for each slide keyed by index.")
    slides: List[GeneratedImage] = Field(..., description="List of slides with index and final image path.")
    files: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional additional files map to include in metadata (e.g., prompts.json path).",
    )
    output_base: str = Field(..., description="Base output folder, e.g., 3_crew/content/output/carousels")


class ExportMetadataTool(BaseTool):
    name: str = "export_metadata"
    description: str = (
        "Write metadata.json and caption.txt for the generated carousel into output/carousels/{slug}."
    )
    args_schema: Type[BaseModel] = ExportMetadataInput

    def _run(
        self,
        slug: str,
        topic: str,
        slide_count: int,
        caption: str,
        hashtags: List[str],
        alt_texts: Dict[int, str],
        slides: List[Dict],
        output_base: str,
        files: Optional[Dict[str, str]] = None,
    ) -> str:
        # Normalize slide models
        slides_models: List[GeneratedImage] = []
        for s in slides:
            slides_models.append(GeneratedImage(index=int(s["index"]), path=str(s["path"])))

        target_dir = os.path.join(output_base, slug)
        ensure_dirs(target_dir + os.sep)

        meta = ExportMetadata(
            slug=slug,
            topic=topic,
            slide_count=slide_count,
            caption=caption,
            hashtags=hashtags,
            alt_texts=alt_texts,
            files=files or {},
            slides=slides_models,
        )

        metadata_path = os.path.join(target_dir, "metadata.json")
        caption_path = os.path.join(target_dir, "caption.txt")

        write_json(metadata_path, meta.model_dump())
        write_text(caption_path, caption + ("\n" + " ".join(f"#{h}" for h in hashtags) if hashtags else ""))

        return metadata_path