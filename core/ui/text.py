import constants
import numpy as np

from typing import List

from core.models.text import ShapeModel
from core.ui.style.mortgage import GuildStyle
from gi.repository import Pango, PangoCairo
from core.models.text import TextModel, TextState
from core.models.layout import Item


class Shape:
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Row(Shape):

    shape: Shape = Shape(0, 0, 0, 0)
    text_arr: List[TextModel] = []

    def __init__(self, text_arr: List[Item], layout, buffer):

        self.layout = layout
        self.text_arr = text_arr

        self.shape = Shape(0, 0, 0, 0)
        width_arr, height_arr = [], []

        for t in text_arr:
            buffer.context.layout.set_text(t.text.text, -1)
            buffer.context.context.set_source_rgb(1, 1, 1)
            ink_rect, logical_rect = buffer.context.layout.get_pixel_extents()
            width_arr.append(logical_rect.width)
            height_arr.append(logical_rect.height)

            t.text.shape.width = logical_rect.width
            t.text.shape.height = logical_rect.height

        self.shape = Shape(0, 0, np.sum(width_arr) + (constants.TEXT_PADDING * (len(width_arr) - 1)), np.max(height_arr))

    def draw_text(self, x, y, text):
        self.layout.context.layout.set_text(text.text, -1)

        data = (x, y, self.layout, text)
        classe = globals()[self.layout.context.company.class_name]()
        getattr(classe, "draw1")(*data)
        pass

    def draw(self, x: float, y: float):
        for i, text in enumerate(self.text_arr):
            self.draw_text(x, y, text.text)
            # self.layout.text.setText(text)
            # self.layout.text.draw(x, y)
            x += text.text.shape.width + constants.TEXT_PADDING
