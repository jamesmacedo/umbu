from abc import ABC, abstractmethod

class IAnimation(ABC):
    
    @staticmethod
    def get_process(star):
        # if current_frame < start: return 0.0
        # if current_frame > start + duration: return 1.0
        #
        # progress = (current_frame - start) / duration
        pass
        
    @abstractmethod
    def update(self, node, current_frame) -> bool:
        pass
