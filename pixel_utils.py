import colorsys
from functools import cache

@cache
def hue(pixel):
    """Return pixel hue."""
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[0]*255)

def lightness(pixel):
    """Return pixel lightness."""
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[1]*255)

@cache
def saturation(pixel):
    """Return pixel saturation."""
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[2]*255)

@cache
def min_value(pixel):
    """Return minimum value of pixel."""
    return min(pixel)

@cache
def max_value(pixel):
    """Return maximum value of pixel."""
    return max(pixel)

@cache
def red(pixel):
    """Return red color of pixel."""
    return pixel[0]

@cache
def green(pixel):
    """Return green color of pixel."""
    return pixel[1]

@cache
def blue(pixel):
    """Return blue color of pixel."""
    return pixel[2]
