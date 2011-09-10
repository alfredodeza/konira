import inspect
import sys
import konira

from konira.util import StringIO
from konira.util import return_exception_trace
from konira    import output


describe "writer and ansi codes":


    before each:
        self.stdout = StringIO()
        self.writer = output.Writer(stdout=self.stdout)

    it "knows if it is atty or not":
        assert self.writer.isatty == False


    it "returns empty strings for colors if it is not atty":
        self.writer.isatty = False
        assert self.writer.color("") == ''


    it "returns empty strings for colors when for is None":
        self.writer.isatty = False
        assert self.writer.color(None) == ''


    it "raises a keyerror when you try to get an invalid color":
        self.writer.isatty = True
        raises KeyError: self.writer.color('foo')


    it "returns blue ansi codes":
        self.writer.isatty = True
        assert self.writer.color('blue') == '\033[94m'
        

    it "returns green ansi codes":
        self.writer.isatty = True
        assert self.writer.color('green') == '\033[92m'


    it "returns yellow ansi codes":
        self.writer.isatty = True
        assert self.writer.color('yellow') == '\033[93m'


    it "returns red ansi codes":
        self.writer.isatty = True
        assert self.writer.color('red') == '\033[91m'


    it "returns bold ansi codes":
        self.writer.isatty = True
        assert self.writer.color('bold') == '\033[1m'


    it "returns ends ansi codes":
        self.writer.isatty = True
        assert self.writer.color('ends') == '\033[0m'



describe "writer stdout ouput":


    before each:
        self.stdout = StringIO()
        self.writer = output.Writer(stdout=self.stdout)


    it "println to stdout the string correctly without colors":
        self.writer.println("a string with no colors")
        assert self.stdout.getvalue() == "a string with no colors"


    it "writes to stdout without newlines but with colors":
        self.writer.isatty = True
        self.writer.write("A blue string", "blue")
        assert self.stdout.getvalue() == '\033[94mA blue string\033[0m'


    it "writes to stdout without newlines with no colors if not atty":
        self.writer.write("A blue string", "blue")
        assert self.stdout.getvalue() == 'A blue string'


    it "writelns with newline and colors":
        self.writer.isatty = True
        self.writer.writeln("A blue string", "blue")
        assert self.stdout.getvalue() == '\n\033[94mA blue string\033[0m'


    it "writelns with newline and no colors":
        self.writer.writeln("A blue string", "blue")
        assert self.stdout.getvalue() == '\nA blue string'


    it "writes n number of newlines":
        self.writer.newline(lines=3)
        assert self.stdout.getvalue() == '\n\n\n'


    it "writes a single newline by default":
        self.writer.newline()
        assert self.stdout.getvalue() == '\n'


    it "returns valid green strings on demand":
        self.writer.isatty = True
        assert self.writer.green("A green string") == '\033[92mA green string\033[0m'


    it "returns valid red strings on demand":
        self.writer.isatty = True
        assert self.writer.red("A red string") == '\033[91mA red string\033[0m' 


    it "returns valid bold strings on demand":
        self.writer.isatty = True
        assert self.writer.bold("A bold string") == '\033[1mA bold string\033[0m' 



describe "terminal writer stdout ouput":


    before each:
        self.stdout         = StringIO()
        self.writer         = output.Writer(stdout=self.stdout)
        self.twriter        = output.TerminalWriter(False)
        self.twriter.writer = self.writer

    after each:
        self.stdout = StringIO()
        
    it "outputs green spec titles":
        self.twriter.green_spec("green spec title")
        assert self.stdout.getvalue() == "\n    Green spec title"


    it "outputs a dot for green specs when dotted option is passed":
        self.twriter.dotted = True
        self.twriter.green_spec("green spec title")
        assert self.stdout.getvalue() == '.'


    it "outputs red spec titles":
        self.twriter.red_spec("red spec title")
        assert self.stdout.getvalue() == "\n    Red spec title"


    it "outputs an eff for red specs when dotted option is passed":
        self.twriter.dotted = True
        self.twriter.red_spec("red spec title")
        assert self.stdout.getvalue() == 'F'


    it "is None when dotted for out case":
        self.twriter.dotted = True
        assert self.twriter.out_case("an out case") == None
        assert self.stdout.getvalue() == ''


    it "outputs an out case when not dotted":
        assert self.twriter.dotted ==  False
        self.twriter.out_case("an out case") 
        assert self.stdout.getvalue() == '\n\nAn out case'



