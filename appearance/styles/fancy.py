from gi.repository import PangoCairo
from core.models.layout import WordState
from core.engine.appearance import Style


class FancyStyle(Style):

    def draw(self, x, y, layer, word):

        layer.data.context.move_to(x, y)

        if word.state is WordState.COMPLETED:
            layer.data.context.set_source_rgb(*super().getColorsCairo("#FFFFFF"))
        elif word.state is WordState.ACTIVATED:
            layer.data.context.set_source_rgb(*super().getColorsCairo("#F9C606"))
        elif word.state is WordState.UNACTIVATED:
            layer.data.context.set_source_rgb(*super().getColorsCairo("#F9C606"))
            layer.data.context.set_line_width(1.5)

        if word.state == WordState.UNACTIVATED:
            PangoCairo.layout_path(layer.data.context, layer.data.layout)
            layer.data.context.stroke()
        else:
            PangoCairo.show_layout(layer.data.context, layer.data.layout)
