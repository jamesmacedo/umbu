from abc import ABC, abstractmethod


class Animation(ABC):

    def __init__(self, canva):
        self.canva = canva

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self):
        pass
