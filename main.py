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
        self.image_data = []
        #self.og_image_data = []

    def main(self):
        self.parse_args()

        start_time = time.monotonic()

        with Image.open(self.input_file) as img:
            self.image_data = img.load()
            self.sort_image(img)

            img.save(f"{int(time.time())}_{os.path.basename(os.path.realpath(img.filename))}.png")

        print(f"finished in {time.monotonic()-start_time} seconds.")

    def parse_args(self):
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        args = arg_parser.parse_args()
        self.input_file = args.input_file

    def sort_image(self, img):
        for y in range(img.size[1]):
            sortedd = sorted([self.image_data[x,y] for x in range(img.size[0])], key=sorting_keys.lightness)
            for x in range(img.size[0]):
                self.image_data[x,y] = sortedd[x]

if __name__ == "__main__":
    app = PixelSort()
    app.main()
