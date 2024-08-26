import argparse
import os
import time

from PIL import Image
import numpy as np

from constants import *
import sorting_keys

class PixelSort:
    def __init__(self):
        self.input_file = None
        self.image_data = np.array([])
        self.sorted_image_data = np.array([])

    def main(self):
        self.parse_args()

        with Image.open(self.input_file) as img:
            self.image_data = np.asarray(img)
            self.sort_image(img)

            img.putdata(self.sorted_image_data.reshape(-1, 3))

            img.save(f"{int(time.time())}_{os.path.basename(os.path.realpath(img.filename))}.png")

    def parse_args(self):
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        args = arg_parser.parse_args()
        self.input_file = args.input_file

    def sort_image(self, img):
        self.sorted_image_data = np.array([
            sorted(self.image_data[y], key=sorting_keys.lightness) for y in range(img.size[1])
        ])

if __name__ == "__main__":
    app = PixelSort()
    app.main()
