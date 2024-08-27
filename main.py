import argparse
import os
import time

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
        self.interval_type = INTERVAL_DEFAULT
        self.skey_choice = SKEY_DEFAULT
        self.skey = skeys[self.skey_choice]
        self.angle = ANGLE_DEFAULT

        self.image_data = []

    def main(self):
        self.parse_args()

        start_time = time.monotonic()

        with Image.open(self.input_file) as img:
            rimg = img.rotate(self.angle, expand=True)
            self.image_data = rimg.load()
            self.sort_image(rimg)
            rimg = rimg.rotate(-self.angle, expand=True)
            rimg = rimg.crop(((rimg.size[0]/2)-(img.size[0]/2), (rimg.size[1]/2)-(img.size[1]/2), (rimg.size[0]/2)+(img.size[0]/2), (rimg.size[1]/2)+(img.size[1]/2)))

            rimg.save(f"{os.path.basename(os.path.realpath(img.filename))}_t{self.threshold}_i_{self.interval_type}_s_{self.skey_choice}_a{self.angle}.png")

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
        arg_parser.add_argument("-s", choices=SKEY_CHOICES,
                                default=SKEY_DEFAULT, dest="skey_choice",
                                help=HELP_SKEY, metavar="skey_choice")
        arg_parser.add_argument("-a", default=ANGLE_DEFAULT, dest="angle",
                                help=HELP_ANGLE, metavar="angle",
                                type=float)
        args = arg_parser.parse_args()
        self.input_file = args.input_file
        self.threshold = args.threshold
        self.interval_type = args.interval_type
        self.skey_choice = args.skey_choice
        self.skey = skeys[self.skey_choice]
        self.angle = args.angle

    def sort_image(self, img):
        if self.interval_type == "edge":
            edge_image = img.filter(ImageFilter.FIND_EDGES).load()

        for y in range(img.size[1]):
            if self.interval_type == "none":
                sorted_row = sorted([self.image_data[x,y] for x in range(img.size[0])], key=self.skey)

            if self.interval_type == "edge":
                interval_begin = 0
                interval_end = 0
                sorted_row = list([self.image_data[x,y] for x in range(img.size[0])])

                for x in range(img.size[0]):
                    if pixel_utils.lightness(edge_image[x, y]) > self.threshold:
                        interval_end = x

                        if interval_end - interval_begin > 1:
                            sorted_row[interval_begin:interval_end] = sorted(sorted_row[interval_begin:interval_end], key=self.skey)

                        interval_begin = x+1

            for x in range(img.size[0]):
                self.image_data[x,y] = sorted_row[x]

if __name__ == "__main__":
    app = PixelSort()
    app.main()
