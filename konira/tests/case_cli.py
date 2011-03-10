# coding: konira

import sys
from cStringIO import StringIO
from konira    import KoniraCommands



describe "stdout messages for the command line":


    before all:
        self.commands = KoniraCommands(argv=[], parse=False, test=True)


    before each:
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stderr = self.mystderr = StringIO()
        sys.stdout = self.mystdout = StringIO()


    after each:
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    
    it "should go to stdout if a flag is passed in":
        self.commands.msg("A stdout message")
        assert self.mystdout.getvalue() == "A stdout message"


    it "does not output stderr messages when stdout flaf is set":
        self.commands.msg("A stdout message")
        assert self.mystderr.getvalue() == ""


    it "outputs to stderr if a flag is passed in":
        self.commands.msg("A stderr message", stdout=False)
        assert self.mystderr.getvalue() == "A stderr message"


    it "does not output to stdout if the stderr flag is set":
        self.commands.msg("A stderr message", stdout=False)
        assert self.mystdout.getvalue() == ""



describe "getting parsed paths":


    before all:
        self.commands = KoniraCommands(argv=[], parse=False, test=True)




