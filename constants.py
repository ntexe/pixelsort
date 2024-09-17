LOG_FOLDER = "logs"
LOG_FORMAT = "{unix_timestamp}.log"
LOGLEVEL_DEFAULT = "INFO"
LOGLEVEL_CHOICES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
AUX_LL_CHOICES = list(map(str.lower, LOGLEVEL_CHOICES))

SEGMENTATION_DEFAULT = "edge"
SEGMENTATION_CHOICES = ["none", "edge", "melting", "chunky", "blocky"]

SKEY_DEFAULT = "lightness"
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]

FORMAT_DEFAULT = "same"
FORMAT_CHOICES = ["png", "jpg", "same"]

THRESHOLD_DEFAULT = 0.1
ANGLE_DEFAULT = 0
SANGLE_DEFAULT = 90
SIZE_DEFAULT = 0.05
RANDOMNESS_DEFAULT = 0
LENGTH_DEFAULT = 10
SCALE_DEFAULT = 1
WIDTH_DEFAULT = 0
HEIGHT_DEFAULT = 0
AMOUNT_DEFAULT = 1

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in images."
HELP_LOGLEVEL = f"Log level for command line. Available choices: {LOGLEVEL_CHOICES} (lowercase is also accepted). Default is {LOGLEVEL_DEFAULT}"
HELP_INPUT_FILENAME = "Input image file name."
HELP_OUTPUT = "Output image file."
HELP_FORMAT = f"Output image format. Available choices: {', '.join(FORMAT_CHOICES)}. Default is {FORMAT_DEFAULT}."
HELP_SEGMENTATION = f"Segmentation. Available choices: {', '.join(SEGMENTATION_CHOICES)}. Default is {SEGMENTATION_DEFAULT}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {SKEY_DEFAULT}."

HELP_THRESHOLD = f"Threshold for edge detection. Value should be between 0 and 1. Default is {THRESHOLD_DEFAULT}."
HELP_ANGLE = f"Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is {ANGLE_DEFAULT}."
HELP_SANGLE = f"Angle for second pass. Value should be between 0 and 360. Default is {SANGLE_DEFAULT}."
HELP_SIZE = f"Size of \"melting\" or \"blocky\" segmentation. Value should be between 0 and 1. Default is {SIZE_DEFAULT}."
HELP_RANDOMNESS = f"Randomness of \"blocky\" or \"chunky\" segmentation. Value should be between 0 and 0.5. Default is {RANDOMNESS_DEFAULT}."
HELP_LENGTH = f"Length of \"chunky\" segmentation. Value should be a natural value. Default is {LENGTH_DEFAULT}."

HELP_SCALE = f"Rescale image before sorting. If width or height are non-zero this value will be ignored. Value should be between 0.01 and 10. Default is {SCALE_DEFAULT}."
HELP_WIDTH = f"Resize to width before sorting. Value should be greater than -1. If value is zero, width is calculated automatically. Default is {WIDTH_DEFAULT}."
HELP_HEIGHT = f"Resize to height before sorting. Value should be greater than -1. If value is zero, height is calculated automatically. Default is {HEIGHT_DEFAULT}."

HELP_AMOUNT = f"Amount of images. Value should be a natural value. Default is {AMOUNT_DEFAULT}."

HELP_SECOND_PASS = "Second pass flag."
HELP_REVERSE = "Reverse sort flag."
HELP_SILENT = "Make app silent in command line."
HELP_NOLOG = "Disable logging."