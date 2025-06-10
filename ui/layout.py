import gi
import cairo
from models.company import Company
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

    context: Context = None
    surface = None

    def __init__(self, width: int = 720, height: int = 1280):
        self.width = width
        self.height = height

    def create(self, company: Company):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)

        layout = PangoCairo.create_layout(ctx)

        fontmap = PangoCairo.FontMap.get_default()
        fontmap = PangoCairo.FontMap.set_default(fontmap)
        fontmap = PangoFT2.FontMap.new()

        self.context = Context(surface, ctx, layout, company)

    def save(self, name: str):
        self.context.surface.write_to_png(name)
