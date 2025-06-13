from core.canva.layer import Layer
from core.models.layout import LayoutState, Word, Cursor

from typing import List


class Canva:

    frame: int = 0
    state: LayoutState
    layers: List[Layer] = []
    buffer: Layer
    composing: Layer

    def __init__(self, chunks: List[Word]):
        self.buffer = Layer()
        self.composing = Layer()

        self.state = LayoutState(
            cursor=Cursor(**{}),
            current_chunk=chunks[0],
            chunks=chunks,
            previous_word=chunks[0][0],
            current_word=None
        )

    def clear(self):
        self.composing.clear()
        self.buffer.clear()
        for layer in self.layers:
            if not layer.locked:
                layer.clear()

    def createLayer(self):
        layer = Layer()
        self.layers.append(layer)
        return layer

    def compose(self, frame: int):
        for layer in self.layers:
            self.composing.data.context.set_source_surface(layer.data.surface, 0, 0)
            self.composing.data.context.paint()

        self.composing.data.surface.write_to_png(f"frames/{frame:08d}.png")
