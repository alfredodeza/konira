import sys
import os
from konira           import tokenizer
from cStringIO        import StringIO
from konira.collector import FileCollector
from konira.runner    import Runner
from konira.exc       import DontReadFromInput
from konira.util      import runner_options
from konira.ext       import cover
from konira.argopts   import ArgOpts
from konira.output    import ReportResults
import konira.tools

__version__ = '0.3.1'

class KoniraCommands(object):

    konira_help = """
konira: A test runner and DSL testing framework for writing readable, 
descriptive tests.

Version: %s

Run tests:
    konira [/path/to/cases] 
    konira ['/path/to/cases::case description::it description']

Control Options:
    --version, version  Shows the current installed version
    -s, no-capture      Avoids capturing stderr and stdout
    -x, fail            Stops at first fail
    -t, traceback       Shows tracebacks with errors/fails
    -d, dots            Displays '.' for passing and 'F' for failed tests.
    -p, profile         Enables profiling displaying the 10 slowest tests
                        forces dotted output.
    --debug             Doesn't remove internal tracebacks

Collection options:
    --collect-match     Provide a regex to match files for collection and avoiding
                        the default ("case_*.py")
    --collect-ci        Case insensitive for collection matching (only useful if
                        '--collect-match' is used.

Coverage Options:
    cover               Runs coverage and (optionally) includes information 
                        for selected packages
    --no-missing        Ommit missing lines in files

Matching Options:
    describe            Matches a case description (needs to be 
                        quoted)
    it                  Matches an 'it' spec (needs to be quoted)

    """ % __version__

    def __init__(self, argv=None, parse=True, test=False):
        self.test             = test
        self.config           = runner_options
        self.running_coverage = False
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._original_stdin  = sys.stdin
        self._stderr_buffer   = StringIO()
        self._stdout_buffer   = StringIO()
        
        if argv is None:
            argv = sys.argv
        if parse:
            self.parseArgs(argv)


    def msg(self, msg, stdout=True):
        if stdout:
            sys.stdout.write(msg+'\n')
        else:
            sys.stderr.write(msg+'\n')
        if not self.test:
            sys.exit(1)


    def test_from_path(self, path):
        spath = path.split('::')
        if len(spath) == 3:
            return dict(
                    path        = spath[0],
                    class_name  = tokenizer.valid_class_name(spath[1]),
                    method_name = tokenizer.valid_method_name(spath[2])
                    )
        elif len(spath) == 2:
            return dict(
                    path       = spath[0],
                    class_name = tokenizer.valid_class_name(spath[1]),
                    )
        else:
            return dict(path = path)


    def path_from_argument(self, argv):
        # Get rid of the executable
        p_argv = argv[1:]
        valid_path = [path for path in p_argv if os.path.exists(os.path.abspath(path.split('::')[0]))]
        if valid_path:
            tests = self.test_from_path(os.path.abspath(valid_path[0]))
            return dict(
                    path        = tests.get('path'),
                    class_name  = tests.get('class_name'),
                    method_name = tests.get('method_name')
                    )
        else:
            return dict(path = os.getcwd())


    def capture(self):
        if self.config['capturing'] is True:
            sys.stderr = self._stderr_buffer
            sys.stdout = self._stdout_buffer
            sys.stdin  = DontReadFromInput()


    def end_capture(self):
        if self.config['capturing'] is True:
            sys.stderr = self._original_stderr
            sys.stdout = self._original_stdout
            sys.stdin  = self._original_stdin


    def parseArgs(self, argv):
        options = ['no-capture', '-s', 'fail', '-x', '-t', '-d', '--debug',
                   'dots', 'traceback', 'tracebacks', 'describe', 'it',
                   '--collect-match', '--collect-ci']
        coverage_options  = ['--show-missing', '--cover-dir', '--cover-report',
                            'cover']
        profiling_options = ['-p', 'profile']
        options.extend(coverage_options)
        options.extend(profiling_options)

        args = ArgOpts(options)
        args.parse_args(argv)
        
        if args.catches_help():
            self.msg(self.konira_help)

        if args.catches_version():
            message = "konira version %s" % __version__
            self.msg(message)

        # Get a valid path
        path_info   = self.path_from_argument(argv)
        search_path = path_info.get('path')
        self.config['class_name']  = path_info.get('class_name')
        self.config['method_name'] = path_info.get('method_name')

        if args.match:

            # Matches for Describe
            if args.has('describe'):
                value = args.get_value('describe')
                if value:
                    self.config['class_name'] = tokenizer.valid_class_name(value)
                else:
                    self.msg("No valid 'describe' name")

            # Matches for it
            if args.has('it'):
                value = args.get_value('it')
                if value:
                    self.config['method_name'] = tokenizer.valid_method_name(value)
                else:
                    self.msg("No valid 'it' name")

            # Collection regex
            if args.has('--collect-match'):
                value = args.get_value('--collect-match')
                if value:
                    self.config['collect-match'] = value
                else:
                    self.msg("'--collect-match' needs a value")

            if args.has('--collect-ci'):
                self.config['collect-ci'] = True

            # Dotted output
            if args.has(['-d','dots']):
                self.config['dotted'] = True

            # Traceback options
            if args.has(['-t', 'traceback']):
                self.config['traceback'] = True

            # Fail options
            if args.has(['-x', 'fail']):
                self.config['first_fail'] = True

            # Capturing options
            if args.has(['-s', 'no-capture']):
                self.config['capturing'] = False

            # Profiling options
            if args.has(['-p', 'profile']):
                self.config['profiling'] = True
                self.config['dotted']    = True

            # Debugging option
            if args.has(['--debug']):
                self.config['debug'] = True

            # Coverage options
            if args.has('cover'):
                self.running_coverage = True
                coverage_options = {}
                value = args.get_value('cover')
                if value:
                    coverage_options['coverpackages'] = [value]
                if args.has('--show-missing'):
                    coverage_options['show_missing'] = True

                run_cover = cover.DoCoverage(coverage_options)


        test_files = FileCollector(search_path, self.config)

        if not test_files:
            self.msg("No cases found to test.")
        try:
            self.capture()
            test_runner = Runner(test_files, self.config)
            test_runner.run()
            self.end_capture()
            report = ReportResults(test_runner)
            report.report()
            if self.running_coverage:
                run_cover.konira_terminal_summary()
            if test_runner.failures or test_runner.errors:
                sys.exit(2)
        except KeyboardInterrupt:
            self.msg("Exiting from konira.")



