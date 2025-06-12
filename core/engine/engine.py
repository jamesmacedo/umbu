import json
import math
import asyncio

from core.ui.layout import Layout
from core.engine.render import Renderer
from core.models.transcription import Transcription
from core.models.layout import Word, WordState, Shape
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
        def create_chunk(arr: List[Any], size: int) -> List[List[Word]]:
            chunks: List[List[Word]] = []
            for i in range(0, len(arr), size):
                raw_chunk = arr[i:i + size]
                item_chunk = [
                    Word(
                        cursor=0,
                        transcription=val,
                        content=val.word,
                        state=WordState.UNACTIVATED,
                        shape=Shape(x=0, y=0, width=0, height=0)
                    )
                    for val in raw_chunk
                ]
                chunks.append(item_chunk)
            return chunks

        with open(path, 'r') as f:
            data = json.load(f)
            self._transcription = [Transcription(**d) for d in data]
            self.chunks = create_chunk(self._transcription, self.chunk_size)

        self._total_frames = math.ceil(self._transcription[-1].end * 60)

    async def state_loop(self, layout, buffer, event):
        for i, chunk in enumerate(self.chunks):

            for word in chunk:
                await asyncio.sleep(0)
                word.state = WordState.ACTIVATED
                event.set()
            #     text_frames = math.ceil((item.transcription.end-item.transcription.start) * 60)
            #     for frame in range(0, text_frames):
            # break

    async def draw_loop(self, layout, buffer, event):
        while not layout.state.done:
            await event.wait()
            event.clear()
            Renderer.render(layout, buffer)
            layout.state.cursor += 1
            print(f"[draw] cursor = {layout.state.cursor}")

            if layout.state.cursor == 4:
                layout.state.done = True
                event.set()

    async def run(self):

        layout = Layout(WIDTH, HEIGHT)
        layout.create(self.chunks)

        buffer = Layout(WIDTH, HEIGHT)
        buffer.create(self.chunks)

        event = asyncio.Event()
        t1 = asyncio.create_task(self.state_loop(layout, buffer, event))
        t2 = asyncio.create_task(self.draw_loop(layout, buffer, event))
        await asyncio.gather(t1, t2)
