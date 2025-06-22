import umbu.constants as constants

from umbu.core.ui import Row, Text
from umbu.core.models.layout import WordState
from umbu.core.engine.appearance import Animation


class DefaultAnimation(Animation):

    def setup(self):
        pass

    def draw(self):

        self.canva.clear()

        layer2 = self.canva.createLayer()
        text = Text(layer2, self.canva.buffer, self.canva.state.current_word, self.canva.style)

        x = (constants.WIDTH - text.word.shape.width)/2
        layer2.setCursor(x, (constants.HEIGHT * constants.VERTICAL_ALIGN))

        text.word.shape.x = layer2.cursor.x
        text.word.shape.y = layer2.cursor.y

        layer2.data.layout.set_text(text.word.content, -1)

        if self.canva.state.current_word.current_frame <= constants.INTRO_THRESHOLD:
            self.canva.state.current_word.size = self.canva.state.current_word.current_frame/constants.INTRO_THRESHOLD * constants.FONT_SIZE
        else:
            self.canva.state.current_word.state = WordState.COMPLETED

        if text.word.shape.width != text.final_shape.width:
            x = text.word.shape.x - text.final_shape.width/2 + text.word.shape.width/2
            y = text.word.shape.y
        else:
            x = text.word.shape.x
            y = text.word.shape.y

        text.word.shape.x = x
        text.word.shape.y = y
        text.draw()

        self.canva.compose(self.canva.frame)
