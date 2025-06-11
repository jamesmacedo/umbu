from enum import IntEnum
from typing import Optional
from pydantic import BaseModel


class TextState(IntEnum):
    UNACTIVATED = 0
    ACTIVATED = 1
    COMPLETED = 2


class ShapeModel(BaseModel):
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0


class TextModel(BaseModel):
    text: str
    state: TextState = TextState.UNACTIVATED
    shape: Optional[ShapeModel]
