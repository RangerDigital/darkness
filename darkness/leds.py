import math
from rpi_ws281x import Adafruit_NeoPixel


# Changes HSV list [360, 0.5, 0.5] into RGB list [127, 63, 63].
def hsv_to_rgb(hsv):
    h = hsv[0] / 360
    s = hsv[1]
    v = hsv[2]

    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i % 6)]

    return [int(r * 255), int(g * 255), int(b * 255)]


## TODO: Add configuration options.
class StripController():
    def __init__(self):
        self.strip = Adafruit_NeoPixel(16, 18)

        self.hsv = [0, 0, 0]
        self._status = True
        self.event_running = False

        # On start changes values to black.
        self.strip.begin()
        self.set_color(self.hsv)


    def set_color(self, hsv, id=None, save_state=True):
        rgb = hsv_to_rgb(hsv)

        # Fix blinking on leds from changing state with status = False.
        if not self._status:
            return

        if id is not None:
            self.strip.setPixelColorRGB(id, *rgb)
        else:
            for led in range(self.strip.numPixels()):
                self.strip.setPixelColorRGB(led, *rgb)

        self.strip.show()

        # Saves color as currently displayed.
        if save_state:
            self.hsv = hsv


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status:
            self.set_color(self.hsv)
        else:
            # Disables leds without saving current color.
            self.set_color([0, 0, 0], save_state=False)

        self._status = status
