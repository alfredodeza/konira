import inspect
import sys
from konira.exc             import KoniraFirstFail, KoniraNoSkip
from konira.util            import StopWatch, get_class_name
from konira.collector       import globals_from_execed_file
from konira.output          import TerminalWriter, ExcFormatter, out_footer


class Runner(object):

    def __init__(self, paths, config):
        self.config         = config
        self.paths          = paths
        self.failures       = []
        self.errors         = []
        self.total_cases    = 0
        self.total_failures = 0
        self.total_errors   = 0
        self.total_skips    = 0
        self.class_name     = config.get('class_name')
        self.method_name    = config.get('method_name')
        self.write          = sys.__stdout__.write
        self.writer         = TerminalWriter(config.get('dotted'))


    def run(self):
        self.timer = StopWatch()
        for f in self.paths:
            try:
                classes = self.classes(f)
            except Exception, e:
                self.total_errors += 1
                self.errors.append(
                    dict(
                        failure   = sys.exc_info(),
                        exc_name  = e.__class__.__name__
                       ) 
                    )
                continue
            try:
                for case in classes:
                    self.run_suite(case)
            except KoniraFirstFail:
                break

        self.elapsed = self.timer.elapsed()


    def run_suite(self, case):
        # Initialize the test class
        suite = case()

        # check test environment setup
        environ = TestEnviron(suite)

        methods = self.methods(suite)
        if not methods: return

        # Name the class
        self.writer.out_case(suite.__class__.__name__)

        # Are we skipping?
        if self.safe_skip_call(environ.set_skip_if):
            self.writer.skipping()
            return

        # Set before all if any
        self.safe_environ_call(environ.set_before_all)

        for test in methods:
            self.total_cases += 1

            # Set before each if any
            self.safe_environ_call(environ.set_before_each)

            try:
                getattr(suite, test)()
                self.writer.green_spec(test)
                
            except BaseException, e:
                trace = inspect.trace()[1]
                self.total_failures += 1
                self.writer.red_spec(test)
                self.failures.append(
                    dict(
                        failure  = sys.exc_info(),
                        trace    = trace,
                        exc_name = e.__class__.__name__
                       ) 
                    )
                if self.config.get('first_fail'):
                    raise KoniraFirstFail

            # Set after each if any
            self.safe_environ_call(environ.set_after_each)

        # Set after all if any
        self.safe_environ_call(environ.set_after_all)


    def safe_environ_call(self, env_call):
        try:
            env_call()
        except Exception, e:
            self.errors.append(
                dict(
                    failure   = sys.exc_info(),
                    exc_name  = e.__class__.__name__
                   ) 
                )


    def safe_skip_call(self, env_call):
        try:
            skip = env_call()
            return True
        except KoniraNoSkip:
            return False
        except Exception:
            return False


    # XXX This is probably the wrong spot for this guy
    def report(self):
        self.write('\n')
        if self.failures:
            format_exc = ExcFormatter(self.failures, self.config)
            format_exc.output_failures()
        if self.errors:
            format_exc = ExcFormatter(self.errors, self.config)
            format_exc.output_errors()
        out_footer(self.total_cases, self.total_failures, self.elapsed)


    def classes(self, filename):
        if self.class_name:
            classes = [i for i in self._collect_classes(filename) 
                        if self.class_name == get_class_name(i)]
        else:
            classes = [i for i in self._collect_classes(filename)]

        return classes


    def methods(self, suite):
        if self.method_name:
            methods = [i for i in self._collect_methods(suite) 
                        if i == self.method_name]
        else:
            methods = self._collect_methods(suite)

        return methods


    def _collect_classes(self, path):
        global_modules = map(globals_from_execed_file, [path])
        return [i for i in global_modules[0].values() if callable(i) and i.__name__.startswith('Case_')]


    def _collect_methods(self, module):
        invalid = ['_before_each', '_before_all', '_after_each', '_after_all']
        return [i for i in dir(module) if not i.startswith('_') and i not in invalid and i.startswith('it_')] 



class TestEnviron(object):
    """
    Checks for all test setup calls and sets a boolean
    flag for each.
    This approach avoids the runner to be checking getattr
    for every time since we alredy did at the beginning.
    """


    def __init__(self, suite):
        self.suite           = suite
        self.has_skip_if     = self._skip_if
        self.has_before_all  = self._before_all
        self.has_before_each = self._before_each
        self.has_after_all   = self._after_all
        self.has_after_each  = self._after_each


    @property
    def _skip_if(self):
        if hasattr(self.suite, '_skip_if'):
            return True
        return False


    @property
    def _before_all(self):
        if hasattr(self.suite, '_before_all'):
            return True
        return False


    @property
    def _before_each(self):
        if hasattr(self.suite, '_before_each'):
            return True
        return False


    @property
    def _after_all(self):
        if hasattr(self.suite, '_after_all'):
            return True
        return False


    @property
    def _after_each(self):
        if hasattr(self.suite, '_after_each'):
            return True
        return False
    

    def set_skip_if(self):
        if self.has_skip_if:
            getattr(self.suite, '_skip_if')()
        else:
            raise KoniraNoSkip


    def set_before_all(self):
        if self.has_before_all:
            getattr(self.suite, '_before_all')()


    def set_before_each(self):
        if self.has_before_each:
            return getattr(self.suite, '_before_each')()


    def set_after_all(self):
        if self.has_after_all:
            return getattr(self.suite, '_after_all')()


    def set_after_each(self):
        if self.has_after_each:
            return getattr(self.suite, '_after_each')()
                

