import time
import sys
import inspect
if sys.version < '3':
    from cStringIO import StringIO
else:
    from io import StringIO

def return_exception_trace():
    """
    For testing purposes we need some valid
    tracebacks created for assertions.
    """
    try:
        assert False
    except Exception, e:
        trace = inspect.trace()
        return dict(
                        failure  = sys.exc_info(),
                        trace    = trace,
                        exc_name = e.__class__.__name__
                       ) 


def name_convertion(name, capitalize=True):
    name = name.replace('_', ' ').replace('Case', '')
    if capitalize:
        name = name.capitalize()
    return name.strip()



def get_class_name(class_name):
    try:
        name = str(class_name).split("'")[1]
    except IndexError:
        return class_name
    if name.startswith('Case_'):
        return name



class StopWatch(object):
 

    def __init__(self, raw=False):
        self.raw = raw
        self.start = time.time()


    def elapsed(self):
        _elapsed = str(time.time() - self.start)
        if not self.raw:
            return _elapsed[:5]
        return _elapsed


runner_options = dict(
        first_fail = False,
        capturing  = True,
        traceback  = False,
        dotted     = False,
        profiling  = False
        )

     
