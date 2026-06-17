import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict, is_dataclass, fields
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
    def on_update(self, node, current_frame):
        pass

    @abstractmethod
    def on_done(self, node, current_frame):
        pass

@dataclass
class AnimationData:
    scale: float = 1.0
    x: int = 0
    y: int = 0
    progress: float = field(default_factory=float)

    def set_x(self, x: int):
        self.x = x

    def set_y(self, y: int):
        self.y = y

    def set_scale(self, scale: int):
        self.scale = scale

    def set_progress(self, progress: float):
        self.progress = progress

    def is_done(self):
        return self.progress == 1

class StyleState(Enum):
    DEFAULT = "default"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DONE = "done"

    # Use this state in case you don't what to vary the text style
    BASE = "base"


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
class ShadowStyle:
    offset_x: float = 2
    offset_y: float = 2
    color: str = "#000000" # hex without alpha 
    opacity: float = 1.0 # 0.0 to 1.0
    
    #TODO: implement gaussian blur
    blur: float = 0

@dataclass
class TextStyle:
    font_family: str = "Montserrat"
    font_size: float = 40.0
    scale: float = 1.0

    color: str = "#00FF00"
    weight: str = "bold"

    outline_color: str = "#FFFFFF"
    outline_width: float = 0.0
    opacity: float = 1.0 # 0.0 to 1.0

    shadow: ShadowStyle|None = None


@dataclass
class StyleData:
    text: TextStyle 
    container: ContainerStyle|None = None


@dataclass
class Style:
    spacing: float = 10
    scale_factor: float = field(default_factory=int)

    states: Dict[StyleState, StyleData] = field(default_factory=dict)
    animation: Animation|None = None 

    def set_factor(self, scale_factor: float):
        self.scale_factor = scale_factor

    def compare(self, default, override):
        if override is None:
            return default

        if not is_dataclass(default):
            return override

        merged = {}

        for field in fields(default):
            default_value = getattr(default, field.name)
            override_value = getattr(override, field.name)

            if override_value is None:
                merged[field.name] = default_value

            elif is_dataclass(default_value):
                merged[field.name] = self.compare(
                    default_value,
                    override_value
                )
            else:
                merged[field.name] = override_value

        return type(default)(**merged)

    def resolve(self, component: 'Text', state: StyleState) -> StyleData:

        if StyleState.BASE in self.states:
            state_style = self.states.get(StyleState.BASE)
        else: 
            state_style = self.states.get(state)

        if state_style is None:
            return StyleData(text=TextStyle())

        style = StyleData(
            text=self.compare(TextStyle(), state_style.text),
            container=self.compare(ContainerStyle(), state_style.container) if state_style.container != None else None,
        ) 

        return style 
