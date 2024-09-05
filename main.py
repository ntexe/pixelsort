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

        self.segmentation = SEGMENTATION_DEFAULT
        self.skey_choice = SKEY_DEFAULT
        self.skey = skeys[self.skey_choice]

        self.t_start, self.t_end, self.threshold = [THRESHOLD_DEFAULT]*3
        self.a_start, self.a_end, self.angle = [ANGLE_DEFAULT]*3
        self.sz_start, self.sz_end, self.size = [SIZE_DEFAULT]*3
        self.r_start, self.r_end, self.randomness = [RANDOMNESS_DEFAULT]*3

        self.amount = AMOUNT_DEFAULT

        self.img_size = [0,0]
        self.img_filename = ""
        self.img = None
        self.image_data = []
        self.edge_image_data = []

    def main(self):
        self.parse_args()

        print("opening picture...")

        img = Image.open(self.input_file)

        self.img_filename = os.path.basename(os.path.realpath(img.filename))
        self.img_size = img.size

        self.img = img.convert("RGB")

        start_time = time.monotonic()

        for i in range(1, self.amount+1):
            self.process_image(i)

        print(f"finished in {time.monotonic()-start_time:.2f} seconds.")

    def parse_args(self):
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        arg_parser.add_argument("-o", default=None, dest="output",
                                help=HELP_OUTPUT, metavar="output")
        arg_parser.add_argument("-sg", choices=SEGMENTATION_CHOICES,
                                default=SEGMENTATION_DEFAULT,
                                dest="segmentation", help=HELP_SEGMENTATION,
                                metavar="segmentation")
        arg_parser.add_argument("-sk", choices=SKEY_CHOICES,
                                default=SKEY_DEFAULT, dest="skey_choice",
                                help=HELP_SKEY, metavar="skey_choice")
        arg_parser.add_argument("-t", default=THRESHOLD_DEFAULT,
                                dest="threshold", help=HELP_THRESHOLD,
                                metavar="threshold", type=float)
        arg_parser.add_argument("-a", default=ANGLE_DEFAULT, dest="angle",
                                help=HELP_ANGLE, metavar="angle", type=int)
        arg_parser.add_argument("-sz", default=SIZE_DEFAULT, dest="size",
                                help=HELP_SIZE, metavar="size", type=float)
        arg_parser.add_argument("-r", default=RANDOMNESS_DEFAULT,
                                dest="randomness", help=HELP_RANDOMNESS,
                                metavar="randomness", type=float)
        arg_parser.add_argument("-am", default=AMOUNT_DEFAULT, dest="amount",
                                help=HELP_AMOUNT, metavar="amount", type=int)
        arg_parser.add_argument("--sp", action="store_true",
                                dest="second_pass", help=HELP_SECOND_PASS)
        arg_parser.add_argument("--rev", action="store_true", dest="reverse",
                                help=HELP_REVERSE)

        args = arg_parser.parse_args()
        self.input_file = args.input_file
        self.segmentation = args.segmentation
        self.skey_choice = args.skey_choice
        self.skey = skeys[self.skey_choice]
        self.threshold = args.threshold
        self.angle = args.angle
        self.size = args.size
        self.randomness = args.randomness
        self.amount = args.amount
        self.output = args.output
        self.second_pass = args.second_pass
        self.reverse = args.reverse

        if self.segmentation != "edge":
            self.threshold = THRESHOLD_DEFAULT

        if not self.segmentation in ("melting", "blocky"):
            self.size = SIZE_DEFAULT

        if self.segmentation != "blocky":
            self.randomness = RANDOMNESS_DEFAULT

        self.t_start, self.t_end = self.parse_range(str(self.threshold), 
                                                    "threshold", 0, 1, float)
        self.a_start, self.a_end = self.parse_range(str(self.angle),
                                                    "angle", 0, 360, int)
        self.sz_start,self.sz_end= self.parse_range(str(self.size),
                                                    "size", 0, 1, float)
        self.r_start, self.r_end = self.parse_range(str(self.randomness),
                                                    "randomness", 0, 1, float)

        if self.amount < 1:
            raise RuntimeError("Amount value is invalid")

    def parse_range(self, arg, arg_name, minv, maxv, vtype):
        if len(arg.split(",")) > 2:
            raise RuntimeError(f"Too many values in {arg_name} argument.")

        start = vtype(arg.split(",")[0])
        end = vtype(arg.split(",")[-1])

        if (not minv <= start <= maxv) or (not minv <= end <= maxv):
            raise RuntimeError(f"{arg_name.capitalize()} value is invalid.")

        return start, end

    def get_balance(self, minv, maxv, i, max_i):
        return (minv*(max(1, max_i-1)-(i-1)) + maxv*(i-1))/max(1, max_i-1)

    def process_image(self, i):
        threshold = self.get_balance(self.t_start, self.t_end, i, self.amount)
        angle = int(self.get_balance(self.a_start, self.a_end, i, self.amount))
        size = self.get_balance(self.sz_start, self.sz_end, i, self.amount)
        randomness = self.get_balance(self.r_start, self.r_end, i, self.amount)

        print(f"image {i}/{self.amount}")
        rimg = self.img.rotate(angle, expand=True)

        if self.segmentation == "edge":
            self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())

        print("sorting...")
        self.image_data = list(rimg.getdata())
        self.sort_image(self.segmentation, self.skey, threshold, angle, size,
                        randomness, rimg.size)
        rimg.putdata(self.image_data)

        if self.second_pass:
            rimg = rimg.rotate(90, expand=True)

            self.image_data = list(rimg.getdata())
            self.sort_image(self.segmentation, self.skey, threshold, angle+90,
                            size, randomness, rimg.size)
            rimg.putdata(self.image_data)

        rimg = rimg.rotate(-angle-(self.second_pass*90), expand=True)
        rimg = rimg.crop(((rimg.size[0]/2)-(self.img_size[0]/2),
                          (rimg.size[1]/2)-(self.img_size[1]/2),
                          (rimg.size[0]/2)+(self.img_size[0]/2),
                          (rimg.size[1]/2)+(self.img_size[1]/2)))

        print("saving...")
        rimg.save(self.generate_filename(self.img_filename, self.segmentation,
            self.skey_choice, threshold, angle, size, randomness, i), quality=95)

    def generate_filename(self, fn, sg, sk, t, a, sz, r, i):
        if self.output:
            return self.output

        filename =  fn.split(".")[0]
        filename += f"_sg_{sg}"    if sg != SEGMENTATION_DEFAULT else ""
        filename += f"_sk_{sk}"    if sk != SKEY_DEFAULT         else ""
        filename += f"_t{t:.3f}"   if t != THRESHOLD_DEFAULT     else ""
        filename += f"_a{a}"       if a != ANGLE_DEFAULT         else ""
        filename += f"_sz{sz:.3f}" if sz != SIZE_DEFAULT         else ""
        filename += f"_r{r:.3f}"   if r != RANDOMNESS_DEFAULT    else ""
        filename += "_sp"          if self.second_pass           else ""
        filename += "_rev"         if self.reverse               else ""
        filename += f"_{i:04}"
        filename += ".jpg"
        return filename

    def sort_image(self, segmentation, skey, threshold, angle, size,
                   randomness, rimg_size):
        x1, y1 = 0, 0

        sin_alpha = math.sin(math.radians(angle%90))
        sin_beta = math.sin(math.radians(90-(angle%90)))

        x1 = int(self.img_size[(angle//90)%2]*sin_beta)
        y1 = int(self.img_size[(angle//90)%2]*sin_alpha)
        x2 = rimg_size[0]-x1
        y2 = rimg_size[1]-y1

        for y in range(rimg_size[1]):
            # search for alpha pixels
            start_x = 0
            end_x = rimg_size[0]

            yoffset = y*rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+rimg_size[0]]

            if angle % 90 != 0:
                start_x = max(x1-int((y/sin_alpha)*sin_beta), x2-int(((rimg_size[1]-y)/sin_beta)*sin_alpha))
                end_x = min(x1+int((y/sin_beta)*sin_alpha), x2+int(((rimg_size[1]-y)/sin_alpha)*sin_beta))

            row = full_row[start_x:end_x]

            if segmentation == "none":
                row.sort(key=skey, reverse=self.reverse)

            if segmentation == "edge":
                segment_begin = 0

                edge_row = self.edge_image_data[yoffset+start_x:yoffset+end_x]

                for x in range(len(row)):
                    if pixel_utils.lightness(edge_row[x]) > threshold:
                        if x - segment_begin > 1:
                            row[segment_begin:x] = sorted(
                                        row[segment_begin:x], key=skey,
                                        reverse=self.reverse)

                        segment_begin = x+1

            if segmentation == "melting":
                width = int(size*self.img_size[0]*(1-(0.5*(random.random()+0.5))))
                offset = random.randint(0, int(size*self.img_size[0]))

                row[:offset] = sorted(row[:offset], key=skey)

                for x in range(offset, len(row), width):
                    row[x:x+width] = sorted(row[x:x+width], key=skey,
                                            reverse=self.reverse)

            if segmentation == "blocky":
                block_size = int(size*self.img_size[0])

                segment_size = int(block_size*(1-(randomness*(random.random()+0.5))))

                for x in range(segment_size, rimg_size[0]+block_size, block_size):
                    start = max(x-segment_size, start_x+1)
                    end = min(x, end_x-2)
                    full_row[start:end] = sorted(full_row[start:end],
                                                 key=skey,
                                                 reverse=(y//block_size)%2 != self.reverse)

                    segment_size = int(block_size*(1-(randomness*(random.random()+0.5))))

            if segmentation in ("none", "edge", "melting"):
                self.image_data[yoffset+start_x:yoffset+end_x] = row
            else:
                self.image_data[yoffset:yoffset+rimg_size[0]] = full_row

if __name__ == "__main__":
    app = PixelSort()
    app.main()
