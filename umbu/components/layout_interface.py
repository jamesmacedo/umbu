
from abc import abstractmethod

from umbu.render.measurer_interface import IMeasurer


class ILayout:

    @abstractmethod
    def measure(self, component: 'Component', measurer: IMeasurer):
        if len(component.children) > 0:
            for child in component.children:
                child.x = component.x
                child.y = component.y
                print("relative x: ", component.x, "relative y: ", component.y)

    @abstractmethod
    def arrange(self, component: 'Component', par_x: float, par_y: float):
        component.x = par_x + component.x
        component.y = par_y + component.y
