THRESHOLD_DEFAULT = 0.5

INTERVAL_DEFAULT = "edge"
INTERVAL_CHOICES = ["none", "edge"]

SKEY_DEFAULT = "lightness"
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in pictures."
HELP_INPUT_FILE = "Input file."
HELP_THRESHOLD = f"Threshold for edge detection. Default is {THRESHOLD_DEFAULT}."
HELP_INTERVAL = f"Interval type. Available choices: {', '.join(INTERVAL_CHOICES)}. Default is {INTERVAL_DEFAULT}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {SKEY_DEFAULT}."