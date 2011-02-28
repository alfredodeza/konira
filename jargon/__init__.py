from cStringIO import StringIO
import sys
import os
from jargon                 import tokenizer
from jargon.collector       import FileCollector
from jargon.runner          import Runner


class JargonCommands(object):

    jargon_help = """
Jargon: A test runner and DSL testing framework for writing readable, 
descriptive tests.

Run tests:

    jargon [PATH] 

Options:

    no-capture      Avoids capturing stderr and stdout
"""

    def __init__(self, argv=None, parse=True):
        self.no_capture = False
        if argv is None:
            argv = sys.argv
        if parse:
            self.parseArgs(argv)


    def msg(self, msg, stdout=True):
        if stdout:
            sys.stdout.write(msg)
        else:
            sys.stderr.write(msg)
        if not self.test:
            sys.exit(1)


    def path_from_argument(self, argv):
        valid_path = [path for path in argv if os.path.exists(os.path.abspath(path))]
        if valid_path:
            return valid_path[0]
        else:
            return os.getcwd()


    @property
    def capture(self):
        if not self.no_capture:
            self.original_stdout = sys.stdout
            sys.stdout = StringIO()


    @property
    def end_capture(self):
        if not self.no_capture:
            sys.stdout = self.original_stdout


    def parseArgs(self, argv):
        # No options for now
        options      = ['no-capture']
        help_options = ['-h', '--h', '--help', 'help']

        # Catch help before anything
        if [i for i in argv if i in help_options]:
            self.msg(self.jargon_help)

        # Get a valid path
        search_path = self.path_from_argument(argv)

        match = [i for i in argv if i in options]

        if match:
            arg_count = {}
            count_arg = {}
            
            for count, argument in enumerate(argv):
                arg_count[argument] = count 
                count_arg[count] = argument

            if arg_count.get('no-capture'):
                self.no_capture = True
                

        test_files = FileCollector(search_path)
        if not test_files:
            self.msg("No cases found to test.")

        self.capture
        test_runner = Runner(test_files)
        test_runner.run()
        self.end_capture

        test_runner.report()



