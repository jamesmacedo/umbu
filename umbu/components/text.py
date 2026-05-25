from umbu.components.layout_interface import ILayout
from umbu.render.measurer_interface import IMeasurer
from umbu.theme.style.interface import ComponentStyle, IAnimation, StyleState
from umbu.theme.style.minimal import MinimalAnimation, minimal 
from .base import Component


class TextLayout(ILayout):
    def measure(self, component: 'Component', measurer:  IMeasurer):
        size = measurer.measure(component)
        component.width = size[0]
        component.height = size[1]

    def arrange(self, component):
        super().arrange(component)


class Text(Component):
    content: str

    start_time: float = 0.0
    end_time: float = 0.0

    animation: IAnimation | None = MinimalAnimation()

    layout: ILayout = TextLayout()

    style: ComponentStyle  = minimal 

    state: StyleState = StyleState.INACTIVE

    def __init__(self, content: str, start_frame, end_frame, total_frames):

        self. total_frames = total_frames
        self.start_frame = start_frame
        self.end_frame = end_frame

        self.content = content

    def measure(self, measurer: IMeasurer):
        self.layout.measure(self, measurer)

    def arrange(self):
        self.layout.arrange(self)

    def draw(self, renderer: 'IRender'):
        renderer.draw_text(self)
