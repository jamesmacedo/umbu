import gi

from umbu.components.base import Component
from umbu.components import Row, Text
from umbu.components import Row, Text
from umbu.render.measurer_interface import IMeasurer
from umbu.render.render_interface import IRender
from umbu.theme.style.interface import StyleState
from . import Layer
from typing import List

from gi.repository import Pango, PangoCairo, PangoFT2

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_version("PangoFT2", "1.0")


class CairoMeasurer(IMeasurer):

    def __init__(self, layout):
        self.buffer = layout

    def measure(self, component: Text):
        resolved_style = component.style.resolve(StyleState.ACTIVE)

        desc = Pango.FontDescription()

        desc.set_family(resolved_style.font_family)
        desc.set_size(resolved_style.font_size * Pango.SCALE)

        if resolved_style.weight == "bold":
            desc.set_weight(Pango.Weight.BOLD)

        self.buffer.data.layout.set_text(component.content, -1)
        self.buffer.data.layout.set_font_description(desc)
        self.buffer.data.context.set_source_rgb(0, 1, 1)

        _, logical_rect = self.buffer.data.layout.get_pixel_extents()

        return (logical_rect.width, logical_rect.height)


class CairoRenderer(IRender):
    layers: List[Layer] = []
    layer: Layer
    buffer: Layer

    def __init__(self):
        self.buffer = Layer("BUFFER")
        self.layer = Layer("COMPOSER")
        self.measurer = CairoMeasurer(self.buffer)

    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, alpha)

    def _hex_to_rgb(self, hex_color: str):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)

    def clear(self):
        self.layer.clear()

    def setup(self, component):

        component.set_position(x=(component.parent.canvas_width -
                               component.width)/2, y=component.parent.canvas_height*0.8)
        component.measure(self.measurer)
        component.arrange()

    def render(self, component: Component):
        self.clear()
        component.transform()
        component.draw(self)
        self.layer.flush()
        return self.layer.data.surface.get_data()
        # return self.layer.data.surface.write_to_png("output.png")

    def draw_row(self, row: Row):

        ctx = self.layer.data.context

        ctx.save()

        ctx.move_to(row.world_x, row.world_y)
        ctx.set_source_rgb(*self._hex_to_rgb("#FF0000"))
        ctx.rectangle(row.world_x, row.world_y, row.width, row.height)
        ctx.fill()

        ctx.restore()


    def draw_text(self, text: Text):

        style = text.style.resolve(text.state)

        desc = Pango.FontDescription()
        desc.set_family(style.font_family)
        desc.set_size((style.font_size * Pango.SCALE) * text.scale)

        ctx = self.layer.data.context
        layout = self.layer.data.layout

        if style.weight == "bold":
            desc.set_weight(Pango.Weight.BOLD)

        ctx.move_to(text.world_x, text.world_y)
        
        layout.set_font_description(desc)
        layout.set_text(text.content, -1)

        if style.outline_width > 0:
            ctx.set_source_rgb(*self._hex_to_rgb(style.color))
            ctx.set_line_width(style.outline_width)
            PangoCairo.layout_path(ctx, layout) 
            ctx.stroke_preserve()
            ctx.set_source_rgb(*self._hex_to_rgb(style.color))
            ctx.fill()
            return

        ctx.set_source_rgb(*self._hex_to_rgb(style.color))

        PangoCairo.update_layout(
            ctx, layout)
        PangoCairo.show_layout(ctx, layout)
