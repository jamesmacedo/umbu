import umbu.constants as constants
import numpy as np

from typing import List

from umbu.core.models.layout import Word, Shape
from gi.repository import Pango


class Text:

    word: Word = None
    final_shape: Shape
    style: type = None

    def setFont(self, font: str = "", size: int = 10):
        desc = Pango.FontDescription()
        desc.set_family(font)
        desc.set_size(size * Pango.SCALE)
        desc.set_weight(Pango.Weight.BOLD)
        self.layer.data.layout.set_font_description(desc)
        self.buffer.data.layout.set_font_description(desc)

    def __init__(self, layer, buffer, word: Word, style: type):
        self.buffer = buffer
        self.layer = layer

        self.style = style

        self.setFont("Montserrant", constants.FONT_SIZE)

        word.content = style.modify(word.content)

        buffer.data.layout.set_text(word.content, -1)
        buffer.data.context.set_source_rgb(1, 1, 1)
        ink_rect, logical_rect = buffer.data.layout.get_pixel_extents()

        self.final_shape = Shape(
            x=0,
            y=0,
            width=logical_rect.width,
            height=logical_rect.height
        )

        self.setFont("Montserrant", word.size)

        buffer.data.layout.set_text(word.content, -1)
        buffer.data.context.set_source_rgb(1, 1, 1)
        ink_rect, logical_rect = buffer.data.layout.get_pixel_extents()

        word.shape.width = logical_rect.width
        word.shape.height = logical_rect.height

        self.word = word

    def draw(self):
        self.layer.data.layout.set_text(self.word.content, -1)

        if self.word.shape.width != self.final_shape.width:
            x = self.word.shape.x + self.final_shape.width/2 - self.word.shape.width/2
            y = self.word.shape.y + self.final_shape.height/2 - self.word.shape.height/2
        else:
            x = self.word.shape.x
            y = self.word.shape.y

        self.style().draw(x, y, self.layer, self.word)


class Row:

    shape: Shape
    components: List[Text] = []

    def __init__(self, layer,  components: List[Text]):
        self.layer = layer
        self.components = components

        width_arr = [component.word.shape.width for component in components]

        width = sum(width_arr) + constants.TEXT_PADDING * (len(width_arr) - 1)
        height = np.max([component.word.shape.height for component in components])

        self.shape = Shape(
            x=0,
            y=0,
            width=width,
            height=height
        )

        # Alterar isso para buscar as proporcoes do Canva
        self.layer.cursor.x = (constants.WIDTH - self.shape.width)/2

    def draw(self):
        for i, comp in enumerate(self.components):

            # if (comp.word.state != WordState.COMPLETED):
            #     comp.word.state = WordState.UNACTIVATED

            comp.word.shape.x = self.layer.cursor.x

            new_x = self.layer.cursor.x + comp.word.shape.width + constants.TEXT_PADDING
            comp.word.shape.y = self.layer.cursor.y
            self.layer.cursor.x = new_x
            comp.draw()
