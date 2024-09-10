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

        self.t_range, self.threshold = (THRESHOLD_DEFAULT,)*2, THRESHOLD_DEFAULT
        self.a_range, self.angle = (ANGLE_DEFAULT,)*2, ANGLE_DEFAULT
        self.sa_range, self.sangle = (SANGLE_DEFAULT,)*2, SANGLE_DEFAULT
        self.sz_range, self.size = (SIZE_DEFAULT,)*2, SIZE_DEFAULT
        self.r_range, self.randomness = (RANDOMNESS_DEFAULT,)*2, RANDOMNESS_DEFAULT
        self.l_range, self.length = (LENGTH_DEFAULT,)*2, LENGTH_DEFAULT

        self.amount = AMOUNT_DEFAULT

        self.img_size = [0,0]
        self.img_filename = ""
        self.img = None
        self.image_data = []
        self.edge_image_data = []

    def main(self):
        """
        Main function in this class.

        Parameters:
        None

        Returns:
        None
        """
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
        """
        Function that parses and processes command line arguments.

        Parameters:
        None

        Returns:
        None
        """
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_file", help=HELP_INPUT_FILE)
        arg_parser.add_argument("-o", default=None, dest="output_file",
                                help=HELP_OUTPUT, metavar="output_file")
        arg_parser.add_argument("-f", choices=FORMAT_CHOICES,
                                default=FORMAT_DEFAULT, dest="format",
                                help=HELP_FORMAT, metavar="format")
        arg_parser.add_argument("-sg", choices=SEGMENTATION_CHOICES,
                                default=SEGMENTATION_DEFAULT,
                                dest="segmentation", help=HELP_SEGMENTATION,
                                metavar="segmentation")
        arg_parser.add_argument("-sk", choices=SKEY_CHOICES,
                                default=SKEY_DEFAULT, dest="skey_choice",
                                help=HELP_SKEY, metavar="skey_choice")
        arg_parser.add_argument("-t", default=THRESHOLD_DEFAULT,
                                dest="threshold", help=HELP_THRESHOLD,
                                metavar="threshold")
        arg_parser.add_argument("-a", default=ANGLE_DEFAULT, dest="angle",
                                help=HELP_ANGLE, metavar="angle")
        arg_parser.add_argument("-sa", default=SANGLE_DEFAULT, dest="sangle",
                                help=HELP_SANGLE, metavar="sangle")
        arg_parser.add_argument("-sz", default=SIZE_DEFAULT, dest="size",
                                help=HELP_SIZE, metavar="size")
        arg_parser.add_argument("-r", default=RANDOMNESS_DEFAULT,
                                dest="randomness", help=HELP_RANDOMNESS,
                                metavar="randomness")
        arg_parser.add_argument("-l", default=LENGTH_DEFAULT, dest="length",
                                help=HELP_LENGTH, metavar="length")
        arg_parser.add_argument("-am", default=AMOUNT_DEFAULT, dest="amount",
                                help=HELP_AMOUNT, metavar="amount", type=int)
        arg_parser.add_argument("--sp", action="store_true",
                                dest="second_pass", help=HELP_SECOND_PASS)
        arg_parser.add_argument("--rev", action="store_true", dest="reverse",
                                help=HELP_REVERSE)

        args = arg_parser.parse_args()
        self.input_file = args.input_file
        self.output_file = args.output_file
        self.format = args.format
        self.segmentation = args.segmentation
        self.skey_choice = args.skey_choice
        self.skey = skeys[self.skey_choice]
        self.threshold = args.threshold
        self.angle = args.angle
        self.sangle = args.sangle
        self.size = args.size
        self.randomness = args.randomness
        self.length = args.length
        self.amount = args.amount
        self.second_pass = args.second_pass
        self.reverse = args.reverse

        if self.segmentation != "edge":
            self.threshold = THRESHOLD_DEFAULT

        if not self.second_pass:
            self.sangle = SANGLE_DEFAULT

        if not self.segmentation in ("melting", "blocky"):
            self.size = SIZE_DEFAULT

        if self.segmentation != "blocky":
            self.randomness = RANDOMNESS_DEFAULT

        if self.segmentation != "chunky":
            self.length = LENGTH_DEFAULT

        self.t_range =  self.parse_range(str(self.threshold), "threshold",
                                                                 0, 1)
        self.a_range =  tuple(map(int, self.parse_range(str(self.angle), "angle",
                                                                 0, 360)))
        self.sa_range = tuple(map(int, self.parse_range(str(self.sangle), "sangle",
                                                                 0, 360)))
        self.sz_range = self.parse_range(str(self.size), "size", 0, 1)
        self.r_range =  self.parse_range(str(self.randomness), "randomness",
                                                                 0, 1)
        self.l_range = tuple(map(int, self.parse_range(str(self.length), "length",
                                                                 0, None)))

        if self.amount < 1:
            raise RuntimeError("Amount value is invalid")

    def parse_range(self, arg: str, arg_name: str, minv: float=None, maxv: float=None) -> tuple:
        """
        Function that parses string with two comma-separated values and checks
        if these values match the following expression: minv <= x <= maxv. If
        not, raises RuntimeError.

        Parameters:
        arg (str):      String to parse
        arg_name (str): Name of argument (used for RuntimeError text)
        minv (float):   Minimum of each value
        maxv (float):   Maximum of each value

        Returns:
        tuple:          Tuple with two float values
        """
        if len(arg.split(",")) > 2:
            raise RuntimeError(f"Too many values in {arg_name} argument.")

        start = float(arg.split(",")[0])
        end = float(arg.split(",")[-1])

        if minv != None:
            if (start < minv) or (end < minv):
                raise RuntimeError(f"{arg_name.capitalize()} value is too small.") 

        if maxv != None:
            if (start > maxv) or (end > maxv):
                raise RuntimeError(f"{arg_name.capitalize()} value is too big.")

        return (start, end)

    def get_balance(self, v: tuple, i:int, max_i:int) -> float:
        """
        Function that mixes two values minv and maxv with ratio i:(max_i/2)

        Parameters:
        v (tuple):   Tuple with two float values
        i (int):     Argument used for ratio
        max_i (int): Argument used for ratio. Must be greater than or equal to i

        Returns:
        float:       Mixed value
        """
        return (v[0]*(max(1, max_i-1)-(i-1)) + v[1]*(i-1))/max(1, max_i-1)

    def process_image(self, i: int):
        """
        Function to process image. 

        Parameters:
        i (int): Number of image

        Returns:
        None
        """

        threshold =  round(self.get_balance(self.t_range, i, self.amount), 3)
        angle =      round(self.get_balance(self.a_range, i, self.amount))
        sangle =     round(self.get_balance(self.sa_range, i, self.amount))
        size =       round(self.get_balance(self.sz_range, i, self.amount), 3)
        randomness = round(self.get_balance(self.r_range, i, self.amount), 3)
        length =     round(self.get_balance(self.l_range, i, self.amount))

        print(f"image {i}/{self.amount}")
        rimg = self.img.rotate(angle, expand=True)

        if self.segmentation == "edge":
            self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())

        print("sorting...")
        self.image_data = list(rimg.getdata())
        self.sort_image(self.segmentation, self.skey, threshold, angle, size,
                        randomness, length, rimg.size)
        rimg.putdata(self.image_data)

        rimg = rimg.rotate(-angle, expand=True)
        rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.second_pass:
            rimg = rimg.rotate(angle+sangle, expand=True)

            if self.segmentation == "edge":
                self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())
                
            self.image_data = list(rimg.getdata())
            self.sort_image(self.segmentation, self.skey, threshold,
                            angle+sangle, size, randomness, length, rimg.size)
            rimg.putdata(self.image_data)

            rimg = rimg.rotate(-(angle+sangle), expand=True)
            rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        print("saving...")

        filename = self.generate_filename(self.img_filename, self.segmentation,
            self.skey_choice, threshold, angle, sangle, size, randomness, length, i)

        rimg.save(filename, quality=95)
        print(f"saved as {filename}")

    def get_crop_rectangle(self, rimg_size: tuple):
        """
        Function that calculates returns crop rectangle.

        Parameters:
        rimg_size (tuple): Tuple with bigger image width and height

        Returns:
        tuple: Tuple containing crop rectange values
        """

        return ((rimg_size[0]/2)-(self.img_size[0]/2),
                (rimg_size[1]/2)-(self.img_size[1]/2),
                (rimg_size[0]/2)+(self.img_size[0]/2),
                (rimg_size[1]/2)+(self.img_size[1]/2))

    def generate_filename(self, fn: str, sg: str, skc: str, t: float, a: int,
                          sa: int, sz: float, r: float, l:int, i: int) -> str:
        """
        Function that generates and returns filename for output image.

        Parameters:
        fn (str):       Input image file name
        sg (str):       Segmentation
        skc (str):      Sorting key choice
        t (float):      Threshold
        a (int):        Angle
        sz (float):     Size
        r (float):      Randomness
        sa (int):       Second pass angle
        i (int):        Number of image

        Returns:
        filename (str): Output file name
        """
        if self.output_file:
            return self.output_file

        filename =  fn.split(".")[0]
        filename += f"_sg_{sg}"    if sg != SEGMENTATION_DEFAULT            else ""
        filename += f"_sk_{skc}"   if skc != SKEY_DEFAULT                   else ""
        filename += f"_t{t:.3f}"   if self.threshold != THRESHOLD_DEFAULT   else ""
        filename += f"_a{a}"       if self.angle != ANGLE_DEFAULT           else ""
        filename += f"_sa{sa}"     if self.sangle != SANGLE_DEFAULT         else ""
        filename += f"_sz{sz:.3f}" if self.size != SIZE_DEFAULT             else ""
        filename += f"_r{r:.3f}"   if self.randomness != RANDOMNESS_DEFAULT else ""
        filename += f"_l{l}"       if self.length != LENGTH_DEFAULT         else ""
        filename += "_sp"          if self.second_pass                      else ""
        filename += "_rev"         if self.reverse                          else ""
        filename += f"_{i:04}"
        filename += f".{fn.split('.')[-1] if self.format == 'same' else self.format}"
        return filename

    def sort_image(self, segmentation: str, skey, threshold: float, angle: int,
                   size: float, randomness: float, length: int, rimg_size: tuple):
        """
        Function that sorts image.

        Parameters:
        segmantation (str): Segmentation
        skey:               Sorting key
        threshold (float):  Threshold
        angle (int):        Angle
        size (float):       Size
        randomness (float): Randomness
        length (int):       Length
        rimg_size (tuple):  Processed image size

        Returns:
        None
        """

        x1, y1 = 0, 0

        sin_alpha = math.sin(math.radians(angle%90))
        sin_beta = math.sin(math.radians(90-(angle%90)))

        x1 = round(self.img_size[(angle//90)%2]*sin_beta)
        y1 = round(self.img_size[(angle//90)%2]*sin_alpha)
        x2 = rimg_size[0]-x1
        y2 = rimg_size[1]-y1

        if segmentation == "chunky":
            for x in range(0, rimg_size[0]*rimg_size[1], length):
                self.image_data[x:x+length] = sorted(self.image_data[x:x+length],
                                                     key=skey,
                                                     reverse=self.reverse)
            return

        for y in range(rimg_size[1]):
            # search for alpha pixels
            start_x = 0
            end_x = rimg_size[0]

            yoffset = y*rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+rimg_size[0]]

            if angle % 90 != 0:
                start_x = max(x1-round((y/sin_alpha)*sin_beta), x2-round(((rimg_size[1]-y)/sin_beta)*sin_alpha))
                end_x = min(x1+round((y/sin_beta)*sin_alpha), x2+round(((rimg_size[1]-y)/sin_alpha)*sin_beta))

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
                offset = int(size*self.img_size[0]*random.random())

                row[:offset] = sorted(row[:offset], key=skey)

                for x in range(offset, len(row), width):
                    row[x:x+width] = sorted(row[x:x+width], key=skey,
                                            reverse=self.reverse)

            if segmentation == "blocky":
                block_size = int(size*self.img_size[0])
                offset = 0

                for x in range(0, rimg_size[0], block_size):
                    last_offset = offset
                    offset = int(block_size*randomness*(random.random() - 0.5))

                    start = max(x+last_offset, start_x)
                    end = min(x+block_size+offset, end_x)
                    full_row[start:end] = sorted(full_row[start:end],
                                                 key=skey,
                                                 reverse=(y//block_size)%2 != self.reverse)

            if segmentation in ("none", "edge", "melting"):
                self.image_data[yoffset+start_x:yoffset+end_x] = row
            else:
                self.image_data[yoffset:yoffset+rimg_size[0]] = full_row

if __name__ == "__main__":
    app = PixelSort()
    app.main()
