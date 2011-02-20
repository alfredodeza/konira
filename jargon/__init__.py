import os
import optparse
import sys
from jargon                 import tokenizer
from jargon.collector       import FileCollector, globals_from_execed_file
from jargon.util            import name_convertion, green, red

def JargonCommands():
    parse = optparse.OptionParser()
    parse.add_option("--verbose","-v", action="store_true",
            help="Prints all the matching files with line numbers")
    parse.add_option("--path", help="Specify a path to report on")
    options, arguments = parse.parse_args()

    verbose = False
    match   = False
    path    = os.getcwd()

    if options.verbose:
        verbose = True 

    if options.path:
        path = os.path.abspath(options.path)

    locate = FileCollector(path, match)
    total_methods = 0
    total_method_fails = 0
    for f in locate:
        global_modules = map(globals_from_execed_file, [f])
        test_modules = [  i for i in global_modules[0].values() if callable(i) and 'test' in i.__name__ ]
        for case in test_modules:
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



main = JargonCommands

def main_():
    main()

