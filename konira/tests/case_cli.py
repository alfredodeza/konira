import os
import sys
from konira.util import StringIO
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
        assert self.mystdout.getvalue() == "A stdout message\n"


    it "does not output stderr messages when stdout flaf is set":
        self.commands.msg("A stdout message")
        assert self.mystderr.getvalue() == ""


    it "outputs to stderr if a flag is passed in":
        self.commands.msg("A stderr message", stdout=False)
        assert self.mystderr.getvalue() == "A stderr message\n"


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


    it "returns the current only the cwd for invalid paths":
        args = ['/bin/konira', '/a/completely/wrong/path']
        path_dict = self.commands.path_from_argument(args)
        assert len(path_dict)        == 1
        assert path_dict.get('path') == self.cwd


    it "if it is a valid path then return a dict with other options":
        args = ['/bin/konira', '/tmp']
        path_dict = self.commands.path_from_argument(args)
        assert len(path_dict)               == 3
        assert path_dict.get('class_name')  == None
        assert path_dict.get('method_name') == None
        assert path_dict.get('path')        == '/tmp'


    it "returns classes with paths if it is valid":
        args = ['/bin/konira', '/tmp::my class']
        path_dict = self.commands.path_from_argument(args)
        assert len(path_dict)               == 3
        assert path_dict.get('class_name')  == 'Case_my_class'
        assert path_dict.get('method_name') == None
        assert path_dict.get('path')        == '/tmp'

        
    it "returns classes and method when valid paths are passed":
        args = ['/bin/konira', '/tmp::my class:: my method']
        path_dict = self.commands.path_from_argument(args)
        assert len(path_dict)               == 3
        assert path_dict.get('class_name')  == 'Case_my_class'
        assert path_dict.get('method_name') == 'it_my_method'
        assert path_dict.get('path')        == '/tmp'


    it "returns the cwd if no paths are sent":
        args = ['/bin/konira']
        path_dict = self.commands.path_from_argument(args)
        assert len(path_dict)        == 1
        assert path_dict.get('path') == self.cwd