describe "footer output":


    before each:
        self.stdout = StringIO()
        self.writer = output.Writer(stdout=self.stdout)
        self.footer = output.out_footer


    it "outputs all passed when no failures and cases are more than zero":
        self.footer(1, 0, 0, std=self.writer)
        assert self.stdout.getvalue() == "\n\n\nAll 1 spec passed in 0 secs.\n"


    it "outputs plural specs when no failures and cases are more than zero":
        self.footer(2, 0, 0, std=self.writer)
        assert self.stdout.getvalue() == "\n\n\nAll 2 specs passed in 0 secs.\n"


    it "outputs failures as singular":
        self.footer(1, 1, 0, std=self.writer)
        assert self.stdout.getvalue() == "\n\n\n1 spec failed, 1 total in 0 secs.\n"



describe "report results":


    before all:
        self.false_failure = return_exception_trace()
        #try:
        #    assert False
        #except Exception as e:
        #    trace = inspect.trace()
        #    self.false_failure = dict(
        #                    failure  = sys.exc_info(),
        #                    trace    = trace,
        #                    exc_name = e.__class__.__name__
        #                   ) 
        #    #self.false_trace = inspect.trace()[0]


    before each:
        class FakeObject(object): pass
        self.stdout         = StringIO()
        self.writer         = output.Writer(stdout=self.stdout)
        self.results        = FakeObject()
        self.results.config = {}
        self.reporter       = output.ReportResults


    it "writes a nice footer":
        self.results.total_cases    = 1
        self.results.total_failures = 1
        self.results.elapsed        = 0
        result = self.reporter(self.results, self.writer)
        result.footer()
        assert self.stdout.getvalue() == "\n\n\n1 spec failed, 1 total in 0 secs.\n"


    it "when sorting it returns only ten items":
        profiles = [(a, a, a) for a in range(0,15)]
        self.results.profiles = profiles 
        result = self.reporter(self.results, self.writer)
        assert len(result._sort_profiles()) == 10
        

    it "when sorting it does so in descending order":
        profiles = [(a, a, a) for a in range(0,15)]
        self.results.profiles = profiles 
        result = self.reporter(self.results, self.writer)
        assert result._sort_profiles()[0] == (14,14,14)
        assert result._sort_profiles()[1] == (13,13,13)
        assert result._sort_profiles()[2] == (12,12,12)


    it "outputs normalized test case names in the profiler":
        profiles = [(a, 'test_case', a) for a in range(0,15)]
        self.results.profiles = profiles 
        result = self.reporter(self.results, self.writer)
        result.profiler()
        assert "14 - Test case" in self.stdout.getvalue()


    it "displays a header showgin profiling is enabled":
        profiles = [(a, 'test_case', a) for a in range(0,15)]
        self.results.profiles = profiles 
        result = self.reporter(self.results, self.writer)
        result.profiler()
        expected = "Profiling enabled\n10 slowest tests shown:\n" 
        assert expected in self.stdout.getvalue()


    it "orders single profile messages by time and case name":
        result = self.reporter(self.results, self.writer)
        result._output_profiles((0, 'test_case'))
        assert self.stdout.getvalue() == '\n0 - Test case'


    it "only gices the 10 first digits in elapsed time":
        result = self.reporter(self.results, self.writer)
        result._output_profiles(('0.00000099999', 'test_case'))
        assert self.stdout.getvalue() == '\n0.00000099 - Test case'


    it "can report profiling errors and failures all at once":
        self.results.total_cases    = 1
        self.results.total_failures = 1
        self.results.elapsed        = 0
        self.results.failures = [self.false_failure]
        self.results.errors = [self.false_failure]
        self.results.profiles = [('0', 'Test_case')]
        result = self.reporter(self.results, self.writer)
        result.report()
        output = self.stdout.getvalue()
        assert 'AssertionError'  in output
        assert 'Failures'        in output
        assert 'Starts and Ends' in output
        assert 'File:'           in output
        assert 'util.py'         in output
        assert '1 spec failed, 1 total in 0 secs.' in output




