import json
import math
import time
import asyncio
import constants

from core.ui.layout import Layout, Cursor
from core.engine.render import Renderer
from core.models.transcription import Transcription
from core.models.layout import Word, WordState, Shape
from typing import List, Any

WIDTH, HEIGHT = 720, 1280


class Engine:
    _transcription: List[Transcription] = []
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
                        cursor=Cursor(),
                        transcription=val,
                        content=val.word,
                        state=WordState.UNACTIVATED,
                        shape=Shape()
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

    async def state_loop(self, layout, buffer, queue):
        for i, chunk in enumerate(self.chunks):
            for word in chunk:
                word.state = WordState.ACTIVATED
                text_frames = math.ceil((word.transcription.end-word.transcription.start) * 60)
                for frame in range(0, text_frames):

                    if frame < 10:
                        word.size = frame/10 * constants.FONT_SIZE

                    layout.state.cursor.position += 1
                    await queue.put(layout.state.copy())
                    await asyncio.sleep(0)

    async def draw_loop(self, buffer, queue):
        while True:
            snapshot = await queue.get()
            if snapshot is None:
                print('break')
                break

            print(snapshot.current_chunk[0].content, snapshot.current_chunk[0].size)
            time.sleep(1)
            buffer.state = snapshot
            Renderer.render(buffer, buffer)

    async def run(self):

        layout = Layout(WIDTH, HEIGHT)
        layout.create(self.chunks)

        buffer = Layout(WIDTH, HEIGHT)
        buffer.create(self.chunks)

        queue = asyncio.Queue(maxsize=20)
        t1 = asyncio.create_task(self.state_loop(layout, buffer, queue))
        t2 = asyncio.create_task(self.draw_loop(buffer, queue))

        await asyncio.gather(t1, t2)
