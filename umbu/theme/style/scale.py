from .base import Animation, ShadowStyle, Style, StyleData, TextStyle, StyleState


class ScaleAnimation(Animation):

    def on_update(self, node, current_frame):
        if node.state != StyleState.DONE:
            factor = self.ease_out_bounce(self.get_process(node, current_frame))
            node.animated.set_scale(factor)

    def on_done(self, node, current_frame):
        pass

scale = Style(
    states={
        StyleState.BASE: StyleData(
            text=TextStyle(
                font_size=20,
                weight="bold",
                color="#FFFFFF",
                outline_color = "#000000",
                outline_width = 7.0,
                shadow=ShadowStyle(
                    offset_x = 5,
                    offset_y = 5,
                    color = "#000000", # hex without alpha
                )
            ),
        ), 
    },
    animation=ScaleAnimation()
)

