class StyleBase:

    def getColorsRGB(self, value: str):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def getColorsCairo(self, value: str):
        value = value.lstrip('#')
        lv = len(value)
        return tuple((int(value[i:i + lv // 3], 16)/255) for i in range(0, lv, lv // 3))
