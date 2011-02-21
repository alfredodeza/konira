
#
# Coloring Codes
#
BLUE   = '\033[94m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m'
ENDS   = '\033[0m'


def green(string):
    """
    Makes incoming string output as green on the terminal
    """
    color_it = "%s%s%s" % (GREEN, string, ENDS)
    return color_it


def red(string):
    """
    Makes incoming string output as red on the terminal
    """
    color_it = "%s%s%s" % (RED, string, ENDS)
    return color_it


def name_convertion(name):
    name = name.replace('_', ' ')
    name = name.capitalize() + '.'
    return name

