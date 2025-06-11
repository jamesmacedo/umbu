import constants
import numpy as np

from typing import List
from core.ui.layout import Layout

from core.ui.style.mortgage import GuildStyle


from gi.repository import Pango, PangoCairo
from core.models.text import TextModel, TextState


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
    temp_layout: Layout

    def __init__(self, text_arr: List[TextModel], text):
        self.text_arr = text_arr
        self.text = text
        self.temp_layout = Layout(720, 1280)

        self.temp_layout.create(None)

        self.shape = Shape(0, 0, 0, 0)
        width_arr, height_arr = [], []

        temp_text = Text(self.temp_layout)
        temp_text.setFont("BadaBoom BB", constants.FONT_SIZE)

        for t in text_arr:
            self.temp_layout.context.layout.set_text(t.text, -1)
            self.temp_layout.context.context.set_source_rgb(1, 1, 1)
            ink_rect, logical_rect = self.temp_layout.context.layout.get_pixel_extents()
            width_arr.append(logical_rect.width)
            height_arr.append(logical_rect.height)

        self.shape = Shape(0, 0, np.sum(width_arr) + (constants.TEXT_PADDING * (len(width_arr) - 1)), np.max(height_arr))

    def draw(self, x: float, y: float):
        for i, text in enumerate(self.text_arr):
            self.text.setText(text)
            self.text.draw(x, y)
            x += self.text.shape.width + constants.TEXT_PADDING


class Text(Shape):

    text: TextModel
    shape: Shape = Shape(0, 0, 0, 0)

    def __init__(self, layout: Layout):
        self.layout = layout

    def setFont(self, font: str = "", size: int = 10):
        desc = Pango.FontDescription()
        desc.set_family(font)
        desc.set_size(size * Pango.SCALE)
        desc.set_weight(Pango.Weight.BOLD)
        self.layout.context.layout.set_font_description(desc)

    def setText(self, text: TextModel):
        self.text = text
        self.layout.context.layout.set_text(text.text, -1)

        ink_rect, logical_rect = self.layout.context.layout.get_pixel_extents()
        self.shape = Shape(0, 0, logical_rect.width, logical_rect.height)

    def draw(self, x: int, y: int):
        data = (x, y, self.layout, self.text)
        classe = globals()[self.layout.context.company.class_name]()
        getattr(classe, "draw3")(*data)
