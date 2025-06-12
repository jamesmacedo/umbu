from typing import List
from enum import IntEnum
from pydantic import BaseModel

from core.models.transcription import Transcription

# class Cursor


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
    cursor: int
    transcription: Transcription
    content: str
    state: WordState = WordState.UNACTIVATED
    shape: Shape


class LayoutState(BaseModel):
    done: bool
    cursor: int
    total_frames: int
    current_chunk: List[Word] | None
    chunks: List[List[Word]]
    duration: float
