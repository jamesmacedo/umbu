from .interface import Animation, Style, StyleData, TextStyle, ContainerStyle, StyleState

minimal_yellow = Style(
    spacing=20,
    states={
        StyleState.ACTIVE: StyleData(
            text=TextStyle(
                font_size=60,
                weight="bold",
                color="#f9fa0c",
                outline_color = "#000000",
                outline_width = 10.0
            ),
        ), 

        StyleState.INACTIVE: StyleData(
            text=TextStyle(
                font_size=60,
                weight="bold",
                color="#f9fa0c",
                outline_color = "#000000",
                outline_width = 10.0
            ),
        ), 

        StyleState.DONE: StyleData(
            text=TextStyle(
                font_size=60,
                weight="bold",
                color="#f9fa0c",
                outline_color = "#000000",
                outline_width = 10.0
            ),
        ),
    },
)
