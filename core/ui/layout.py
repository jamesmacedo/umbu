import gi
import cairo
import constants

from core.models.layout import LayoutState, Cursor
from gi.repository import Pango, PangoCairo, PangoFT2

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_version("PangoFT2", "1.0")


class Context:
    surface = None
    context = None
    layout = None

    def __init__(self, surface, context, layout):
        self.surface = surface
        self.context = context
        self.layout = layout


class Canvas:

    state: LayoutState = None
    context: Context = None

    def __init__(self, width: int = 720, height: int = 1280):
        self.width = width
        self.height = height

    def create(self, chunks):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)

        layout = PangoCairo.create_layout(ctx)

        self.state = LayoutState(
            done=False,
            cursor=Cursor(**{}),
            total_frames=0,
            current_chunk=chunks[0],
            chunks=chunks,
            duration=0
        )

        fontmap = PangoCairo.FontMap.get_default()
        fontmap = PangoCairo.FontMap.set_default(fontmap)
        fontmap = PangoFT2.FontMap.new()

        self.context = Context(surface, ctx, layout)

    def clear(self):
        self.context.context.save()
        self.context.context.set_operator(cairo.OPERATOR_CLEAR)
        self.context.context.paint()
        self.context.context.restore()

    def save(self, name: str):
        self.context.surface.write_to_png(name)
