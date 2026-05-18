from umbu.components.layout_interface import ILayout
from pydantic import Field

from umbu.render.measurer_interface import IMeasurer

from .base import Component
from typing import List


class RowLayout(ILayout):

    def measure(self, component: 'RowComponent', measurer: IMeasurer):
        spacing = component.spacing

        for child in component.children:
            child.measure(measurer)
            component.width += child.width + spacing 
            component.height = max(component.height, child.height) 

        # if len(component.children) > 1:  
        #     component.width += spacing * (len(component.children) - 1)   
        
    
    def arrange(self, component, par_x: float, par_y: float):

        cursor_x = component.x 
        for child in component.children:
            child.x = cursor_x 
            child.y = component.y 

            print("child x: ", child.x)
            cursor_x += child.width + component.spacing 
            child.arrange(par_x, par_y)

        super().arrange(component, par_x, par_y)

class Row(Component):

    start_frame: int = 0
    end_frame: int = 0
    
    start_time: float = 0.0
    end_time: float = 0.0

    spacing: float = 10

    layout_type: type[ILayout] = RowLayout

    children: List['Component'] = Field(default_factory=list)

    def __init__(self, children):
        self.children = children
