'''
file: strip.py
contains functions and classes about ws281x Led strip
'''
import os.path
from collections import namedtuple

from pizstrip.helpers import cursor

Color = namedtuple("Color", ['red', 'green', 'blue'])


def make_strip(cfg, led_count):
    '''
    return either a NoStrip or an Adafruit Strip based on if we are running on
    a Raspberry Pi or else
    '''

    if os.path.isfile('/sys/firmware/devicetree/base/model'):
        # we are on a pi
        import rpi_ws281x as np  # pragma: no cover pylint: ignore import-error
        ret = np.Adafruit_NeoPixel(
            led_count,
            cfg.getint("general", "led_pin"),
            cfg.getint("general", "led_freq"),
            cfg.getint("general", "led_dma"),
            cfg.getboolean("general", "led_invert"),
            cfg.getint("general", "brightness"),
            cfg.getint("general", "led_channel")
        )
    else:
        ret = NoStrip(led_count, size_x=32, size_y=9)

    return ret


def get_color_class():
    '''
    get color class depending on platform
    '''
    if os.path.isfile('/sys/firmware/devicetree/base/model'):
        # we are on a pi
        import rpi_ws281x as np  # pragma: no cover pylint: ignore import-error
        ret = np.Color
    else:
        ret = Color
    return ret


class NoStrip():
    """
    this class only prints the strip to stdout
    """
    # pylint: disable=invalid-name

    def __init__(self, length, **kwargs):
        self.pixels = []
        self.length = length
        for i in range(length):
            pixel = Pixel(x=i, color=Color(0, 0, 0))
            self.pixels.append(pixel)

    def show(self):
        '''
        show the current strip on the screen as text
        '''
        line=[]
        for pixel in self.pixels:
            char = "\x1b[38;2;{};{};{}m#\x1b[0m".format(
                pixel.color.red, pixel.color.green, pixel.color.blue)
            line.append(char)
        data = "".join(str(_) for _ in line)
        cursor(5, 10, data)

    def begin(self):
        '''
        method to initialize the strip (if it is a real Adafruit_NeoPixel strip
        '''

    def setPixelColor(self, pixel, color):
        '''
        set the pixel at position `pixel` to color
        '''
        self.pixels[pixel].color = color

    def getPixelColor(self, pixel):
        '''
        returns the color of the pixel at position `pixel` in the strip
        '''
        color = (self.pixels[pixel].red<<16) | \
            (self.pixels[pixel].green<<8) | self.pixels[pixel].blue
        return color

    def numPixels(self):
        '''
        function returning the number of pixels in the strip
        '''
        return self.length


class Pixel():  # pylint: disable=too-few-public-methods
    '''
    class representing a singel Pixel in the LED Strip
    '''

    def __init__(self, x=0, y=0, color=None):
        self.color = color
        self.x = x  # pylint: disable=invalid-name
        self.y = y  # pylint: disable=invalid-name

    @property
    def red(self):  # pylint: disable=missing-docstring
        return self.color.red

    @property
    def green(self):  # pylint: disable=missing-docstring
        return self.color.green

    @property
    def blue(self):  # pylint: disable=missing-docstring
        return self.color.blue

    def set_color(self, color):
        '''
        set color of the pixel to given color array
        '''
        self.color = color
