import constants

from core.ui import Row, Text
from core.engine.appearance import Animation


class DefaultAnimation(Animation):

    def setup(self):
        pass

    def draw(self):

        # force = self.canva.state.previous_chunk != self.canva.state.current_chunk
        self.canva.clear()

        if (self.canva.chunk_frame == 0 or self.canva.state.previous_word != self.canva.state.current_word):
            layer = self.canva.createLayer()
            layer.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))
            row = Row(layer, [Text(layer, self.canva.buffer, word.copy(update={"size": constants.FONT_SIZE})) for word in self.canva.state.current_chunk])
            row.draw()
            layer.lock()

        layer2 = self.canva.createLayer()
        layer2.setCursor(0, 0)
        text = Text(layer2, self.canva.buffer, self.canva.state.current_word)
        print(f"current_size: {self.canva.state.current_word.size}")
        text.draw()

        self.canva.compose(self.canva.frame)
        pass
