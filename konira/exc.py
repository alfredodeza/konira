import inspect
import difflib



class DontReadFromInput(object):
    """Temporary stub class.  Ideally when stdin is accessed, the
    capturing should be turned off, with possibly all data captured
    so far sent to the screen.  This should be configurable, though,
    because in automated test runs it is better to crash than
    hang indefinitely.
    """
    msg = "reading from stdin while output is captured (using pdb?)"


    def flush(self, *args):
        raise KoniraIOError(self.msg)


    def write(self, *args):
        raise KoniraIOError(self.msg)


    def read(self, *args):
        raise KoniraIOError(self.msg)


    readline  = read
    readlines = read
    __iter__  = read



class KoniraExecutionError(Exception):


    def __init__(self, exc_name, filename, lineno, msg, exc):
        self.exc_name = exc_name
        self.msg      = msg
        self.filename = filename
        self.lineno   = lineno
        self.exc      = exc
        Exception.__init__(self, msg)



class KoniraNoSkip(Exception):


    def __init__(self, msg=''):
        Exception.__init__(self, msg)



class KoniraReassertError(Exception):


    def __init__(self, msg=''):
        Exception.__init__(self, msg)



class KoniraFirstFail(Exception):


    def __init__(self, msg=''):
        Exception.__init__(self, msg)



class KoniraIOError(Exception):


    def __init__(self, msg):
        Exception.__init__(self, msg)



class Source(object):


    def __init__(self, trace):
        self.trace    = trace
        self.line     = self.get_assert_line
        self.operand  = self.get_operand
        self.is_valid = True
        self._locals  = self.get_locals
        if not self.line or not self.operand:
            self.is_valid = False


    @property
    def get_locals(self):
        frame = self.trace[0]
        return inspect.getargvalues(frame).locals


    @property
    def get_assert_line(self):
        line = self.trace[-2][0]
        if 'assert' in line:
            return line.replace('assert', '').strip()
        return False


    @property
    def get_operand(self):
        operators = ['==', '!=', '>', '<', 
                     '>=', '<=', ' is ', ' not in ']
        operator = [i for i in operators if i in self.line]
        if len(operator) > 1: # probably <, >, mixed with <= >= operators 
            return operator[-1]
        if operator:
            return operator[0]


    @property
    def _left_text(self):
        operator = self.operand
        return self.line.split(operator)[0].strip()


    @property
    def _right_text(self):
        operator = self.operand
        return self.line.split(operator)[1].strip()


    @property
    def right_value(self):
        right = self._locals.get(self._right_text)
        if right:
            return right
        return self._eval(self._right_text)


    @property
    def left_value(self):
        left = self._locals.get(self._left_text)
        if left:
            return left
        return self._eval(self._left_text)


    def _eval(self, code):
        return eval(code, None, self._locals)



def konira_assert(trace):
    source  = Source(trace)
    if source.is_valid:
        try:
            left     = source.left_value
            right    = source.right_value
            operand  = source.operand
            line     = source.line
        except NameError:
            return None

        # At this point we have tried everything we can to
        # get a valid comparison so return to basic Assertion
        # to avoid a huge traceback
        except Exception:
            return None

        try:
            reassert = assertrepr_compare(operand, left, right)
        except KoniraReassertError:
            return None

        if reassert:
            return reassert
        return assert_description(operand, left, right, line)



def assert_description(op, left, right, line):
    explanation = [line]
    explanation.append('%s %s %s' % (left, op, right))
    return explanation

    

def assertrepr_compare(op, left, right):
    """return specialised explanations for some operators/operands"""
    width      = 80 - 15 - len(op) - 2 # 15 chars indentation, 1 space around op
    left_repr  = left
    right_repr = right
    summary    = '%s %s %s' % (left_repr, op, right_repr)

    issequence = lambda x: isinstance(x, (list, tuple))
    istext     = lambda x: isinstance(x, basestring)
    isdict     = lambda x: isinstance(x, dict)
    isset      = lambda x: isinstance(x, set)

    explanation = None
    try:
        if op == '==':
            if istext(left) and istext(right):
                explanation = _diff_text(left, right)
            elif issequence(left) and issequence(right):
                explanation = _compare_eq_sequence(left, right)
            elif isset(left) and isset(right):
                explanation = _compare_eq_set(left, right)
            elif isdict(left) and isdict(right):
                explanation = _diff_text(str(left), str(right))
        elif op == ' not in ':
            if istext(left) and istext(right):
                explanation = _notin_text(left, right)
    except Exception, e:
        raise KoniraReassertError(e)

    if not explanation:
        return None

    # Don't include pageloads of data, should be configurable
    if len(''.join(explanation)) > 80*8:
        explanation = ['Detailed information too verbose, truncated']

    return [summary] + explanation


def _diff_text(left, right):
    """Return the explanation for the diff between text

    This will skip leading and trailing characters which are
    identical to keep the diff minimal.
    """
    explanation = []
    i = 0 # just in case left or right has zero length
    for i in range(min(len(left), len(right))):
        if left[i] != right[i]:
            break
    if i > 42:
        i -= 10                 # Provide some context
        explanation = ['Skipping %s identical '
                       'leading characters in diff' % i]
        left  = left[i:]
        right = right[i:]
    if len(left) == len(right):
        for i in range(len(left)):
            if left[-i] != right[-i]:
                break
        if i > 42:
            i -= 10     # Provide some context
            explanation += ['Skipping %s identical '
                            'trailing characters in diff' % i]
            left  = left[:-i]
            right = right[:-i]
    explanation += [line.strip('\n')
                    for line in difflib.ndiff(left.splitlines(),
                                                     right.splitlines())]
    return explanation


def _compare_eq_sequence(left, right):
    explanation = []
    for i in range(min(len(left), len(right))):
        if left[i] != right[i]:
            explanation += ['At index %s diff: %r != %r' %
                            (i, left[i], right[i])]
            break
    if len(left) > len(right):
        explanation += ['Left contains more items, '
            'first extra item: %s' % (left[len(right)],)]
    elif len(left) < len(right):
        explanation += ['Right contains more items, '
            'first extra item: %s' % (right[len(left)],)]
    return explanation # + _diff_text(py.std.pprint.pformat(left),
                       #             py.std.pprint.pformat(right))


def _compare_eq_set(left, right):
    explanation = []
    diff_left   = left - right
    diff_right  = right - left
    if diff_left:
        explanation.append('Extra items in the left set:')
        for item in diff_left:
            explanation.append(repr(item))
    if diff_right:
        explanation.append('Extra items in the right set:')
        for item in diff_right:
            explanation.append(repr(item))
    return explanation


def _notin_text(term, text):
    index        = text.find(term)
    head         = text[:index]
    tail         = text[index+len(term):]
    correct_text = head + tail
    diff         = _diff_text(correct_text, text)
    newdiff      = ['%s is contained here:' % repr(term, maxsize = 42)]
    for line in diff:
        if line.startswith('Skipping'):
            continue
        if line.startswith('- '):
            continue
        if line.startswith('+ '):
            newdiff.append('  ' + line[2:])
        else:
            newdiff.append(line)
    return newdiff

