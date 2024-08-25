import argparse
import os
import time

from PIL import Image

from constants import *

class PixelSort:
    def __init__(self):
        self.input_file = None
        self.image_data = None
        self.sorted_image_data = []

    def main(self):
        self.parse_args()

        with Image.open(self.input_file) as img:
            self.image_data = img.load()
            self.sort_image(img)

            img.putdata(self.sorted_image_data)

            img.save(f"{time.time()}_{os.path.basename(os.path.realpath(img.filename))}.png")

    def parse_args(self):
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        args = arg_parser.parse_args()
        self.input_file = args.input_file

    def sort_image(self, img):
        for y in range(img.size[1]):
            self.sorted_image_data.extend(sorted([self.image_data[i, y] for i in range(img.size[0])],
                                                 key=lambda pixel: sum(pixel))) # intensivity of the pixel

if __name__ == "__main__":
    app = PixelSort()
    app.main()
