THRESHOLD_DEFAULT = 0.5
INTERVAL_DEFAULT = "edge"
INTERVAL_CHOICES = ["none", "edge"]

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in pictures."
HELP_INPUT_FILE = "Input file."
HELP_THRESHOLD = f"Threshold for edge detection. Default is {THRESHOLD_DEFAULT}."
HELP_INTERVAL = f"Interval type. Available choices: {', '.join(INTERVAL_CHOICES)}. Default is {INTERVAL_DEFAULT}."
