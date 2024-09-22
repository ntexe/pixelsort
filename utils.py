# option_type can be 0, 1 or 2.
# 0 - argument is a flag (bool value)
# 1 - argument can contain only one value
# 2 - argument can contain multiple values (list)

class Option(object):
    """Option object. Not to be confused with Options object"""
    def __init__(self, name=None, short=None, option_type=None, default=None,
                 choices=None, help_string=None, value=None, val_type=None,
                 keyframes=None, bounds=None, isvariable=False, show=False):
        self.name = name
        self.short = short
        self.option_type = option_type
        self.default = default
        self.choices = choices
        self.help_string = help_string
        self.value = value
        self.val_type = val_type
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
            res = 1
            return

        splitted = str(self.value).split(",")

        if len(splitted) > 2:
            self.set_to_default()
            res = 1
            return res

        start = self.val_type(splitted[0])
        end = self.val_type(splitted[-1])

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

class SortParams(object):
    """Sort parameters object."""
    pass
