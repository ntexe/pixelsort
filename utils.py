# option_type can be 0, 1 or 2.
# 0 - argument is a flag (bool value)
# 1 - argument can contain only one value
# 2 - argument can contain multiple values (list)

class Option(object):
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
        self.value = self.default

class SortParams(object):
    pass