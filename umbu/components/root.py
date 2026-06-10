from umbu.components.layout_interface import Layout
from umbu.components.row import Row
import umbu.constants as constants
from umbu.render.measurer_interface import IMeasurer

from .base import Component
from typing import Optional


class RootLayout(Layout):
    def measure(self, component, measurer:  IMeasurer):
        component.width = 0
        for child in component.children:
            child.measure(measurer)
            component.width += child.width

    def arrange(self, component):
        for child in component.children:
            child.arrange()
        # super().arrange(component, par_x, par_y)


class Root(Component):
    x: float = 0
    y: float = 0

    background_color: Optional[str] = None
    canvas_width: int = constants.WIDTH
    canvas_height: int = constants.HEIGHT

    layout: Layout = RootLayout()

    def __init__(self, children):
        for child in children:
            child.parent = self
        self.children = children

    def measure(self, measurer: IMeasurer):
        self.layout.measure(self, measurer)

    def arrange(self):
        self.layout.arrange(self)

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y

    def draw(self, renderer: 'IRender'):
        for child in self.children:
            child.draw(renderer)
