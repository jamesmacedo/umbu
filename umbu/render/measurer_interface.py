from abc import ABC, abstractmethod


class IMeasurer(ABC):
    @abstractmethod
    def measure(self, component: 'Component') -> tuple[float, float]:
        pass

