from sys                    import stdout, exc_info
from jargon.util            import name_convertion, green, red



class ExcFormatter(object):


    def __init__(self, failures):
        self.failures = failures
        for failure in failures:
            self.single_exception(failure)


    def single_exception(self, failure):
        failure     = exc_info()
        tb          = failure[2]
        exc_name    = self.exc.__class__.__name__




def out_green(title):
    string = "  - %s" % (green(name_convertion(title)))
    stdout.write(string)



def out_red(title):
    string = "  - %s" % (red(name_convertion(title)))
    stdout.write(string)



def out_spec(title):
    stdout.write("\n%s" % name_convertion(title.__class__.__name__))




