# coding: konira

from konira.exc         import KoniraIOError, KoniraExecutionError
from konira             import exc


describe "dont read from input":

    before each:
        self.dont_read = exc.DontReadFromInput()

    it "asks if you are using pdb":
        message = "reading from stdin while output is captured (using pdb?)"
        assert self.dont_read.msg == message

    it "throws an exception if you call flush":
        raises KoniraIOError: self.dont_read.flush()

    it "throws an exception if you call flush with any arguments":
        raises KoniraIOError: self.dont_read.flush(True, False)

    it "throws an exception if you call write":
        raises KoniraIOError: self.dont_read.write()

    it "throws an exception if you call write with any arguments":
        raises KoniraIOError: self.dont_read.write(True, False)

    it "throws an exception if you call read":
        raises KoniraIOError: self.dont_read.read()

    it "throws an exception if you call read with any arguments":
        raises KoniraIOError: self.dont_read.read(True, False)

    it "raises when you call readline, readlines or iter":
        raises KoniraIOError: self.dont_read.__iter__()
        raises KoniraIOError: self.dont_read.readline()
        raises KoniraIOError: self.dont_read.readlines()


describe "konira execution error":

    before all:
        self.exc_err = exc.KoniraExecutionError 

    
    it "raises when there are insufficient args":
        raises TypeError: self.exc_err()

    it "raises a konira execution error":
        args = ('exc_name', 'filename', 1, 'a message', 'exc')
        exc = self.exc_err('a', 'b', 'c', 'd', 'e')
        raises KoniraExecutionError: raise exc

