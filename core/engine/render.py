import constants

from core.ui.text import Row


class Renderer:

    @staticmethod
    def render(layout, buffer):
        if layout.state.cursor.position == 0:
            row = Row(layout.state.current_chunk,
                    layout,
                    buffer)
            row.draw((layout.width - row.shape.width)/2, (layout.height * constants.VERTICAL_ALIGN) - row.shape.height/2)
        else:
            pass
        layout.save(f"frames/{layout.state.cursor.position:03d}.png")
