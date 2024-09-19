import colorsys
import functools

@functools.cache
def hue(pixel):
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[0]*255)

@functools.cache
def lightness(pixel):
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[1]*255)

@functools.cache
def saturation(pixel):
    return int(colorsys.rgb_to_hls(*[i/255 for i in pixel])[2]*255)

@functools.cache
def min_value(pixel):
    return min(pixel)

@functools.cache
def max_value(pixel):
    return max(pixel)

@functools.cache
def red(pixel):
    return pixel[0]

@functools.cache
def green(pixel):
    return pixel[1]

@functools.cache
def blue(pixel):
    return pixel[2]
