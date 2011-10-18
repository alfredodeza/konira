import os
import inspect
from konira        import Runner
from konira.runner import TestEnviron, safe_skip_call


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
        result = safe_skip_call(self._not_raise)
        assert result


    it "returns false when it raises anything but a NoSkip exception":
        result = safe_skip_call(self._raise)
        assert result == False


    it "returns false when it raises a KoniraNoSkip exception":
        result = safe_skip_call(self._skip_raise)
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



describe "get test environ setup values":


    before each:
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


    it "checks for before all properties":
        before_all = self.object()
        before_all._before_all = True
        environ = TestEnviron(before_all)
        assert environ.has_skip_if     == False
        assert environ.has_before_all  == True
        assert environ.has_before_each == False
        assert environ.has_after_all   == False
        assert environ.has_after_each  == False


    it "checks for before each properties":
        before_each = self.object()
        before_each._before_each = True
        environ = TestEnviron(before_each)
        assert environ.has_skip_if     == False
        assert environ.has_before_all  == False
        assert environ.has_before_each == True
        assert environ.has_after_all   == False
        assert environ.has_after_each  == False


    it "checks for after all properties":
        after_all = self.object()
        after_all._after_all = True
        environ = TestEnviron(after_all)
        assert environ.has_skip_if     == False
        assert environ.has_before_all  == False
        assert environ.has_before_each == False
        assert environ.has_after_all   == True
        assert environ.has_after_each  == False


    it "checks for after each properties":
        after_each = self.object()
        after_each._after_each = True
        environ = TestEnviron(after_each)
        assert environ.has_skip_if     == False
        assert environ.has_before_all  == False
        assert environ.has_before_each == False
        assert environ.has_after_all   == False
        assert environ.has_after_each  == True


    it "catches all properties set":
        properties = self.object()
        properties._after_all   = True
        properties._after_each  = True
        properties._before_all  = True
        properties._before_each = True
        properties._skip_if     = True

        environ = TestEnviron(properties)
        assert environ.has_skip_if     == True
        assert environ.has_before_all  == True
        assert environ.has_before_each == True
        assert environ.has_after_all   == True
        assert environ.has_after_each  == True



describe "cached let attributes":

    let is_cached   = True
    let cached_dict = {'value' : False}

    it "correctly sees a cached attribute":
        assert self.is_cached == True


    it "mangles attributes that get reset":
        self.is_cached = False
        assert self.is_cached == False


    it "adds values to a cached dict attr":
        assert self.cached_dict.get('value') == False
        self.cached_dict = {'value': True}
        assert self.cached_dict.get('value') == True


    it "will get reset back to the original dict":
        assert self.cached_dict.get('value') == False
