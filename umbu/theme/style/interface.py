import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Container, Optional, Dict



class Animation(ABC):

    def count(self, frame_count: int):
        self.total_frames = frame_count
        return self

    def ease_in_elastic(self, x: float):
        c4 = (2 * math.pi)/3
        return 0 if x == 0 else 1 if x == 1 else math.pow(2, -10*x) * math.sin(x * 10 - 0.75 * c4)+1

    def ease_out_bounce(self, x: float) -> float:
        n1 = 7.5625
        d1 = 2.75

        if x < 1 / d1:
            return n1 * x * x
        elif x < 2 / d1:
            x -= 1.5 / d1
            return n1 * x * x + 0.75
        elif x < 2.5 / d1:
            x -= 2.25 / d1
            return n1 * x * x + 0.9375
        else:
            x -= 2.625 / d1
            return n1 * x * x + 0.984375

    def lerp(self, start: float, end: float, factor: float) -> float:
        return start + (end - start) * factor

    def get_process(self, node, current_frame: int) -> float:
        return (current_frame/self.total_frames)

    @abstractmethod
    def update(self, node, current_frame):
        pass


class StyleState(Enum):
    DEFAULT = "default"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DONE = "done"


@dataclass
class ContainerStyle:

    width: float = 1.0 # percentage 0.0 to 1.0
    height: float = 1.0 # percentage 0.0 to 1.0

    scale: float = 1.0

    x: float = 0 
    y: float = 0 

    padding_top: float = 0.0
    padding_right: float = 0.0
    padding_bottom: float = 0.0
    padding_left: float = 0.0

    margin_top: float = 0.0
    margin_right: float = 0.0
    margin_bottom: float = 0.0
    margin_left: float = 0.0

    color: str | None = None
    opacity: float = 1.0

    border_color: str | None = None
    border_width: float = 0.0
    border_radius: float = 10.0

    shadow_color: str | None = None
    shadow_blur: float = 0.0
    shadow_offset_x: float = 0.0
    shadow_offset_y: float = 0.0

    align_horizontal: str = "center"  # left, center, right
    align_vertical: str = "center"    # top, center, bottom

@dataclass
class TextStyle:
    font_family: str = "Montserrat"
    font_size: float = 40.0

    color: str = "#00FF00"
    weight: str = "bold"

    outline_color: str = "#FFFFFF"
    outline_width: float = 0.0
    opacity: float = 1.0


@dataclass
class StyleData:
    text: TextStyle 
    container: ContainerStyle|None = None


@dataclass
class AnimationData:
    text: Animation|None = None
    container: Animation|None = None


@dataclass
class Style:
    spacing: float = 10

    states: Dict[StyleState, StyleData] = field(default_factory=dict)
    animation: AnimationData = field(default_factory=AnimationData)

    def compare(self, default: dict, new: dict):
        for field, value in default.items():
            override_value = new[field]
            if override_value != value:
                new[field] = override_value
        return new

    def resolve(self, state: StyleState) -> StyleData:
        state_style = self.states.get(state)

        if state_style is None:
            return StyleData(text=TextStyle())

        return StyleData(
            text=TextStyle(**self.compare(asdict(TextStyle()), asdict(state_style.text))),
            container=ContainerStyle(**self.compare(asdict(ContainerStyle()), asdict(state_style.container))) if state_style.container != None else None,
        )

        # if not state_style:
        #     return default_style 
        #
        # return self.merge_styles(default_style, state_style)
