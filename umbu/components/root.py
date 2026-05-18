from umbu.components.layout_interface import ILayout
from umbu.components.row import Row
import umbu.constants as constants
from umbu.render.measurer_interface import IMeasurer

from pydantic import Field

from .base import Component
from typing import Optional
from typing import List


class RootLayout(ILayout):
    def measure(self, component, measurer:  IMeasurer):
        for child in component.children:
            child.measure(measurer)
            component.width += child.width

    def arrange(self, component, par_x: float, par_y: float):
        for child in component.children:
            child.arrange(par_x, par_y)
        super().arrange(component, par_x, par_y)


class Root(Component):
    x: float = 0
    y: float = 0

    background_color: Optional[str] = None
    canvas_width: int = constants.WIDTH
    canvas_height: int = constants.HEIGHT

    layout_type: type[ILayout] = RootLayout

    children: List['Component'] = Field(default_factory=list)

    def __init__(self, children):
        self.children = children

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y
