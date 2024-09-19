import colorsys
from functools import cache

@cache
def hue(pixel):
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[0]*255)

@cache
def lightness(pixel):
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[1]*255)

@cache
def saturation(pixel):
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[2]*255)

@cache
def min_value(pixel):
    return min(pixel)

@cache
def max_value(pixel):
    return max(pixel)

@cache
def red(pixel):
    return pixel[0]

@cache
def green(pixel):
    return pixel[1]

@cache
def blue(pixel):
    return pixel[2]
