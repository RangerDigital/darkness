import math


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


# Used for functional testing on amd64 machines without GPIO.
class Mock_Adafruit_NeoPixel():
    def __init__(self, leds, port):
        self.leds = leds

    def begin(self):
        print("WARNING: Couldn't find rpi_ws281x library! Entering dry_run mode.")

    def numPixels(self):
        return self.leds

    def setPixelColorRGB(self, led, r, g, b):
        print("LED: {} -> RGB: {}/{}/{}".format(str(led).zfill(2), r, g, b))

    def show(self):
        print("DEBUG: Strip state was updated!")


class StripController():
    def __init__(self, led_count, led_gpio):
        try:
            from rpi_ws281x import Adafruit_NeoPixel

            self.strip = Adafruit_NeoPixel(led_count, led_gpio)
            self.strip.begin()
        except:
            self.strip = Mock_Adafruit_NeoPixel(led_count, led_gpio)
            self.strip.begin()

        self.hsv = [0, 0, 0]
        self.status = True
        self.event_running = False

        # On start changes values to black.
        self.set_color(self.hsv)

    def get_state(self):
        state = {"hue": self.hsv[0], "saturation": self.hsv[1],
                 "value": self.hsv[2], "status": self.status}

        return state

    def set_state(self, state):
        self.hsv = [state["hue"], state["saturation"], state["value"]]
        self.status = state["status"]

        if state["status"]:
            self.set_color(self.hsv)
        else:
            # Disables leds without saving current color.
            self.set_color([0, 0, 0], save_state=False)

    def set_color(self, hsv, id=None, save_state=True):
        rgb = hsv_to_rgb(hsv)

        # Fix blinking on leds from changing state with status = False.
        if not self.status:
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
