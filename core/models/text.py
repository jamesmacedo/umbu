from enum import IntEnum
from pydantic import BaseModel


class TextState(IntEnum):
    UNACTIVATED = 0
    ACTIVATED = 1
    COMPLETED = 2


class TextModel(BaseModel):
    text: str
    state: TextState = TextState.UNACTIVATED
