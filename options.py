from constants import *

# option_type can be 0, 1 or 2.
# 0 - argument is a flag (bool value)
# 1 - argument can contain only one value
# 2 - argument can contain multiple values (list)

class Option(object):
    """Option object. Not to be confused with Options class."""
    def __init__(self, *, name=None, short=None, option_type=None, default=None,
                 choices=None, help_string=None, val_type=None,
                 keyframes=None, bounds=None, isvariable=False, show=False):
        self.name = name
        self.short = short
        self.option_type = option_type
        self.default = default if option_type != 0 else False
        self.choices = choices
        self.help_string = help_string
        self.value = None
        self.val_type = val_type if option_type != 0 else bool
        self.keyframes = keyframes
        self.bounds = bounds
        self.isvariable = isvariable # is value variable or constant?
        self.show = show # include this option to filename?

    def set_to_default(self):
        """Set value to default."""
        self.value = self.default

    def parse_keyframes(self) -> int:
        """
        Parse keyframes from value of Option object.
        If value is invalid, use default and return 1.
        """

        res = 0

        if not self.isvariable:
            return 1

        splitted = str(self.value).split(",")

        if len(splitted) > 2:
            self.set_to_default()
            splitted = str(self.value).split(",")
            res = 1

        start = self.val_type(splitted[0])
        end = self.val_type(splitted[-1])

        # we need cleanup here

        if self.bounds[0] != None:
            if start < self.bounds[0]:
                start = self.default
                res = 1

            if end < self.bounds[0]:
                end = self.default
                res = 1

        if self.bounds[1] != None:
            if start > self.bounds[1]:
                start = self.default
                res = 1

            if end > self.bounds[1]:
                end = self.default
                res = 1

        self.keyframes = (start, end)
        return res

    def get_balance(self, vals: tuple):
        """
        Get keyframes from Option object and return calculated value.

        :param vals: Values for ratio
        :type vals: tuple

        :returns: Calculated value
        """

        ratio = (vals[0]-1)/max(1, vals[1]-1)

        return round(self.keyframes[0]*(1-ratio) + self.keyframes[1]*ratio, 3 if self.val_type == float else None)

class Options(object):
    """Options object. Not to be confused with Option class."""
    def __init__(self):
        """Generate options."""
        self.input_path = Option(name="input_path", short="input_path",
                                    option_type=1, help_string=HELP_INPUT_PATH, val_type=str)
        self.o =  Option(name="output", short="o", option_type=1,
                         default=OPTION_DEFAULTS["output"],
                         help_string=HELP_OUTPUT, val_type=str)
        self.e =  Option(name="ext", short="e", option_type=1,
                         default=OPTION_DEFAULTS["ext"],
                         help_string=HELP_EXT, val_type=str)
        self.m =  Option(name="mask", short="m", option_type=1,
                         default=OPTION_DEFAULTS["mask"], 
                         help_string=HELP_MASK, val_type=str, show=True)

        self.ll = Option(name="loglevel", short="ll", option_type=1,
                         default=OPTION_DEFAULTS["loglevel"],
                         choices=LOGLEVEL_CHOICES+AUX_LL_CHOICES, help_string=HELP_LOGLEVEL,
                         val_type=str)

        self.sg = Option(name="segmentation", short="sg", option_type=1,
                         default=OPTION_DEFAULTS["segmentation"],
                         choices=SEGMENTATION_CHOICES, help_string=HELP_SEGMENTATION,
                         val_type=str, show=True)
        self.sk = Option(name="skey_choice", short="sk", option_type=1,
                         default=OPTION_DEFAULTS["skey_choice"],
                         choices=SKEY_CHOICES, help_string=HELP_SKEY,
                         val_type=str, show=True)

        self.t =  Option(name="threshold", short="t", option_type=1,
                         default=OPTION_DEFAULTS["threshold"], help_string=HELP_THRESHOLD,
                         bounds=(0,1), val_type=float, isvariable=True, show=True)
        self.a =  Option(name="angle", short="a", option_type=1,
                         default=OPTION_DEFAULTS["angle"], help_string=HELP_ANGLE,
                         bounds=(0,360), val_type=int, isvariable=True, show=True)
        self.sa = Option(name="sangle", short="sa", option_type=1,
                         default=OPTION_DEFAULTS["sangle"], help_string=HELP_SANGLE,
                         bounds=(0,360), val_type=int, isvariable=True, show=True)
        self.sz = Option(name="size", short="sz", option_type=1,
                         default=OPTION_DEFAULTS["size"], help_string=HELP_SIZE,
                         bounds=(0.001,1), val_type=float, isvariable=True, show=True)
        self.r =  Option(name="randomness", short="r", option_type=1,
                         default=OPTION_DEFAULTS["randomness"], help_string=HELP_RANDOMNESS,
                         bounds=(0,0.5), val_type=float, isvariable=True, show=True)
        self.l =  Option(name="length", short="l", option_type=1,
                         default=OPTION_DEFAULTS["length"], help_string=HELP_LENGTH,
                         bounds=(1,None), val_type=float, isvariable=True, show=True)

        self.sc = Option(name="scale", short="sc", option_type=1,
                         default=OPTION_DEFAULTS["scale"], help_string=HELP_SCALE,
                         bounds=(0.01,10), val_type=float, isvariable=True, show=True)
        self.w =  Option(name="width", short="w", option_type=1,
                         default=OPTION_DEFAULTS["width"], help_string=HELP_WIDTH,
                         bounds=(0,None), val_type=int, isvariable=True, show=True)
        self.hg = Option(name="height", short="hg", option_type=1,
                         default=OPTION_DEFAULTS["height"], help_string=HELP_HEIGHT,
                         bounds=(0,None), val_type=int, isvariable=True, show=True)

        self.am = Option(name="amount", short="am", option_type=1,
                         default=OPTION_DEFAULTS["amount"], help_string=HELP_AMOUNT,
                         bounds=(1,None), val_type=int)

        self.sp = Option(name="second_pass", short="sp", option_type=0,
                         help_string=HELP_SECOND_PASS, show=True)
        self.re = Option(name="reverse", short="re", option_type=0,
                         help_string=HELP_REVERSE, show=True)
        self.pr = Option(name="preserve_res", short="pr", option_type=0,
                         help_string=HELP_PRESERVE_RES, show=True)
        self.sm = Option(name="symmetry", short="sm", option_type=0,
                         help_string=HELP_SYMMETRY, show=True)

        self.sl = Option(name="silent", short="sl", option_type=0,
                         help_string=HELP_SILENT)
        self.nl = Option(name="nolog", short="nl", option_type=0,
                         help_string=HELP_NOLOG)
