LOG_FOLDER = "logs"
LOG_FORMAT = "{unix_timestamp}.log"

LOGLEVEL_CHOICES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
AUX_LL_CHOICES = list(map(str.lower, LOGLEVEL_CHOICES))
SEGMENTATION_CHOICES = ["none", "edge", "melting", "chunky", "blocky"]
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]
FORMAT_CHOICES = ["png", "jpg", "same"]

OPTION_DEFAULTS = {
    "output_folder": "pixelsorted", "loglevel": "INFO", "segmentation": "edge",
    "skey_choice": "lightness", "format": "same", "threshold": 0.1, "angle": 0,
    "sangle": 90, "size": 0.05, "randomness": 0, "length": 10, "scale": 1,
    "width": 0, "height": 0, "amount": 1
}

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in images."

HELP_INPUT_PATH = "Input image file path."
HELP_OUTPUT_PATH = "Output image file path."
HELP_OUTPUT_FOLDER = f"Output folder. If output path specified this value will be ignored. Default is {OPTION_DEFAULTS['output_folder']}"
HELP_FORMAT = f"Output image format. If output path specified this value will be ignored. Available choices: {', '.join(FORMAT_CHOICES)}. Default is {OPTION_DEFAULTS['format']}."

HELP_LOGLEVEL = f"Log level for command line. Available choices: {', '.join(LOGLEVEL_CHOICES)} (lowercase is also accepted). Default is {OPTION_DEFAULTS['loglevel']}"

HELP_SEGMENTATION = f"Segmentation. Available choices: {', '.join(SEGMENTATION_CHOICES)}. Default is {OPTION_DEFAULTS['segmentation']}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {OPTION_DEFAULTS['skey_choice']}."

HELP_THRESHOLD = f"Threshold for edge detection. Value should be between 0 and 1. Default is {OPTION_DEFAULTS['threshold']}."
HELP_ANGLE = f"Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is {OPTION_DEFAULTS['angle']}."
HELP_SANGLE = f"Angle for second pass. Value should be between 0 and 360. Default is {OPTION_DEFAULTS['sangle']}."
HELP_SIZE = f"Size of \"melting\" or \"blocky\" segmentation. Value should be between 0.001 and 1. Default is {OPTION_DEFAULTS['size']}."
HELP_RANDOMNESS = f"Randomness of \"blocky\" or \"chunky\" segmentation. Value should be between 0 and 0.5. Default is {OPTION_DEFAULTS['randomness']}."
HELP_LENGTH = f"Length of \"chunky\" segmentation. Value should be a natural value. Default is {OPTION_DEFAULTS['length']}."

HELP_SCALE = f"Rescale image before sorting. If width or height are non-zero this value will be ignored. Value should be between 0.01 and 10. Default is {OPTION_DEFAULTS['scale']}."
HELP_WIDTH = f"Resize to width before sorting. Value should be greater than or equal to 0. If value is zero, width is calculated automatically. Default is {OPTION_DEFAULTS['width']}."
HELP_HEIGHT = f"Resize to height before sorting. Value should be greater than or equal to 0. If value is zero, height is calculated automatically. Default is {OPTION_DEFAULTS['height']}."

HELP_AMOUNT = f"Amount of images. Value should be a natural value. Default is {OPTION_DEFAULTS['amount']}."

HELP_SECOND_PASS = "Second pass flag."
HELP_REVERSE = "Reverse sort flag."
HELP_SILENT = "Make app silent in command line."
HELP_NOLOG = "Disable logging."
