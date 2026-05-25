from umbu.components.layout_interface import ILayout
from umbu.render.measurer_interface import IMeasurer
from umbu.theme.style.interface import IAnimation

from pydantic import Field
from typing import List


class Component:
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    # id: str = Field(default_factory=lambda: "node_id")
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    start_frame: int = 0
    end_frame: int = 0

    opacity: float = 1.0
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0

    world_x: float = 0
    world_y: float = 0

    parent: type['Component']

    animation: IAnimation | None
    layout: ILayout

    active: bool = False
    children: List['Component'] = [] 


    def update(self, current_frame):
        if self.animation is not None:
            self.animation.count(self.end_frame).update(self, current_frame)

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
