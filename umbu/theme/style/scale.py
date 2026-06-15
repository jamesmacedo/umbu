from .interface import Animation, ShadowStyle, Style, StyleData, TextStyle, StyleState


class ScaleAnimation(Animation):

    def update(self, node, current_frame):

        initial_frames = 2

        process = self.get_process(node, current_frame)

        if process == 1:
            node.state = StyleState.DONE
            return

        if node.total_frames < initial_frames:
            node.state = StyleState.DONE
            return

        if current_frame < initial_frames:
            node.state = StyleState.INACTIVE

        if current_frame > initial_frames:
            node.state = StyleState.ACTIVE

        if node.state != StyleState.DONE:
            factor = self.ease_out_bounce(
                self.get_process(node, current_frame))
            node.text.scale = factor

scale = Style(
    spacing=20,
    states={
        StyleState.BASE: StyleData(
            text=TextStyle(
                font_size=60,
                weight="bold",
                color="#FFFFFF",
                outline_color = "#000000",
                outline_width = 10.0,
                shadow=ShadowStyle(
                    offset_x = 8,
                    offset_y = 8,
                    color = "#000000FF" # hex with alpha
                )
            ),
        ), 
    },
    animation=ScaleAnimation()
)

