#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: img2txt.py <imgfile> [--max-len=<max_len>]
"""

import sys

from docopt import docopt
from PIL import Image
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
import numpy as np


def trim_whitespace(img):
    # Do some whitespace trimming.
    pix = np.asarray(img)

    # Drop the alpha channel
    pix = pix[:,:,0:3]

    # Drop the color when finding edges
    idx = np.where(pix - 255)[0:2]
    box = map(min,idx)[::-1] + map(max, idx)[::-1]


    # Crop the image with the new bounding box.
    return img.crop(box)

def resize_to_max_length(img, max_len):
    # resize to: the max of the img is maxLen
    width, height = img.size

    rate = max_len / max(width, height)

    # cast to int
    width = int(rate * width)
    height = int(rate * height)

    # and resize the image.
    resized = img.resize((width, height))
    return resized

def convert_to_ansi_color(img):
    # get pixels
    pixels = img.load()

    string = ""

    for h in xrange(img.size[1]):
        for w in xrange(img.size[0]):
            rgb = pixels[w, h]
            string += rgb256(rgb[0], rgb[1], rgb[2]) + "▇ "+ reset.sequence
        string += "\n"

    return string

def ansify_image(img, max_len):
    max_len = float(max_len)

    cropped_img = trim_whitespace(img)
    resized_img = resize_to_max_length(cropped_img, max_len)
    ansified_colors = convert_to_ansi_color(resized_img)

    return ansified_colors

if __name__ == '__main__':
    dct = docopt(__doc__)

    img_name = dct['<imgfile>']
    max_len = dct['--max-len']

    try:
        max_len = float(max_len)
    except:
        # default max_len: 100px
        max_len = 100.0

    try:
        img = Image.open(img_name)
    except IOError:
        exit("File not found: " + img_name)

    ansified_colors = ansify_image(img, max_len)

    sys.stdout.write(ansified_colors)
    sys.stdout.flush()
