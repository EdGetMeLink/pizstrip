'''
file: test_strip.py

contains tests fro the strip module
'''

import os

from pizstrip.strip import Color, NoStrip, Pixel, get_color_class, make_strip


def test_make_strip():
    '''
    test make strip function
    '''
    if os.path.isfile('/sys/firmware/devicetree/base/model'):
        import neopixel as np  # pragma: no cover pylint: disable=import-error
        expected = np.Adafruit_NeoPixel
    else:
        expected = NoStrip
    result = make_strip("blah", 1)
    assert isinstance(result, expected)


def test_get_color_class():
    '''
    test get color class
    '''
    if os.path.isfile('/sys/firmware/devicetree/base/model'):
        import neopixel as np  # pragma: no cover pylint: disable=import-error
        expected = np.Color
    else:
        expected = Color
    result = get_color_class()(0, 0, 0)
    assert isinstance(result, expected)


def test_set_pixel_color():
    '''
    test set pixel color method
    '''
    pixel = Pixel()
    pixel.set_color(Color(1, 2, 3))
    expected = Color(1, 2, 3)
    assert pixel.color == expected
    assert pixel.red == 1
    assert pixel.green == 2
    assert pixel.blue == 3


def test_strip_set_get_pixel_color():
    '''
    test setting the color of a pixel
    '''
    strip = NoStrip(3)
    strip.setPixelColor(1, Color(1, 2, 4))
    expected = (1 << 16) | (2 << 8) | 4
    result = strip.getPixelColor(1)
    assert expected == result


def test_pixel_blink():
    '''
    test pixel blink functionality
    '''
    strip = NoStrip(3)
