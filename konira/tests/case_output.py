# coding: konira

from cStringIO import StringIO
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

