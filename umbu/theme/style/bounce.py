from .base import Animation, ShadowStyle, Style, StyleData, TextStyle, StyleState


class BounceAnimation(Animation):

    def on_update(self, node, current_frame):

        offset_y = 5

        if node.state != StyleState.DONE:
            factor = self.ease_out_bounce(self.get_process(node, current_frame))
            node.animated.set_y(node.world_y + (offset_y * factor))

    def on_done(self, node, current_frame):
        node.world_y = node.animated.y

scale = Style(
    spacing=20,
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
    animation=BounceAnimation()
)

