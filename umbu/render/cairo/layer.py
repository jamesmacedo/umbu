import gi
import cairo
import umbu.constants as constants

from umbu.models.layout import LayoutState, Cursor
from gi.repository import PangoCairo

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

    id: str
    cursor: Cursor
    state: LayoutState = None
    data: Data 
    components: List = []
    locked: bool = False

    def __init__(self, id, width: int, height: int):
        self.id = id
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        layout = PangoCairo.create_layout(ctx)
        self.data = Data(surface, ctx, layout)
        self.cursor = Cursor(**{})

    def lock(self):
        self.locked = True

    def setCursor(self, x: float, y: float):
        self.cursor.x = x
        self.cursor.y = y

    def render(self):
        self.data.layout

    def flush(self):
        self.data.surface.flush()

    def paint(self):
        self.data.context.set_source_surface(layer.data.surface, 0, 0)
        self.data.context.paint()

    def clear(self):
        ctx = self.data.context 

        ctx.save()

        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.paint()

        ctx.restore()

    def get_data(self):
        return self.data.surface.get_data()

    def dispose(self):
        self.data.surface.flush()
