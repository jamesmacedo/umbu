from abc import ABC, abstractmethod
from umbu.components import Component 


class IRender(ABC):
    
    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def render(self, component: Component):
        pass
