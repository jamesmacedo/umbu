
from abc import abstractmethod

from umbu.render.measurer_interface import IMeasurer


class Layout:

    @abstractmethod
    def measure(self, component: 'Component', measurer: IMeasurer):
        if len(component.children) > 0:
            for child in component.children:
                child.x = component.x
                child.y = component.y

    @abstractmethod
    def arrange(self, component: 'Component'):
        pass
