import argparse
import logging
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

loglevels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

class PixelSort:
    def __init__(self):
        self.logger = None

        self.file_loglevel = logging.DEBUG
        self.stream_loglevel = logging.INFO

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

        self.sc_range, self.scale = (SCALE_DEFAULT,)*2, SCALE_DEFAULT
        self.w_range, self.width = (WIDTH_DEFAULT,)*2, WIDTH_DEFAULT
        self.h_range, self.height = (HEIGHT_DEFAULT,)*2, HEIGHT_DEFAULT

        self.amount = AMOUNT_DEFAULT

        self.img_size = [0,0]
        self.img_filename = ""
        self.img = None
        self.image_data = []
        self.edge_image_data = []

    def main(self) -> None:
        """
        Main function in this class.

        Parameters:
        None

        Returns:
        None
        """
        self.setup_logging()
        self.parse_args()

        self.img_filename = os.path.basename(os.path.realpath(self.input_file))
        self.logger.info(f"Opening image {self.img_filename}...")

        img = Image.open(self.input_file)

        self.logger.debug("Converting image to RGB...")
        self.img = img.convert("RGB")

        for i in range(1, self.amount+1):
            start_time = time.monotonic()
            self.process_image(i)
            self.logger.info(f"Image {i} done in {time.monotonic()-start_time:.2f} seconds.")

    def setup_logging(self):
        """
        Function that creates and configures self.logger

        Parameters:
        None

        Return:
        None
        """
        self.logger = logging.getLogger("pixelsort")
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)

        self.file_handler = logging.FileHandler(f"{LOG_FOLDER}/{LOG_FORMAT.format(unix_timestamp=int(time.time()))}", delay=True)
        self.file_handler.setLevel(self.file_loglevel)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(self.stream_loglevel)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def parse_args(self) -> None:
        """
        Function that parses and processes command line arguments.

        Parameters:
        None

        Returns:
        None
        """
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)

        arg_parser.add_argument("-ll", choices=LOGLEVEL_CHOICES,
                                default=LOGLEVEL_DEFAULT,dest="loglevel",
                                help=HELP_LOGLEVEL, metavar="loglevel")

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

        arg_parser.add_argument("-sc", default=SCALE_DEFAULT, dest="scale",
                                help=HELP_SCALE, metavar="scale")
        arg_parser.add_argument("-w", default=WIDTH_DEFAULT, dest="width",
                                help=HELP_WIDTH, metavar="width")
        arg_parser.add_argument("-hg", default=HEIGHT_DEFAULT, dest="height",
                                help=HELP_HEIGHT, metavar="height")

        arg_parser.add_argument("-am", default=AMOUNT_DEFAULT, dest="amount",
                                help=HELP_AMOUNT, metavar="amount", type=int)

        arg_parser.add_argument("--sp", action="store_true",
                                dest="second_pass", help=HELP_SECOND_PASS)
        arg_parser.add_argument("--rev", action="store_true", dest="reverse",
                                help=HELP_REVERSE)
        arg_parser.add_argument("--silent", action="store_true", dest="silent",
                                help=HELP_SILENT)
        arg_parser.add_argument("--no-log", action="store_true", dest="nolog")

        args = arg_parser.parse_args()

        self.loglevel = args.loglevel

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

        self.scale = args.scale
        self.width = args.width
        self.height = args.height

        self.amount = args.amount
        self.second_pass = args.second_pass
        self.reverse = args.reverse

        self.silent = args.silent
        self.nolog = args.nolog

        self.stream_handler.setLevel(self.loglevel)
        if self.silent or self.nolog:
            self.logger.removeHandler(self.stream_handler)
        if self.nolog:
            self.logger.removeHandler(self.file_handler)

        if self.segmentation != "edge":
            self.threshold = THRESHOLD_DEFAULT

        if not self.second_pass:
            self.sangle = SANGLE_DEFAULT

        if not self.segmentation in ("melting", "blocky"):
            self.size = SIZE_DEFAULT

        if not self.segmentation in ("blocky", "chunky"):
            self.randomness = RANDOMNESS_DEFAULT

        if self.segmentation != "chunky":
            self.length = LENGTH_DEFAULT

        if str(self.width) != "0" or str(self.height) != "0":
            self.scale = SCALE_DEFAULT

        self.t_range =  self.parse_range(str(self.threshold), "threshold",
                                                                   0, 1)
        self.a_range =  tuple(map(int, self.parse_range(str(self.angle), "angle",
                                                                   0, 360)))
        self.sa_range = tuple(map(int, self.parse_range(str(self.sangle), "sangle",
                                                                   0, 360)))
        self.sz_range = self.parse_range(str(self.size), "size",   0, 1)
        self.r_range =  self.parse_range(str(self.randomness), "randomness",
                                                                   0, 1)
        self.l_range = tuple(map(int, self.parse_range(str(self.length), "length",
                                                                   1, None)))

        self.sc_range = self.parse_range(str(self.scale), "scale", 0.01, 10)
        self.w_range =  tuple(map(int, self.parse_range(str(self.width), "width",
                                                                   0, None)))
        self.h_range =  tuple(map(int, self.parse_range(str(self.height), "height",
                                                                   0, None)))

        self.logger.debug("Arg parsing done.")

        if self.amount < 1:
            self.logger.warning(f"Amount value is invalid, will use {AMOUNT_DEFAULT} (default).")
            self.amount = AMOUNT_DEFAULT

        # it is temporary, we need store ranges in dictionary

        self.logger.debug(f"self.input_file = {self.input_file}")
        self.logger.debug(f"self.output_file = {self.output_file}")
        self.logger.debug(f"self.format = {self.format}")
        self.logger.debug(f"self.segmentation = {self.segmentation}")
        self.logger.debug(f"self.skey_choice = {self.skey_choice}")

        self.logger.debug(f"self.t_range = {self.t_range}")
        self.logger.debug(f"self.a_range = {self.a_range}")
        self.logger.debug(f"self.sa_range = {self.sa_range}")
        self.logger.debug(f"self.sz_range = {self.sz_range}")
        self.logger.debug(f"self.r_range = {self.r_range}")
        self.logger.debug(f"self.l_range = {self.l_range}")
        self.logger.debug(f"self.sc_range = {self.sc_range}")
        self.logger.debug(f"self.w_range = {self.w_range}")
        self.logger.debug(f"self.h_range = {self.h_range}")

        self.logger.debug(f"self.amount = {self.amount}")
        self.logger.debug(f"self.second_pass = {self.second_pass}")
        self.logger.debug(f"self.reverse = {self.reverse}")
        self.logger.debug(f"self.silent = {self.reverse}")
        self.logger.debug(f"self.nolog = {self.nolog}")

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

        # TODO: instead of runtimeerror just warn and set the value to default

        if len(arg.split(",")) > 2:
            raise RuntimeError(f"Too many values in {arg_name} argument.")

        start = float(arg.split(",")[0])
        end = float(arg.split(",")[-1])

        if minv != None:
            if start < minv or end < minv:
                raise RuntimeError(f"{arg_name.capitalize()} value is too small.") 

        if maxv != None:
            if start > maxv or end > maxv:
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

    def calc_dims(self, dims:tuple, scale: float, arg_dims: tuple) -> tuple:
        """
        Function to calculate dimensions of new image.

        Parameters:
        dims (tuple):     Tuple of original dimensions
        scale (float):    Scale argument
        arg_dims (tuple): Tuple of width and height arguments

        Returns:
        tuple:            Tuple of new dimensions
        """

        new_width, new_height = dims

        if arg_dims[1] != 0 or arg_dims[0] != 0:
            if arg_dims[0] != 0:
                new_width = arg_dims[0]

                if arg_dims[1] == 0:
                    new_height = round((dims[1] / dims[0]) * arg_dims[0])

            if arg_dims[1] != 0:
                new_height = arg_dims[1]

                if arg_dims[0] == 0:
                    new_width = round((dims[0] / dims[1]) * arg_dims[1])

            return (new_width, new_height)

        if scale != 1:
            new_width, new_height = round(dims[0]*scale), round(dims[1]*scale)

        return (new_width, new_height)

    def process_image(self, i: int) -> None:
        """
        Function to process image. 

        Parameters:
        i (int): Number of image

        Returns:
        None
        """

        self.logger.info(f"Preparing image {i}/{self.amount}...")

        self.logger.debug("Calculating parameters...")

        threshold =  round(self.get_balance(self.t_range,  i, self.amount), 3)
        angle =      round(self.get_balance(self.a_range,  i, self.amount)   )
        sangle =     round(self.get_balance(self.sa_range, i, self.amount)   )
        size =       round(self.get_balance(self.sz_range, i, self.amount), 3)
        randomness = round(self.get_balance(self.r_range,  i, self.amount), 3)
        length =     round(self.get_balance(self.l_range,  i, self.amount)   )

        scale =      round(self.get_balance(self.sc_range, i, self.amount), 3)
        width =      round(self.get_balance(self.w_range,  i, self.amount)   )
        height =     round(self.get_balance(self.h_range,  i, self.amount)   )

        self.logger.debug(f"threshold = {threshold}")
        self.logger.debug(f"angle = {angle}")
        self.logger.debug(f"sangle = {sangle}")
        self.logger.debug(f"size = {size}")
        self.logger.debug(f"randomness = {randomness}")
        self.logger.debug(f"length = {length}")
        self.logger.debug(f"scale = {scale}")
        self.logger.debug(f"width = {width}")
        self.logger.debug(f"height = {height}")

        # resize
        new_dims = self.calc_dims(self.img.size, scale, (width,height))
        self.logger.debug(f"Resizing image to {new_dims[0]}x{new_dims[1]}...")
        rimg = self.img.resize(new_dims)
        self.img_size = new_dims

        # rotate
        self.logger.debug(f"Rotating image by {angle} degrees...")
        rimg = rimg.rotate(angle, expand=True)

        # edge detection
        if self.segmentation == "edge":
            self.logger.debug("Creating new image with FIND_EDGES filter for edge detecting...")
            self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())

        self.logger.info("Sorting image...")
        self.image_data = list(rimg.getdata())
        self.sort_image(self.segmentation, self.skey, threshold, angle, size,
                        randomness, length, rimg.size)
        rimg.putdata(self.image_data)
        self.logger.debug("First pass sorting done." if self.second_pass else "Sorting done.")

        self.logger.debug(f"Rotating image by {-angle} degrees...")
        rimg = rimg.rotate(-angle, expand=True)
        rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.second_pass:
            self.logger.info("Second pass preparing...")

            self.logger.debug(f"Rotating image by {angle+sangle} degrees...")
            rimg = rimg.rotate(angle+sangle, expand=True)

            if self.segmentation == "edge":
                self.logger.debug("Creating new image with FIND_EDGES filter for edge detecting...")
                self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())
            
            self.logger.info("Second pass sorting...")
            self.image_data = list(rimg.getdata())
            self.sort_image(self.segmentation, self.skey, threshold,
                            angle+sangle, size, randomness, length, rimg.size)
            rimg.putdata(self.image_data)
            self.logger.debug("Second pass sorting done.")

            self.logger.debug(f"Rotating image by {-(angle+sangle)} degrees...")
            rimg = rimg.rotate(-(angle+sangle), expand=True)
            rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        filename = self.generate_filename(self.img_filename, self.segmentation,
            self.skey_choice, threshold, angle, sangle, size, randomness,
            length, scale, width, height, i)

        self.logger.info(f"Saving to {filename}...")

        rimg.save(filename, quality=95)
        self.logger.info("Saved.")

    def get_crop_rectangle(self, rimg_size: tuple) -> tuple:
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
                          sa: int, sz: float, r: float, l:int, sc:float,
                          w:int, hg:int, i: int) -> str:
        """
        Function that generates and returns filename for output image.

        Parameters:
        fn (str):   Input image file name
        sg (str):   Segmentation
        skc (str):  Sorting key choice
        t (float):  Threshold
        a (int):    Angle
        sa (int):   Second pass angle
        sz (float): Size
        r (float):  Randomness
        l (int):    Length
        i (int):    Number of image

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
        filename += f"_sc{sc:.3f}" if self.scale != SCALE_DEFAULT           else ""
        filename += f"_w{w}"       if self.width != WIDTH_DEFAULT           else ""
        filename += f"_hg{hg}"     if self.height != HEIGHT_DEFAULT         else ""
        filename += "_sp"          if self.second_pass                      else ""
        filename += "_rev"         if self.reverse                          else ""
        filename += f"_{i:04}"
        filename += f".{fn.split('.')[-1] if self.format == 'same' else self.format}"
        return filename

    def sort_image(self, segmentation: str, skey, threshold: float, angle: int,
                   size: float, randomness: float, length: int,
                   rimg_size: tuple) -> None:
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

        x1 = self.img_size[(angle//90)%2]*sin_beta
        y1 = self.img_size[(angle//90)%2]*sin_alpha
        x2 = rimg_size[0]-x1
        y2 = rimg_size[1]-y1

        chunky_offset = 0

        for y in range(rimg_size[1]):
            start_x = 0
            end_x = rimg_size[0]

            yoffset = y*rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+rimg_size[0]]

            if angle % 90 != 0:
                start_x = round(max(x1-(y/sin_alpha)*sin_beta, x2-((rimg_size[1]-y)/sin_beta)*sin_alpha))
                end_x = round(min(x1+(y/sin_beta)*sin_alpha, x2+((rimg_size[1]-y)/sin_alpha)*sin_beta))

            row = full_row[start_x:end_x]

            if len(row) < 2:
                continue

            if segmentation == "none":
                row.sort(key=skey, reverse=self.reverse)

            if segmentation == "edge":
                segment_begin = 0

                edge_row = self.edge_image_data[yoffset+start_x:yoffset+end_x]

                for x in range(len(row)):
                    if pixel_utils.lightness(edge_row[x])/255 > threshold:
                        if x - segment_begin > 1:
                            row[segment_begin:x] = sorted(
                                        row[segment_begin:x], key=skey,
                                        reverse=self.reverse)

                        segment_begin = x+1

            if segmentation == "melting":
                width = size*self.img_size[0]*(1-(0.5*(random.random()+0.5)))

                x = 0
                while x < len(row):
                    last_x = round(x)
                    x += width*random.random() if x == 0 else width

                    row[last_x:round(x)] = sorted(row[last_x:round(x)], key=skey,
                                            reverse=self.reverse)

            if segmentation == "blocky":
                block_size = size*self.img_size[0]
                offset = round(block_size*randomness*(random.random() - 0.5))

                x = (start_x//block_size)*block_size
                first_iter = True

                while x < end_x:
                    last_x = max(round(x)-start_x, 0)

                    x += block_size + offset * first_iter
                    x = max(x, start_x)

                    if max(0, end_x-x) <= -offset+1:
                        x -= offset

                    row[last_x:round(x)-start_x] = sorted(row[last_x:round(x)-start_x], key=skey,
                                            reverse=(y//block_size)%2 != self.reverse)

                    first_iter = False

            if segmentation == "chunky":
                offset = 0
                x = -(length-chunky_offset)

                while x < len(row):
                    last_offset = offset
                    offset = round(length*randomness*(random.random() - 0.5))

                    last_x = max(x, 0)
                    x += length

                    row[last_x+last_offset:x+offset] = sorted(row[last_x+last_offset:x+offset], key=skey,
                                            reverse=self.reverse)

                chunky_offset = (((((len(row) - chunky_offset) // length)+1) * length) + chunky_offset) % len(row)
            
            self.image_data[yoffset+start_x:yoffset+end_x] = row

if __name__ == "__main__":
    app = PixelSort()
    app.main()
