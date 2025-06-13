from typing import List
from enum import IntEnum
from pydantic import BaseModel

from core.models.transcription import Transcription


class Cursor(BaseModel):
    x: int = 0
    y: int = 0
    position: int = 0


class Shape(BaseModel):
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0


class WordState(IntEnum):
    UNACTIVATED = 0
    ACTIVATED = 1
    COMPLETED = 2


class Word(BaseModel):
    cursor: Cursor | None
    transcription: Transcription
    content: str
    state: WordState = WordState.UNACTIVATED
    shape: Shape
    size: float = 0


class LayoutState(BaseModel):
    done: bool
    cursor: Cursor | None
    total_frames: int
    current_chunk: List[Word] | None
    chunks: List[List[Word]]
    duration: float
