import umbu.constants as constants

from umbu.core.ui import Row, Text
from umbu.core.models.layout import WordState
from umbu.core.engine.appearance import Animation


class StaticAnimation(Animation):

    def setup(self):
        pass

    def draw(self, state):

        self.canva.clear()

        layer = self.canva.createOrFindLayer("STAGE")
        layer.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))

        row = Row(layer, [Text(layer, self.canva.buffer, word.copy(update={"size": constants.FONT_SIZE, "state": WordState.ACTIVATED}), self.canva.style) for word in state.current_chunk])
        row.draw()
        bytes = self.canva.compose()
        self.canva.dispose()
        return bytes
