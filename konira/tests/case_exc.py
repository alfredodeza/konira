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



describe "konira execution error exception":


    before all:
        self.exc_err = exc.KoniraExecutionError 

    
    it "is an Exception type":
        type(self.exc_err) == Exception
    

    it "raises when there are insufficient args":
        raises TypeError: self.exc_err()


    it "raises a konira execution error":
        args = ('exc_name', 'filename', 1, 'a message', 'exc')
        exc = self.exc_err('a', 'b', 'c', 'd', 'e')
        raises KoniraExecutionError: raise exc



describe "konira no skip exception":


    it "is an Exception type":
        exc_err = exc.KoniraNoSkip
        type(exc_err) == Exception



describe "konira reassert error exception":


    it "is an Exception type":
        exc_err = exc.KoniraReassertError
        type(exc_err) == Exception



describe "konira first fail exception":


    it "is an Exception type":
        exc_err = exc.KoniraFirstFail
        type(exc_err) == Exception



describe "konira IO Error exception":


    it "is an Exception type":
        exc_err = exc.KoniraIOError
        type(exc_err) == Exception
    


describe "Source from frame objects":


    before all:
        self.invalid_trace = [[["this is", ["an invalid"], "an invalid trace"]

    before each:
        self.source = exc.Source


    it "returns invalid when it cannot match correctly":

        validate = self.source(self.invalid_trace)
        assert validate.is_valid == False
