from .interface import ShadowStyle, Style, StyleData, TextStyle, StyleState

minimal_white = Style(
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
)
