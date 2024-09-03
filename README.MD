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
usage: main.py [-h] [-o output] [-sg segmentation] [-sk skey_choice] [-t threshold] [-a angle] [-sz size] [-r randomness] [-am amount] [--sp] input_file

PixelSort is a python tool for sorting pixels in pictures.

positional arguments:
  input_file        Input image file.

options:
  -h, --help        show this help message and exit
  -o output         Output image file.
  -sg segmentation  Segmentation. Available choices: none, edge, melting, blocky. Default is edge.
  -sk skey_choice   Sorting key. Available choices: hue, lightness, saturation, min_value, max_value, red, green, blue. Default is lightness.
  -t threshold      Threshold for edge detection. Value should be between 0 and 1. Default is 0.1.
  -a angle          Angle to rotate the image before sorting in degrees. Value should be between 0 and 360. Default is 0
  -sz size          Size of "melting" or "blocky" segmentation. Value should be between 0 and 1. Default is 0.05
  -r randomness     Randomness of "blocky" segmentation. Value should be between 0 and 0.5. Default is 0.1
  -am amount        Amount of images. Value should be an integer. Default is 1
  --sp              Second pass flag.
```

### Segmentation
#### None
Row segmentation isn't used.
#### Edge
The tool detects edges and determines segments based on this data
#### Melting
Random values are used to determine segments. Use -sz argument to adjust size of the segments.
#### Blocky
This segmentation looks like "melting" segmentation but blocky.

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
You can pass range of values to threshold, angle, size and randomness. If amount is greater than 1, value of parameters will range from first to second value.
Example: `python main.py img.jpg -a 0,45 -am 3` will generate three images with angle parameter 0, 22 and 45.

### Examples
Original

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg" width=50%>

`python main.py img.jpg`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_edge_sk_lightness_t0.10_a0_sz0.050_r0.100_0001.png" width=50%>

`python main.py img.jpg -a 45`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_edge_sk_lightness_t0.10_a45_sz0.050_r0.100_0001.png" width=50%>

`python main.py img.jpg -sg none`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_none_sk_lightness_t0.10_a0_sz0.050_r0.100_0001.png" width=50%>

`python main.py img.jpg -sg melting`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_melting_sk_lightness_t0.10_a0_sz0.050_r0.100_0001.png" width=50%>

`python main.py img.jpg -sg melting -a 45`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_melting_sk_lightness_t0.10_a45_sz0.050_r0.100_0001.png" width=50%>

`python main.py img.jpg -sg blocky`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_blocky_sk_lightness_t0.10_a0_sz0.050_r0.100_0001.png" width=50%>

`python main.py img.jpg -sg blocky -a 45`

<img src="https://raw.githubusercontent.com/ntexe/pixelsort/main/examples/img.jpg_sg_blocky_sk_lightness_t0.10_a45_sz0.050_r0.100_0001.png" width=50%>

<br>

Tested on Windows 10 22H2 Python 3.11.9 (x64)

TODO:

- add multithreading
- add masking
- make filenames shorter
- rotate option for second pass