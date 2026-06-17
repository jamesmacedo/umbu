from umbu.components.layout_interface import Layout
from pydantic import Field

from umbu.render.measurer_interface import IMeasurer
from umbu.theme.style import Animation

from .base import Component
from typing import List


class RowLayout(Layout):

    def measure(self, component: 'RowComponent', measurer: IMeasurer):
        component.width = 0
        component.height = 0
        spacing = component.spacing

        for child in component.children:
            child.measure(measurer)
            component.width += child.width
            component.height = max(component.height, child.height)

        if len(component.children) > 1:
            component.width += spacing * (len(component.children) - 1)

    def arrange(self, component):
        cursor_x = 0 
        for child in component.children:
            child.x = cursor_x
            child.y = 0  
            cursor_x += child.width + component.spacing
            child.arrange()


class Row(Component):

    start_frame: int = 0
    end_frame: int = 0

    start_time: float = 0.0
    end_time: float = 0.0

    spacing: float = 10

    layout: Layout = RowLayout()

    animation: Animation|None = None 

    parent: type['Component']

    children: List['Component'] = Field(default_factory=list)

    def __init__(self, start_frame, end_frame, total_frames, children):
        self. total_frames = total_frames
        self.start_frame = start_frame
        self.end_frame = end_frame

        for child in children:
            child.parent = self

        self.children = children

    def measure(self, measurer: IMeasurer):
        self.layout.measure(self, measurer)

    def arrange(self):
        self.layout.arrange(self)

    def draw(self, renderer: 'IRender'):
        renderer.draw_row(self)
        for child in self.children:
            child.draw(renderer)
