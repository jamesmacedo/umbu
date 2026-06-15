import gi
import math

from umbu.components.base import Component
from umbu.components import Row, Text
from umbu.components import Row, Text
from umbu.render.cairo.font import FontCache
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
        self.font = FontCache()

    def measure(self, component: Text):
        style = component.style.resolve(component, StyleState.ACTIVE)

        font = self.font.get_font_description(style.text, component.style.scale_factor)

        self.buffer.data.layout.set_text(component.content, -1)
        self.buffer.data.layout.set_font_description(font)
        self.buffer.data.context.set_source_rgb(0, 1, 1)

        _, logical_rect = self.buffer.data.layout.get_pixel_extents()

        return (logical_rect.width, logical_rect.height)


class CairoRenderer(IRender):
    layer: Layer
    buffer: Layer
    fonts: dict = {}

    def __init__(self, width, height):
        self.font = FontCache()

        self.buffer = Layer("BUFFER", width, height)
        self.layer = Layer("COMPOSER", width, height)
        self.measurer = CairoMeasurer(self.buffer)

    # def _hex_to_rgba(self, hex_color: str):
    #     hex_color = hex_color.lstrip('#')
    #     r = int(hex_color[0:2], 16) / 255.0
    #     g = int(hex_color[2:4], 16) / 255.0
    #     b = int(hex_color[4:6], 16) / 255.0
    #     a = int(hex_color[6:8], 16) / 255.0
    #     return (r, g, b, a)

    def _hex_to_rgb(self, hex_color: str, opacity: float = 1.0):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, opacity)

    def clear(self):
        self.layer.clear()

    def setup(self, component):
        component.measure(self.measurer)
        component.set_position(x=(component.parent.canvas_width - component.width)/2, y=component.parent.canvas_height*0.8)
        component.arrange()

    def render(self, component: Component):
        self.clear()
        component.transform()
        component.draw(self)
        self.layer.flush()
        return self.layer.data.surface.get_data()
        # return self.layer.data.surface.write_to_png("output.png")

    def draw_row(self, row: Row):
        return

        ctx = self.layer.data.context

        ctx.save()

        ctx.move_to(row.world_x, row.world_y)
        ctx.set_source_rgb(*self._hex_to_rgb("#FF0000"))
        ctx.rectangle(row.world_x, row.world_y, row.width, row.height)
        ctx.fill()

        ctx.restore()

    def draw_container(self, text, style):

        ctx = self.layer.data.context
        layout = self.layer.data.layout
        
        ctx.save()

        radius = style.container.border_radius
        width, height = (text.width * style.container.scale),(text.height * style.container.scale) 

        x, y = text.world_x + style.container.x, text.world_y + style.container.y

        # x, y = x - width / 2, y - height / 2

        #TODO: custom border radius for each corner
        tl = radius
        tr = radius
        br = radius
        bl = radius

        ctx.new_sub_path()

        ctx.move_to(x + tl, y)

        ctx.line_to(x + width - tr, y)
        ctx.arc(
            x + width - tr,
            y + tr,
            tr,
            -math.pi / 2,
            0
        )

        ctx.line_to(x + width, y + height - br)
        ctx.arc(
            x + width - br,
            y + height - br,
            br,
            0,
            math.pi / 2
        )

        ctx.line_to(x + bl, y + height)
        ctx.arc(
            x + bl,
            y + height - bl,
            bl,
            math.pi / 2,
            math.pi
        )

        ctx.line_to(x, y + tl)
        ctx.arc(
            x + tl,
            y + tl,
            tl,
            math.pi,
            3 * math.pi / 2
        )

        ctx.set_source_rgba(*self._hex_to_rgb(style.container.color))
        ctx.fill()

        ctx.restore()

    def draw_shadow(self, cords, text, font, style, ctx, layout, scale_factor):

        x, y = cords

        ctx.save()
        ctx.move_to(x + (style.text.shadow.offset_x + scale_factor), y + (style.text.shadow.offset_y * scale_factor))

        layout.set_font_description(font)
        layout.set_text(text.content, -1)

        ctx.set_source_rgba(*self._hex_to_rgb(style.text.shadow.color, style.text.shadow.opacity))
        PangoCairo.update_layout(ctx, layout)
        PangoCairo.show_layout(ctx, layout)
        ctx.restore()

    def draw_outline(self, cords, text, font, style, ctx, layout, scale_factor):
        x, y = cords
        ctx.save()
        ctx.move_to(x, y)

        layout.set_font_description(font)
        layout.set_text(text.content, -1)

        ctx.set_source_rgba(*self._hex_to_rgb(style.text.outline_color, style.text.opacity))
        ctx.set_line_width((style.text.outline_width * scale_factor))
        PangoCairo.layout_path(ctx, layout) 
        ctx.stroke_preserve()
        ctx.set_source_rgba(*self._hex_to_rgb(style.text.color, style.text.opacity))
        ctx.fill()
        ctx.restore()


    def draw_text(self, text: Text):

        scale_factor = text.style.scale_factor
        style = text.style.resolve(text, text.state)

        if style.container:
            self.draw_container(text, text.animated)

        ctx = self.layer.data.context
        layout = self.layer.data.layout

        font = self.font.get_font_description(style.text, text.style.scale_factor) 

        x, y = text.world_x, text.world_y
        
        if style.text.shadow:
            self.draw_shadow(
                font=font,
                cords=(x,y),
                text=text, 
                style=style,
                ctx=ctx, 
                layout=layout,
                scale_factor=scale_factor 
            )

        if style.text.outline_width > 0:
            self.draw_outline(
                font=font,
                cords=(x,y),
                text=text, 
                style=style,
                ctx=ctx, 
                layout=layout,
                scale_factor=scale_factor 
            )
            return

        # Draw the text itself
        ctx.move_to(x, y)

        layout.set_font_description(font)
        layout.set_text(text.content, -1)

        PangoCairo.update_layout(ctx, layout)
        PangoCairo.show_layout(ctx, layout)
        # End

        ctx.set_source_rgba(*self._hex_to_rgb(style.text.color, style.text.opacity))
        ctx.fill()
