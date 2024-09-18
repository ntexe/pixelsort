from collections import namedtuple

from constants import *
from utils import Option

option_names = ["input_path", "o", "ll", "sg", "sk", "f", "t", "a", "sa","sz",
                "r", "l", "sc", "w", "hg", "am", "sp", "re", "sl", "nl"]

Options = namedtuple("Options", option_names, defaults=[None]*len(option_names))

def gen_options():
    options = Options()
    options = options._replace(input_path=Option(name="input_path", short="input_path",
                                                 option_type=1, help=HELP_INPUT_PATH, type=str))

    options = options._replace(o= Option(name="output_path", short="o", option_type=1,
                                         help=HELP_OUTPUT_PATH, type=str))
    options = options._replace(ll=Option(name="loglevel", short="ll", option_type=1,
                                         default=OPTION_DEFAULTS["loglevel"],
                                         choices=LOGLEVEL_CHOICES+AUX_LL_CHOICES,
                                         help=HELP_LOGLEVEL, type=str))
    options = options._replace(sg=Option(name="segmentation", short="sg", option_type=1,
                                         default=OPTION_DEFAULTS["segmentation"],
                                         choices=SEGMENTATION_CHOICES,
                                         help=HELP_SEGMENTATION, type=str))
    options = options._replace(sk=Option(name="skey_choice", short="sk", option_type=1,
                                         default=OPTION_DEFAULTS["skey_choice"],
                                         choices=SKEY_CHOICES,
                                         help=HELP_SKEY, type=str))
    options = options._replace(f= Option(name="format", short="f", option_type=1,
                                         default=OPTION_DEFAULTS["format"],
                                         choices=FORMAT_CHOICES,
                                         help=HELP_FORMAT, type=str))

    options = options._replace(t= Option(name="threshold", short="t", option_type=1,
                                         default=OPTION_DEFAULTS["threshold"], help=HELP_THRESHOLD,
                                         range=(0.1,0.1), bounds=(0,1), type=float))
    options = options._replace(a= Option(name="angle", short="a", option_type=1,
                                         default=OPTION_DEFAULTS["angle"], help=HELP_ANGLE,
                                         range=(0,0), bounds=(0,360), type=int))
    options = options._replace(sa=Option(name="sangle", short="sa", option_type=1,
                                         default=OPTION_DEFAULTS["sangle"], help=HELP_SANGLE,
                                         range=(90,90), bounds=(0,360), type=int))
    options = options._replace(sz=Option(name="size", short="sz", option_type=1,
                                         default=OPTION_DEFAULTS["size"], help=HELP_SIZE,
                                         range=(0.05,0.05), bounds=(0.01,1), type=float))
    options = options._replace(r= Option(name="randomness", short="r", option_type=1,
                                         default=OPTION_DEFAULTS["randomness"], help=HELP_RANDOMNESS,
                                         range=(0,0), bounds=(0,0.5), type=float))
    options = options._replace(l= Option(name="length", short="l", option_type=1,
                                         default=OPTION_DEFAULTS["length"], help=HELP_LENGTH,
                                         range=(10,10), bounds=(2,None), type=int))

    options = options._replace(sc=Option(name="scale", short="sc", option_type=1,
                                         default=OPTION_DEFAULTS["scale"], help=HELP_SCALE,
                                         range=(1,1), bounds=(0.01,10), type=float))
    options = options._replace(w= Option(name="width", short="w", option_type=1,
                                         default=OPTION_DEFAULTS["width"], help=HELP_WIDTH,
                                         range=(0,0), bounds=(0,None), type=int))
    options = options._replace(hg=Option(name="height", short="hg", option_type=1,
                                         default=OPTION_DEFAULTS["height"], help=HELP_HEIGHT,
                                         range=(0,0), bounds=(0,None), type=int))

    options = options._replace(am=Option(name="amount", short="am", option_type=1,
                                         default=OPTION_DEFAULTS["amount"], help=HELP_AMOUNT,
                                         bounds=(1,None), type=int))

    options = options._replace(sp=Option(name="second_pass", short="sp", option_type=0,
                                         help=HELP_SECOND_PASS, type=bool))
    options = options._replace(re=Option(name="reverse", short="re", option_type=0,
                                         help=HELP_REVERSE, type=bool))
    options = options._replace(sl=Option(name="silent", short="sl", option_type=0,
                                         help=HELP_SILENT, type=bool))
    options = options._replace(nl=Option(name="nolog", short="nl", option_type=0,
                                         help=HELP_NOLOG, type=bool))

    return options
