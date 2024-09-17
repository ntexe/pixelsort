LOG_FOLDER = "logs"
LOG_FORMAT = "{unix_timestamp}.log"

LOGLEVEL_CHOICES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
AUX_LL_CHOICES = list(map(str.lower, LOGLEVEL_CHOICES))
SEGMENTATION_CHOICES = ["none", "edge", "melting", "chunky", "blocky"]
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]
FORMAT_CHOICES = ["png", "jpg", "same"]

DEFAULTS = {
    "input_path":     "",
    "output_path":    "",
    "loglevel":       "INFO",
    "segmentation":   "edge",
    "skey_choice":    "lightness",
    "format":         "same",
    "threshold_arg":  0.1,
    "angle_arg":      0,
    "sangle_arg":     90,
    "size_arg":       0.05,
    "randomness_arg": 0,
    "length_arg":     10,
    "scale_arg" :     1,
    "width_arg":      0,
    "height_arg":     0,
    "amount":         1,
    "second_pass":    False,
    "reverse":        False,
    "silent":         False,
    "nolog":          False
}

RANGE_DEFAULTS = {
    "t_range":  (DEFAULTS["threshold_arg"] ,)*2,
    "a_range":  (DEFAULTS["angle_arg"]     ,)*2,
    "sa_range": (DEFAULTS["sangle_arg"]    ,)*2,
    "sz_range": (DEFAULTS["size_arg"]      ,)*2,
    "r_range":  (DEFAULTS["randomness_arg"],)*2,
    "l_range":  (DEFAULTS["length_arg"]    ,)*2,
    "sc_range": (DEFAULTS["scale_arg"]     ,)*2,
    "w_range":  (DEFAULTS["width_arg"]     ,)*2,
    "h_range":  (DEFAULTS["height_arg"]    ,)*2,
}

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in images."
HELP_LOGLEVEL = f"Log level for command line. Available choices: {', '.join(LOGLEVEL_CHOICES)} (lowercase is also accepted). Default is {DEFAULTS['loglevel']}"
HELP_INPUT_PATH = "Input image file path."
HELP_OUTPUT_PATH = "Output image file path."
HELP_FORMAT = f"Output image format. Available choices: {', '.join(FORMAT_CHOICES)}. Default is {DEFAULTS['format']}."
HELP_SEGMENTATION = f"Segmentation. Available choices: {', '.join(SEGMENTATION_CHOICES)}. Default is {DEFAULTS['segmentaion']}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {DEFAULTS['skey_choice']}."

HELP_THRESHOLD = f"Threshold for edge detection. Value should be between 0 and 1. Default is {DEFAULTS['threshold']}."
HELP_ANGLE = f"Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is {DEFAULTS['angle']}."
HELP_SANGLE = f"Angle for second pass. Value should be between 0 and 360. Default is {DEFAULTS['sangle']}."
HELP_SIZE = f"Size of \"melting\" or \"blocky\" segmentation. Value should be between 0 and 1. Default is {DEFAULTS['size']}."
HELP_RANDOMNESS = f"Randomness of \"blocky\" or \"chunky\" segmentation. Value should be between 0 and 0.5. Default is {DEFAULTS['randomness']}."
HELP_LENGTH = f"Length of \"chunky\" segmentation. Value should be a natural value. Default is {DEFAULTS['length']}."

HELP_SCALE = f"Rescale image before sorting. If width or height are non-zero this value will be ignored. Value should be between 0.01 and 10. Default is {DEFAULTS['scale']}."
HELP_WIDTH = f"Resize to width before sorting. Value should be greater than or equal to 0. If value is zero, width is calculated automatically. Default is {DEFAULTS['width']}."
HELP_HEIGHT = f"Resize to height before sorting. Value should be greater than or equal to 0. If value is zero, height is calculated automatically. Default is {DEFAULTS['height']}."

HELP_AMOUNT = f"Amount of images. Value should be a natural value. Default is {DEFAULTS['amount']}."

HELP_SECOND_PASS = "Second pass flag."
HELP_REVERSE = "Reverse sort flag."
HELP_SILENT = "Make app silent in command line."
HELP_NOLOG = "Disable logging."
