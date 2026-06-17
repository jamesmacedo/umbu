from .base import Animation, ShadowStyle, Style, StyleData, TextStyle, StyleState


minimal_yellow = Style(
    states={
        StyleState.BASE: StyleData(
            text=TextStyle(
                font_size=20,
                weight="bold",
                color="#f9fa0c",
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
