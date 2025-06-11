from pydantic import BaseModel, PositiveFloat


class Transcription(BaseModel):
    word: str
    start: PositiveFloat
    end: PositiveFloat
