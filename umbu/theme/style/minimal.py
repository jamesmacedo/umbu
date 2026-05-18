from pydantic import BaseModel
from typing import Optional

class BaseStyle(BaseModel):
    font_family: str = "Montserrat"
    font_size: float = 40.0
    color: str = "#FFFFFF"
    weight: str = "bold"
    outline_color: Optional[str] = None
    outline_width: float = 0.0
