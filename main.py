from argparse import ArgumentParser
import logging
import logging.handlers
import os
import time
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

from constants import *
import pixel_utils
from utils import SortParams
from options import Option, Options
from sorting import SortingEngine

class PixelSort:
    """Pixelsort app class."""
    def __init__(self):
        self.logger = None
        self.stream_handler = None
        self.file_handler = None
        
        self.options = Options()
        self.supported_exts = list(Image.registered_extensions().keys())
        self.img_count = 0
        self.sorting_engine = None
        self.img_path = ""
        self.img_size = (0, 0)

        self.mask_image = None

    def main(self) -> None:
        """Do main work."""
        self.setup_logging()
        self.parse_args()

        img_filenames = self.get_image_filenames()

        self.img_count = len(img_filenames)

        self.logger.debug("Initializing SortingEngine object...")
        self.sorting_engine = SortingEngine(self.options)

        if self.options.m.value != "":
            self.logger.info(f"Opening mask image...")
            self.mask_image = ImageOps.invert(
                Image.open(self.options.m.value).convert("L")
            )

        for img_number in range(self.img_count):
            start_time = time.monotonic()

            self.img_path = img_filenames[img_number]
            self.logger.debug(f"Found {self.img_count} images.")
            self.logger.info(f"Opening image {self.img_path.name}...")
            img = Image.open(self.img_path)

            images = []

            # append every frame to images list
            for i in range(1, getattr(img, "n_frames", 1)+1):
                img.seek(i-1)
                self.logger.debug(f"Converting frame {i} to RGB...")
                images.append(img.convert("RGB"))

            sort_params = SortParams()
            # set amount to n_frames, if n_frames > 1
            if getattr(img, "n_frames", 1) > 1:
                self.options.am.value = img.n_frames

            # duplicate references to the same object.
            if len(images) < self.options.am.value:
                images = [images[0] for i in range(self.options.am.value)]

            # sort every frame
            for i in range(self.options.am.value):
                self.logger.info(f"Preparing frame {i+1}/{self.options.am.value}...")

                rimg, sort_params = self.process_image(images[i], i)

                if self.get_out_ext() == ".gif":
                    images[i] = rimg.copy() # we will save it later
                else:
                    self.save_file(sort_params, i+1, [rimg])

            if self.get_out_ext() == ".gif":
                self.save_file(sort_params, 1, images)

            elapsed_time = round(time.monotonic()-start_time, 3)

            self.logger.info(
                f"{self.img_path.name} done in {elapsed_time} seconds.")

    def setup_logging(self) -> None:
        """Setup logging."""
        self.logger = logging.getLogger("pixelsort")
        self.logger.setLevel("DEBUG")

        os.makedirs(LOG_FOLDER, exist_ok=True)

        self.file_handler = logging.handlers.RotatingFileHandler(
                                f"{LOG_FOLDER}/{LOG_FORMAT}",
                                maxBytes=100000, backupCount=3,
                                delay=True
                            )
        self.stream_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.file_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def setup_argparser(self):
        arg_parser = ArgumentParser(description=HELP_DESCRIPTION)
        arg_parser.add_argument("input_path", help=HELP_INPUT_PATH)
        for option in self.options.__dict__.values():
            if option.name == "input_path":
                continue

            if option.option_type == 0:
                arg_parser.add_argument(f"--{option.short}",
                    f"--{option.name.replace('_', '-')}",
                    action="store_true", help=option.help_string,
                    dest=option.short)

            elif option.option_type == 1:
                arg_parser.add_argument(f"-{option.short}",
                    f"--{option.name.replace('_', '-')}",
                    choices=(
                        option.choices if option.name != "ext"
                        else self.supported_exts+["same"]
                    ),
                    type=str if option.isvariable else option.val_type,
                    help=option.help_string, metavar="",
                    dest=option.short, default=option.default)

        return arg_parser

    def parse_args(self) -> None:
        """Parse command line arguments."""
        arg_parser = self.setup_argparser()
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

        if (str(self.options.w.value) != "0"
            or str(self.options.hg.value) != "0"):
            self.options.sc.set_to_default()

        self.process_options()

        self.logger.debug("Arg parsing done.")
        self.log_options_values()

    def process_options(self) -> None:
        """Process options."""
        for option in self.options.__dict__.values():
            # parse keyframes or validate
            if option.isvariable:
                if not option.parse_keyframes():
                    self.warn_invalid(option)
            else:
                if not option.check_value(option.value):
                    option.set_to_default()
                    self.warn_invalid(option)

    def warn_invalid(self, option) -> None:
        """Warn user about invalid value."""
        cap = option.name.capitalize()
        self.logger.warning(f"{cap} value is invalid, will use default.")

    def log_options_values(self) -> None:
        """Log options' values on DEBUG level."""
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
            new_width  = round(self.img_size[0]*sort_params.sc)
            new_height = round(self.img_size[1]*sort_params.sc)

        return (new_width, new_height)

    def process_image(self, img: Image, i: int) -> tuple:
        """
        Process image.

        :param img: Image object.
        :type img: Image
        :param i: Number of image.
        :type i: int

        :returns: Tuple of output image and SortParams object.
        :rtype: tuple
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
        self.img_size = img.size
        new_dims = self.calc_dims(sort_params)
        self.logger.debug(f"Resizing image to {new_dims[0]}x{new_dims[1]}...")
        rimg = img.resize(new_dims)
        self.img_size = new_dims

        # rotate
        self.logger.debug(f"Rotating image by {sort_params.a} degrees...")
        rimg = rimg.rotate(sort_params.a, expand=True)

        # first pass sorting
        self.logger.info("Sorting image...")
        self.sorting_engine.sort_image(sort_params=sort_params,
                                       image=rimg,
                                       og_image_size=self.img_size)
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
            self.sorting_engine.sort_image(sort_params=sp_sort_params,
                                           image=rimg,
                                           og_image_size=self.img_size)
            self.logger.debug("Second pass sorting done.")

            # rotate back
            self.logger.debug(f"Rotating image by {-sp_sort_params.a} degrees...")
            rimg = rimg.rotate(-sp_sort_params.a, expand=True)
            rimg = rimg.crop(self.get_crop_rectangle(rimg.size))

        if self.options.pr.value: # preserve resolution
            self.logger.debug(f"Resizing image back to {img.size}")
            rimg = rimg.resize(img.size)

        if self.options.m.value != "":
            rimg.paste(img.resize(rimg.size), None, self.mask_image.resize(rimg.size))

        return (rimg, sort_params)

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

    def save_file(self, sort_params: SortParams, i: int, imgs: list) -> None:
        """
        Save image (or images) to file.
        If len(imgs) > 1, images will be saved to one multi frame file.

        :param sort_params: SortParams object.
        :type sort_params: SortParams
        :param i: Image number.
        :type i: int
        :param imgs: list with Image objects to save.
        :type imgs: list
        """
        if len(imgs) == 0:
            self.logger.debug("Empty array passed to save_file function arguments.")
            return

        file_path = Path(self.generate_file_path(sort_params, i))
        os.makedirs(file_path.parent, exist_ok=True)

        self.logger.info(f"Saving to {file_path}...")

        if len(imgs) == 1: # save to single frame file
            imgs[0].save(file_path, quality=95)

        else: # save to multi frame file
            imgs[0].save(file_path, quality=95, save_all=True,
                         append_images=imgs[1:], loop=0)

        self.logger.info("Saved.")

    def generate_file_path(self, sort_params: SortParams, i: int=None):
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
            if self.options.am.value == 1 and self.img_count == 1:
                return self.options.o.value
            else: # if amount is greater than one
                folder = output_path.parent
                filename = output_path.stem            

        for option in self.options.__dict__.values():
            if option.name == "amount" and self.get_out_ext() == ".gif":
                option.show = True
            if option.show and option.value != option.default:
                if option.isvariable and self.get_out_ext() != ".gif":
                    filename += f"_{option.short}" + \
                                str(getattr(sort_params, option.short))
                elif option.val_type == bool or option.name == "mask":
                    filename += f"_{option.short}"
                else:
                    filename += f"_{option.short}_{option.value}"

        filename += f"_{i:04}" if i != None else ""
        filename += self.get_out_ext()

        file_path = folder / filename

        return file_path

    def get_out_ext(self):
        """Get output image file extension."""
        return self.img_path.suffix if self.options.e.value == 'same' else self.options.e.value

    def get_image_filenames(self) -> list:
        """
        Return list of image filenames.

        :returns: List of image filenames.
        :rtype: list
        """
        input_path = Path(self.options.input_path.value)

        if input_path.is_dir():
            # return all images with supported extension in dir
            return list([
                        input_path / filename
                        for filename in os.listdir(input_path)
                        if Path(filename).suffix in self.supported_exts
            ])

        if input_path.is_file():
            # return input path
            return [input_path]

        # path does not exist
        self.logger.critical(f"Input path is invalid, exiting...")
        exit(1)

if __name__ == "__main__":
    app = PixelSort()
    app.main()
