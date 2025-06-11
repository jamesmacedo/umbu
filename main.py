import json
import yaml
import math
import constants

from core.models.transcription import Transcription
from core.models.company import Company
from core.models.text import TextModel, TextState
from core.ui.layout import Layout
from core.ui.text import Text, Row
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

final = transcription[-1].end

# async def animate():
#     cursor = 0
#     x = 0
#     for chunk in chunk_array(transcription, chunk_size):
#
#         for tra in chunk:
#             frames = (tra.end - tra.start)*constants.FPS
#             cursor += math.ceil(frames)
#         break
#
# while(True):
#     row = Row([TextModel(
#                 text=transcription.word,
#                 state=TextState.UNACTIVATED) for i, transcription in enumerate(chunk)],
#                 text)
#     row.draw((layout.width - row.shape.width)/2, (layout.height * constants.VERTICAL_ALIGN) - row.height/2)
#     layout.save("frames/frame.png")
