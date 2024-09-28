from constants import *
from utils import Option

class Options(object):
    """Options object. Not to be confused with Option object."""
    pass

def gen_options():
    """Generate options."""
    options = Options()

    options.input_path = Option(name="input_path", short="input_path",
                                option_type=1, help_string=HELP_INPUT_PATH, val_type=str)
    options.o =  Option(name="output", short="o", option_type=1,
                        default=OPTION_DEFAULTS["output"],
                        help_string=HELP_OUTPUT, val_type=str)
    options.e =  Option(name="ext", short="e", option_type=1,
                        default=OPTION_DEFAULTS["ext"],
                        help_string=HELP_EXT, val_type=str)
    options.m =  Option(name="mask", short="m", option_type=1,
                        default=OPTION_DEFAULTS["mask"], 
                        help_string=HELP_MASK, val_type=str, show=True)

    options.ll = Option(name="loglevel", short="ll", option_type=1,
                        default=OPTION_DEFAULTS["loglevel"],
                        choices=LOGLEVEL_CHOICES+AUX_LL_CHOICES, help_string=HELP_LOGLEVEL,
                        val_type=str)

    options.sg = Option(name="segmentation", short="sg", option_type=1,
                        default=OPTION_DEFAULTS["segmentation"],
                        choices=SEGMENTATION_CHOICES, help_string=HELP_SEGMENTATION,
                        val_type=str, show=True)
    options.sk = Option(name="skey_choice", short="sk", option_type=1,
                        default=OPTION_DEFAULTS["skey_choice"],
                        choices=SKEY_CHOICES, help_string=HELP_SKEY, val_type=str, show=True)

    options.t =  Option(name="threshold", short="t", option_type=1,
                        default=OPTION_DEFAULTS["threshold"], help_string=HELP_THRESHOLD,
                        bounds=(0,1), val_type=float, isvariable=True, show=True)
    options.a =  Option(name="angle", short="a", option_type=1,
                        default=OPTION_DEFAULTS["angle"], help_string=HELP_ANGLE,
                        bounds=(0,360), val_type=int, isvariable=True, show=True)
    options.sa = Option(name="sangle", short="sa", option_type=1,
                        default=OPTION_DEFAULTS["sangle"], help_string=HELP_SANGLE,
                        bounds=(0,360), val_type=int, isvariable=True, show=True)
    options.sz = Option(name="size", short="sz", option_type=1,
                        default=OPTION_DEFAULTS["size"], help_string=HELP_SIZE,
                        bounds=(0.001,1), val_type=float, isvariable=True, show=True)
    options.r =  Option(name="randomness", short="r", option_type=1,
                        default=OPTION_DEFAULTS["randomness"], help_string=HELP_RANDOMNESS,
                        bounds=(0,0.5), val_type=float, isvariable=True, show=True)
    options.l =  Option(name="length", short="l", option_type=1,
                        default=OPTION_DEFAULTS["length"], help_string=HELP_LENGTH,
                        bounds=(1,None), val_type=float, isvariable=True, show=True)

    options.sc = Option(name="scale", short="sc", option_type=1,
                        default=OPTION_DEFAULTS["scale"], help_string=HELP_SCALE,
                        bounds=(0.01,10), val_type=float, isvariable=True, show=True)
    options.w =  Option(name="width", short="w", option_type=1,
                        default=OPTION_DEFAULTS["width"], help_string=HELP_WIDTH,
                        bounds=(0,None), val_type=int, isvariable=True, show=True)
    options.hg = Option(name="height", short="hg", option_type=1,
                        default=OPTION_DEFAULTS["height"], help_string=HELP_HEIGHT,
                        bounds=(0,None), val_type=int, isvariable=True, show=True)

    options.am = Option(name="amount", short="am", option_type=1,
                        default=OPTION_DEFAULTS["amount"], help_string=HELP_AMOUNT,
                        bounds=(1,None), val_type=int)

    options.sp = Option(name="second_pass", short="sp", option_type=0, default=False,
                        help_string=HELP_SECOND_PASS, val_type=bool, show=True)
    options.re = Option(name="reverse", short="re", option_type=0, default=False,
                        help_string=HELP_REVERSE, val_type=bool, show=True)
    options.pr = Option(name="preserve_res", short="pr", option_type=0, default=False,
                        help_string=HELP_PRESERVE_RES, val_type=bool, show=True)
    options.sl = Option(name="silent", short="sl", option_type=0, default=False,
                        help_string=HELP_SILENT, val_type=bool)
    options.nl = Option(name="nolog", short="nl", option_type=0, default=False,
                        help_string=HELP_NOLOG, val_type=bool)

    return options
