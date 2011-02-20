import sys
from jargon.collector       import globals_from_execed_file
from jargon.util            import name_convertion, green, red


class Runner(object):

    def __init__(self, paths):
        self.paths = paths


    def run(self):
        total_methods = 0
        total_method_fails = 0
        for f in self.paths:
            for case in self._collect_classes(f):
                suite_methods = 0
                suite = case()
                print "\n%s" % name_convertion(suite.__class__.__name__)
                methods = [i for i in dir(suite) if not i.startswith('_')]
                for test in methods:
                    try:
                        t = getattr(suite, test)
                        t()
                        print green(name_convertion(test))
                        #print "%s  - %s%s"% (GREEN, name_convertion(test), ENDS)
                        total_methods += 1
                    except BaseException, e:
                        failure              = sys.exc_info()
                        tb                   = failure[2]
                        exc_name             = e.__class__.__name__
                        total_method_fails   += 1
                        print red(name_convertion(test))
                        #print "%s  - %s%s" % (RED, name_convertion(test), ENDS)
        if not total_methods:
            print "No collected tests to run."

        elif total_method_fails:
            string = "\n%s out of %s failed" % (total_method_fails, total_methods)
            print red(string)
            
            #print "\n%s%s out of %s failed%s" % (RED,total_method_fails, total_methods, ENDS)
        else:
            string = "\nall %s test(s) passed" % (total_methods)
            print green(string)
            #print "\n%sall %s test(s) passed%s" % (GREEN, total_methods, ENDS)


    def _collect_classes(self, path):
            global_modules = map(globals_from_execed_file, [path])
            test_modules = [  i for i in global_modules[0].values() if callable(i) and 'test' in i.__name__ ]
            return test_modules


    def _collect_methods(self, module):
            methods = [i for i in dir(module) if not i.startswith('_')]
            return methods
