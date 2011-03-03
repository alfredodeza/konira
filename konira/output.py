import traceback
from os.path                import dirname, abspath
from sys                    import stdout
from konira.util            import name_convertion, green, red, bold
from konira.exc             import konira_assert



def green_spec(title):
    string = "\n    %s" % (green(name_convertion(title)))
    stdout.write(string)



def red_spec(title):
    string = "\n    %s" % (red(name_convertion(title)))
    stdout.write(string)



def out_case(title):
    stdout.write("\n%s" % name_convertion(title))



def out_bold(string):
    stdout.write("%s" % (bold(string)))



def out_footer(cases, failures, elapsed):
    if not failures:
        spec_verb = 'specs' if cases > 1 else 'spec'
        string = green("\nAll %s %s passed in %s secs.\n" % (cases, spec_verb, elapsed))
    elif failures:
        spec_verb = 'specs' if failures > 1 else 'spec'
        string = red("\n%s %s failed, %s total in %s secs.\n" % (failures, spec_verb, cases, elapsed))
    if not cases:
        string = "\nNo cases/specs collected.\n"
    stdout.write(string)


def format_file_line(filename, line):
    return bold("%s:%s:" % (filename, line))


class ExcFormatter(object):


    def __init__(self, failures, config):
        self.config      = config
        self.failures    = failures
        self.failed_test = 1


    def output_failures(self):
        stdout.write(red('\n\nFailures:\n---------'))
        for failure in self.failures:
            self.single_exception(failure)
        stdout.write('\n\n')


    def output_errors(self):
        stdout.write(red('\n\nErrors:\n-------'))
        for error in self.failures:
            error = self.build_error_output(error)
            self.failure_header(error['description'])
            stdout.write(red("File: "))
            stdout.write(format_file_line(error['filename'], error['lineno']))
            if self.config.get('traceback') and error['text']:
                stdout.write(red('\n'+error['text']))
        stdout.write('\n\n')


    def build_error_output(self, error):
        exc = {}
        p_error = PrettyExc(error['failure'], error=True)
        exc['description'] = p_error.exception_description
        exc['filename']    = p_error.exception_file
        exc['lineno']      = p_error.exception_line
        exc['text']        = p_error.formatted_exception
        return exc


    def single_exception(self, failure):
        exc        = failure.get('failure')
        name       = failure.get('exc_name')
        trace      = failure.get('trace')
        pretty_exc = PrettyExc(exc)

        self.failure_header(pretty_exc.exception_description)
        stdout.write(red("File: "))
        stdout.write(format_file_line(pretty_exc.exception_file, pretty_exc.exception_line))
        if self.config.get('traceback'):
            if name == 'AssertionError':
                reassert = konira_assert(trace)            
                if reassert:
                    self.assertion_diff(reassert)
                else:
                    stdout.write("\n")
                    stdout.write(pretty_exc.formatted_exception)
            else:
                stdout.write("\n")
                stdout.write(pretty_exc.formatted_exception)


    def assertion_diff(self, diff):
        stdout.write(red("\nAssert Diff: ")) 

        # remove actual assert line
        diff.pop(0)
        for line in diff:
            if "?" and "^" in line:
                stdout.write(red('\nE  '+line))
            else:
                stdout.write(red('\nE  ')+line)


    def failure_header(self, name):
        string = "\n\n%s ==> %s\n" % (self.failed_test, name)
        self.failed_test += 1
        stdout.write(red(string))



class PrettyExc(object):


    def __init__(self, exc_info, error=False):
        self.error = error
        self.exc_type, self.exc_value, self.exc_traceback = exc_info
        if self.error:
            self.exc_traceback =  self._last_traceback(self.exc_traceback)
        self.exc_traceback  = self._remove_konira_from_traceback(self.exc_traceback)
        self.exception_line = self.exc_traceback.tb_lineno
        self.exception_file = self.exc_traceback.tb_frame.f_code.co_filename
        self.exc_info       = exc_info


    @property
    def formatted_exception(self):
        traceback_lines = traceback.format_exception(self.exc_type,
                                                     self.exc_value,
                                                     self.exc_traceback)
        return ''.join(traceback_lines)


    @property
    def indented_traceback(self):
        trace = self.formatted_exception.split('\n')
        add_indent = ["    "+i for i in trace]
        return '\n'.join(add_indent)


    def _remove_konira_from_traceback(self, traceback):
        if self.error: return traceback
        konira_dir = dirname(abspath(__file__))

        while True:
            frame    = traceback.tb_frame
            code     = frame.f_code
            filename = code.co_filename
            code_dir = dirname(abspath(filename))
            if code_dir != konira_dir:
                break
            else:
                traceback = traceback.tb_next

        return traceback


    @property
    def exception_description(self):
        desc = traceback.format_exception_only(self.exc_type, self.exc_value)
        return self._short_exception_description(desc)


    def _short_exception_description(self, exception_description_lines):
        return exception_description_lines[-1].strip()


    def _last_traceback(self, tb):
        while tb.tb_next:
            tb = tb.tb_next
        return tb


