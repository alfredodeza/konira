# coding: konira

from konira import Runner


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


