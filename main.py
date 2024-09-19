import argparse
import logging
import math
import os
import time
import random

from PIL import Image, ImageFilter

from constants import *
import pixel_utils
from utils import Option, SortParams
from options import Options, gen_options

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
    """Pixelsort app class."""
    def __init__(self):
        self.img = None
        self.logger = None

        self.options = gen_options()

        self.skey = skeys[self.options.sk.default]

        self.img_size = [0,0]
        self.img_filename = ""
        self.image_data = []
        self.edge_image_data = []

    def main(self) -> None:
        """Do main work."""
        self.setup_logging()
        self.parse_args()

        self.img_filename = os.path.basename(os.path.realpath(self.options.input_path.value))
        self.logger.info(f"Opening image {self.img_filename}...")

        img = Image.open(self.options.input_path.value)

        self.logger.debug("Converting image to RGB...")
        self.img = img.convert("RGB")

        for i in range(1, self.options.am.value+1):
            start_time = time.monotonic()
            self.process_image(i)
            self.logger.info(f"Image {i} done in {time.monotonic()-start_time:.2f} seconds.")

    def setup_logging(self) -> None:
        """Setup logging."""
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
        """Parse command line arguments."""
        arg_parser = argparse.ArgumentParser(description=HELP_DESCRIPTION)

        arg_parser.add_argument("input_path", help=HELP_INPUT_PATH)

        for option in self.options.__dict__.values():
            if option.option_type == 0:
                arg_parser.add_argument(f"--{option.short}", f"--{option.name}",
                                        action="store_true", help=option.help_string,
                                        dest=option.short)

            if option.option_type == 1:
                if option.isvariable:
                    arg_parser.add_argument(f"-{option.short}", f"--{option.name}",
                                            default=option.default, 
                                            choices=option.choices, help=option.help_string,
                                            metavar="", dest=option.short)
                else:
                    arg_parser.add_argument(f"-{option.short}", f"--{option.name}",
                                            default=option.default, 
                                            choices=option.choices, help=option.help_string,
                                            metavar="", dest=option.short, type=option.val_type)


        args = arg_parser.parse_args()

        # apply args to options object
        for option in self.options.__dict__.values():
            setattr(option, "value", args.__dict__[option.short])

        self.skey = skeys[self.options.sk.value]

        # change options of logging
        self.stream_handler.setLevel(self.options.ll.value.upper())
        if self.options.sl.value or self.options.nl.value:
            self.logger.removeHandler(self.stream_handler)
        if self.options.nl.value:
            self.logger.removeHandler(self.file_handler)

        # set values to default if these values will not be used
        if self.options.sg.value != "edge":
            self.options.t.set_to_default()

        if not self.options.sp.value:
            self.options.sa.set_to_default()

        if not self.options.sg.value in ("melting", "blocky"):
            self.options.sz.set_to_default()

        if not self.options.sg.value in ("blocky", "chunky"):
            self.options.r.set_to_default()

        if self.options.sg.value != "chunky":
            self.options.l.set_to_default()

        if str(self.options.w.value) != "0" or str(self.options.hg.value) != "0":
            self.options.sc.set_to_default()

        for option in self.options.__dict__.values():
            # parse keyframes
            if option.isvariable:
                self.parse_keyframes(option)

            # validate
            if option.bounds != None and not option.isvariable:
                if option.bounds[0] != None:
                    if option.value < option.bounds[0]:
                        self.logger.warning(f"{option.name.capitalize()} value is too small, will use default.")
                        option.set_to_default()

                if option.bounds[1] != None:
                    if option.value > option.bounds[1]:
                        self.logger.warning(f"{option.name.capitalize()} value is too big, will use default.")
                        option.set_to_default()

        self.logger.debug("Arg parsing done.")

        for option in self.options.__dict__.values():
            self.logger.debug(f"{option.name} = {option.value}")

    def parse_keyframes(self, option: Option) -> None:
        """
        Parse keyframes from value of Option object. If value is invalid, use default.

        :param option: Option object
        :type option: Option
        """

        if not option.isvariable:
            return

        splitted = str(option.value).split(",")

        if len(splitted) > 2:
            self.logger.warning(f"Too many values in {option.name} argument, will use default.")
            option.set_to_default()
            return (option.value,)*2

        start = option.val_type(splitted[0])
        end = option.val_type(splitted[-1])

        if option.bounds[0] != None:
            if start < option.bounds[0]:
                self.logger.warning(f"{option.name.capitalize()} first value is too small, will use default.")
                start = option.default

            if end < option.bounds[0]:
                self.logger.warning(f"{option.name.capitalize()} second value is too small, will use default.")
                end = option.default

        if option.bounds[1] != None:
            if start > option.bounds[1]:
                self.logger.warning(f"{option.name.capitalize()} first value is too big, will use default.")
                start = option.default

            if end > option.bounds[1]:
                self.logger.warning(f"{option.name.capitalize()} second value is too big, will use default.")
                end = option.default

        option.keyframes = (start, end)

    def get_balance(self, option: Option, i: int, max_i: int) -> float:
        """
        Get keyframes from Option object and return calculated value.

        :param option: Option object
        :type option: Option
        :param i: First value for ratio
        :type i: int
        :param max_i: Second value for ratio
        :type max_i: int

        :returns: Calculated value
        :rtype: float
        """

        ratio = (i-1)/max(1, max_i-1)

        return option.keyframes[0]*(1-ratio) + option.keyframes[1]*ratio

    def calc_dims(self, sort_params: SortParams) -> tuple:
        """
        Calculate and return new dimensions of image.

        :param sort_params: SortParams object
        :type sort_params: SortParams

        :returns: New dimensions of image
        :rtype: tuple
        """

        new_width, new_height = self.img_size

        if sort_params.w != 0 or sort_params.hg != 0: # if width or height nonzero
            if sort_params.w == 0:
                new_width = round((self.img_size[0] / self.img_size[1]) * sort_params.hg)
            else: # width is nonzero
                new_width = sort_params.w

            if sort_params.hg == 0:
                new_height = round((self.img_size[1] / self.img_size[0]) * sort_params.w)
            else: # height is nonzero
                new_height = sort_params.hg

            return (new_width, new_height)

        if sort_params.sc != 1: # if scale is not one
            new_width, new_height = round(self.img_size[0]*sort_params.sc), round(self.img_size[1]*sort_params.sc)

        return (new_width, new_height)

    def process_image(self, i: int) -> None:
        """
        Process image.

        :param i: Number of image
        :type i: int
        """
        sort_params = SortParams()
        sp_sort_params = SortParams()

        self.logger.info(f"Preparing image {i}/{self.options.am.value}...")

        self.logger.debug("Calculating parameters...")

        for option in self.options.__dict__.values():
            if option.isvariable:
                setattr(sort_params, option.short, round(self.get_balance(option, i, self.options.am.value), 3 if option.val_type == float else None))
                # copy sort_params to sp_sort_params
                setattr(sp_sort_params, option.short, getattr(sort_params, option.short))
                # log parameters
                self.logger.debug(f"{option.short} = {sort_params.__dict__[option.short]}")

        sp_sort_params.a = sort_params.a+sort_params.sa

        # resize
        self.img_size = self.img.size
        new_dims = self.calc_dims(sort_params)
        self.logger.debug(f"Resizing image to {new_dims[0]}x{new_dims[1]}...")
        rimg = self.img.resize(new_dims)
        self.img_size = new_dims

        # rotate
        self.logger.debug(f"Rotating image by {sort_params.a} degrees...")
        rimg = rimg.rotate(sort_params.a, expand=True)

        # edge detection
        if self.options.sg.value == "edge":
            self.logger.debug("Creating new image with FIND_EDGES filter for edge detecting...")
            self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())

        self.logger.info("Sorting image...")
        self.image_data = list(rimg.getdata())
        self.sort_image(sort_params, rimg.size)
        rimg.putdata(self.image_data)
        self.logger.debug("First pass sorting done." if self.options.sp.value else "Sorting done.")

        self.logger.debug(f"Rotating image by {-sort_params.a} degrees...")
        rimg = rimg.rotate(-sort_params.a, expand=True)
        rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.options.sp.value:
            self.logger.info("Second pass preparing...")

            self.logger.debug(f"Rotating image by {sp_sort_params.a} degrees...")
            rimg = rimg.rotate(sp_sort_params.a, expand=True)

            if self.options.sg.value == "edge":
                self.logger.debug("Creating new image with FIND_EDGES filter for edge detecting...")
                self.edge_image_data = list(rimg.filter(ImageFilter.FIND_EDGES).getdata())
            
            self.logger.info("Second pass sorting...")
            self.image_data = list(rimg.getdata())
            self.sort_image(sp_sort_params, rimg.size)
            rimg.putdata(self.image_data)
            self.logger.debug("Second pass sorting done.")

            self.logger.debug(f"Rotating image by {-sp_sort_params.a} degrees...")
            rimg = rimg.rotate(-sp_sort_params.a, expand=True)
            rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        filename = self.generate_filename(sort_params, i)

        self.logger.info(f"Saving to {filename}...")

        rimg.save(filename, quality=95)
        self.logger.info("Saved.")

    def get_crop_rectangle(self, rimg_size: tuple) -> tuple:
        """
        Calculate crop rectangle.

        :param rimg_size: Tuple with bigger image width and height
        :type rimg_size: tuple
        :returns: Crop rectangle
        :rtype: tuple
        """

        return ((rimg_size[0]/2)-(self.img_size[0]/2),
                (rimg_size[1]/2)-(self.img_size[1]/2),
                (rimg_size[0]/2)+(self.img_size[0]/2),
                (rimg_size[1]/2)+(self.img_size[1]/2))

    def generate_filename(self, sort_params: SortParams, i: int) -> str:
        """
        Generate and return filename for output image.

        :param sort_params: SortParams object
        :type sort_params: SortParams
        :param i: Image number
        :type i: int
        :returns: Output file name
        :rtype: str
        """

        if self.options.o.value:
            return self.options.o.value

        splitted = self.img_filename.split(".")
        filename = ".".join(splitted[:-1])

        for option in self.options.__dict__.values():
            if option.show and option.value != option.default:
                if option.isvariable:
                    filename += f"_{option.short}_{getattr(sort_params, option.short)}"
                elif option.val_type == bool:
                    filename += f"_{option.short}"
                else:
                    filename += f"_{option.short}_{option.value}"

        filename += f"_{i:04}"
        filename += f".{splitted[-1] if self.options.f.value == 'same' else self.options.f.value}"

        return filename

    def sort_image(self, sort_params: SortParams, rimg_size: tuple) -> None:
        """
        Sort image.

        :param sort_params: SortParams object
        :type sort_params: SortParams
        :param rimg_size: Image size
        :type rimg_size: tuple
        """

        t = sort_params.t
        a = sort_params.a
        sz = sort_params.sz
        r = sort_params.r
        l = sort_params.l

        x1, y1 = 0, 0

        sin_alpha = math.sin(math.radians(a%90))
        sin_beta = math.sin(math.radians(90-(a%90)))

        x1 = self.img_size[(a//90)%2]*sin_beta
        y1 = self.img_size[(a//90)%2]*sin_alpha
        x2 = rimg_size[0]-x1
        y2 = rimg_size[1]-y1

        chunky_offset = 0

        sg = self.options.sg.value
        re = self.options.re.value

        for y in range(rimg_size[1]):
            start_x = 0
            end_x = rimg_size[0]

            yoffset = y*rimg_size[0]

            full_row = self.image_data[yoffset:yoffset+rimg_size[0]]

            if a % 90 != 0:
                start_x = round(max(x1-(y/sin_alpha)*sin_beta, x2-((rimg_size[1]-y)/sin_beta)*sin_alpha))
                end_x = round(min(x1+(y/sin_beta)*sin_alpha, x2+((rimg_size[1]-y)/sin_alpha)*sin_beta))

            row = full_row[start_x:end_x]

            if len(row) < 2:
                continue

            if sg == "none":
                row.sort(key=self.skey, reverse=re)

            if sg == "edge":
                segment_begin = 0

                edge_row = self.edge_image_data[yoffset+start_x:yoffset+end_x]

                for x in range(len(row)):
                    if pixel_utils.lightness(edge_row[x]) > t*255:
                        if x - segment_begin > 1:
                            row[segment_begin:x] = sorted(
                                        row[segment_begin:x], key=self.skey,
                                        reverse=re)

                        segment_begin = x+1

            if sg == "melting":
                width = sz*self.img_size[0]*(1-(0.5*(random.random()+0.5)))

                x = 0
                while x < len(row):
                    last_x = round(x)
                    x += width*random.random() if x == 0 else width

                    row[last_x:round(x)] = sorted(row[last_x:round(x)], key=self.skey,
                                            reverse=re)

            if sg == "blocky":
                block_size = sz*self.img_size[0]
                offset = round(block_size*r*(random.random() - 0.5))

                x = (start_x//block_size)*block_size
                first_iter = True

                while x < end_x:
                    last_x = max(round(x)-start_x, 0)

                    x += block_size + offset * first_iter
                    x = max(x, start_x)

                    if max(0, end_x-x) <= -offset+1:
                        x -= offset

                    row[last_x:round(x)-start_x] = sorted(row[last_x:round(x)-start_x], key=self.skey,
                                            reverse=(y//block_size)%2 != re)

                    first_iter = False

            if sg == "chunky":
                offset = 0
                x = -(l-chunky_offset)

                while x < len(row):
                    last_offset = offset
                    offset = round(l*r*(random.random() - 0.5))

                    last_x = max(x, 0)
                    x += l

                    row[last_x+last_offset:x+offset] = sorted(row[last_x+last_offset:x+offset], key=self.skey,
                                            reverse=re)

                chunky_offset = (((((len(row) - chunky_offset) // l)+1) * l) + chunky_offset) % len(row)
            
            self.image_data[yoffset+start_x:yoffset+end_x] = row

if __name__ == "__main__":
    app = PixelSort()
    app.main()
