"""
Write and report coverage data with the 'coverage' package.
Original code by Ross Lawley. 

Requires Ned Batchelder's excellent coverage:
http://nedbatchelder.com/code/coverage/
"""

import sys


def pytest_addoption(parser):
    group = parser.getgroup('Coverage options')
    group.addoption('--cover', action='append', default=[],
            dest='coverpackages',
            help='(multi allowed) only include info from specified package.')
    group.addoption('--cover-report', action='store', default=None,
            dest='report_type', type="choice", 
            choices=['report', 'annotate', 'html'],
            help="""
                html: Directory for html output.
                report: Output a text report.
                annotate: Annotate your source code for which lines were executed and which were not.
            """.strip())
    group.addoption('--cover-directory', action='store', default=None,
            dest='directory', 
            help='Directory for the reports (html / annotate results) defaults to ./coverage')
    group.addoption('--cover-show-missing', action='store_true', default=False,
            dest='show_missing',
            help='Show missing files')
    group.addoption('--cover-ignore-errors', action='store', default=None,
            dest='ignore_errors', 
            help='Ignore errors of finding source files for code.')


def import_coverage():
    try:
        from coverage import coverage
        return coverage()
    except ImportError:
        msg = "coverage is not installed or not available in current sys.path"
        sys.stdout.write(msg)
        sys.exit(2)


class DoCoverage(object):


    def __init__(self, options=None):
        if not options:
            self.options = self._defaults
        else:
            self.options = options
        self._coverage = import_coverage()
        self._coverage.use_cache(False)
        self._coverage.start()


    @property
    def _defaults(self):
        return dict(
                    show_missing  = True,
                    report        = 'report',
                    directory     = 'coverage',
                    ignore_errors = True,
                    coverpackages = False
                    )


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
