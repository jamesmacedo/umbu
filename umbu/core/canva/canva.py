import os
from core.canva.layer import Layer
from core.models.layout import LayoutState, Word, Cursor

from typing import List


class Canva:

    style: type
    frame: int = 0
    chunk_frame: int = 0
    state: LayoutState
    layers: List[Layer] = []
    buffer: Layer
    composing: Layer
    destination_path: str

    def __init__(self, chunks: List[Word], style: type):
        self.buffer = Layer()
        self.composing = Layer()

        self.style = style

        self.state = LayoutState(
            cursor=Cursor(**{}),
            current_chunk=chunks[0],
            chunks=chunks,
            previous_word=chunks[0][0],
            current_word=None
        )

    def clear(self, force: bool = False):
        self.composing.clear()
        self.buffer.clear()
        for layer in self.layers:
            if not layer.locked or force:
                layer.clear()

    def createLayer(self):
        layer = Layer()
        self.layers.append(layer)
        return layer

    def compose(self, frame: int):
        for layer in self.layers:
            self.composing.data.context.set_source_surface(layer.data.surface, 0, 0)
            self.composing.data.context.paint()

        os.makedirs(self.destination_path, exist_ok=True)
        self.composing.data.surface.write_to_png(os.path.join(self.destination_path, f"{frame:08d}.png"))
