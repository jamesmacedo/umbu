import json
import math
import asyncio
import constants

from core.canva.canva import Canva
from core.canva.layer import Layer
from core.models.transcription import Transcription
from core.models.layout import Word, WordState, Shape
from typing import List, Any


class Engine:
    _transcription: List[Transcription] = []

    layout: Canva | None = None
    buffer: Layer | None = None

    def __init__(self):
        self._chunk_size = constants.CHUNK_SIZE

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

        # self._total_frames = math.ceil(self._transcription[-1].end * 60)

    async def state_loop(self, canva, queue):
        for i, chunk in enumerate(canva.state.chunks):
            canva.clear(True)
            canva.state.current_chunk = chunk
            for word in chunk:
                canva.state.current_word = word
                word.state = WordState.ACTIVATED

                total_frames = math.ceil((word.transcription.end-word.transcription.start) * constants.FPS)
                word.total_frames = total_frames
                for frame in range(0, total_frames):
                    word.current_frame = frame
                    await queue.put(canva.state.copy())
                    await asyncio.sleep(0)

                canva.state.previous_word = canva.state.current_word

                # await queue.put(canva.state.copy())
                # await asyncio.sleep(0)
            # await queue.put(canva.state.copy())
            # await asyncio.sleep(0)

        print("finished")
        await queue.put(None)
        await asyncio.sleep(0)

    async def draw_loop(self, canva, classe, queue):

        while True:
            snapshot = await queue.get()
            if snapshot is None:
                break

            canva.state = snapshot
            classe(canva).draw()
            canva.frame += 1

    async def run(self, classe, style):

        canva = Canva(self.chunks, style)

        queue = asyncio.Queue(maxsize=20)
        t1 = asyncio.create_task(self.state_loop(canva, queue))
        t2 = asyncio.create_task(self.draw_loop(canva, classe, queue))

        await asyncio.gather(t1, t2)
