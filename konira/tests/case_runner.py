# coding: konira

import os
import inspect
from konira import Runner
from konira.runner import TestEnviron


describe "safe test environment calls":

    before all:
        def _raise():
            assert False
        
        def _not_raise():
            assert True
        self._raise     = _raise
        self._not_raise = _not_raise

    before each:
        self.runner = Runner(None, {})


    it "appends an error when an exception happens":
        self.runner.safe_environ_call(self._raise)
        assert len(self.runner.errors)               == 1
        assert self.runner.errors[0].get('exc_name') == 'AssertionError'


    it "does not append errors if the call does not raise":
        self.runner.safe_environ_call(self._not_raise)
        assert len(self.runner.errors) == 0
        assert self.runner.errors      == []


describe "save skip calls":


    before all:
        def _raise():
            assert False
        
        def _not_raise():
            assert True

        def _skip_raise():
            raise KoniraNoSkip

        self._raise      = _raise
        self._not_raise  = _not_raise
        self._skip_raise = _skip_raise


    before each:
        self.runner = Runner(None, {})


    it "returns true when it does not raise":
        result = self.runner.safe_skip_call(self._not_raise)
        assert result


    it "returns false when it raises anything but a NoSkip exception":
        result = self.runner.safe_skip_call(self._raise)
        assert result == False


    it "returns false when it raises a KoniraNoSkip exception":
        result = self.runner.safe_skip_call(self._skip_raise)
        assert result == False


describe "running a spec suite":


    before all:
        self.cwdir    = os.getcwd()
        self.cwfile   = inspect.getfile(inspect.currentframe())


    before each:
        self.runner = Runner(None, {})


    it "appends an error when it raises at class collection":
        self.runner.paths = [self.cwdir]
        self.runner.run()
        assert len(self.runner.errors) == 1
        assert self.runner.errors[0].get('exc_name') == 'IOError'


    it "validates class names with convertion":
        class_name = "'Case_foo'"
        assert self.runner._class_name(class_name) == 'Case_foo'


    it "returns none if a class name does not match":
        class_name = "'CaseBad'"
        assert self.runner._class_name(class_name) == None



describe "get test environ setup values":


    before all:
        class Object(object):
            pass
        self.object = Object


    it "does not have any environ attribute":
        environ = TestEnviron(self.object)
        assert environ.has_skip_if     == False
        assert environ.has_before_all  == False
        assert environ.has_before_each == False
        assert environ.has_after_all   == False
        assert environ.has_after_each  == False


    it "checks for skip if properties":
        skip_if          = self.object()
        skip_if._skip_if = True
        environ          = TestEnviron(skip_if)
        assert environ.has_skip_if     == True
        assert environ.has_before_all  == False
        assert environ.has_before_each == False
        assert environ.has_after_all   == False
        assert environ.has_after_each  == False


