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

    locate = FileCollector(path, match)
    test_runner = Runner(locate)
    test_runner.run()


main = JargonCommands


def main_():
    main()
