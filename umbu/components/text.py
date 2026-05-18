from umbu.components.layout_interface import ILayout
from umbu.render.measurer_interface import IMeasurer
from umbu.theme.style.minimal import BaseStyle 
from .base import Component

class TextLayout(ILayout):
    def measure(self, component: 'Component', measurer:  IMeasurer):
        size = measurer.measure(component)
        component.width = size[0]
        component.height = size[1]

    def arrange(self, component, par_x: float, par_y: float):
        super().arrange(component, par_x, par_y)

class Text(Component):
    content: str
    style: BaseStyle = BaseStyle()
    
    start_frame: int = 0
    end_frame: int = 0
    
    start_time: float = 0.0
    end_time: float = 0.0

    layout_type: type[ILayout] = TextLayout

    def __init__(self, content: str):
        self.content = content
