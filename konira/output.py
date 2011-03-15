import sys
import traceback
from os.path                import dirname, abspath
from konira.util            import name_convertion 
from konira.exc             import konira_assert


class TerminalWriter(object):


    def __init__(self, dotted):
        self.dotted = dotted
        self.writer = Writer()


    def green_spec(self, title):
        string = "    %s" % (name_convertion(title))
        if not self.dotted:
            self.writer.writeln(string, 'green')
        else:
            self.writer.println('.')
            self.writer.flush()


    def red_spec(self, title):
        string = "    %s" % (name_convertion(title))
        if not self.dotted:
            self.writer.writeln(string, 'red')
        else:
            self.writer.println('F')
            self.writer.flush()


    def out_case(self, title):
        if not self.dotted:
            self.writer.println("\n\n%s" % name_convertion(title))


    def out_bold(self, string):
        self.writer.write(string, 'bold')


    def skipping(self):
        if not self.dotted:
            self.write.println(' ...skipping')
        else:
            self.writer.println('S')
            self.writer.flush()



def out_footer(cases, failures, elapsed, std=None):
    if not std:
        std = Writer()
    std.newline(2)
    if not failures and cases > 0:
        spec_verb = 'specs' if cases > 1 else 'spec'
        string = "All %s %s passed in %s secs.\n" % (cases, spec_verb, elapsed)
        std.writeln(string, 'green')
        return
    elif failures:
        spec_verb = 'specs' if failures > 1 else 'spec'
        string = "%s %s failed, %s total in %s secs.\n" % (failures, spec_verb, cases, elapsed)
        std.writeln(string, 'red')
        return
    if not cases or cases == 0:
        string = "No cases/specs collected.\n"
        std.writeln(string, 'bold')



def format_file_line(filename, line):
    return Writer().bold("%s:%s:" % (filename, line))



class ExcFormatter(object):


    def __init__(self, failures, config):
        self.config      = config
        self.failures    = failures
        self.failed_test = 1
        self.std = Writer()


    def output_failures(self):
        self.std.writeln('Failures:\n---------', 'red')
        for failure in self.failures:
            self.single_exception(failure)


    def output_errors(self):
        self.std.writeln('\n\nErrors:\n-------', 'red')
        for error in self.failures:
            error = self.build_error_output(error)
            self.failure_header(error['description'])
            self.std.writeln("File: ", 'red')
            self.std.println(format_file_line(error['filename'], error['lineno']))
            if self.config.get('traceback') and error['text']:
                self.std.writeln(error['text'], 'red')


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
        starts = pretty_exc.exception_file_start 
        ends= pretty_exc.exception_file_end
        if starts == ends:
            self.std.writeln("Starts and Ends: ", 'red')
            self.std.println(format_file_line(pretty_exc.exception_file_start, pretty_exc.exception_line_start))
        else:
            self.std.writeln("Starts: ", 'red')
            self.std.println(format_file_line(pretty_exc.exception_file_start, pretty_exc.exception_line_start))
            self.std.writeln("Ends: ", 'red')
            self.std.println(format_file_line(pretty_exc.exception_file_end, pretty_exc.exception_line_end))

        if self.config.get('traceback'):
            if name == 'AssertionError':
                reassert = konira_assert(trace)            
                if reassert:
                    self.assertion_diff(reassert)
                    self.std.writeln(pretty_exc.formatted_exception)
                else:
                    self.std.writeln(pretty_exc.formatted_exception)
            else:
                self.std.writeln(pretty_exc.formatted_exception)


    def assertion_diff(self, diff):
        self.std.writeln("Assert Diff: %s" % str(diff[0].__repr__()), 'red') 

        # remove actual assert line
        diff.pop(0)
        for line in diff:
            if "?" and "^" in line:
                self.std.writeln(self.std.red('E            '+line))
            else:
                self.std.writeln(self.std.red('E            ')+line)


    def failure_header(self, name):
        string = "\n%s ==> %s" % (self.failed_test, name)
        self.failed_test += 1
        self.std.writeln(string, 'red')



class PrettyExc(object):


    def __init__(self, exc_info, error=False):
        self.error = error
        self.exc_type, self.exc_value, self.exc_traceback = exc_info
        if self.error:
            self.exc_traceback =  self._last_traceback(self.exc_traceback)
        self.exc_traceback = self._remove_konira_from_traceback(self.exc_traceback)
        self.end_traceback = self._last_traceback(self.exc_traceback)
        self.exception_file_start = self.exc_traceback.tb_frame.f_code.co_filename
        self.exception_line_start = self.exc_traceback.tb_lineno
        self.exception_file_end   = self.end_traceback.tb_frame.f_code.co_filename
        self.exception_line_end   = self.end_traceback.tb_lineno
        self.exception_line       = self.exc_traceback.tb_lineno
        self.exception_file       = self.exc_traceback.tb_frame.f_code.co_filename
        
        self.exc_info             = exc_info


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



class Writer(object):


    def __init__(self, stdout=None):
        if not stdout:
            self.stdout = sys.__stdout__
        else:
            self.stdout = stdout
        self.out    = self.stdout.write
        self.isatty = self.stdout.isatty()
        self.flush  = self.stdout.flush


    def color(self, form):
        if not self.isatty: return ''
        if form == None: return ''
        available = dict(
                blue   = '\033[94m',
                green  = '\033[92m',
                yellow = '\033[93m',
                red    = '\033[91m',
                bold   = '\033[1m',
                ends   = '\033[0m'
            )
        try:
            return available[form]
        except:
            raise KeyError('%s is not a valid format/color' % form) 


    def println(self, string):
        self.out("%s" % string)


    def write(self, string, form):
        """No new line before or after"""
        color   = self.color(form)
        ends    = self.color('ends')
        out_str = "%s%s%s" % (color, string, ends)
        self.out(out_str)


    def writeln(self, string, form=None):
        """With a new line before and after"""
        color   = self.color(form)
        ends    = self.color('ends')
        out_str = "\n%s%s%s" % (color, string, ends)
        self.out(out_str)


    def newline(self, lines=1):
        nln = '\n'*lines
        self.out(nln)
        

    def green(self, string):
        """
        Makes incoming string output as green on the terminal
        """
        color   = self.color('green')
        ends    = self.color('ends')
        color_it = "%s%s%s" % (color, string, ends)
        return color_it


    def red(self, string):
        """
        Makes incoming string output as red on the terminal
        """
        color   = self.color('red')
        ends    = self.color('ends')
        color_it = "%s%s%s" % (color, string, ends)
        return color_it


    def bold(self, string):
        """
        Makes text bold in the terminal
        """
        color   = self.color('bold')
        ends    = self.color('ends')
        bold_it = "%s%s%s" % (color, string, ends)
        return bold_it

