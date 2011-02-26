import inspect
import sys
from jargon.util            import StopWatch
from jargon.collector       import globals_from_execed_file
from jargon.output          import (out_red, out_green, out_spec, 
                                    ExcFormatter, out_footer)



class Runner(object):

    def __init__(self, paths):
        self.paths          = paths
        self.failures       = []
        self.errors         = []
        self.total_cases    = 0
        self.total_failures = 0
        self.total_errors   = 0


    def run(self):
        self.timer = StopWatch()
        for f in self.paths:
            try:
                classes = [i for i in self._collect_classes(f)]
            except Exception, e:
                self.total_errors += 1
                self.errors.append(e)
                continue
            for case in classes:
                suite = case()
                self.run_suite(suite)
        self.elapsed = self.timer.elapsed()


    def run_suite(self, suite, before_all=None):
        sys.stdout.write('\n')
        out_spec(suite.__class__.__name__)
        methods = self._collect_methods(suite)
        for test in methods:
            self.total_cases += 1
            try:
                t = getattr(suite, test)
                t()
                out_green(test)
                
            except BaseException, e:
                trace = inspect.trace()
                self.total_failures += 1
                out_red(test)
                self.failures.append(
                    dict(
                        failure   = sys.exc_info(),
                        exc_name  = e.__class__.__name__
                       ) 
                    )

    def set_before_all(self, case, methods):
        if hasattr(case, 'before_all'):
            return getattr(case, 'before_all')


    def set_before_each(self, case, methods):
        if hasattr(case, 'before_each'):
            return getattr(case, 'before_each')


    def set_after_all(self, case, methods):
        if hasattr(case, 'after_all'):
            return getattr(case, 'after_all')


    def set_after_each(self, case, methods):
        if hasattr(case, 'after_each'):
            return getattr(case, 'after_each')
                

    def report(self):
        sys.stdout.write('\n')
        if self.failures:
            format_exc = ExcFormatter(self.failures)
            format_exc.output_failures()
        if self.errors:
            format_exc = ExcFormatter(self.errors)
            format_exc.output_errors()
        out_footer(self.total_cases, self.total_failures, self.elapsed)


    def _collect_classes(self, path):
            global_modules = map(globals_from_execed_file, [path])
            return [i for i in global_modules[0].values() if callable(i) and i.__name__.startswith('Case_')]


    def _collect_methods(self, module):
            return [i for i in dir(module) if not i.startswith('_')]
