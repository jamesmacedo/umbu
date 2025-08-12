from abc import ABC, abstractmethod
from umbu.core.models.layout import Shape
import umbu.constants as constants
from gi.repository import Pango


class Style(ABC):

    def __init__(self):
        pass

    def setFont(self, layer, buffer, font: str = "", size: int = 10):
        desc = Pango.FontDescription()
        desc.set_family(font)
        desc.set_size(size * Pango.SCALE)
        desc.set_weight(Pango.Weight.BOLD)
        layer.data.layout.set_font_description(desc)
        buffer.data.layout.set_font_description(desc)

    def setup(self, word, layer, buffer):

        self.setFont(layer, buffer, "Montserrant", constants.FONT_SIZE)

        buffer.data.layout.set_text(word.content, -1)
        buffer.data.context.set_source_rgb(1, 1, 1)

        ink_rect, logical_rect = buffer.data.layout.get_pixel_extents()

        final_shape = Shape(
            x=0,
            y=0,
            width=logical_rect.width,
            height=logical_rect.height
        )

        self.setFont(layer, buffer, "Montserrant", word.size)

        buffer.data.layout.set_text(word.content, -1)
        buffer.data.context.set_source_rgb(1, 1, 1)
        ink_rect, logical_rect = buffer.data.layout.get_pixel_extents()

        current_shape = Shape(
            x=0,
            y=0,
            width=logical_rect.width,
            height=logical_rect.height
        )

        return final_shape, current_shape

    @staticmethod
    def modify(text):
        return text

    def getColorsRGB(self, value: str):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def getColorsCairo(self, value: str):
        value = value.lstrip('#')
        lv = len(value)
        return tuple((int(value[i:i + lv // 3], 16)/255) for i in range(0, lv, lv // 3))
