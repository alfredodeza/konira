import konira
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
    


describe "Source False value and assertions":

    before all:
        try:
            assert False
        except:
            self.false_trace = inspect.trace()[0]

    before each:
        self.source = exc.Source(self.false_trace)


    it "returns invalid when it cannot match correctly":
        assert self.source.is_valid == False


    it "can return the actual assert line stripping out assert":
        assert self.source.line == 'False'


    it "parses and evals a single assert statement":
        assert self.source._left_text == 'False'
        assert self.source.left_value == False


    it "raises index error when doing eval of a right value of a single assert":
        raises IndexError: self.source.right_value


    it "is able to get the actual source line":
        assert self.source.line == 'False'


    it "should not be valid because there is no operand":
        assert self.source.is_valid == False


describe "Source equality assertions and values":

    before all:
        try:
            assert 1 == 2
        except:
            self.eq_trace = inspect.trace()[0]

    before each:
        self.source = exc.Source(self.eq_trace)


    it "catches equality operand":
        assert self.source.operand == '=='


    it "parses and evalueates left values and text values with an equality operand":
        assert self.source._left_text == '1'
        assert self.source.left_value == 1


    it "parses and evaluates right values and text values with an equality operand":
        assert self.source._right_text == '2'
        assert self.source.right_value == 2


    it "is able to get the actual source line":
        assert self.source.line ==  '1 == 2'



describe "Source more than or equal assertions and values":


    before all:
        try:
            assert 1 >= 2
        except:
            self.mte_trace = inspect.trace()[0]


    before each:
        self.source = exc.Source(self.mte_trace)


    it "catches more than or equal operand":
        assert self.source.operand == '>='


    it "parses and evalueates left values and text values with an equality operand":
        assert self.source._left_text == '1'
        assert self.source.left_value == 1


    it "parses and evaluates right values and text values with an equality operand":
        assert self.source._right_text == '2'
        assert self.source.right_value == 2


    it "is able to get the actual source line":
        assert self.source.line == '1 >= 2'



describe "Source less than or equal assertions and values":


    before all:
        try:
            assert 2 <= 1
        except:
            self.lte_trace = inspect.trace()[0]


    before each:
        self.source = exc.Source(self.lte_trace)


    it "catches less than or equal operand":
        assert self.source.operand == '<='


    it "parses and evalueates left values and text values with an equality operand":
        assert self.source._left_text == '2'
        assert self.source.left_value == 2


    it "parses and evaluates right values and text values with an equality operand":
        assert self.source._right_text == '1'
        assert self.source.right_value == 1
     

    it "is able to get the actual source line":
        assert self.source.line == '2 <= 1'



describe "Source not equal assertions and values":


    before all:
        try:
            assert 'foo' != 'foo'
        except:
            self.ne_trace = inspect.trace()[0]


    before each:
        self.source = exc.Source(self.ne_trace)
        
        
    it "catches not equal operand":
        assert self.source.operand == '!='


    it "parses and evaluates right values and text values with a not equal operand":
        assert type(self.source._right_text) == str
        assert self.source.right_value       == 'foo'


    it "parses and evaluates left values and text values with a not equal operand":
        assert type(self.source._left_text) == str
        assert self.source.left_value       == 'foo'


    it "is able to get the actual source line":
        assert self.source.line == """'foo' != 'foo'"""

    

describe "Source is assertions and values":


    before all:
        try:
            assert 'foo' is 'Foo'
        except:
            self.is_trace = inspect.trace()[0]


    before each:
        self.source = exc.Source(self.is_trace)


    it "catches the is keyword operand":
        assert self.source.operand == ' is '


    it "parses and evals right values and text values with an is operand":
        assert type(self.source._right_text) == str
        assert self.source.right_value       == 'Foo'

    
    it "parses and evals left values and text values with an is operand":
        assert type(self.source._left_text) == str
        assert self.source.left_value       == 'foo'


    it "is able to get the actual source line":
        assert self.source.line == """'foo' is 'Foo'"""



describe "Source more than assertions and values":


    before all:
        try:
            assert 1 > 2
        except:
            self.mt_trace = inspect.trace()[0]

    before each:
        self.source = exc.Source(self.mt_trace)


    it "catches more than operand":
        assert self.source.operand == '>'


    it "parses and evaluates left values and text values with an equality operand":
        assert self.source._left_text == '1'
        assert self.source.left_value == 1


    it "parses and evaluates right values and text values with an equality operand":
        assert self.source._right_text == '2'
        assert self.source.right_value == 2


    it "is able to get the actual source line":
        assert self.source.line == '1 > 2'
    


describe "Source less than assertions and values":


    before all:
        try:
            assert 2 < 1
        except:
            self.lt_trace = inspect.trace()[0]


    before each:
        self.source = exc.Source(self.lt_trace)


    it "catches less than operand":
        assert self.source.operand == '<'


    it "parses and evals right values and text values with a less than operand":
        assert self.source._right_text == '1'
        assert self.source.right_value == 1


    it "parses and evals left values and text values with a less than operand":
        assert self.source._left_text == '2'
        assert self.source.left_value == 2


    it "is able to get the actual source line":
        assert self.source.line == '2 < 1'



describe "Source not in values and assertions":


    before all:
        try:
            assert 'foo' not in 'a foo here'
        except:
            self.notin_trace = inspect.trace()[0]


    before each:
        self.source = exc.Source(self.notin_trace)


    it "catches the not int keyword operand":
        assert self.source.operand == ' not in '


    it "parses and evals left and text values from a not in operand":
        assert type(self.source._left_text) == str
        assert self.source.left_value       == 'foo'


    it "parses and evals right and text values from a not in operand":
        assert type(self.source._right_text) == str
        assert self.source.right_value       == 'a foo here'


    it "is able to get the actual source line":
        assert self.source.line == """'foo' not in 'a foo here'"""



describe "konira assert helper function":


    before all:
        try:
            assert False
        except:
            self.trace = inspect.trace()[0]

        try:
            assert "long string" == "Long string"
        except:
            self.bad_trace = inspect.trace()[0]

        try:
            assert ('a',1) == ('b',1)
        except:
            self.tpl_trace = inspect.trace()[0]

        try:
            assert {'a':1} == {'b':1}
        except:
            self.dict_trace = inspect.trace()[0]


    it "is None when the source is invalid":
        reassert = exc.konira_assert(self.trace)
        assert reassert == None


    it "returns a valid diff when comparing strings":
        reassert = exc.konira_assert(self.bad_trace)
        description = ['long string == Long string', '- long string', '? ^', '+ Long string', '? ^']
        assert reassert == description
        
        
    it "returns valid dictionary comparisons":
        reassert = exc.konira_assert(self.dict_trace)
        description = ["{'a': 1} == {'b': 1}", "- {'a': 1}", '?   ^', "+ {'b': 1}", '?   ^']
        assert reassert == description


    it "returns tuple comparisons":
        reassert = exc.konira_assert(self.tpl_trace)
        description = ["('a', 1) == ('b', 1)", "At index 0 diff: 'a' != 'b'", "- ('a', 1)", '?   ^', "+ ('b', 1)", '?   ^']
        assert reassert == description



describe "Assert repr from source lines":


    it "returns None when it does not have an equality operand":
        _repr = exc.assertrepr_compare('==', None, '')
        assert _repr == None
