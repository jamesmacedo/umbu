import json
import yaml
import constants
from models.transcription import Transcription
from models.company import Company
from models.text import TextModel, TextState
from ui.layout import Layout
from ui.text import Text, Row
from typing import List


WIDTH, HEIGHT = 720, 1280
CHUNK_SIZE = 3
TEXT_PADDING = 20


chunk_size: int = 4
transcription: List[Transcription] = []


def chunk_array(arr, size):
    return [arr[i:i + size] for i in range(0, len(arr), size)]


with open('transcription.json', 'r') as f:
    data = json.load(f)
    transcription = [Transcription(**d) for d in data]


def getCompany(company_id: str):
    with open('companies.yaml') as file:
        try:
            data = yaml.safe_load(file)['companies'][company_id]
        except yaml.YAMLError as e:
            print(e)
    company = Company(**data)
    return company


company = getCompany("guild")

layout = Layout(WIDTH, HEIGHT)
layout.create(company)

text = Text(layout)
text.setFont(company.font, constants.FONT_SIZE)

testing = [TextState.COMPLETED, TextState.ACTIVATED, TextState.UNACTIVATED]


for chunk in chunk_array(transcription, chunk_size):
    x = 0
    row = Row([TextModel(
                text=transcription.word,
                state=TextState.UNACTIVATED if i >= len(testing) else testing[i]) for i, transcription in enumerate(chunk)],
                text)
    row.draw((layout.width - row.shape.width)/2, (layout.height * constants.VERTICAL_ALIGN) - row.height/2)
    break

layout.save("frames/frame.png")
