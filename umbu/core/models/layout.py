from typing import List
from enum import IntEnum
from pydantic import BaseModel

from umbu.core.models.transcription import Transcription


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
    transcription: Transcription
    content: str
    state: WordState = WordState.UNACTIVATED
    shape: Shape
    size: float = 0
    current_frame: int = 0
    total_frames: int = 0


class LayoutState(BaseModel):
    previous_word: Word | None = None
    previous_chunk: List[Word] | None = None
    current_word: Word | None
    current_chunk: List[Word] | None
    chunks: List[List[Word]]
    duration: float = 0
    total_frames: int = 0
