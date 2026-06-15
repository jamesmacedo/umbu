from .interface import ShadowStyle, Style, StyleData, TextStyle, StyleState

minimal_white = Style(
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
)
