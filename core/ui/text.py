import constants
import numpy as np

from typing import List

from core.models.layout import Shape as ShapeModel
from core.ui.style.mortgage import GuildStyle
from gi.repository import Pango, PangoCairo
from core.models.layout import Word, Shape


class Row:

    shape: Shape = Shape()
    words = []

    def __init__(self, words: List[Word], layout, buffer):

        self.layout = layout
        self.buffer = buffer
        self.words = words

        width_arr, height_arr = [], []

        for word in words:
            buffer.context.layout.set_text(word.content, -1)
            buffer.context.context.set_source_rgb(1, 1, 1)
            ink_rect, logical_rect = buffer.context.layout.get_pixel_extents()
            width_arr.append(logical_rect.width)
            height_arr.append(logical_rect.height)

            word.shape.width = logical_rect.width
            word.shape.height = logical_rect.height

        self.shape = Shape(x=0, y=0, width=np.sum(width_arr) + (constants.TEXT_PADDING * (len(width_arr) - 1)), height=np.max(height_arr))

    def draw_text(self, x, y, word):
        self.layout.setFont(self.layout.context.layout, "Montserrant", word.size)
        self.layout.context.layout.set_text(word.content, -1)

        ink_rect, logical_rect = self.buffer.context.layout.get_pixel_extents()

        word.shape.width = logical_rect.width
        word.shape.height = logical_rect.height

        x = x - word.shape.width/2
        y = y - word.shape.height/2

        data = (x, y, self.layout, word)
        classe = globals()["GuildStyle"]()
        getattr(classe, "draw1")(*data)

    def draw(self, x: float, y: float):
        for i, word in enumerate(self.words):
            self.draw_text(x, y, word)
            # self.layout.text.setText(text)
            # self.layout.text.draw(x, y)
            x += word.shape.width + constants.TEXT_PADDING


class Text:

    def __init__(self, layout):
        self.layout = layout

    def draw_text(self, x, y, word):
        self.layout.context.layout.set_text(word.content, -1)

        data = (x, y, self.layout, word)
        classe = globals()["GuildStyle"]()
        getattr(classe, "draw1")(*data)

    def draw(self, x: float, y: float):
        for i, word in enumerate(self.words):
            self.draw_text(x, y, word)
            x += word.shape.width + constants.TEXT_PADDING
