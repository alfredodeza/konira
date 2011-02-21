import os
import optparse
from jargon                 import tokenizer
from jargon.collector       import FileCollector
from jargon.runner          import Runner



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

    test_files  = FileCollector(path, match)
    if not test_files:
        print "No cases found to test."
        return
    test_runner = Runner(test_files)
    test_runner.run()


main = JargonCommands


def main_():
    main()

