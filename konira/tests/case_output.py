# coding: konira

from cStringIO import StringIO
from konira    import output


describe "writer and ansi codes":


    before each:
        self.stdout = StringIO()

    it "knows if it is atty or not":
        writer = output.Writer(stdout=self.stdout)
        assert writer.isatty == False


    it "returns empty strings for colors if it is not atty":
        writer = output.Writer(stdout=self.stdout)
        writer.isatty = False
        assert writer.color("") == ''

    it "returns empty strings for colors when for is None":
        writer = output.Writer(stdout=self.stdout)
        writer.isatty = False
        assert writer.color(None) == ''



