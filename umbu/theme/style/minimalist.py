from .base import Style, StyleData, TextStyle, StyleState


minimalist = Style(
    states={
        StyleState.BASE: StyleData(
            text=TextStyle(
                font_size=20,
                color="#FFFFFF",
            ),
        ),
    },
)
