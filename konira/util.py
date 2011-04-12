import time


def name_convertion(name):
    name = name.replace('_', ' ').replace('Case', '')
    name = name.capitalize().strip() 
    return name



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

     
