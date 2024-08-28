THRESHOLD_DEFAULT = 0.5

SEGMENTATION_DEFAULT = "edge"
SEGMENTATION_CHOICES = ["none", "edge", "melting"]

SKEY_DEFAULT = "lightness"
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]

ANGLE_DEFAULT = 0

SIZE_DEFAULT = 0.05

RANDOMNESS_DEFAULT = 0.1

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in pictures."
HELP_INPUT_FILE = "Input file."
HELP_THRESHOLD = f"Threshold for edge detection. Value should be between 0 and 1. Default is {THRESHOLD_DEFAULT}."
HELP_SEGMENTATION = f"Segmentation. Available choices: {', '.join(SEGMENTATION_CHOICES)}. Default is {SEGMENTATION_DEFAULT}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {SKEY_DEFAULT}."
HELP_ANGLE = f"Angle to rotate the image before sorting in degrees. Default is {ANGLE_DEFAULT}"
HELP_SIZE = f"Size of \"melting\" segmentation. Value should be between 0 and 1. Default is {SIZE_DEFAULT}"
HELP_RANDOMNESS = f"Randomness of \"melting\" segmentation. Value should be between 0 and 1. Default is {RANDOMNESS_DEFAULT}"
