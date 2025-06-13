import constants
import numpy as np

from typing import List

from core.models.layout import Shape as ShapeModel
from core.ui.style.mortgage import GuildStyle
from gi.repository import Pango, PangoCairo
from core.models.layout import Word, Shape

# class Row:
#
#     shape: Shape = Shape()
#     words = []
#
#     def __init__(self, words: List[Word], layout, buffer):
#
#         self.layout = layout
#         self.buffer = buffer
#         self.words = words
#
#         width_arr, height_arr = [], []
#
#         for word in words:
#             buffer.context.layout.set_text(word.content, -1)
#             buffer.context.context.set_source_rgb(1, 1, 1)
#             ink_rect, logical_rect = buffer.context.layout.get_pixel_extents()
#             width_arr.append(logical_rect.width)
#             height_arr.append(logical_rect.height)
#
#             word.shape.width = logical_rect.width
#             word.shape.height = logical_rect.height
#
#         self.shape = Shape(x=0, y=0, width=np.sum(width_arr) + (constants.TEXT_PADDING * (len(width_arr) - 1)), height=np.max(height_arr))
#
#     def draw_text(self, x, y, word):
#         self.layout.setFont(self.layout.context.layout, "Montserrant", word.size)
#         self.layout.context.layout.set_text(word.content, -1)
#
#         ink_rect, logical_rect = self.buffer.context.layout.get_pixel_extents()
#
#         word.shape.width = logical_rect.width
#         word.shape.height = logical_rect.height
#
#         x = x - word.shape.width/2
#         y = y - word.shape.height/2
#
#         data = (x, y, self.layout, word)
#         classe = globals()["GuildStyle"]()
#         getattr(classe, "draw1")(*data)
#
#     def draw(self, x: float, y: float):
#         for i, word in enumerate(self.words):
#             self.draw_text(x, y, word)
#             # self.layout.text.setText(text)
#             # self.layout.text.draw(x, y)
#             x += word.shape.width + constants.TEXT_PADDING


class Text:

    word: Word = None

    def setFont(self, font: str = "", size: int = 10):
        desc = Pango.FontDescription()
        desc.set_family(font)
        desc.set_size(size * Pango.SCALE)
        desc.set_weight(Pango.Weight.BOLD)
        self.layer.data.layout.set_font_description(desc)
        self.buffer.data.layout.set_font_description(desc)

    def __init__(self, layer, buffer, word: Word):
        self.buffer = buffer
        self.layer = layer

        self.setFont("Montserrant", constants.FONT_SIZE)

        print(word.state)

        buffer.data.layout.set_text(word.content, -1)
        buffer.data.context.set_source_rgb(1, 1, 1)
        ink_rect, logical_rect = buffer.data.layout.get_pixel_extents()

        word.shape.width = logical_rect.width
        word.shape.height = logical_rect.height

        self.word = word

    def draw(self):
        self.layer.data.layout.set_text(self.word.content, -1)
        data = (self.word.shape.x, self.word.shape.y, self.layer, self.word)
        classe = globals()["GuildStyle"]()
        getattr(classe, "draw1")(*data)


class Row:

    shape: Shape
    components: List[Text] = []

    def __init__(self, layer,  components: List[Text]):
        self.layer = layer
        self.components = components

        width_arr = [component.word.shape.width for component in components]

        width = np.sum(np.sum(width_arr) + (constants.TEXT_PADDING * (len(width_arr) - 1)))
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
            comp.word.shape.x = self.layer.cursor.x

            new_x = self.layer.cursor.x + comp.word.shape.width + constants.TEXT_PADDING
            comp.word.shape.y = self.layer.cursor.y
            self.layer.cursor.x = new_x
            comp.draw()
