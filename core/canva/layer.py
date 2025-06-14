import gi
import cairo
import constants

from core.models.layout import LayoutState, Cursor
from gi.repository import Pango, PangoCairo, PangoFT2

from core.ui.text import Text
from typing import List

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_version("PangoFT2", "1.0")


class Data:
    surface = None
    context = None
    layout = None

    def __init__(self, surface, context, layout):
        self.surface = surface
        self.context = context
        self.layout = layout


class Layer:

    cursor: Cursor
    state: LayoutState = None
    data: Data = None
    components: List[Text] = []

    # def setFont(self, layout, font: str = "", size: int = 10):
    #     desc = Pango.FontDescription()
    #     desc.set_family(font)
    #     desc.set_size(size * Pango.SCALE)
    #     desc.set_weight(Pango.Weight.BOLD)
    #     layout.set_font_description(desc)

    def __init__(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, constants.WIDTH, constants.HEIGHT)
        ctx = cairo.Context(surface)

        layout = PangoCairo.create_layout(ctx)
        # self.setFont(layout, "Montserrant", constants.FONT_SIZE)
        self.data = Data(surface, ctx, layout)
        self.cursor = Cursor(**{})

    def setCursor(self, x: float, y: float):
        self.cursor.x = x
        self.cursor.y = y

    def render(self):
        self.data.layout

    def clear(self):
        self.data.context.save()
        self.data.context.set_operator(cairo.OPERATOR_CLEAR)
        self.data.context.paint()
        self.data.context.restore()
