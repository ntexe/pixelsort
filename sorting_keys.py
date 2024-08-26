import colorsys

def hue(pixel):
    return colorsys.rgb_to_hls(*[i/255 for i in pixel])[0]

def lightness(pixel):
    return colorsys.rgb_to_hls(*[i/255 for i in pixel])[1]

def saturation(pixel):
    return colorsys.rgb_to_hls(*[i/255 for i in pixel])[2]

def min_value(pixel):
    return min(pixel)

def max_value(pixel):
    return max(pixel)