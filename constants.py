SEGMENTATION_DEFAULT = "edge"
SEGMENTATION_CHOICES = ["none", "edge", "melting", "blocky"]
#SEGMENTATION_SHORT = {"none": "n", "edge": "e", "melting": "m", "blocky": "b"}

SKEY_DEFAULT = "lightness"
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]
#SKEY_SHORT = {"hue": "h", "lightness": "l", "saturation": "s", "min_value": "minv", "max_value": "maxv", "red": "r", "green": "g", "blue": "b"}

THRESHOLD_DEFAULT = 0.1
ANGLE_DEFAULT = 0
SANGLE_DEFAULT = 90
SIZE_DEFAULT = 0.05
RANDOMNESS_DEFAULT = 0.1
AMOUNT_DEFAULT = 1

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in pictures."
HELP_INPUT_FILE = "Input image file."
HELP_OUTPUT = "Output image file."
HELP_SEGMENTATION = f"Segmentation. Available choices: {', '.join(SEGMENTATION_CHOICES)}. Default is {SEGMENTATION_DEFAULT}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {SKEY_DEFAULT}."
HELP_THRESHOLD = f"Threshold for edge detection. Value should be between 0 and 1. Default is {THRESHOLD_DEFAULT}."
HELP_ANGLE = f"Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is {ANGLE_DEFAULT}"
HELP_SIZE = f"Size of \"melting\" or \"blocky\" segmentation. Value should be between 0 and 1. Default is {SIZE_DEFAULT}"
HELP_RANDOMNESS = f"Randomness of \"blocky\" segmentation. Value should be between 0 and 0.5. Default is {RANDOMNESS_DEFAULT}"
HELP_AMOUNT = f"Amount of images. Value should be an integer. Default is {AMOUNT_DEFAULT}"
HELP_SANGLE = f"Angle for second pass. Default is {SANGLE_DEFAULT}."
HELP_SECOND_PASS = "Second pass flag."
HELP_REVERSE = "Reverse sort flag."
