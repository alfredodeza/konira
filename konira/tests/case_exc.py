# coding: konira

import inspect
from konira.exc         import (KoniraIOError, KoniraExecutionError, KoniraNoSkip, 
                                KoniraReassertError, KoniraFirstFail)
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


    it "raises a konira no skip exception":
        exc_err = exc.KoniraNoSkip
        raises KoniraNoSkip: raise exc_err



describe "konira reassert error exception":


    it "raises a reassert error exception":
        exc_err = exc.KoniraReassertError
        raises KoniraReassertError: raise exc_err



describe "konira first fail exception":


    it "raises a first fail exception":
        exc_err = exc.KoniraFirstFail
        raises KoniraFirstFail: raise exc_err



describe "konira IO Error exception":


    it "raises TypeError when arguments are not enough":
        exc_err = exc.KoniraIOError
        raises TypeError: raise exc_err

    it "raises a konira IO Error":
        exc_err = exc.KoniraIOError
        raises KoniraIOError: raise exc_err("an exception message")
    


describe "Source operands and values from frame objects":

    before all:
        try:
            assert 1 == 2
        except:
            self.eq_trace = inspect.trace()[0]
        try:
            assert 1 >= 2
        except:
            self.mte_trace = inspect.trace()[0]
        try:
            assert 2 <= 1
        except:
            self.lte_trace = inspect.trace()[0]
        try:
            assert 'foo' != 'foo'
        except:
            self.ne_trace = inspect.trace()[0]
        try:
            assert 'foo' is 'Foo'
        except:
            self.is_trace = inspect.trace()[0]
        try:
            assert 1 > 2
        except:
            self.mt_trace = inspect.trace()[0]
        try:
            assert 2 < 1
        except:
            self.lt_trace = inspect.trace()[0]
        try:
            assert 'foo' not in 'a foo here'
        except:
            self.notin_trace = inspect.trace()[0]
        try:
            assert False
        except:
            self.false_trace = inspect.trace()[0]

    before each:
        self.source = exc.Source


    it "returns invalid when it cannot match correctly":
        validate = self.source(self.false_trace)
        assert validate.is_valid == False


    it "can return the actual assert line stripping out assert":
        source = self.source(self.false_trace)
        assert source.line == 'False'


    it "catches equality operand":
        source = self.source(self.eq_trace)
        assert source.operand == '=='


    it "catches not equal operand":
        source = self.source(self.ne_trace)
        assert source.operand == '!='


    it "catches more than operand":
        source = self.source(self.mt_trace)
        assert source.operand == '>'


    it "catches less than operand":
        source = self.source(self.lt_trace)
        assert source.operand == '<'


    it "catches more than or equal operand":
        source = self.source(self.mte_trace)
        assert source.operand == '>='


    it "catches less than or equal operand":
        source = self.source(self.lte_trace)
        assert source.operand == '<='


    it "catches the is keyword operand":
        source = self.source(self.is_trace)
        assert source.operand == ' is '


    it "catches the not int keyword operand":
        source = self.source(self.notin_trace)
        assert source.operand == ' not in '


    it "parses and evalueates left values and text values with an equality operand":
        source = self.source(self.eq_trace)
        assert source._left_text == '1'
        assert source.left_value == 1


    it "parses and evaluates right values and text values with an equality operand":
        source = self.source(self.eq_trace)
        assert source._right_text == '2'
        assert source.right_value == 2


    it "parses and evaluates right values and text values with a not equal operand":
        source = self.source(self.ne_trace)
        assert type(source._right_text) == str
        assert source.right_value       == 'foo'


    it "parses and evaluates left values and text values with a not equal operand":
        source = self.source(self.ne_trace)
        assert type(source._left_text) == str
        assert source.left_value       == 'foo'

    
    it "parses and evals right values and text values with an is operand":
        source = self.source(self.is_trace)
        assert type(source._right_text) == str
        assert source.right_value       == 'Foo'

    
    it "parses and evals left values and text values with an is operand":
        source = self.source(self.is_trace)
        assert type(source._left_text) == str
        assert source.left_value       == 'foo'


    it "parses and evals right values and text values with a less than operand":
        source = self.source(self.lt_trace)
        assert source._right_text == '1'
        assert source.right_value == 1


    it "parses and evals left values and text values with a less than operand":
        source = self.source(self.lt_trace)
        assert source._left_text == '2'
        assert source.left_value == 2


    it "parses and evals left and text values from a not in operand":
        source = self.source(self.notin_trace)
        assert type(source._left_text) == str
        assert source.left_value       == 'foo'


    it "parses and evals right and text values from a not in operand":
        source = self.source(self.notin_trace)
        assert type(source._right_text) == str
        assert source.right_value       == 'a foo here'


    it "parses and evals a single assert statement":
        source = self.source(self.false_trace)
        assert source._left_text == 'False'
        assert source.left_value == False


    it "raises index error when doing eval of a right value of a single assert":
        source = self.source(self.false_trace)
        raises IndexError: source.right_value
