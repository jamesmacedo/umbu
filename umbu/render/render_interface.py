from abc import ABC, abstractmethod
from umbu.components import Component, Text


class IRender(ABC):

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def render(self, component: Component):
        pass

    @abstractmethod
    def draw(self, text: Text):
        pass
