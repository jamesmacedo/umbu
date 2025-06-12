from gi.repository import PangoCairo
from core.models.layout import WordState
from core.ui.style.base import StyleBase


class GuildStyle(StyleBase):

    def draw1(self, x, y, layout, word):
        if word.state is WordState.COMPLETED:
            layout.context.context.set_source_rgb(1, 1, 1)
        elif word.state is WordState.ACTIVATED:
            layout.context.context.set_source_rgb(0,1,0)
        elif word.state is WordState.UNACTIVATED:
            layout.context.context.set_source_rgb(1,0,1)
            layout.context.context.set_line_width(1.5)

        layout.context.context.move_to(x, y)
        if word.state == WordState.UNACTIVATED:
            PangoCairo.layout_path(layout.context.context, layout.context.layout)
            layout.context.context.stroke()
        else:
            PangoCairo.show_layout(layout.context.context, layout.context.layout)

    def draw2(self, x, y, layout, word):
        if word.state is WordState.COMPLETED:
            layout.context.context.set_source_rgb(1, 1, 1)
        elif word.state is WordState.ACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
        elif word.state is WordState.UNACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
            layout.context.context.set_line_width(1.5)

        layout.context.context.move_to(x, y)
        if word.state == WordState.UNACTIVATED:
            PangoCairo.layout_path(layout.context.context, layout.context.layout)
            layout.context.context.stroke()
        else:
            PangoCairo.show_layout(layout.context.context, layout.context.layout)

    def draw3(self, x, y, layout, word):
        if word.state is WordState.COMPLETED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
        elif word.state is WordState.ACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.primary))
        elif word.state is WordState.UNACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.primary))
            layout.context.context.set_line_width(1.5)

        layout.context.context.move_to(x, y)
        if word.state == WordState.UNACTIVATED:
            PangoCairo.layout_path(layout.context.context, layout.context.layout)
            layout.context.context.stroke()
        else:
            PangoCairo.show_layout(layout.context.context, layout.context.layout)
