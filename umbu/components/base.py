
from umbu.components.layout_interface import ILayout
from umbu.render.measurer_interface import IMeasurer
from umbu.theme.animation import IAnimation


class Component:
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    # id: str = Field(default_factory=lambda: "node_id")

    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    opacity: float = 1.0
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0

    animation: IAnimation | None = None
    layout_type: type[ILayout]

    def measure(self, measurer:  IMeasurer):
        self.layout_type().measure(self, measurer)

    def arrange(self, par_x: float, par_y: float):
        self.layout_type().arrange(self, par_x, par_y)

