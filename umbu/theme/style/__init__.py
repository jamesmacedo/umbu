from .minimal_white import minimal_white
from .minimal_yellow import minimal_yellow
from .scale import scale
from .bounce import bounce 
from .minimalist import minimalist  
from .base import Animation, Style, StyleState, StyleData, AnimationData

__all__ = [
    # Available default styles
    'minimal_yellow',
    'minimal_white',
    'scale',
    'bounce',
    'minimalist',

    # Internal classes
    'Animation',
    'Style',
    'StyleState',
    'AnimationData',
    'StyleData',
]
