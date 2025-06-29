from umbu.core.canva.layer import Layer
from umbu.core.models.layout import LayoutState, Word

from typing import List


class Canva:

    style: type
    frame: int = 0
    chunk_frame: int = 0
    layers: List[Layer] = []
    buffer: Layer
    composing: Layer

    def __init__(self, style: type):
        self.buffer = Layer("BUFFER")
        self.composing = Layer("COMPOSER")

        self.style = style

        # self.state = LayoutState(
        #     current_chunk=chunks[0],
        #     chunks=chunks,
        #     previous_word=chunks[0][0],
        #     current_word=None
        # )

    def clear(self, force: bool = False):
        self.composing.clear()
        self.buffer.clear()
        for layer in self.layers:
            if not layer.locked or force:
                layer.clear()

    def findLayerById(self, id: str):
        indexed = {obj.id: obj for obj in self.layers}
        return indexed.get(id, None)

    def createOrFindLayer(self, layer_id: str):

        layer = self.findLayerById(id)
        if layer:
            return layer
        else:
            layer = Layer(id)
            self.layers.append(layer)
            return layer

    def dispose(self):
        for layer in self.layers:
            layer.dispose()
        self.buffer.dispose()
        self.composing.dispose()

    def compose(self):
        for layer in self.layers:
            self.composing.data.context.set_source_surface(layer.data.surface, 0, 0)
            self.composing.data.context.paint()
            layer.data.surface.flush()

        self.composing.data.surface.flush()
        return self.composing.data.surface.get_data()

        # frame = 1
        # self.composing.data.surface.write_to_png(os.path.join(self.destination_path, f"{frame:08d}.png"))
