from .interface import IAnimation, ComponentStyle, TextStyle, StyleState

class MinimalAnimation(IAnimation):

    def update(self, node, current_frame):

        initial_frames = 5

        if self.get_process(node, current_frame) == 1:
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


minimal = ComponentStyle(
    base=TextStyle(
        font_size=50,
    ),

    states={
        StyleState.ACTIVE: TextStyle(
            color="#00FF00",
        ),

        StyleState.INACTIVE: TextStyle(
            color="#00FF00",
            outline_width=4
        ),

        StyleState.DONE: TextStyle(
            color="#999999"
        )
    }
)
