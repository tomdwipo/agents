from __future__ import annotations

from typing import Any, Dict, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from content.tools.io_utils import write_json


class SaveJSONInput(BaseModel):
    path: str = Field(..., description="File path to write JSON content to.")
    data: Dict[str, Any] = Field(..., description="JSON-serializable data to write.")


class SaveJSONTool(BaseTool):
    name: str = "save_json"
    description: str = "Persist JSON data to disk at the specified path."
    args_schema: Type[BaseModel] = SaveJSONInput

    def _run(self, path: str, data: Dict[str, Any]) -> str:
        write_json(path, data)
        return path