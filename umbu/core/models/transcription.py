from pydantic import BaseModel 


class Transcription(BaseModel):
    word: str
    start: float
    end: float
