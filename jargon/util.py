import time

#
# Coloring Codes
#
BLUE   = '\033[94m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m'
BOLD   = '\033[1m'
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


def bold(string):
    """
    Makes text bold in the terminal
    """
    bold_it = "%s%s%s" % (BOLD, string, ENDS)
    return bold_it


def name_convertion(name):
    name = name.replace('_', ' ')
    name = name.capitalize() 
    return name



class StopWatch(object):
 

    def __init__(self):
        self.start = time.time()


    def elapsed(self):

        _elapsed = str(time.time() - self.start)
        return _elapsed[:5]



class Source(object):
    """A helper to try and grab the 3 most important
    things when re-evaluating a failed assert:
    - left value
    - operand
    - right value
    """
    pass

     
