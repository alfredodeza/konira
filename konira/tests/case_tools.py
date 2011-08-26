import konira
from konira.exc import KoniraReassertError
from konira     import tools


describe "raises tool":

    before each:
        self.r = tools.raises

    it "is True when the exception matches":
        with self.r(): raise



describe "assert raises":

    it "raises when the exception does not match":
        assert_raises = tools.AssertRaises(Exception, None)
        raises KoniraReassertError: assert_raises.__exit__(None, None, None)


    it "is true when the exception matches":
        assert_raises = tools.AssertRaises(Exception, None)
        assert assert_raises.__exit__(Exception, None, None)


    it "raises when the exception message does not match":
        assert_raises = tools.AssertRaises(Exception, "foo")
        raises KoniraReassertError: assert_raises.__exit__(Exception, None, None)


