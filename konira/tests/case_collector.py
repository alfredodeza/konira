import os
import konira
from konira.util      import StringIO
from konira.collector import FileCollector, globals_from_file
from util             import Foo


describe "path collection":


    before each:
        self.f = FileCollector(path='/asdf')


    it "should be a list":
        assert isinstance(self.f, list)


    it "does not match normal python files":
        py_file = "foo.py"
        assert self.f.valid_module_name.match(py_file) == None


    it "matches upper case python cases":
        py_file = "CASE_foo.py"
        assert self.f.valid_module_name.match(py_file)


    it "does not match case without underscores":
        py_file = "casfoo.py"
        assert self.f.valid_module_name.match(py_file) == None


    it "does not match if it doesn't start with case_":
        py_file = "foo_case.py"
        assert self.f.valid_module_name.match(py_file) == None


    it "matches if it has camelcase":
        py_file = "CaSe_foo.py"
        assert self.f.valid_module_name.match(py_file)


    it "does not match if it starts with underscore":
        py_file = "case_foo.py"
        assert self.f.valid_module_name.match(py_file)


    it "raises SystemExit if it user match is borked":
        raises SystemExit: FileCollector(path='/tmp', config={'collect-match':'*.py'})


    it "if user_match and case_insensitive IGNORECASE is used":
        config = {'collect-match': 'bar', 'collect-ci': True}
        collector = FileCollector(path='/asdf', config=config)

        assert collector.valid_module_name.match('BaR')


    it "if user_match and not case_insensitive no IGNORECASE is used":
        config = {'collect-match': 'bar'}
        collector = FileCollector(path='/asdf', config=config)

        assert collector.valid_module_name.match('BaR') == None



describe 'global values from file':


    before each:
        with open('/tmp/case_test.py', 'w') as self.case_test:
            self.case_test.write("import sys")


    after each:
        try:
            os.remove('/tmp/case_test.py')
        except:
            pass # who cares if you can't


    it 'should see globals':
        globs = globals_from_file('/tmp/case_test.py')
        assert globs
        assert len(globs) == 2


    it "raises IOError when it tries an invalid path":
        raises IOError: globals_from_file('/foo/bar/foo.py')


    it "raises TypeError when no filename is passed":
        raises TypeError: globals_from_file()

    it "is able to import from relative or same level modules":
        subject = Foo()
        assert subject.bar() is True
