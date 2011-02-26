import os
import optparse
from jargon                 import tokenizer
from jargon.collector       import FileCollector
from jargon.runner          import Runner



def JargonCommands():
    parse = optparse.OptionParser()
    options, arguments = parse.parse_args()

    match   = False
    path    = os.getcwd()

    test_files  = FileCollector(path, match)
    if not test_files:
        print "No cases found to test."
        return

    test_runner = Runner(test_files)
    test_runner.run()
    test_runner.report()


main = JargonCommands


def main_():
    main()

