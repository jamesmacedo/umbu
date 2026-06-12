from umbu.components.layout_interface import Layout
from umbu.render.measurer_interface import IMeasurer
from umbu.theme.style.interface import Animation, Style, StyleState

from pydantic import Field
from typing import List


class Component:
 
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    start_frame: int = 0
    end_frame: int = 0

    total_frames: int = 0

    opacity: float = 1.0
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0

    world_x: float = 0
    world_y: float = 0

    parent: type['Component']
    
    style: Style
    animation: Animation | None
    layout: Layout

    active: bool = False
    children: List['Component'] = [] 

    initial_frames = 2


    def update(self, current_frame):

        # update the state based on the timeline
        self.progress = (current_frame/self.total_frames)

        if self.progress == 1:
            self.state = StyleState.DONE
            return

        if self.total_frames < self.initial_frames:
            self.state = StyleState.DONE
            return

        if current_frame < self.initial_frames:
            self.state = StyleState.INACTIVE

        if current_frame > self.initial_frames:
            self.state = StyleState.ACTIVE

        # start animation (if configured)
        if self.style.animation is not None:
            self.style.animation.count(self.total_frames).update(self, current_frame)

    def transform(self):

        self.world_x = self.parent.world_x + self.x
        self.world_y = self.parent.world_y + self.y

        for child in self.children:
            child.transform()

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y

    def draw(self, renderer: 'IRender'):
        pass
