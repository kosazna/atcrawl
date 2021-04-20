from dataclasses import dataclass


@dataclass
class Color:
    name: str
    hex_value: str
    rgb_value: tuple

    def rgb(self, a=None):
        if a is None:
            return f"rgb{self.rgb_value!r}"
        else:
            _rgb = (*self.rgb_value, a)
            return f"rgba{_rgb!r}"

    def hex(self):
        return self.hex_value


blue = Color('blue', '#0D6EFD', (13, 110, 253))
grey = Color('grey', '#6C757D', (108, 117, 125))
light_grey = Color('light_grey', '#D6D6D6', (214, 214, 214))
red = Color('red', '#EF3E4F', (239, 62, 79))
yellow = Color('yellow', '#FFC107', (255, 193, 7))
green = Color('green', '#2AD66B', (42, 214, 107))
teal = Color('teal', '#20C997', (32, 201, 151))
cyan = Color('cyan', '#0DCAF0', (13, 202, 79))
orange = Color('orange', '#FD7E14', (253, 126, 20))
dark = Color('dark', '#212529', (33, 37, 41))
white = Color('white', '#F8F8FF', (248, 248, 255))


def make_stylesheet(background: Color = white,
                    foreground: Color = dark,
                    radius: int = 5,
                    alpha: float = 0.8) -> str:

    _stylesheet = (f"background-color: {background.rgb(alpha)};\n"
                   f"color: {foreground.rgb()};\n"
                   f"border-radius: {radius}px;")

    return _stylesheet


def make_color(color: Color, alpha: float = 0.8) -> str:
    return f"background-color: {color.rgb(alpha)};\n"
