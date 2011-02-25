import difflib
import inspect


class JargonImportError(Exception):


    def __init__(self, exc_name, filename,lineno, msg,exc):
        self.exc_name = exc_name
        self.msg      = msg
        self.filename = filename
        self.lineno   = lineno
        self.exc      = exc
        Exception.__init__(self, msg)



class Source(object):


    def __init__(self, trace):
        self.trace = trace
        self.line = self.get_source 


    @property
    def get_source(self):
        source_string = inspect.trace()[-1][-2][0]
        source_line = source_string.strip().strip('assert').strip()
        return source_line


    def define_operand(self):
        operators = ['==', '!=', '<>', '>', '<', 
                     '>=', '<=', ' is ', ' not in ']
        source = self.get_source
        operator = [i for i in operators if i in self.line]
        if operator:
            return operator[0]


    @property
    def left_value(self):
        operator = self.define_operand()
        return eval(self.line.split(operator)[0].strip())


    @property
    def right_value(self):
        operator = self.define_operand()
        return eval(self.line.split(operator)[1].strip())


def jargon_assert(trace):
    source  = Source(trace)
    left    = source.left_value
    right   = source.right_value
    operand = source.define_operand()
    assertrepr_compare(operand, left, right)

def assertrepr_compare(op, left, right):
    """return specialised explanations for some operators/operands"""
    width = 80 - 15 - len(op) - 2 # 15 chars indentation, 1 space around op
    left_repr = left
    right_repr = right
    summary = '%s %s %s' % (left_repr, op, right_repr)

    issequence = lambda x: isinstance(x, (list, tuple))
    istext = lambda x: isinstance(x, basestring)
    isdict = lambda x: isinstance(x, dict)
    isset = lambda x: isinstance(x, set)

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
                explanation = _diff_text(left, right)
        elif op == ' not in ':
            if istext(left) and istext(right):
                explanation = _notin_text(left, right)
    except:
        #excinfo = py.code.ExceptionInfo()
        explanation = ['representation of '
            'details failed. Probably an object has a faulty __repr__.)']


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
        left = left[i:]
        right = right[i:]
    if len(left) == len(right):
        for i in range(len(left)):
            if left[-i] != right[-i]:
                break
        if i > 42:
            i -= 10     # Provide some context
            explanation += ['Skipping %s identical '
                            'trailing characters in diff' % i]
            left = left[:-i]
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
    diff_left = left - right
    diff_right = right - left
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
    index = text.find(term)
    head = text[:index]
    tail = text[index+len(term):]
    correct_text = head + tail
    diff = _diff_text(correct_text, text)
    newdiff = ['%s is contained here:' % repr(term, maxsize=42)]
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

