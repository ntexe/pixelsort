from collections import namedtuple

# option_type can be 0, 1 or 2.
# 0 - argument is a flag (bool value)
# 1 - argument can contain only one value
# 2 - argument can contain multiple values (list)
option_fields = ["name", "short", "option_type", "default", "choices", "help",
                 "value", "range", "bounds", "type"]

Option = namedtuple("Option", option_fields, defaults=[None]*len(option_fields))
