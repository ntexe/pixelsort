import argparse
import logging
import math
import os
import time
import random

from PIL import Image, ImageFilter

from constants import *
import pixel_utils
from utils import Option
from options import options

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
        self.img = None
        self.logger = None

        self.options = options

        self.skey = skeys[self.settings["skey_choice"]]

        self.img_size = [0,0]
        self.img_filename = ""
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

        self.img_filename = os.path.basename(os.path.realpath(options.input_path.value))
        self.logger.info(f"Opening image {self.img_filename}...")

        img = Image.open(self.settings["input_path"])

        self.logger.debug("Converting image to RGB...")
        self.img = img.convert("RGB")

        for i in range(1, self.settings["amount"]+1):
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
        self.logger.setLevel("DEBUG")

        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)

        self.file_handler = logging.FileHandler(f"{LOG_FOLDER}/{LOG_FORMAT.format(unix_timestamp=int(time.time()))}", delay=True)
        self.stream_handler = logging.StreamHandler()

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

        arg_parser.add_argument("-ll", choices=LOGLEVEL_CHOICES+AUX_LL_CHOICES,
                                default=DEFAULTS["loglevel"],dest="loglevel",
                                help=HELP_LOGLEVEL, metavar="loglevel")

        arg_parser.add_argument("input_path", help=HELP_INPUT_PATH)
        arg_parser.add_argument("-o", default=DEFAULTS["output_path"],
                                dest="output_path", help=HELP_OUTPUT_PATH,
                                metavar="output_path")
        arg_parser.add_argument("-f", choices=FORMAT_CHOICES,
                                default=DEFAULTS["format"], dest="format",
                                help=HELP_FORMAT, metavar="format")

        arg_parser.add_argument("-sg", choices=SEGMENTATION_CHOICES,
                                default=DEFAULTS["segmentation"],
                                dest="segmentation", help=HELP_SEGMENTATION,
                                metavar="segmentation")
        arg_parser.add_argument("-sk", choices=SKEY_CHOICES, 
                                default=DEFAULTS["skey_choice"],
                                dest="skey_choice", help=HELP_SKEY,
                                metavar="skey_choice")

        arg_parser.add_argument("-t", default=DEFAULTS["threshold_arg"],
                                dest="threshold_arg", help=HELP_THRESHOLD,
                                metavar="threshold_arg")
        arg_parser.add_argument("-a", default=DEFAULTS["angle_arg"],
                                dest="angle_arg", help=HELP_ANGLE,
                                metavar="angle_arg")
        arg_parser.add_argument("-sa", default=DEFAULTS["sangle_arg"],
                                dest="sangle_arg", help=HELP_SANGLE,
                                metavar="sangle_arg")
        arg_parser.add_argument("-sz", default=DEFAULTS["size_arg"],
                                dest="size_arg", help=HELP_SIZE,
                                metavar="size_arg")
        arg_parser.add_argument("-r", default=DEFAULTS["randomness_arg"],
                                dest="randomness_arg", help=HELP_RANDOMNESS,
                                metavar="randomness_arg")
        arg_parser.add_argument("-l", default=DEFAULTS["length_arg"],
                                dest="length_arg", help=HELP_LENGTH,
                                metavar="length_arg")

        arg_parser.add_argument("-sc", default=DEFAULTS["scale_arg"],
                                dest="scale_arg", help=HELP_SCALE,
                                metavar="scale_arg")
        arg_parser.add_argument("-w", default=DEFAULTS["width_arg"],
                                dest="width_arg", help=HELP_WIDTH,
                                metavar="width_arg")
        arg_parser.add_argument("-hg", default=DEFAULTS["height_arg"],
                                dest="height_arg", help=HELP_HEIGHT,
                                metavar="height_arg")

        arg_parser.add_argument("-am", default=DEFAULTS["amount"],
                                dest="amount", help=HELP_AMOUNT,
                                metavar="amount", type=int)

        arg_parser.add_argument("--sp", action="store_true", dest="second_pass",
                                help=HELP_SECOND_PASS)
        arg_parser.add_argument("--rev", action="store_true", dest="reverse",
                                help=HELP_REVERSE)
        arg_parser.add_argument("--silent", action="store_true", dest="silent",
                                help=HELP_SILENT)
        arg_parser.add_argument("--no-log", action="store_true", dest="nolog",
                                help=HELP_NOLOG)

        args = arg_parser.parse_args()

        self.loglevel = args.loglevel

        for arg in args.__dict__.keys():
            self.settings[arg] = args.__dict__[arg]

        self.skey = skeys[self.settings["skey_choice"]]

        self.stream_handler.setLevel(self.settings["loglevel"].upper())
        if self.settings["silent"] or self.settings["nolog"]:
            self.logger.removeHandler(self.stream_handler)
        if self.settings["nolog"]:
            self.logger.removeHandler(self.file_handler)

        if self.settings["segmentation"] != "edge":
            self.settings["threshold_arg"] = DEFAULTS["threshold_arg"]

        if not self.settings["second_pass"]:
            self.settings["sangle_arg"] = DEFAULTS["sangle_arg"]

        if not self.settings["segmentation"] in ("melting", "blocky"):
            self.settings["size_arg"] = DEFAULTS["size_arg"]

        if not self.settings["segmentation"] in ("blocky", "chunky"):
            self.settings["randomness_arg"] = DEFAULTS["randomness_arg"]

        if self.settings["segmentation"] != "chunky":
            self.settings["length_arg"] = DEFAULTS["length_arg"]

        if str(self.settings["width_arg"]) != "0" or str(self.settings["height_arg"]) != "0":
            self.settings["scale_arg"] = DEFAULTS["scale_arg"]

        self.ranges["t_range"] =  self.parse_range(str(self.settings["threshold_arg"]), "threshold_arg",
                                                                   0, 1)
        self.ranges["a_range"] =  tuple(map(int, self.parse_range(str(self.settings["angle_arg"]), "angle_arg",
                                                                   0, 360)))
        self.ranges["sa_range"] = tuple(map(int, self.parse_range(str(self.settings["sangle_arg"]), "sangle_arg",
                                                                   0, 360)))
        self.ranges["sz_range"] = self.parse_range(str(self.settings["size_arg"]), "size_arg",
                                                                   0.01, 1)
        self.ranges["r_range"] =  self.parse_range(str(self.settings["randomness_arg"]), "randomness_arg",
                                                                   0, 1)
        self.ranges["l_range"] = tuple(map(int, self.parse_range(str(self.settings["length_arg"]), "length_arg",
                                                                   1, None)))

        self.ranges["sc_range"] = self.parse_range(str(self.settings["scale_arg"]), "scale_arg",
                                                                   0.01, 10)
        self.ranges["w_range"] =  tuple(map(int, self.parse_range(str(self.settings["width_arg"]), "width_arg",
                                                                   0, None)))
        self.ranges["h_range"] =  tuple(map(int, self.parse_range(str(self.settings["height_arg"]), "height_arg",
                                                                   0, None)))

        self.logger.debug("Arg parsing done.")

        if self.settings["amount"] < 1:
            self.logger.warning(f"Amount value is invalid, will use {DEFAULTS['amount']} instead (default).")
            self.settings["amount"] = DEFAULTS["amount"]

        for i in self.settings.keys():
            self.logger.debug(f"{i} = {self.settings[i]}")

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

        # TODO: cleanup

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

        self.logger.info(f"Preparing image {i}/{self.settings['amount']}...")

        self.logger.debug("Calculating parameters...")

        sort_params = {}
        for r in self.ranges.keys():
            sort_params[RANGE_NAMES[r]] = round(self.get_balance(self.ranges[r], i, self.settings['amount']), 3 if RANGE_TYPES[r] == float else None)

        for p in sort_params.keys():
            self.logger.debug(f"{p} = {sort_params[p]}")

        sp_sort_params = sort_params.copy()
        sp_sort_params["angle"] = sort_params["angle"]+sort_params["sangle"]

        # resize
        new_dims = self.calc_dims(self.img.size, sort_params["scale"], (sort_params["width"],sort_params["height"]))
        self.logger.debug(f"Resizing image to {new_dims[0]}x{new_dims[1]}...")
        rimg = self.img.resize(new_dims)
        self.img_size = new_dims

        # rotate
        self.logger.debug(f"Rotating image by {sort_params['angle']} degrees...")
        rimg = rimg.rotate(sort_params["angle"], expand=True)

        # edge detection
        if self.settings["segmentation"] == "edge":
            self.logger.debug("Creating new image with FIND_EDGES filter for edge detecting...")
            self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())

        self.logger.info("Sorting image...")
        self.image_data = list(rimg.getdata())
        self.sort_image(sort_params, rimg.size)
        rimg.putdata(self.image_data)
        self.logger.debug("First pass sorting done." if self.settings["second_pass"] else "Sorting done.")

        self.logger.debug(f"Rotating image by {-sort_params['angle']} degrees...")
        rimg = rimg.rotate(-sort_params["angle"], expand=True)
        rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.settings["second_pass"]:
            self.logger.info("Second pass preparing...")

            self.logger.debug(f"Rotating image by {sort_params['angle']+sort_params['sangle']} degrees...")
            rimg = rimg.rotate(sort_params["angle"]+sort_params["sangle"], expand=True)

            if self.settings["segmentation"] == "edge":
                self.logger.debug("Creating new image with FIND_EDGES filter for edge detecting...")
                self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())
            
            self.logger.info("Second pass sorting...")
            self.image_data = list(rimg.getdata())
            self.sort_image(sp_sort_params, rimg.size)
            rimg.putdata(self.image_data)
            self.logger.debug("Second pass sorting done.")

            self.logger.debug(f"Rotating image by {-sp_sort_params['angle']} degrees...")
            rimg = rimg.rotate(-sp_sort_params["angle"], expand=True)
            rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        filename = self.generate_filename(self.img_filename, sort_params, i)

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

    def generate_filename(self, fn: str, sp: dict, i: int) -> str:
        """
        Function that generates and returns filename for output image.

        Parameters:
        fn (str):           Input image file name
        sp (dict): Sort parameters
        i (int):            Number of image

        Returns:
        filename (str): Output file name
        """

        if self.settings["output_path"]:
            return self.settings["output_path"]

        filename =  fn.split(".")[0]
        filename += f"_sg_{self.settings['segmentation']}" if self.settings["segmentation"] != DEFAULTS["segmentation"] else ""
        filename += f"_sk_{self.settings['skey_choice']}"  if self.settings["skey_choice"] != DEFAULTS["skey_choice"]   else ""
        filename += f"_t{sp['threshold']:.3f}"  if self.settings["threshold_arg"] != DEFAULTS["threshold_arg"]       else ""
        filename += f"_a{sp['angle']}"          if self.settings["angle_arg"] != DEFAULTS["angle_arg"]               else ""
        filename += f"_sa{sp['sangle']}"        if self.settings["sangle_arg"] != DEFAULTS["sangle_arg"]             else ""
        filename += f"_sz{sp['size']:.3f}"      if self.settings["size_arg"] != DEFAULTS["size_arg"]                 else ""
        filename += f"_r{sp['randomness']:.3f}" if self.settings["randomness_arg"] != DEFAULTS["randomness_arg"]     else ""
        filename += f"_l{sp['length']}"         if self.settings["length_arg"] != DEFAULTS["length_arg"]             else ""
        filename += f"_sc{sp['scale']:.3f}"     if self.settings["scale_arg"] != DEFAULTS["scale_arg"]               else ""
        filename += f"_w{sp['width']}"          if self.settings["width_arg"] != DEFAULTS["width_arg"]               else ""
        filename += f"_hg{sp['height']}"        if self.settings["height_arg"] != DEFAULTS["height_arg"]             else ""
        filename += "_sp"                       if self.settings["second_pass"]                              else ""
        filename += "_rev"                      if self.settings["reverse"]                                  else ""
        filename += f"_{i:04}"
        filename += f".{fn.split('.')[-1] if self.settings['format'] == 'same' else self.settings['format']}"
        return filename

    def sort_image(self, sp: dict, rimg_size: tuple) -> None:
        """
        Function that sorts image.

        Parameters:
        sp (dict):         Sorting parameters
        rimg_size (tuple): Processed image size

        Returns:
        None
        """

        x1, y1 = 0, 0

        sin_alpha = math.sin(math.radians(sp["angle"]%90))
        sin_beta = math.sin(math.radians(90-(sp["angle"]%90)))

        x1 = self.img_size[(sp["angle"]//90)%2]*sin_beta
        y1 = self.img_size[(sp["angle"]//90)%2]*sin_alpha
        x2 = rimg_size[0]-x1
        y2 = rimg_size[1]-y1

        chunky_offset = 0

        for y in range(rimg_size[1]):
            start_x = 0
            end_x = rimg_size[0]

            yoffset = y*rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+rimg_size[0]]

            if sp["angle"] % 90 != 0:
                start_x = round(max(x1-(y/sin_alpha)*sin_beta, x2-((rimg_size[1]-y)/sin_beta)*sin_alpha))
                end_x = round(min(x1+(y/sin_beta)*sin_alpha, x2+((rimg_size[1]-y)/sin_alpha)*sin_beta))

            row = full_row[start_x:end_x]

            if len(row) < 2:
                continue

            if self.settings["segmentation"] == "none":
                row.sort(key=self.skey, reverse=self.settings["reverse"])

            if self.settings["segmentation"] == "edge":
                segment_begin = 0

                t = sp["threshold"]

                edge_row = self.edge_image_data[yoffset+start_x:yoffset+end_x]

                for x in range(len(row)):
                    if pixel_utils.lightness(edge_row[x])/255 > t:
                        if x - segment_begin > 1:
                            row[segment_begin:x] = sorted(
                                        row[segment_begin:x], key=self.skey,
                                        reverse=self.settings["reverse"])

                        segment_begin = x+1

            if self.settings["segmentation"] == "melting":
                width = sp["size"]*self.img_size[0]*(1-(0.5*(random.random()+0.5)))

                x = 0
                while x < len(row):
                    last_x = round(x)
                    x += width*random.random() if x == 0 else width

                    row[last_x:round(x)] = sorted(row[last_x:round(x)], key=self.skey,
                                            reverse=self.settings["reverse"])

            if self.settings["segmentation"] == "blocky":
                block_size = sp["size"]*self.img_size[0]
                offset = round(block_size*sp["randomness"]*(random.random() - 0.5))

                x = (start_x//block_size)*block_size
                first_iter = True

                while x < end_x:
                    last_x = max(round(x)-start_x, 0)

                    x += block_size + offset * first_iter
                    x = max(x, start_x)

                    if max(0, end_x-x) <= -offset+1:
                        x -= offset

                    row[last_x:round(x)-start_x] = sorted(row[last_x:round(x)-start_x], key=self.skey,
                                            reverse=(y//block_size)%2 != self.settings["reverse"])

                    first_iter = False

            if self.settings["segmentation"] == "chunky":
                offset = 0
                l = sp["length"]
                r = sp["randomness"]
                x = -(l-chunky_offset)

                while x < len(row):
                    last_offset = offset
                    offset = round(l*r*(random.random() - 0.5))

                    last_x = max(x, 0)
                    x += l

                    row[last_x+last_offset:x+offset] = sorted(row[last_x+last_offset:x+offset], key=self.skey,
                                            reverse=self.settings["reverse"])

                chunky_offset = (((((len(row) - chunky_offset) // l)+1) * l) + chunky_offset) % len(row)
            
            self.image_data[yoffset+start_x:yoffset+end_x] = row

if __name__ == "__main__":
    app = PixelSort()
    app.main()
