import gi
import cairo
import constants

from core.ui.text import Row
from core.models.company import Company
from core.models.layout import LayoutState
from gi.repository import Pango, PangoCairo, PangoFT2

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_version("PangoFT2", "1.0")


class Context:
    surface = None
    context = None
    layout = None
    company: Company = None

    def __init__(self, surface, context, layout, company):
        self.surface = surface
        self.context = context
        self.layout = layout
        self.company = company


class Layout:

    state: LayoutState = None
    context: Context = None
    surface = None
    text = None

    def __init__(self, width: int = 720, height: int = 1280):
        self.width = width
        self.height = height

    def setFont(self, layout, font: str = "", size: int = 10):
        desc = Pango.FontDescription()
        desc.set_family(font)
        desc.set_size(size * Pango.SCALE)
        desc.set_weight(Pango.Weight.BOLD)
        layout.set_font_description(desc)

    def create(self, company: Company, chunks):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)

        layout = PangoCairo.create_layout(ctx)

        self.state = LayoutState(
            done=False,
            cursor=0,
            total_frames=0,
            current_chunk=chunks[0],
            chunks=chunks,
            duration=0
        )

        fontmap = PangoCairo.FontMap.get_default()
        fontmap = PangoCairo.FontMap.set_default(fontmap)
        fontmap = PangoFT2.FontMap.new()

        self.setFont(layout, company.font, constants.FONT_SIZE)

        self.context = Context(surface, ctx, layout, company)

    def save(self, name: str):
        self.context.surface.write_to_png(name)
