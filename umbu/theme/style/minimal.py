from .interface import Animation, AnimationData, Style, StyleData, TextStyle, ContainerStyle, StyleState

class ContainerAnimation(Animation):

    def update(self, node, current_frame):
        pass

class TextAnimation(Animation):

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

        # if node.state != StyleState.DONE:
        #     factor = self.ease_out_bounce(self.get_process(node, current_frame))
        #     node.style.scale = factor

minimal = Style(
    spacing=20,
    states={
        StyleState.ACTIVE: StyleData(
            text=TextStyle(
                font_size=50,
                weight="bold",
                color="#FFFFFF",
            ),
            container=ContainerStyle(
                color="#FF0000"
            ),
        ), 
        # StyleState.INACTIVE: {},
        # StyleState.DONE: {} 
    },

    animation=AnimationData(
        text=TextAnimation(),
        container=ContainerAnimation()
    ) 
)
