# coding: jargon

from jargon.collector import FileCollector


describe "collect paths":

    it "should be a list":
        f = FileCollector(path='/asdf')
        assert isinstance(f, list)
