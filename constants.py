SEGMENTATION_DEFAULT = "edge"
SEGMENTATION_CHOICES = ["none", "edge", "melting", "blocky"]

SKEY_DEFAULT = "lightness"
SKEY_CHOICES = ["hue", "lightness", "saturation", "min_value", "max_value", "red", "green", "blue"]

THRESHOLD_DEFAULT = 0.1
ANGLE_DEFAULT = 0
SIZE_DEFAULT = 0.05
RANDOMNESS_DEFAULT = 0.1
AMOUNT_DEFAULT = 1

OUTPUT_DEFAULT = "{fn}_sg_{sg}_sk_{sk}_t{t:.2f}_a{a}_sz{sz:.3f}_r{r:.3f}_{i:04}.png"

HELP_DESCRIPTION = "PixelSort is a python tool for sorting pixels in pictures."
HELP_INPUT_FILE = "Input image file."
HELP_SEGMENTATION = f"Segmentation. Available choices: {', '.join(SEGMENTATION_CHOICES)}. Default is {SEGMENTATION_DEFAULT}."
HELP_SKEY = f"Sorting key. Available choices: {', '.join(SKEY_CHOICES)}. Default is {SKEY_DEFAULT}."
HELP_THRESHOLD = f"Threshold for edge detection. Value should be between 0 and 1. Default is {THRESHOLD_DEFAULT}."
HELP_ANGLE = f"Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is {ANGLE_DEFAULT}"
HELP_SIZE = f"Size of \"melting\" or \"blocky\" segmentation. Value should be between 0 and 1. Default is {SIZE_DEFAULT}"
HELP_RANDOMNESS = f"Randomness of \"blocky\" segmentation. Value should be between 0 and 0.5. Default is {RANDOMNESS_DEFAULT}"
HELP_AMOUNT = f"Amount of images. Value should be an integer. Default is {AMOUNT_DEFAULT}"
HELP_OUTPUT = f"Output image file."
HELP_SECOND_PASS = f"Second pass flag."