from functools import cache
import math
import random

from PIL import Image, ImageFilter

import pixel_utils
from options import Options
from utils import SortParams

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

class SortingEngine:
    def __init__(self, sort_params: SortParams, options: Options):
        self.sort_params = sort_params
        self.options = options

        self.image = None
        self.og_image_size = (0, 0)
        self.image_size = (0, 0)
        self.image_data = []
        self.edge_image_data = []

        self.skey = None

    def set_image(self, image: Image):
        self.image = image

    def set_og_image_size(self, og_image_size: tuple):
        self.og_image_size = og_image_size

    @cache
    def calc_bounds(self, y: int) -> tuple:
        start = 0
        end = self.image_size[0]

        yoffset = y * self.image_size[0]

        if self.sort_params.a % 90 != 0:
            start = round(max(self.x1-(y/self.sin_alpha)*self.sin_beta, self.x2-((self.image_size[1]-y)/self.sin_beta)*self.sin_alpha))
            end =   round(min(self.x1+(y/self.sin_beta)*self.sin_alpha, self.x2+((self.image_size[1]-y)/self.sin_alpha)*self.sin_beta))

        return (start, end, yoffset+start, yoffset+end)

    def sort_image(self):
        self.image_data = list(self.image.getdata())
        self.image_size = self.image.size

        self.sin_alpha = math.sin(math.radians(self.sort_params.a%90))
        self.sin_beta = math.sin(math.radians(90-(self.sort_params.a%90)))

        self.x1 = self.og_image_size[(self.sort_params.a//90)%2]*self.sin_beta
        self.y1 = self.og_image_size[(self.sort_params.a//90)%2]*self.sin_alpha
        self.x2 = self.image_size[0]-self.x1
        self.y2 = self.image_size[1]-self.y1

        self.chunky_offset = 0

        self.skey = skeys[self.options.sk.value]
        self.re = self.options.re.value

        if self.options.sg.value == "none":
            self.none_sort()

        if self.options.sg.value == "edge":
            self.edge_sort()

        self.image.putdata(self.image_data)

    def none_sort(self):
        for y in range(self.image_size[1]):
            # rstart, rend - relative x
            # start, end - absolute x
            rstart, rend, start, end = self.calc_bounds(y)

            row = self.image_data[start:end]
            row.sort(key=self.skey, reverse=self.re)
            self.image_data[start:end] = row
            # it works faster than accessing self.image_data directly

    def edge_sort(self):
        self.edge_image_data = list(self.image.filter(ImageFilter.FIND_EDGES).getdata())

        t = self.sort_params.t

        for y in range(self.image_size[1]):
            rstart, rend, start, end = self.calc_bounds(y)

            row = self.image_data[start:end]
            edge_row = self.edge_image_data[start:end]

            segment_begin = 0
            for x in range(len(row)):
                if pixel_utils.lightness(edge_row[x]) > t*255:
                    if x - segment_begin > 1:
                        row[segment_begin:x] = sorted(row[segment_begin:x], key=self.skey, reverse=self.re)

                    if x != 0:
                        segment_begin = x+1

            self.image_data[start:end] = row

    def melting_sort(self, row, sz, re):
        width = sz*self.img_size[0]*(1-(0.5*(random.random()+0.5)))

        x = 0
        while x < len(row):
            last_x = round(x)
            x += width*random.random() if x == 0 else width

            row[last_x:round(x)] = sorted(row[last_x:round(x)], key=self.skey,
                                    reverse=re)

    def blocky_sort(self, row, y, start_x, end_x, sz, r, re):
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

    def chunky_sort(self, row, l, r, re):
        offset = 0
        x = -(l-self.chunky_offset)

        while x < len(row):
            last_offset = offset
            offset = round(l*r*(random.random() - 0.5))

            last_x = max(x, 0)
            x += l

            row[last_x+last_offset:x+offset] = sorted(row[last_x+last_offset:x+offset], key=self.skey,
                                    reverse=re)

        self.chunky_offset = (((((len(row) - self.chunky_offset) // l)+1) * l) + self.chunky_offset) % len(row)
