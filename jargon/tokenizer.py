from tokenize           import NAME, OP, STRING, generate_tokens
from encodings          import utf_8
import codecs
import cStringIO
import encodings
import tokenize



def quote_remover(string):
    return string.replace("'", "")



def valid_name(token):
    transform = token.strip().replace(" ", "_").replace("\"","" )
    return "Case_%s" % quote_remover(transform)
    


def translate(readline):
    result = []
    last_token = None
    for tokenum, value, _, _, _ in generate_tokens(readline):

        # From Describe to class
        if tokenum == NAME and value == 'describe':
            result.append([tokenum, 'class'])
        elif tokenum == STRING and last_token == 'describe':
            result.extend(([NAME, valid_name(value)],
                           [OP, '('],
                           [NAME, 'object'],
                           [OP, ')'],))

        # Before Constructors
        elif tokenum == NAME and value == 'before_all':
            result.extend([(tokenum, 'def _before_all'),
                           (OP, '('),
                           (NAME, 'self'),
                           (OP, ')')])
        elif tokenum == NAME and value == 'before_each':
            result.extend([(tokenum, 'def _before_each'),
                           (OP, '('),
                           (NAME, 'self'),
                           (OP, ')')])

        # After Constructors
        elif tokenum == NAME and value == 'after_all':
            result.extend([(tokenum, 'def _after_all'),
                           (OP, '('),
                           (NAME, 'self'),
                           (OP, ')')])
        elif tokenum == NAME and value == 'after_each':
            result.extend([(tokenum, 'def _after_each'),
                           (OP, '('),
                           (NAME, 'self'),
                           (OP, ')')])

        # From it to def
        elif tokenum == NAME and value == 'it':
            result.append([tokenum, 'def'])
        elif tokenum == STRING and last_token == 'it':
            result.extend(([tokenum, quote_remover(value.replace(' ', '_')[1:-1]),],
                           [OP, '('],
                           [NAME, 'self'],
                           [OP, ')'],))
        else:
            result.append([tokenum, value])
        last_token = value
    return result



class StreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        data = tokenize.untokenize(translate(self.stream.readline))
        self.stream = cStringIO.StringIO(data)



def search_function(s):
    if s!='jargon': return None
    utf8=encodings.search_function('utf8')
    return codecs.CodecInfo(
        name='jargon',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
        streamreader=StreamReader,
        streamwriter=utf8.streamwriter)



codecs.register(search_function)


