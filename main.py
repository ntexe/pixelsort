import argparse
import logging
import math
import os
import time
import random
from pathlib import Path

from PIL import Image, ImageFilter

from constants import *
import pixel_utils
from utils import Option, SortParams
from options import Options, gen_options
from sorting import SortingEngine

class PixelSort:
    """Pixelsort app class."""
    def __init__(self):
        self.img = None
        self.logger = None

        self.options = gen_options()

        self.input_path = ""
        self.supported_exts = list(Image.registered_extensions().keys())
        self.imgs_to_process = []

    def main(self) -> None:
        """Do main work."""
        self.setup_logging()
        self.parse_args()

        self.input_path = Path(self.options.input_path.value)

        if self.input_path.is_dir():
            for filename in os.listdir(self.input_path):
                if Path(filename).suffix in self.supported_exts:
                    self.imgs_to_process.append(self.input_path / filename)

        elif self.input_path.is_file():
            self.imgs_to_process = [self.input_path]

        else:
            self.logger.critical(f"Input path is invalid, exiting...")
            exit(1)

        self.img_count = len(self.imgs_to_process)

        for i in range(1, self.img_count+1):
            self.img_path = self.imgs_to_process[i-1]
            self.logger.info(f"Opening image {i}/{self.img_count} {self.img_path.name}...")
            img = Image.open(self.img_path)

            self.logger.debug("Converting image to RGB...")
            self.img = img.convert("RGB")

            self.logger.debug("Initializing SortingEngine object...")
            self.sorting_engine = SortingEngine(self.options)

            for j in range(1, self.options.am.value+1):
                self.logger.info(f"Preparing image {i}.{j}/{i}.{self.options.am.value}...")
                start_time = time.monotonic()
                self.process_image(j)
                self.logger.info(f"Image {i}.{j}/{i}.{self.options.am.value} done in {time.monotonic()-start_time:.2f} seconds.")

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
            if option.name == "input_path":
                continue

            if option.name == "ext":
                arg_parser.add_argument(f"-{option.short}", f"--{option.name.replace('_', '-')}",
                                        default=option.default, 
                                        choices=self.supported_exts+["same"],
                                        help=option.help_string,
                                        metavar="", dest=option.short, type=option.val_type)
            elif option.option_type == 0:
                arg_parser.add_argument(f"--{option.short}", f"--{option.name.replace('_', '-')}",
                                        action="store_true", help=option.help_string,
                                        dest=option.short)

            elif option.option_type == 1:
                if option.isvariable:
                    arg_parser.add_argument(f"-{option.short}", f"--{option.name.replace('_', '-')}",
                                            default=option.default, 
                                            choices=option.choices, help=option.help_string,
                                            metavar="", dest=option.short)
                else:
                    arg_parser.add_argument(f"-{option.short}", f"--{option.name.replace('_', '-')}",
                                            default=option.default, 
                                            choices=option.choices, help=option.help_string,
                                            metavar="", dest=option.short, type=option.val_type)


        args = arg_parser.parse_args()

        # apply args to options object
        for option in self.options.__dict__.values():
            setattr(option, "value", args.__dict__[option.short])

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
                if option.parse_keyframes() == 1:
                    self.logger.warning(f"{option.name.capitalize()} value is invalid, will use default.")

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

        self.logger.debug("Calculating parameters...")

        for option in self.options.__dict__.values():
            if option.isvariable:
                setattr(sort_params, option.short, option.get_balance((i, self.options.am.value)))
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

        # first pass sorting
        self.logger.info("Sorting image...")

        self.sorting_engine.set_sort_params(sort_params)
        self.sorting_engine.set_image(rimg)
        self.sorting_engine.set_og_image_size(self.img_size)
        self.sorting_engine.sort_image()

        self.logger.debug("First pass sorting done." if self.options.sp.value else "Sorting done.")

        # rotate back
        self.logger.debug(f"Rotating image by {-sort_params.a} degrees...")
        rimg = rimg.rotate(-sort_params.a, expand=True)
        rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.options.sp.value:
            self.logger.info("Second pass preparing...")

            # rotate
            self.logger.debug(f"Rotating image by {sp_sort_params.a} degrees...")
            rimg = rimg.rotate(sp_sort_params.a, expand=True)
            
            # second pass sorting
            self.logger.info("Second pass sorting...")

            self.sorting_engine.set_sort_params(sp_sort_params)
            self.sorting_engine.set_image(rimg)
            self.sorting_engine.set_og_image_size(self.img_size)
            self.sorting_engine.sort_image()

            self.logger.debug("Second pass sorting done.")

            # rotate back
            self.logger.debug(f"Rotating image by {-sp_sort_params.a} degrees...")
            rimg = rimg.rotate(-sp_sort_params.a, expand=True)
            rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.options.pr.value:
            self.logger.debug(f"Resizing image back to {self.img.size}")
            rimg = rimg.resize(self.img.size)

        file_path = Path(self.generate_file_path(sort_params, i))

        self.logger.info(f"Saving to {file_path}...")

        if not os.path.exists(file_path.parent):
            os.makedirs(file_path.parent)

        rimg.save(file_path, quality=95)
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

    def generate_file_path(self, sort_params: SortParams, i: int):
        """
        Generate and return file path for output image.

        :param sort_params: SortParams object
        :type sort_params: SortParams
        :param i: Image number
        :type i: int

        :returns: Output file path
        """

        folder = self.img_path.parent
        filename = self.img_path.stem

        output_path = Path(self.options.o.value)

        if output_path.suffix == "": # output argument is folder
            folder = output_path
        else:                        # output argument is file
            if self.options.am.value == 1:
                return self.options.o.value
            else: # if amount is greater than one
                folder = output_path.parent
                filename = output_path.stem            

        for option in self.options.__dict__.values():
            if option.show and option.value != option.default:
                if option.isvariable:
                    filename += f"_{option.short}_{getattr(sort_params, option.short)}"
                elif option.val_type == bool:
                    filename += f"_{option.short}"
                else:
                    filename += f"_{option.short}_{option.value}"

        filename += f"_{i:04}"
        filename += self.img_path.suffix if self.options.e.value == 'same' else self.options.e.value

        file_path = folder / filename

        return file_path

if __name__ == "__main__":
    app = PixelSort()
    app.main()
