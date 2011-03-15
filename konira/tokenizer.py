from tokenize           import NAME, OP, STRING, generate_tokens
from encodings          import utf_8
import codecs
import cStringIO
import encodings
import tokenize



def quote_remover(string):
    _string = string.replace(",", "").replace(".", "")
    return _string.replace("'", "")


def valid_method_name(token):
    transform = token.strip().replace(" ", "_").replace("\"","" )
    return "it_%s" % quote_remover(transform)


def valid_class_name(token):
    transform = token.strip().replace(" ", "_").replace("\"","" )
    return "Case_%s" % quote_remover(transform)
    

def initial_imports():
    case_imports = []
    import_raise = case_imports.extend(([NAME, 'import'],[NAME, 'konira']))
    return case_imports


def translate(readline):
    result     = []
    last_kw    = None
    last_token = None
    last_type  = None
    descr_obj  = False

    # add imports
    result.extend(initial_imports())

    for tokenum, value, _, _, _ in generate_tokens(readline):

        # From Describe to class - includes inheritance
        if tokenum == NAME and value == 'describe':
            last_kw = 'describe'
            result.extend(([tokenum, 'class'],))
        elif tokenum == STRING and last_token == 'describe':
            last_kw   = 'describe'
            descr_obj = True
            result.extend(([NAME, valid_class_name(value)],))

        elif tokenum == OP and value == ',' and last_type == STRING and last_kw == 'describe':
            if descr_obj:
                result.extend(([OP, '('],))
                last_kw   = 'describe'
                descr_obj = True

        elif tokenum == NAME and last_type == OP and last_kw == 'describe':
            if descr_obj:
                result.extend(([NAME, value],
                               [OP, ')'],))
                last_kw   = None
                descr_obj = False

        elif last_type == STRING and last_kw == 'describe':
            if descr_obj:
                result.extend(([OP, '('],
                               [NAME, 'object'],
                               [OP, ')'],
                               [OP, ':'],))
                last_kw   = None
                descr_obj = False

        # Skip if Constructors
        elif tokenum == NAME and value == 'skip':
            result.extend(([tokenum, 'def'],))

        elif tokenum == NAME and last_token == 'skip' and value == 'if':
            result.extend(([tokenum, '_skip_if'],
                           [OP, '('],
                           [NAME, 'self'],
                           [OP, ')']))

        # Before Constructors
        elif tokenum == NAME and value == 'before':
            result.extend(([tokenum, 'def'],))

        elif tokenum == NAME and last_token == 'before':
            result.extend(([tokenum, '_before_%s' % value],
                           [OP, '('],
                           [NAME, 'self'],
                           [OP, ')']))

        # After Constructors
        elif tokenum == NAME and value == 'after':
            result.extend(([tokenum, 'def'],))

        elif tokenum == NAME and last_token == 'after':
            result.extend(([tokenum, '_after_%s' % value],
                           [OP, '('],
                           [NAME, 'self'],
                           [OP, ')']))

        # From it to def
        elif tokenum == NAME and value == 'it':
            result.extend(([tokenum, 'def'],))
        elif tokenum == STRING and last_token == 'it':
            result.extend(([tokenum, valid_method_name(value)],
                           [OP, '('],
                           [NAME, 'self'],
                           [OP, ')'],))

        # From raises to with konira.tools.raises
        elif tokenum == NAME and value == 'raises':
            result.extend(([tokenum, 'with konira.tools.raises'],))

        elif tokenum == NAME and last_token == 'raises':
            result.extend(([OP, '('],
                           [NAME, value],
                           [OP, ')'],))

        else:
            result.append([tokenum, value])
        last_token = value
        last_type  = tokenum
    
    return result



class StreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        data = tokenize.untokenize(translate(self.stream.readline))
        self.stream = cStringIO.StringIO(data)



def search_function(s):
    if s!='konira': return None
    utf8=encodings.search_function('utf8')
    return codecs.CodecInfo(
        name='konira',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
        streamreader=StreamReader,
        streamwriter=utf8.streamwriter)



codecs.register(search_function)


