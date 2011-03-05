import time


def name_convertion(name):
    name = name.replace('_', ' ').replace('Case', '')
    name = name.capitalize().strip() 
    return name



class StopWatch(object):
 

    def __init__(self):
        self.start = time.time()


    def elapsed(self):

        _elapsed = str(time.time() - self.start)
        return _elapsed[:5]


runner_options = dict(
        first_fail = False,
        capturing  = True,
        traceback  = False
        )

     
