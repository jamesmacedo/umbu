import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict


class IAnimation(ABC):

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
class TextStyle:
    font_family: str = "Montserrat"
    font_size: float = 40.0

    color: str = "#FFFFFF"
    weight: str = "bold"

    outline_width: float = 0.0
    opacity: float = 1.0


@dataclass
class ComponentStyle:
    base: TextStyle = field(default_factory=TextStyle)

    states: Dict[StyleState, TextStyle] = field(default_factory=dict)

    def merge_styles(self, base: TextStyle, override: TextStyle) -> TextStyle:
        data = asdict(base)

        for field_name, field_def in override.__dataclass_fields__.items():
            override_value = getattr(override, field_name)
            default_value = field_def.default

            if override_value != default_value:
                data[field_name] = override_value

        return TextStyle(**data)

    def resolve(self, state: StyleState) -> TextStyle:
        state_style = self.states.get(state)

        if not state_style:
            return self.base

        return self.merge_styles(self.base, state_style)
