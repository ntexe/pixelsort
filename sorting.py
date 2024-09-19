import random

import pixel_utils

def none_sort(self, row, re):
    row.sort(key=self.skey, reverse=re)

def edge_sort(self, row, yoffset, start_x, end_x, t, re):
    segment_begin = 0

    edge_row = self.edge_image_data[yoffset+start_x:yoffset+end_x]

    for x in range(len(row)):
        if pixel_utils.lightness(edge_row[x]) > t*255:
            if x - segment_begin > 1:
                row[segment_begin:x] = sorted(
                            row[segment_begin:x], key=self.skey,
                            reverse=re)

            segment_begin = x+1

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
