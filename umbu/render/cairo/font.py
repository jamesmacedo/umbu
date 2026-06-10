from gi.repository import Pango, PangoCairo, PangoFT2

class FontCache:

    def __init__(self):
        self.fonts = {}

    def get_font_description(self, style, scale):

        key = (
            style.font_family,
            style.font_size * scale,
            style.weight
        )

        if key in self.fonts:
            return self.fonts[key]

        desc = Pango.FontDescription()
        desc.set_family(style.font_family)
        desc.set_size((style.font_size * Pango.SCALE) * scale)

        if style.weight == "bold":
            desc.set_weight(Pango.Weight.BOLD)

        self.fonts[key] = desc

        return desc
