# coding: konira

from konira.collector import FileCollector


class Foo(object):
    bar = True
f
class Bar(Exception):
    def __init__(self, msg=''):
        Exception.__init__(self, msg)

describe "collect paths" Foo:


    before each:
        self.f = FileCollector(path='/asdf')
    
#    it "compares tuples":
#        assert ('a tuple') == ('a tuplE')

#    it "can compare dicts":
#        assert {'a':1} == {'a':2}

    it "should see config":
        assert konira.util

    it "should see konira as imported":
        assert konira

    it "should be able to verify a raise":
        raises AttributeError: Bar()

    it "should see bar":
        assert self.bar


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
