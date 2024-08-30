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
        self.size = SIZE_DEFAULT
        self.randomness = RANDOMNESS_DEFAULT
        self.amount = AMOUNT_DEFAULT

        self.image_data = []
        self.iimg_size = [0,0]
        self.rimg_size = [0,0]

        self.edge_image = None

    def main(self):
        self.parse_args()

        print("opening picture...")

        with Image.open(self.input_file) as img:
            mimg = img.convert("RGB")
            mimg = mimg.convert("RGBA")

            self.iimg_size = img.size

            start_time = time.monotonic()

            for i in range(1, self.amount+1):
                print(f"image {i}/{self.amount}")
                rimg = mimg.rotate(self.angle, expand=True, fillcolor=(0,)*4)

                self.image_data = list(rimg.getdata())

                if self.segmentation == "edge":
                    self.edge_image = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())

                self.rimg_size = rimg.size

                print("sorting...")
                self.sort_image()

                rimg.putdata(self.image_data)

                rimg = rimg.rotate(-self.angle, expand=True)
                rimg = rimg.crop(((rimg.size[0]/2)-(img.size[0]/2),
                                  (rimg.size[1]/2)-(img.size[1]/2),
                                  (rimg.size[0]/2)+(img.size[0]/2),
                                  (rimg.size[1]/2)+(img.size[1]/2)))
                rimg = rimg.convert("RGB")

                print("saving...")
                rimg.save(FILENAME_TEMPLATE.format(
                        fn=os.path.basename(os.path.realpath(img.filename)),
                        t=self.threshold, sg=self.segmentation,
                        sk=self.skey_choice, a=self.angle, sz=self.size,
                        r=self.randomness, i=i))

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
                                help=HELP_ANGLE, metavar="angle", type=int)
        arg_parser.add_argument("-sz", default=SIZE_DEFAULT, dest="size",
                                help=HELP_SIZE, metavar="size", type=float)
        arg_parser.add_argument("-r", default=RANDOMNESS_DEFAULT,
                                dest="randomness", help=HELP_RANDOMNESS,
                                metavar="randomness", type=float)
        arg_parser.add_argument("-am", default=AMOUNT_DEFAULT, dest="amount",
                                help=HELP_AMOUNT, metavar="amount", type=int)
        args = arg_parser.parse_args()
        self.input_file = args.input_file
        self.threshold = args.threshold
        self.segmentation = args.segmentation
        self.skey_choice = args.skey_choice
        self.skey = skeys[self.skey_choice]
        self.angle = args.angle
        self.size = args.size
        self.randomness = args.randomness
        self.amount = args.amount

    def sort_image(self):
        for y in range(self.rimg_size[1]):
            # search for alpha pixels
            start_x = 0
            end_x = self.rimg_size[0]

            yoffset = y*self.rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+self.rimg_size[0]]

            non_alpha_found = False

            for x in range(self.rimg_size[0]):
                if self.angle % 90 == 0:
                    break

                if non_alpha_found:
                    if full_row[x][3] == 0:
                        end_x = x
                        break
                    continue

                if full_row[x][3] == 255:
                    non_alpha_found = True
                    start_x = x

            row = full_row[start_x:end_x]

            if self.segmentation == "none":
                row.sort(key=self.skey)

            if self.segmentation == "edge":
                segment_begin = 0

                edge_row = self.edge_image[yoffset+start_x:yoffset+end_x]

                for x in range(len(row)):
                    if pixel_utils.lightness(edge_row[x]) > self.threshold:
                        if x - segment_begin > 1:
                            row[segment_begin:x] = sorted(
                                        row[segment_begin:x], key=self.skey)

                        segment_begin = x+1

            if self.segmentation == "melting":
                width = int(self.size*self.iimg_size[0]*(1-(0.5*(random.random()+0.5))))
                offset = random.randint(0, int(self.size*self.iimg_size[0]))

                row[:offset] = sorted(row[:offset], key=self.skey)

                for x in range(offset, len(row), width):
                    row[x:x+width] = sorted(row[x:x+width], key=self.skey)

            if self.segmentation == "blocky":
                block_size = int(self.size*self.iimg_size[0])

                segment_size = int(block_size*(1-(self.randomness*(random.random()+0.5))))

                for x in range(segment_size, self.rimg_size[0]+block_size, block_size):
                    full_row[x-segment_size:x] = sorted(
                                                    full_row[x-segment_size:x],
                                                    key=self.skey,
                                                    reverse=(y//block_size)%2)

                    segment_size = int(block_size*(1-(self.randomness*(random.random()+0.5))))

            if self.segmentation in ("none", "edge", "melting"):
                self.image_data[yoffset+start_x:yoffset+end_x] = row
            else:
                self.image_data[yoffset:yoffset+self.rimg_size[0]] = full_row

if __name__ == "__main__":
    app = PixelSort()
    app.main()
