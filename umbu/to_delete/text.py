import umbu.constants as constants
import numpy as np

from typing import List

from umbu.core.models.layout import Word, Shape


class Text:

    word: Word = None
    final_shape: Shape
    style: type = None

    def __init__(self, layer, buffer, word: Word, style: type):
        self.buffer = buffer
        self.layer = layer

        self.style = style

        word.content = style.modify(word.content)

        final_shape, current_shape = style().setup(word, layer, buffer)
        self.final_shape = final_shape

        word.shape = current_shape
        self.word = word

    def draw(self):
        self.layer.data.layout.set_text(self.word.content, -1)

        if self.word.shape.width != self.final_shape.width:
            x = self.word.shape.x + self.final_shape.width/2 - self.word.shape.width/2
            y = self.word.shape.y + self.final_shape.height/2 - self.word.shape.height/2
        else:
            x = self.word.shape.x
            y = self.word.shape.y

        self.style().draw(x, y, self.layer, self.word)


class Row:

    shape: Shape
    components: List[Text] = []

    def __init__(self, layer,  components: List[Text]):
        self.layer = layer
        self.components = components

        width_arr = [component.word.shape.width for component in components]

        width = sum(width_arr) + constants.TEXT_PADDING * (len(width_arr) - 1)
        height = np.max([component.word.shape.height for component in components])

        self.shape = Shape(
            x=0,
            y=0,
            width=width,
            height=height
        )

        # Alterar isso para buscar as proporcoes do Canva
        self.layer.cursor.x = (constants.WIDTH - self.shape.width)/2

    def draw(self):
        for i, comp in enumerate(self.components):

            # if (comp.word.state != WordState.COMPLETED):
            #     comp.word.state = WordState.UNACTIVATED

            comp.word.shape.x = self.layer.cursor.x

            new_x = self.layer.cursor.x + comp.word.shape.width + constants.TEXT_PADDING
            comp.word.shape.y = self.layer.cursor.y
            self.layer.cursor.x = new_x
            comp.draw()
