import constants
import numpy as np
from ui.layout import Layout
from gi.repository import Pango, PangoCairo
from models.text import TextModel, TextState
from typing import List


class Shape:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Row(Shape):

    shape: Shape = Shape(0, 0, 0, 0)
    text_arr: List[TextModel] = []
    temp_layout: Layout

    def __init__(self, text_arr: str, text):
        self.text_arr = text_arr
        self.text = text
        self.temp_layout = Layout(720, 1280)

        self.temp_layout.create()

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

    def draw(self, x: int, y: int):
        for i, text in enumerate(self.text_arr):
            self.text.setText(text)
            self.text.draw(x, y)
            x += self.text.shape.width + constants.TEXT_PADDING


class Text(Shape):

    shape: Shape = Shape(0, 0, 0, 0)

    def _define_font(self):
        pass

    def __init__(self, layout: Layout):
        self.layout = layout

    def setFont(self, font: str = "BadaBoom BB", size: int = 10):
        font_description = Pango.font_description_from_string(f"{font} {size}")
        self.layout.context.layout.set_font_description(font_description)

    def setText(self, text: TextModel):
        self.layout.context.layout.set_text(text.text, -1)

        if text.state is TextState.COMPLETED:
            self.layout.context.context.set_source_rgb(1, 1, 1)
        elif text.state is TextState.ACTIVATED:
            self.layout.context.context.set_source_rgb(1, 0, 0)
        elif text.state is TextState.UNACTIVATED:
            self.layout.context.context.set_source_rgb(1, 0, 0)
            self.layout.context.context.set_line_width(2)
            self.layout.context.context.set_source_rgba(0, 0, 0, 1)

        ink_rect, logical_rect = self.layout.context.layout.get_pixel_extents()
        self.shape = Shape(0, 0, logical_rect.width, logical_rect.height)

    def draw(self, x: int, y: int):
        self.layout.context.context.move_to(x, y)
        PangoCairo.show_layout(self.layout.context.context, self.layout.context.layout)
