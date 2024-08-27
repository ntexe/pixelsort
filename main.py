import argparse
import os
import time

from PIL import Image, ImageFilter
import numpy as np

from constants import *
import pixel_utils

class PixelSort:
    def __init__(self):
        self.input_file = None
        self.threshold = THRESHOLD_DEFAULT
        self.interval_type = INTERVAL_DEFAULT

        self.image_data = []

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
        arg_parser.add_argument("-t", default=THRESHOLD_DEFAULT,
                                dest="threshold", help=HELP_THRESHOLD,
                                metavar="threshold", type=float)
        arg_parser.add_argument("-i", choices=INTERVAL_CHOICES,
                                default=INTERVAL_DEFAULT,
                                dest="interval_type", help=HELP_INTERVAL,
                                metavar="interval_type")
        args = arg_parser.parse_args()
        self.input_file = args.input_file
        self.threshold = args.threshold
        self.interval_type = args.interval_type

    def sort_image(self, img):
        if self.interval_type == "edge":
            edge_image = img.filter(ImageFilter.FIND_EDGES).load()

        for y in range(img.size[1]):
            if self.interval_type == "none":
                sorted_row = sorted([self.image_data[x,y] for x in range(img.size[0])], key=pixel_utils.lightness)

            if self.interval_type == "edge":
                interval_begin = 0
                interval_end = 0
                sorted_row = list([self.image_data[i, y] for i in range(img.size[0])])

                for x in range(img.size[0]):
                    if pixel_utils.lightness(edge_image[x, y]) > self.threshold:
                        if x != 0:
                            interval_end = x
                        #print(interval_begin, interval_end, y)
                        if interval_end - interval_begin > 1:
                            sorted_row[interval_begin:interval_end] = sorted(sorted_row[interval_begin:interval_end], key=pixel_utils.lightness)

                        interval_begin = x+1

            for x in range(img.size[0]):
                self.image_data[x,y] = sorted_row[x]

if __name__ == "__main__":
    app = PixelSort()
    app.main()
