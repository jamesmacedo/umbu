import json
import yaml
import math
import asyncio
import constants

from core.ui.layout import Layout
from core.ui.text import Row
from core.engine.render import Renderer
from core.models.transcription import Transcription
from core.models.text import TextModel, TextState, ShapeModel
from core.models.company import Company
from core.models.layout import Item, LayoutState
from typing import List, Any

WIDTH, HEIGHT = 720, 1280


class Engine:
    _transcription: List[Transcription] = []
    _cursor = 0
    _total_frames = 0

    layout: Layout | None = None
    buffer: Layout | None = None

    def __init__(self):
        self._chunk_size = 4

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        if value < 0:
            raise ValueError("The chunk size should be an positive value")

        self._chunk_size = value

    @property
    def chunks(self) -> List[List[Transcription]]:
        return self._chunks

    @chunks.setter
    def chunks(self, c) -> List[List[Transcription]]:
        self._chunks = c

    def load(self, path: str):
        def create_chunk(arr: List[Any], size: int) -> List[List[Item]]:
            chunks: List[List[Item]] = []
            for i in range(0, len(arr), size):
                raw_chunk = arr[i:i + size]
                item_chunk = [
                    Item(transcription=val, text=TextModel(text=val.word, state=TextState.UNACTIVATED, shape=ShapeModel(x=0, y=0, width=0, height=0)))
                    for val in raw_chunk
                ]
                chunks.append(item_chunk)
            return chunks

        with open(path, 'r') as f:
            data = json.load(f)
            self._transcription = [Transcription(**d) for d in data]
            self.chunks = create_chunk(self._transcription, self.chunk_size)

        self._total_frames = math.ceil(self._transcription[-1].end * 60)

    def render(self, layout, buffer):
        for i, chunk in enumerate(self.chunks):

            for item in chunk:
                text_frames = math.ceil((item.transcription.end-item.transcription.start) * 60)
                for frame in range(0, text_frames):
                    if frame > 5:
                        item.text.state = TextState.ACTIVATED

                    if layout.state.cursor == 10:
                        layout.state.done = True
                        break
            break

    def run(self):

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
        layout.create(company, self.chunks)

        buffer = Layout(WIDTH, HEIGHT)
        buffer.create(company, self.chunks)

        while not layout.state.done:
            self.render(layout, buffer)
            Renderer.render(layout, buffer)

            layout.state.cursor += 1
            print(layout.state.cursor)
