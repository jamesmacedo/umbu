from .interface import Animation, Style, TextStyle, StyleState

class MinimalAnimation(Animation):

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
            factor = self.ease_out_bounce(self.get_process(node, current_frame))
            node.y = self.lerp(node.y, node.y-10, factor)


minimal = Style(
    spacing=20,
    text=TextStyle(
        font_family = "Luckiest Guy",
        font_size=50,
        weight="bold",
        color="#63FFC1",
        outline_width=12.0,
        outline_color="#000000"
    ),

    states={
        StyleState.ACTIVE: TextStyle(
        ),

        StyleState.INACTIVE: TextStyle(
        ),

        StyleState.DONE: TextStyle(
        )
    }
)
