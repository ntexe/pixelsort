import argparse
import math
import os
import time
import random

from PIL import Image, ImageFilter

from constants import *
import pixel_utils

skeys = {
    "hue": pixel_utils.hue,
    "lightness": pixel_utils.lightness,
    "saturation": pixel_utils.saturation,
    "min_value": pixel_utils.min_value,
    "max_value": pixel_utils.max_value,
    "red": pixel_utils.red,
    "green": pixel_utils.green,
    "blue": pixel_utils.blue,
}

class PixelSort:
    def __init__(self):
        self.input_file = None
        self.threshold = THRESHOLD_DEFAULT
        self.segmentation = SEGMENTATION_DEFAULT
        self.skey_choice = SKEY_DEFAULT
        self.skey = skeys[self.skey_choice]
        self.angle = ANGLE_DEFAULT

        self.image_data = []

    def main(self):
        self.parse_args()

        start_time = time.monotonic()

        print("opening picture...")

        with Image.open(self.input_file) as img:
            rimg = img.convert("RGB")
            rimg = rimg.convert("RGBA")

            rimg = rimg.rotate(self.angle, expand=True, fillcolor=(0,0,0,0))
            self.image_data = rimg.load()
            self.img = rimg

            print("sorting...")
            print("progress: ")
            self.sort_image()
            print()

            rimg = rimg.rotate(-self.angle, expand=True)
            rimg = rimg.crop(((rimg.size[0]/2)-(img.size[0]/2), (rimg.size[1]/2)-(img.size[1]/2), (rimg.size[0]/2)+(img.size[0]/2), (rimg.size[1]/2)+(img.size[1]/2)))
            rimg = rimg.convert("RGB")

            print("saving...")

            rimg.save(f"{os.path.basename(os.path.realpath(img.filename))}_t{self.threshold}_sg_{self.segmentation}_sk_{self.skey_choice}_a{self.angle}{f'_sz{self.size}' if self.segmentation=='melting' else ''}.png")

        print(f"finished in {time.monotonic()-start_time} seconds.")

    def parse_args(self):
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        arg_parser.add_argument("-t", default=THRESHOLD_DEFAULT,
                                dest="threshold", help=HELP_THRESHOLD,
                                metavar="threshold", type=float)
        arg_parser.add_argument("-sg", choices=SEGMENTATION_CHOICES,
                                default=SEGMENTATION_DEFAULT,
                                dest="segmentation", help=HELP_SEGMENTATION,
                                metavar="segmentation")
        arg_parser.add_argument("-sk", choices=SKEY_CHOICES,
                                default=SKEY_DEFAULT, dest="skey_choice",
                                help=HELP_SKEY, metavar="skey_choice")
        arg_parser.add_argument("-a", default=ANGLE_DEFAULT, dest="angle",
                                help=HELP_ANGLE, metavar="angle", type=float)
        arg_parser.add_argument("-sz", default=SIZE_DEFAULT, dest="size",
                                help=HELP_SIZE, metavar="size", type=float)
        #arg_parser.add_argument("-r", default=RANDOMNESS_DEFAULT,
        #                        dest="randomness", help=HELP_RANDOMNESS,
        #                        metavar="randomness", type=float)
        args = arg_parser.parse_args()
        self.input_file = args.input_file
        self.threshold = args.threshold
        self.segmentation = args.segmentation
        self.skey_choice = args.skey_choice
        self.skey = skeys[self.skey_choice]
        self.angle = args.angle
        self.size = args.size
        #self.randomness = args.randomness

    def sort_image(self):
        if self.segmentation == "edge":
            edge_image = self.img.filter(ImageFilter.FIND_EDGES).load()

        for y in range(self.img.size[1]):
            # search for alpha pixels
            start_x = 0
            end_x = self.img.size[0]

            non_alpha_found = False

            for x in range(self.img.size[0]):
                if non_alpha_found:
                    if self.image_data[x,y][3] == 0:
                        end_x = x
                        break
                    continue

                if self.image_data[x,y][3] == 255:
                    non_alpha_found = True
                    start_x = x

            print(f"\r{y}/{self.img.size[1]} rows", end="")
            if self.segmentation == "none":
                for x, item in enumerate(sorted([self.image_data[x,y] for x in range(start_x, end_x)], key=self.skey)):
                    self.image_data[start_x+x,y] = item

            if self.segmentation == "edge":
                segment_begin = 0

                for x in range(start_x, end_x):
                    if pixel_utils.lightness(edge_image[x, y]) > self.threshold:
                        if x - segment_begin > 1:
                            for i, item in enumerate(sorted([self.image_data[x,y] for x in range(segment_begin, x)], key=self.skey)):
                                self.image_data[segment_begin+i, y] = item

                        segment_begin = x+1

            if self.segmentation == "melting":
                width = int(self.size*self.img.size[0] * (1-(0.5*(random.random()+0.5))))
                offset = random.randint(0, int(self.size*self.img.size[0]))

                for x, item in enumerate(sorted([self.image_data[x,y] for x in range(start_x+offset)], key=self.skey)):
                    self.image_data[x,y] = item

                for x in range(offset+start_x, end_x, width):
                    for i, item in enumerate(sorted([self.image_data[j,y] for j in range(x, min(x+width, end_x))], key=self.skey)):
                        self.image_data[x+i,y] = item

if __name__ == "__main__":
    app = PixelSort()
    app.main()
