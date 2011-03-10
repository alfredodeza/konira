# coding: konira

import os
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


describe "getting tests and paths from arguments":


    before all:
        self.commands = KoniraCommands(argv=[], parse=False, test=True)


    it "returns the path only when it cannot split further":
        path = "/path/to/my/tests"
        from_path = self.commands.test_from_path(path)
        assert from_path.get('path') == path
        assert len(from_path)        == 1


    it "returns a class name if it can split more than once":
        path = "/path/to/my/tests::myclass"
        from_path = self.commands.test_from_path(path)
        assert len(from_path)              == 2
        assert from_path.get('class_name') == 'Case_myclass'
        assert from_path.get('path')       == '/path/to/my/tests'


    it "returns a valid case class name if it can split the path":
        path = "/path/to/my/tests::my separated class"
        from_path = self.commands.test_from_path(path)
        assert len(from_path)              == 2
        assert from_path.get('class_name') == 'Case_my_separated_class'
        assert from_path.get('path')       == '/path/to/my/tests'


    it "returns the path class and method name if it can":
        path = "/path::my class::my method"
        from_path = self.commands.test_from_path(path)
        assert len(from_path)               == 3
        assert from_path.get('class_name')  == 'Case_my_class'
        assert from_path.get('method_name') == 'it_my_method'
        assert from_path.get('path')        == '/path'


    it "always return the path if it fails to split garbage":
        path = "/path$$$"
        from_path = self.commands.test_from_path(path)
        assert len(from_path)        == 1
        assert from_path.get('path') == path



describe "getting parsed paths from arguments":


    before all:
        self.commands = KoniraCommands(argv=[], parse=False, test=True)
        self.cwd = os.getcwd()


    it "returns the current cwd for invalid paths":
        args = ['/usr/bin/executable', '/a/completely/wrong/path']
        path_dict = self.commands.path_from_argument(args)
        assert path_dict.get('path') == self.cwd


     


