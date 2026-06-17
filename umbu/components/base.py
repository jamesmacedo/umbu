from umbu.components.layout_interface import Layout
from umbu.render.measurer_interface import IMeasurer
from umbu.theme.style import AnimationData, Style, StyleState

from pydantic import Field
from typing import List


class Component:
 
    x: int = 0
    y: int = 0
    width: float = 0
    height: float = 0

    start_frame: int = 0
    end_frame: int = 0

    total_frames: int = 0

    world_x: int = 0
    world_y: int = 0

    parent: type['Component']
    
    style: Style
    animated: AnimationData 
    layout: Layout

    active: bool = False
    children: List['Component'] = [] 

    initial_frames = 2

    def __init__(self):
        self.animated = AnimationData(
            scale=1.0,
            x=self.world_x,
            y=self.world_y,
        )

    def update(self, current_frame):

        # update the state based on the timeline
        self.animated.set_progress((current_frame/self.total_frames))

        if self.animated.is_done() == 1:
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
            self.style.animation.count(self.total_frames).on_update(self, current_frame)
            if self.animated.is_done() == 1:
                self.style.animation.count(self.total_frames).on_done(self, current_frame)
        
    def transform(self):

        self.world_x = self.parent.world_x + self.x
        self.world_y = self.parent.world_y + self.y

        self.animated = AnimationData(
            scale=1.0,
            x=self.world_x,
            y=self.world_y,
        )

        for child in self.children:
            child.transform()

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, renderer: 'IRender'):
        pass
