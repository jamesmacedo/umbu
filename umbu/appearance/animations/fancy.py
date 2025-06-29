import umbu.constants as constants

from umbu.core.ui import Row, Text
from umbu.core.models.layout import WordState
from umbu.core.engine.appearance import Animation


class FancyAnimation(Animation):

    def setup(self):
        pass

    def draw(self, state):

        self.canva.clear(True)

        if state.current_chunk is None:
            bytes = self.canva.compose()
            self.canva.dispose()
            return bytes

        layer = self.canva.createOrFindLayer("BACKGROUND")
        layer.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))
        row = Row(layer, [Text(layer, self.canva.buffer, word.copy(update={"size": constants.FONT_SIZE}), self.canva.style) for word in state.current_chunk])
        row.draw()
        layer.lock()

        layer2 = self.canva.createOrFindLayer("FOREGROUND")
        layer2.setCursor(0, 0)

        word_state = WordState.ACTIVATED
        if state.current_word.current_frame >= state.current_word.total_frames-4:
            word_state = WordState.COMPLETED
            print(f"frame fancy: {state.current_word.current_frame}")

        print(f"state: {word_state}")

        text = Text(layer2, self.canva.buffer, state.current_word.copy(update={'state': word_state}), self.canva.style)
        text.draw()

        bytes = self.canva.compose()
        self.canva.dispose()
        return bytes
