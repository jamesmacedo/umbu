import umbu.constants as constants

from umbu.core.ui import Row, Text
from umbu.core.models.layout import WordState
from umbu.core.engine.appearance import Animation


class ClassicAnimation(Animation):

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

        words = []
        found = False

        for word in state.current_chunk:
            if not found and word.content == state.current_word.content:
                words.append(word.copy(update={"state": WordState.ACTIVATED}))
                found = True
            elif not found:
                words.append(word.copy(update={"state": WordState.COMPLETED}))
            else:
                words.append(word.copy(update={"state": WordState.UNACTIVATED}))

        layer2 = self.canva.createOrFindLayer("BACKGROUND")
        layer2.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))
        row = Row(
            layer2,
            [Text(layer2, self.canva.buffer, word.copy(update={"size": constants.FONT_SIZE}), self.canva.style)
             for word in words]
        )
        row.draw()

        bytes = self.canva.compose()
        self.canva.dispose()
        return bytes
