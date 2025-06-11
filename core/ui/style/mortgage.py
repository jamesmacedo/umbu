from gi.repository import PangoCairo
from core.models.text import TextModel, TextState
from core.ui.style.base import StyleBase


class GuildStyle(StyleBase):


    def draw1(self, x, y, layout, text: TextModel):
        if text.state is TextState.COMPLETED:
            layout.context.context.set_source_rgb(1, 1, 1)
        elif text.state is TextState.ACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
        elif text.state is TextState.UNACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
            layout.context.context.set_line_width(1.5)

        layout.context.context.move_to(x, y)
        if text.state == TextState.UNACTIVATED:
            PangoCairo.layout_path(layout.context.context, layout.context.layout)
            layout.context.context.stroke()
        else:
            PangoCairo.show_layout(layout.context.context, layout.context.layout)

    def draw2(self, x, y, layout, text: TextModel):
        if text.state is TextState.COMPLETED:
            layout.context.context.set_source_rgb(1, 1, 1)
        elif text.state is TextState.ACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
        elif text.state is TextState.UNACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
            layout.context.context.set_line_width(1.5)

        layout.context.context.move_to(x, y)
        if text.state == TextState.UNACTIVATED:
            PangoCairo.layout_path(layout.context.context, layout.context.layout)
            layout.context.context.stroke()
        else:
            PangoCairo.show_layout(layout.context.context, layout.context.layout)

    def draw3(self, x, y, layout, text: TextModel):
        if text.state is TextState.COMPLETED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.secondary))
        elif text.state is TextState.ACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.primary))
        elif text.state is TextState.UNACTIVATED:
            layout.context.context.set_source_rgb(*super().getColorsCairo(layout.context.company.colors.primary))
            layout.context.context.set_line_width(1.5)

        layout.context.context.move_to(x, y)
        if text.state == TextState.UNACTIVATED:
            PangoCairo.layout_path(layout.context.context, layout.context.layout)
            layout.context.context.stroke()
        else:
            PangoCairo.show_layout(layout.context.context, layout.context.layout)
