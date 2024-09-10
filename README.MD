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
usage: main.py [-h] [-o output_file] [-f format] [-sg segmentation] [-sk skey_choice] [-t threshold] [-a angle] [-sa sangle] [-sz size] [-r randomness]
               [-l length] [-am amount] [--sp] [--rev]
               input_file

PixelSort is a python tool for sorting pixels in images.

positional arguments:
  input_file        Input image file.

options:
  -h, --help        show this help message and exit
  -o output_file    Output image file.
  -f format         Output image format. Available choices: png, jpg, same. Default is same
  -sg segmentation  Segmentation. Available choices: none, edge, melting, chunky, blocky. Default is edge.
  -sk skey_choice   Sorting key. Available choices: hue, lightness, saturation, min_value, max_value, red, green, blue. Default is lightness.
  -t threshold      Threshold for edge detection. Value should be between 0 and 1. Default is 0.1.
  -a angle          Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is 0
  -sa sangle        Angle for second pass. Value should be between 0 and 360. Default is 90.
  -sz size          Size of "melting" or "blocky" segmentation. Value should be between 0 and 1. Default is 0.05
  -r randomness     Randomness of "blocky" or "chunky" segmentation. Value should be between 0 and 0.5. Default is 0
  -l length         Length of "chunky" segmentation. Value should be a natural value. Default is 10
  -am amount        Amount of images. Value should be a natural value. Default is 1
  --sp              Second pass flag.
  --rev             Reverse sort flag.
```

### Segmentation
#### None
Row segmentation isn't used.
#### Edge
The tool detects edges and determines segments based on this data. Use -t parameter to adjust threshold.
#### Melting
Random values are used to determine segments. Use -sz argument to adjust size of the segments.
#### Blocky
This segmentation looks like "melting" segmentation but blocky. Use -sz and -r arguments to adjust size of blocks and randomness of segments' sizes.
#### Chunky
Fixed length is used to determine segments. Use -l and -r arguments to adjust length and randomness of segments' sizes.

<br>

### Sorting key
#### Hue, saturation and lightness
Color is converted to HSL and pixels in segments are sorted by hue, saturation or lightness.
#### min_value and max_value
Pixels in segments are sorted by minimum or maximum value of red, green or blue color.
#### Red, green and blue
Pixels in segments are sorted by value of red, green or blue color.

<br>

### Animation
You can pass two comma-separated values to threshold, angle, second pass angle, size, randomness and length. If amount is greater than 1, value of parameters will range from first to second value.
Example: `python main.py img.jpg -a 0,45 -am 3` will generate three images with angle parameter 0, 22 and 45.

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

`python main.py img.jpg -sg blocky -a 45 -r 0.1`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img_sg_blocky_a45_r0.100_0001.jpg" width=50%>

<br>

Tested on:
- Windows 10 22H2 Python 3.11.9 (x64)
- Android 12 Termux Python 3.11.9 (arm64)
