import constants

from core.ui.text import Row, Text
from core.models.layout import WordState


class Renderer:

    @staticmethod
    def render(canva):

        # force = canva.state.previous_chunk != canva.state.current_chunk
        canva.clear()

        if (canva.chunk_frame == 0 or canva.state.previous_word != canva.state.current_word):
            layer = canva.createLayer()
            layer.setCursor(0, (constants.HEIGHT * constants.VERTICAL_ALIGN))
            row = Row(layer, [Text(layer, canva.buffer, word.copy(update={"size": constants.FONT_SIZE})) for word in canva.state.current_chunk])
            row.draw()
            layer.lock()

        layer2 = canva.createLayer()
        layer2.setCursor(0, 0)
        text = Text(layer2, canva.buffer, canva.state.current_word)
        print(f"current_size: {canva.state.current_word.size}")
        text.draw()

        canva.compose(canva.frame)
