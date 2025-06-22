import umbu.constants as constants

from umbu.core.ui import Row, Text
from umbu.core.models.layout import WordState
from umbu.core.engine.appearance import Animation


class FancyAnimation(Animation):

    def setup(self):
        pass

    def draw(self):

        self.canva.clear()

        if (self.canva.frame == 0 or self.canva.state.previous_word != self.canva.state.current_word):
            layer = self.canva.createLayer()
            layer.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))
            row = Row(layer, [Text(layer, self.canva.buffer, word.copy(update={"size": constants.FONT_SIZE}), self.canva.style) for word in self.canva.state.current_chunk])
            row.draw()
            layer.lock()

        layer2 = self.canva.createLayer()
        layer2.setCursor(0, 0)
        text = Text(layer2, self.canva.buffer, self.canva.state.current_word, self.canva.style)

        if self.canva.state.current_word.current_frame >= self.canva.state.current_word.total_frames-2:
            self.canva.state.current_word.state = WordState.COMPLETED

        text.draw()

        self.canva.compose(self.canva.frame)
