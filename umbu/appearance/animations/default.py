import umbu.constants as constants

from umbu.core.ui import Row, Text
from umbu.core.models.layout import WordState
from umbu.core.engine.appearance import Animation


class DefaultAnimation(Animation):

    def setup(self):
        pass

    def draw(self, state):

        self.canva.clear()

        layer2 = self.canva.createOrFindLayer("STAGE")
        word_state = WordState.ACTIVATED

        size = constants.FONT_SIZE
        if state.current_word.current_frame <= constants.INTRO_THRESHOLD:
            size = state.current_word.current_frame/constants.INTRO_THRESHOLD * constants.FONT_SIZE
        else:
            word_state = WordState.COMPLETED

        text = Text(layer2, self.canva.buffer, state.current_word.copy(update={'size': size, 'state': word_state}), self.canva.style)

        x = (constants.WIDTH - text.word.shape.width)/2
        layer2.setCursor(x, (constants.HEIGHT * constants.VERTICAL_ALIGN))

        text.word.shape.x = layer2.cursor.x
        text.word.shape.y = layer2.cursor.y

        layer2.data.layout.set_text(text.word.content, -1)

        if text.word.shape.width != text.final_shape.width:
            x = text.word.shape.x - text.final_shape.width/2 + text.word.shape.width/2
            y = text.word.shape.y
        else:
            x = text.word.shape.x
            y = text.word.shape.y

        text.word.shape.x = x
        text.word.shape.y = y
        text.draw()

        bytes = self.canva.compose()
        self.canva.dispose()
        return bytes
