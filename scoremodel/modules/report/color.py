from colorsys import hsv_to_rgb


class Color:

    # https://stackoverflow.com/questions/340209/generate-colors-between-red-and-green-for-a-power-meter
    # 0 = red; 1 = green
    def rgb(self, color_power):
        hsv = (color_power * 0.35, 0.9, 0.9)
        return hsv_to_rgb(*hsv)

    # RGB from self.rgb are coordinates, but we want web-colors
    def rgb_to_web(self, rgb):
        web = []
        for c in rgb:
            if int(c * 256) == 256:
                web.append(255)
            else:
                web.append(int(c * 256))
        return web

    # pos 0 = red; pos max = green
    def range(self, ordered_list):
        mapped = {}
        i = 0
        highest_index = len(ordered_list) - 1
        for item in ordered_list:
            mapped[item] = self.rgb_to_web(self.rgb(i / highest_index))
            i += 1
        return mapped
