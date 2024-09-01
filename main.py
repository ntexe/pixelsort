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

        self.threshold_start = THRESHOLD_DEFAULT
        self.threshold_end = THRESHOLD_DEFAULT
        self.threshold = THRESHOLD_DEFAULT

        self.segmentation = SEGMENTATION_DEFAULT
        self.skey_choice = SKEY_DEFAULT
        self.skey = skeys[self.skey_choice]

        self.angle_start = ANGLE_DEFAULT
        self.angle_end = ANGLE_DEFAULT
        self.angle = ANGLE_DEFAULT

        self.size_start = SIZE_DEFAULT
        self.size_end = SIZE_DEFAULT
        self.size = SIZE_DEFAULT

        self.randomness_start = RANDOMNESS_DEFAULT
        self.randomness_end = RANDOMNESS_DEFAULT
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

            self.iimg_size = img.size

            start_time = time.monotonic()

            for i in range(1, self.amount+1):
                self.threshold = (self.threshold_start*(max(1, self.amount-1)-(i-1)) + self.threshold_end*(i-1))/max(1, self.amount-1)
                self.angle = int((self.angle_start*(max(1, self.amount-1)-(i-1)) + self.angle_end*(i-1))/max(1, self.amount-1))
                self.size = (self.size_start*(max(1, self.amount-1)-(i-1)) + self.size_end*(i-1))/max(1, self.amount-1)
                self.randomness = (self.randomness_start*(max(1, self.amount-1)-(i-1)) + self.randomness_end*(i-1))/max(1, self.amount-1)

                print(f"image {i}/{self.amount}")
                rimg = mimg.rotate(self.angle, expand=True)

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

                print("saving...")
                rimg.save(self.output.format(
                        fn=os.path.basename(os.path.realpath(img.filename)),
                        t=self.threshold, sg=self.segmentation,
                        sk=self.skey_choice, a=self.angle, sz=self.size,
                        r=self.randomness, i=i), quality=95)

            print(f"finished in {time.monotonic()-start_time:.2f} seconds.")

    def parse_args(self):
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        arg_parser.add_argument("-o", default=OUTPUT_DEFAULT, dest="output",
                                help=HELP_OUTPUT, metavar="output")
        arg_parser.add_argument("-t", default=str(THRESHOLD_DEFAULT),
                                dest="threshold", help=HELP_THRESHOLD,
                                metavar="threshold")
        arg_parser.add_argument("-sg", choices=SEGMENTATION_CHOICES,
                                default=SEGMENTATION_DEFAULT,
                                dest="segmentation", help=HELP_SEGMENTATION,
                                metavar="segmentation")
        arg_parser.add_argument("-sk", choices=SKEY_CHOICES,
                                default=SKEY_DEFAULT, dest="skey_choice",
                                help=HELP_SKEY, metavar="skey_choice")
        arg_parser.add_argument("-a", default=str(ANGLE_DEFAULT), dest="angle",
                                help=HELP_ANGLE, metavar="angle")
        arg_parser.add_argument("-sz", default=str(SIZE_DEFAULT), dest="size",
                                help=HELP_SIZE, metavar="size")
        arg_parser.add_argument("-r", default=str(RANDOMNESS_DEFAULT),
                                dest="randomness", help=HELP_RANDOMNESS,
                                metavar="randomness")
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
        self.output = args.output

        if len(self.threshold.split(",")) > 2:
            raise RuntimeError("Too many values in threshold argument.")
        self.threshold_start = float(self.threshold.split(",")[0])
        self.threshold_end = float(self.threshold.split(",")[-1])
        if (not 0 <= self.threshold_start <= 1) or (not 0 <= self.threshold_end <= 1):
            raise RuntimeError("Threshold value is invalid.")

        if len(self.angle.split(",")) > 2:
            raise RuntimeError("Too many values in angle argument.")
        self.angle_start = int(self.angle.split(",")[0])
        self.angle_end = int(self.angle.split(",")[-1])
        if (not -180 <= self.angle_start <= 180) or (not -180 <= self.angle_end <= 180):
            raise RuntimeError("Angle value is invalid.")

        if len(self.size.split(",")) > 2:
            raise RuntimeError("Too many values in size argument.")
        self.size_start = float(self.size.split(",")[0])
        self.size_end = float(self.size.split(",")[-1])
        if (not 0 <= self.size_start <= 1) or (not 0 <= self.size_end <= 1):
            raise RuntimeError("Size value is invalid.")

        if len(self.randomness.split(",")) > 2:
            raise RuntimeError("Too many values in randomness argument.")
        self.randomness_start = float(self.randomness.split(",")[0])
        self.randomness_end = float(self.randomness.split(",")[-1])
        if (not 0 <= self.randomness_start <= 1) or (not 0 <= self.randomness_end <= 1):
            raise RuntimeError("Randomness value is invalid.")

        if self.amount < 1:
            raise RuntimeError("Amount value is invalid")

    def sort_image(self):
        x1, y1 = 0, 0

        sin_alpha = math.sin(math.radians(self.angle%90))
        sin_beta = math.sin(math.radians(90-(self.angle%90)))

        x1 = int(self.iimg_size[(self.angle//90)%2]*sin_beta)
        y1 = int(self.iimg_size[(self.angle//90)%2]*sin_alpha)
        x2 = self.rimg_size[0]-x1
        y2 = self.rimg_size[1]-y1

        for y in range(self.rimg_size[1]):
            # search for alpha pixels
            start_x = 0
            end_x = self.rimg_size[0]

            yoffset = y*self.rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+self.rimg_size[0]]

            if self.angle % 90 != 0:
                start_x = max(x1-int((y/sin_alpha)*sin_beta), x2-int(((self.rimg_size[1]-y)/sin_beta)*sin_alpha))
                end_x = min(x1+int((y/sin_beta)*sin_alpha), x2+int(((self.rimg_size[1]-y)/sin_alpha)*sin_beta))

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
