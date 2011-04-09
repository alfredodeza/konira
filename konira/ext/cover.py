"""
Write and report coverage data with the 'coverage' package.
Original code by Ross Lawley. 

Requires Ned Batchelder's excellent coverage:
http://nedbatchelder.com/code/coverage/
"""
import sys


def import_coverage():
    try:
        from coverage import coverage
        return coverage()
    except ImportError:
        msg = "coverage is not installed or not available in current sys.path\n"
        msg +="make sure it is installed properly and try again."
        sys.stdout.write(msg)
        sys.exit(2)


class DoCoverage(object):


    __defaults__ = dict(
                    show_missing  = False,
                    report        = 'report',
                    directory     = 'coverage',
                    ignore_errors = True,
                    coverpackages = False
                    )


    def __init__(self, options=None):
        self.options = self.__defaults__
        if options:
            self.options.update(options)
        self._coverage = import_coverage()
        self._coverage.use_cache(False)
        self._coverage.start()


    def konira_terminal_summary(self):
        self._coverage.stop()
        self._coverage.save()

        show_missing = self.options.get('show_missing')
        report_type  = self.options.get('report')
        directory    = self.options.get('directory')
        ignore_err   = self.options.get('ignore_errors')
        
        report_args = {
            'ignore_errors': ignore_err,
        }

        coverpackages = self.options.get('coverpackages')
        if coverpackages:
            modules = report_args['morfs'] = []
            for name, module in sys.modules.items():
                if module is not None and hasattr(module, '__file__'):
                    fn = module.__file__
                    for pkg in coverpackages:
                        if name.startswith(pkg):
                            modules.append(fn)
                            break
        
        
        if report_type == 'report':
            self._coverage.report(show_missing=show_missing, file=sys.stdout,
                    **report_args)
        elif report_type == 'annotate':
            self._coverage.annotate(directory=directory, **report_type)
        elif report_type == 'html':
            self._coverage.html_report(directory=directory, **report_args)
