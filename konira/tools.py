from konira.exc import KoniraReassertError


def raises(cls=Exception, message=None):
    return AssertRaises(cls, message)



class AssertRaises(object):


    def __init__(self, exception_class, message):
        self._exception_class = exception_class
        self.message          = message


    def __enter__(self):
        pass


    def __exit__(self, exc_type, exc_value, traceback):
        success = not exc_type
        if success:
            raise KoniraReassertError(
                'Expected an exception of type %s but got none'
                % self._exception_class.__name__)
        else:
            return self.validate_failure(exc_type, exc_value)


    def validate_failure(self, exc_type, exc_value):
        wrong_message_was_raised = (self.message and
                                    self.message != str(exc_value))
        if wrong_message_was_raised:
            raise KoniraReassertError(
                "Expected %s('%s') but got %s('%s')" %
                 (self._exception_class.__name__,
                  str(self.message),
                  exc_type.__name__,
                  str(exc_value)))
        elif issubclass(exc_type, self._exception_class):
            return True
        else:
            pass

