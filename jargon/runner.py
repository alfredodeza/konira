import sys
from jargon.collector       import globals_from_execed_file
from jargon.output          import out_red, out_green, out_spec, ExcFormatter, out_footer


class Runner(object):

    def __init__(self, paths):
        self.paths    = paths
        self.failures = []
        self.total_cases = 0
        self.total_failures = 0


    def run(self):
        for f in self.paths:
            classes = [i for i in self._collect_classes(f)]
            for case in self._collect_classes(f):
                suite = case()
                self.run_suite(suite)
        if self.failures:
            ExcFormatter(self.failures)
        out_footer(self.total_cases, self.total_failures)


    def run_suite(self, suite):
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
                self.total_failures += 1
                out_red(test)
                self.failures.append(
                    dict(
                        failure   = sys.exc_info(),
                        exc_name  = e.__class__.__name__
                       ) 
                    )
                

    def _collect_classes(self, path):
            global_modules = map(globals_from_execed_file, [path])
            return [i for i in global_modules[0].values() if callable(i)]


    def _collect_methods(self, module):
            return [i for i in dir(module) if not i.startswith('_')]
