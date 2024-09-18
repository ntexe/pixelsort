from collections import namedtuple

from constants import *
from utils import Option

Options = namedtuple("Options", fieldnames=[
    "input_path", "o", "ll", "sg", "sk", "f", "t", "a", "sa", "sz", "r", "l",
    "sc", "w", "hg", "am", "sp", "re", "sl", "nl"
])

options = Options()
options.input_path = Option(name="input_path", short="input_path",
                            option_type=1, help=HELP_INPUT_PATH, type=str)

options.o =  Option(name="output_path", short="o", option_type=1,
                    help=HELP_OUTPUT_PATH, type=str)
options.ll = Option(name="loglevel", short="ll", option_type=1, default="INFO", choices=LOGLEVEL_CHOICES+AUX_LL_CHOICES,
                    help=HELP_LOGLEVEL, type=str)
options.sg = Option(name="segmentation", short="sg", option_type=1, default="edge", choices=SEGMENTATION_CHOICES,
                    help=HELP_SEGMENTATION, type=str)
options.sk = Option(name="skey_choice", short="sk", option_type=1, default="lightness", choices=SKEY_CHOICES,
                    help=HELP_SKEY, type=str)
options.f =  Option(name="format", short="f", option_type=1, default="same", choices=FORMAT_CHOICES,
                    help=HELP_FORMAT, type=str)

options.t =  Option(name="threshold", short="t", option_type=1, default=0.1,
                    help=HELP_THRESHOLD, range=(0.1,0.1), bounds=(0,1), type=float)
options.a =  Option(name="angle", short="a", option_type=1, default=0,
                    help=HELP_ANGLE, range=(0,0), bounds=(0,360), type=int)
options.sa = Option(name="sangle", short="sa", option_type=1, default=90,
                    help=HELP_SANGLE, range=(90,90), bounds=(0,360), type=int)
options.sz = Option(name="size", short="sz", option_type=1, default=0.05,
                    help=HELP_SIZE, range=(0.05,0.05), bounds=(0.01,1), type=float)
options.r =  Option(name="randomness", short="r", option_type=1, default=0,
                    help=HELP_RANDOMNESS, range=(0,0), bounds=(0,0.5), type=float)
options.l =  Option(name="length", short="l", option_type=1, default=10,
                    help=HELP_LENGTH, range=(10,10), bounds=(2,None), type=int)

options.sc = Option(name="scale", short="sc", option_type=1, default=1,
                    help=HELP_SCALE, range=(1,1), bounds=(0.01,10), type=float)
options.w =  Option(name="width", short="w", option_type=1, default=0,
                    help=HELP_WIDTH, range=(0,0), bounds=(0,None), type=int)
options.hg = Option(name="height", short="hg", option_type=1, default=0,
                    help=HELP_HEIGHT, range=(0,0), bounds=(0,None), type=int)

options.am = Option(name="amount", short="am", option_type=1, default=1,
                    help=HELP_AMOUNT, bounds=(1,None), type=int)

options.sp = Option(name="second_pass", short="sp", option_type=0, default=False,
                    help=HELP_SECOND_PASS, type=bool)
options.re = Option(name="reverse", short="re", option_type=0, default=False,
                    help=HELP_REVERSE, type=bool)
options.sl = Option(name="silent", short="sl", option_type=0, default=False,
                    help=HELP_SILENT, type=bool)
options.nl = Option(name="nolog", short="nl", option_type=0, default=False,
                    help=HELP_NOLOG, type=bool)
