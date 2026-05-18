import gi

from umbu.components.base import Component
from umbu.components import Row, Text
from umbu.components import Row, Text
from umbu.render.measurer_interface import IMeasurer
from umbu.render.render_interface import IRender
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
        desc = Pango.FontDescription()

        desc.set_family(component.style.font_family)
        desc.set_size(component.style.font_size * Pango.SCALE)

        if component.style.weight == "bold":
            desc.set_weight(Pango.Weight.BOLD)

        self.buffer.data.layout.set_text(component.content, -1)
        self.buffer.data.layout.set_font_description(desc)
        self.buffer.data.context.set_source_rgb(1, 1, 1)

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

    def clear(self):
        self.layer.clear()

    def render(self, component: Component):
        self.clear()

        # layout = RowLayout(self.layer.data.context)
        # layout.compute(component)

        # self._draw_layout(component)
        component.measure(self.measurer)

        print("canvas width: ", component.canvas_width, " component width:", component.width)
        component.arrange((component.canvas_width-component.width)/2, component.canvas_height*0.8)

        self._draw_component(component)

        self.layer.flush()
        # return self.layer.get_data()
        return self.layer.data.surface.write_to_png("output.png")


    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, alpha)

    
    def _draw_layout(self, component):
        component.layout(self.measurer)
        if component.children:
            for child in component.children:
                self._draw_layout(child)


    def _draw_component(self, component: Component):

        if isinstance(component, Text):
            self._draw_text(component)
            return 
        
        if component.children:
            for child in component.children:
                self._draw_component(child)

    def _draw_text(self, component: Text):

        desc = Pango.FontDescription()

        desc.set_family(component.style.font_family)
        desc.set_size(component.style.font_size * Pango.SCALE)

        if component.style.weight == "bold":
            desc.set_weight(Pango.Weight.BOLD)


        print("text x: ", component.x, " text y: ", component.y)
        self.layer.data.context.move_to(component.x, component.y)
        self.layer.data.layout.set_font_description(desc)
        self.layer.data.layout.set_text(component.content, -1)

        r, g, b, _ = self._hex_to_rgba(component.style.color)

        alpha = component.opacity 
        
        self.layer.data.context.set_source_rgba(r, g, b, alpha)
        
        PangoCairo.update_layout(self.layer.data.context, self.layer.data.layout)
        PangoCairo.show_layout(self.layer.data.context, self.layer.data.layout)
