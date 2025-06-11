
from typing import List
from pydantic import BaseModel

from core.models.transcription import Transcription
from core.models.text import TextModel


class Item(BaseModel):
    transcription: Transcription
    text: TextModel


class LayoutState(BaseModel):
    done: bool
    cursor: int
    total_frames: int
    current_chunk: List[Item] | None
    chunks: List[List[Item]]
    duration: float
