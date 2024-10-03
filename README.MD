PixelSort is a Python tool for sorting pixels in images.

## Requirements
Python 3.9+, Pillow.

## Instalation
```bash
git clone https://github.com/ntexe/pixelsort
pip install Pillow
```

## Usage
```
usage: main.py [-h] [-o] [-e] [-m] [-ll] [-sg] [-sk] [-t] [-a] [-sa] [-sz] [-r] [-l] [-sc] [-w]
               [-hg] [-am] [--sp] [--re] [--pr] [--sm] [--de] [--sl] [--nl]
               input_path

PixelSort is a python tool for sorting pixels in images.

positional arguments:
  input_path            Input file path or folder.

options:
  -h, --help            show this help message and exit
  -o , --output         Output file path or folder. Default is pixelsorted.
  -e , --ext            Output image extension. If output path specified this value will be
                        ignored. Default is same.
  -m , --mask           Mask file path.
  -ll , --loglevel      Log level for command line. Available choices: DEBUG, INFO, WARNING,
                        ERROR, CRITICAL (lowercase is also accepted). Default is INFO
  -sg , --segmentation
                        Segmentation. Available choices: none, row, edge, melting, chunky,
                        blocky. Default is edge.
  -sk , --skey-choice   Sorting key. Available choices: hue, lightness, saturation, min_value,
                        max_value, red, green, blue. Default is lightness.
  -t , --threshold      Threshold for edge detection. Value should be between 0 and 1. Default
                        is 0.1.
  -a , --angle          Angle to rotate the image before sorting in degrees. Value should be
                        between 0 and 360. Default is 0.
  -sa , --sangle        Angle for second pass. Value should be between 0 and 360. Default is
                        90.
  -sz , --size          Size of "melting" or "blocky" segmentation. Value should be between
                        0.001 and 1. Default is 0.05.
  -r , --randomness     Randomness of "blocky" or "chunky" segmentation. Value should be
                        between 0 and 0.5. Default is 0.
  -l , --length         Length of "chunky" segmentation. Value should be greater than or equal
                        to 1. Default is 10.
  -sc , --scale         Rescale image before sorting. If width or height are non-zero this
                        value will be ignored. Value should be between 0.01 and 10. Default is
                        1.
  -w , --width          Resize to width before sorting. Value should be greater than or equal
                        to 0. If value is zero, width is calculated automatically. Default is
                        0.
  -hg , --height        Resize to height before sorting. Value should be greater than or equal
                        to 0. If value is zero, height is calculated automatically. Default is
                        0.
  -am , --amount        Amount of images. Value should be a natural value. If input is animated
                        this value will be ignored. Default is 1.
  --sp, --second-pass   Do second pass.
  --re, --reverse       Reverse sort.
  --pr, --preserve-res  Preserve resolution.
  --sm, --symmetry      Make sort symmetrical.
  --de, --decompose     Decompose image to R, G and B channels and sort each separately.
  --sl, --silent        Make app silent in command line.
  --nl, --nolog         Disable logging.
```

<br>

### Segmentation
#### None
Segmentation isn't used.
#### Row
Segmentation is based on rows.
#### Edge
Segmentation is based on detected edges. Use -t parameter to adjust threshold.
#### Melting
Segmentation is based on random values. Use -sz argument to adjust size of the segments.
#### Blocky
Segmentation is based on size argument and output image looks blocky. Use -sz and -r arguments to adjust size of blocks and randomness of segments' sizes.
#### Chunky
Segmentation is based on length argument and output image looks glitchy. Use -l and -r arguments to adjust length and randomness of segments' sizes.

<br>

### Sorting keys
#### Hue, saturation and lightness
Color is converted to HSL and pixels are sorted by hue, saturation or lightness.
#### min_value and max_value
Pixels are sorted by minimum or maximum value of pixel.
#### Red, green and blue
Pixels are sorted by red, green or blue color.

<br>

### Sort every image in folder
You can pass folder to arguments to make this script sort every image in folder.

### Second pass flag
You can set the "--sp" flag to "second pass" the image. After the first pass image is rotated by angle specified in "-sa" argument (90 by default), the tool does second pass and rotates image back to normal.

### Animation
This tool has GIF support, so you can pass .gif file to command line arguments and the tool will sort every frame of input image and save output to animated .gif file. Note that amount is ignored, if input file has multiple frames.
You can pass two comma-separated values to threshold, angle, second pass angle, size, randomness, length, scale, width and height. If amount is greater than 1, value of parameters will range from first to second value.

Example: `python main.py img.jpg -a 0,45 -am 3` will generate three images with angle parameter 0, 22 and 45.

Example: `python main.py gif.gif -a 0,360` will generate one gif file with variable angle.

### Preserve resolution
You can set the "--pr" flag to preserve original resolution of image, regardless of scale, width and height.

### Mask
You can pass mask image path to -m (--mask) argument. Mask image is automatically converted to grayscale and resized to required size.

### Symmetry flag
You can set the --sm flag to make sort symmetrical.

### Decompose flag
You can set the --de flag to decompose image to R, G, B channels and sort each separately.

<br>

### Examples
Original

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg" width=50%>

`python main.py img.jpg`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_0001.jpg" width=50%>

`python main.py img.jpg -a 45`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_a45_0001.jpg" width=50%>

`python main.py img.jpg -sg none`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_none_0001.jpg" width=50%>

`python main.py img.jpg -sg none -a 45`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_none_a45_0001.jpg" width=50%>

`python main.py img.jpg -sg row`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_row_0001.jpg" width=50%>

`python main.py img.jpg -sg melting`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_melting_0001.jpg" width=50%>

`python main.py img.jpg -sg melting -a 45`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_melting_a45_0001.jpg" width=50%>

`python main.py img.jpg -sg chunky -l 93`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_chunky_l93_0001.jpg" width=50%>

`python main.py img.jpg -sg chunky -l 93 --sp`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_chunky_l93_sp_0001.jpg" width=50%>

`python main.py img.jpg -sg chunky -l 31 --sp`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_chunky_l31_sp_0001.jpg" width=50%>

`python main.py img.jpg -sg blocky -r 0.1`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_blocky_r0.100_0001.jpg" width=50%>

`python main.py img.jpg -sg row --sm`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_row_sm_0001.jpg" width=50%>

`python main.py img.jpg -sg melting --pr -sc 4`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_melting_sc_4.0_pr_0001.jpg" width=50%>

This image is smoother than the one generated by `python main.py img.jpg -sg melting`.

`python main.py img.jpg -sg melting -sz 0.1 --de`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_melting_sz0.1_de_0001.jpg" width=50%>

<br>

Original

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/matrix.gif" width=50%>

`python main.py matrix.gif -sg melting`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/matrix_sg_melting_am_30_0001.gif" width=50%>

<br>

Tested on:
- Windows 10 22H2 Python 3.11.9 (x64)
- Android 12 Termux Python 3.11.9 (arm64)
