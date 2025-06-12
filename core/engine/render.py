import constants

from core.ui.text import Row


class Renderer:

    @staticmethod
    def render(layout, buffer):
        row = Row(layout.state.current_chunk,
                layout,
                buffer)
        row.draw((layout.width - row.shape.width)/2, (layout.height * constants.VERTICAL_ALIGN) - row.height/2)
        layout.save(f"frames/{layout.state.cursor:03d}.png")
