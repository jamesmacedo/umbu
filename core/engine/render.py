import constants

from core.ui.text import Row, Text
from core.models.layout import WordState


class Renderer:

    @staticmethod
    def render(canva):

        canva.clear()

        # layer = canva.createLayer()
        # layer.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))
        # row = Row(layer, [Text(layer, canva.buffer, word.copy(update={"state": WordState.UNACTIVATED})) for word in canva.state.current_chunk])
        # row.draw()

        layer2 = canva.createLayer()
        layer2.setCursor(0, 0)
        # row2 = Row(layer2, [Text(layer2, canva.buffer, word) for word in canva.state.current_chunk])

        text = Text(layer2, canva.buffer, canva.state.current_word)
        text.draw()

        canva.compose(canva.frame)
