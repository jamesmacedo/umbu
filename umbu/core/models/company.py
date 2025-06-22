
from pydantic import BaseModel
from typing import Dict


class Colors(BaseModel):
    primary: str
    secondary: str
    accent: str

class Company(BaseModel):
    id: str
    font: str
    class_name: str
    colors: Colors

    # def __init__(self, company: str):
    #     self.id = company
    #     self.colors = self._getColors()
    #
