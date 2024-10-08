import math
import random

from PIL import Image, ImageFilter

import pixel_utils
from options import Options
from utils import SortParams

class SortingEngine:
    """Sorting engine class."""
    def __init__(self, options: Options):
        self.options = options

        self.image = None
        self.og_image_size = (0, 0)
        self.image_size = (0, 0)
        self.image_data = None
        self.edge_image_data = None

        self.skey = None

    def make_symmetrical(self, array):
        """Make symmetrical if self.sm==True"""
        if self.sm:
            return array[::2] + array[::-2]
        return array

    def calc_bounds(self, y: int) -> tuple:
        """
        Calculate bounds for sorting. It prevents sorting black parts of image when angle is nonzero.

        :param y: Current y
        :type y: int
        :returns: Relative left bound, relative right bound, start index and end index.
        :rtype: tuple
        """
        start = 0
        end = self.image_size[0]

        yoffset = y * self.image_size[0]

        if self.sort_params.a % 90 != 0:
            start = round(max(self.x1-(y/self.sin_alpha)*self.sin_beta, self.x2-((self.image_size[1]-y)/self.sin_beta)*self.sin_alpha))
            end =   round(min(self.x1+(y/self.sin_beta)*self.sin_alpha, self.x2+((self.image_size[1]-y)/self.sin_alpha)*self.sin_beta))

        return (start, end, yoffset+start, yoffset+end)

    def sort_image(self, *, sort_params: SortParams, image: Image, og_image_size: tuple) -> None:
        """
        Sort image.

        :param sort_params: SortParams object
        :type sort_params: SortParams
        :param image: Image object
        :type image: Image
        :param og_image_size: Original image size
        :type og_image_size: tuple
        """

        self.sort_params = sort_params
        self.image = image
        self.og_image_size = og_image_size

        self.image_data = list(self.image.getdata())
        self.image_size = self.image.size

        self.sin_alpha = math.sin(math.radians(self.sort_params.a%90))
        self.sin_beta = math.sin(math.radians(90-(self.sort_params.a%90)))

        self.x1 = self.og_image_size[(self.sort_params.a//90)%2]*self.sin_beta
        self.y1 = self.og_image_size[(self.sort_params.a//90)%2]*self.sin_alpha
        self.x2 = self.image_size[0]-self.x1
        self.y2 = self.image_size[1]-self.y1

        self.chunky_offset = 0

        self.skey = getattr(pixel_utils, self.options.sk.value)
        self.re = self.options.re.value
        self.sm = self.options.sm.value

        if self.options.de.value:
            og_image_data = self.image_data.copy()

            # red
            self.image_data = [(i[0], 0, 0) for i in og_image_data]
            getattr(self, self.options.sg.value+"_sort")()
            self.image_data = [(self.image_data[i][0], og_image_data[i][1], og_image_data[i][2]) for i in range(len(og_image_data))]
            og_image_data = self.image_data.copy()

            # green
            self.image_data = [(0, i[1], 0) for i in og_image_data]
            getattr(self, self.options.sg.value+"_sort")()
            self.image_data = [(og_image_data[i][0], self.image_data[i][1], og_image_data[i][2]) for i in range(len(og_image_data))]
            og_image_data = self.image_data.copy()

            # blue
            self.image_data = [(0, 0, i[2]) for i in og_image_data]
            getattr(self, self.options.sg.value+"_sort")()
            self.image_data = [(og_image_data[i][0], og_image_data[i][1], self.image_data[i][2]) for i in range(len(og_image_data))]
            og_image_data = self.image_data.copy()
        else:
            # execute sort method
            getattr(self, self.options.sg.value+"_sort")()

        self.image.putdata(self.image_data)

        self.image_data = None
        self.edge_image_data = None

    def none_sort(self) -> None:
        """Sort with none segmentation."""
        to_sort = []
        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            to_sort.extend(self.image_data[start:end])

        to_sort.sort(key=self.skey, reverse=self.re)

        index = 0
        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            self.image_data[start:end] = self.make_symmetrical(to_sort[index:index+end-start])
            index += end-start

    def row_sort(self) -> None:
        """Sort with row segmentation."""
        for y in range(self.image_size[1]):
            # rstart, rend - relative x
            # start, end - absolute x
            rstart, rend, start, end = self.calc_bounds(y)

            row = self.image_data[start:end]
            row.sort(key=self.skey, reverse=self.re)

            if self.sm:
                row = self.make_symmetrical(row)

            self.image_data[start:end] = row
            # it works faster than accessing self.image_data directly

    def edge_sort(self) -> None:
        """Sort with edge segmentation."""
        self.edge_image_data = list(self.image.filter(ImageFilter.FIND_EDGES).getdata())

        t = self.sort_params.t
        of = self.sort_params.of

        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            row = self.image_data[start:end]
            edge_row = self.edge_image_data[start:end]

            segment_begin = 0
            for x in range(len(row)):
                if pixel_utils.lightness(edge_row[min(x-of, len(row)-1)]) > t*255 or x==len(row)-1:
                    if x - segment_begin > 1:
                        row[segment_begin:x] = self.make_symmetrical(sorted(row[segment_begin:x], key=self.skey, reverse=self.re))

                    if x != 0:
                        segment_begin = x+1

            self.image_data[start:end] = row

    def melting_sort(self) -> None:
        """Sort with melting segmentation."""
        sz = self.sort_params.sz

        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            row = self.image_data[start:end]
            width = sz*self.og_image_size[0]*(1-(0.5*(random.random()+0.5)))

            x = 0
            while x < len(row):
                last_x = round(x)
                x += width*random.random() if x == 0 else width

                row[last_x:round(x)] = self.make_symmetrical(sorted(row[last_x:round(x)], key=self.skey, reverse=self.re))

            self.image_data[start:end] = row

    def blocky_sort(self) -> None:
        """Sort with blocky segmentation."""
        sz = self.sort_params.sz
        r = self.sort_params.r

        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            row = self.image_data[start:end]

            block_size = sz*self.og_image_size[0]
            offset = round(block_size*r*(random.random() - 0.5))

            x = (rstart//block_size)*block_size
            first_iter = True

            while x < rend:
                last_x = max(round(x)-rstart, 0)

                x += block_size + offset * first_iter
                x = max(x, rstart)

                if max(0, rend-x) <= -offset+1:
                    x -= offset

                row[last_x:round(x)-rstart] = self.make_symmetrical(sorted(row[last_x:round(x)-rstart], key=self.skey,
                    reverse=(y//block_size)%2 != self.re))


                first_iter = False

            self.image_data[start:end] = row

    def chunky_sort(self) -> None:
        """Sort with chunky segmentation."""
        l = self.sort_params.l
        r = self.sort_params.r

        chunky_offset = 0

        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            if rend-rstart < 2:
                continue

            row = self.image_data[start:end]

            offset = 0
            x = -(l-chunky_offset)

            while x < len(row):
                last_offset = offset
                offset = round(l*r*(random.random() - 0.5))

                last_x = round(max(x, 0))
                x += l

                row[last_x+last_offset:round(x+offset)] = self.make_symmetrical(sorted(row[last_x+last_offset:round(x+offset)], key=self.skey,
                    reverse=self.re))

            chunky_offset = (((((len(row) - chunky_offset) // l)+1) * l) + chunky_offset) % len(row)

            self.image_data[start:end] = row
