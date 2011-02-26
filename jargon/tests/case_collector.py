# coding: jargon

from jargon.collector import FileCollector


describe "collect paths":

    it "should be a list":
        f = FileCollector(path='/asdf')
        assert isinstance(f, list)


    it "does not match normal python files":
        f = FileCollector(path='/asdf')
        py_file = "foo.py"
        assert f.valid_module_name.match(py_file) == None
