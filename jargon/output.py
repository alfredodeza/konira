import traceback
from os.path                import dirname, abspath
from sys                    import stdout, exc_info
from jargon.util            import name_convertion, green, red



def out_green(title):
    string = "\n  - %s" % (green(name_convertion(title)))
    stdout.write(string)



def out_red(title):
    string = "\n  - %s" % (red(name_convertion(title)))
    stdout.write(string)



def out_spec(title):
    stdout.write("\n%s" % name_convertion(title))


def out_footer(cases, failures):
    if not failures:
        string = green("\nAll %s cases passed.\n" % cases)
    elif failures:
        string = red("\n%s cases failed, %s total.\n" % (failures, cases))
    stdout.write(string)



class ExcFormatter(object):


    def __init__(self, failures):
        self.failures = failures
        self.failed_test = 1
        for failure in failures:
            self.single_exception(failure)
        stdout.write('\n\n')


    def single_exception(self, failure):
        exc       = failure.get("failure")
        name      = failure.get("exc_name")
        
        pretty_exc = PrettyExc(exc)
        self.failure_header(pretty_exc.exception_description)
        stdout.write(red("File: ")) 
        stdout.write(pretty_exc.exception_file)
        stdout.write(red("\nLine: "))
        stdout.write(str(pretty_exc.exception_line))


    def failure_header(self, name):
        string = "\n\n%s ==> %s\n" % (self.failed_test, name)
        self.failed_test += 1
        stdout.write(red(string))



class PrettyExc(object):


    def __init__(self, exc_info):
        self.exc_type, self.exc_value, exc_traceback = exc_info
        self.exc_traceback = self._remove_jargon_from_traceback(exc_traceback)
        self.exception_line = self.exc_traceback.tb_lineno
        self.exception_file = self.exc_traceback.tb_frame.f_code.co_filename
        self.exc_info = exc_info


    @property
    def formatted_exception(self):
        traceback_lines = traceback.format_exception(self.exc_type,
                                                     self.exc_value,
                                                     self.exc_traceback)
        return ''.join(traceback_lines)


    def _remove_jargon_from_traceback(self, traceback):
        jargon_dir = dirname(abspath(__file__))
        while True:
            frame    = traceback.tb_frame
            code     = frame.f_code
            filename = code.co_filename
            code_dir = dirname(abspath(filename))
            if code_dir != jargon_dir:
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

    


