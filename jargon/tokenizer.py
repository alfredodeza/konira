from encodings          import utf_8
import codecs
import cStringIO
import encodings
import tokenize
from tokenize import NAME, NEWLINE, OP, STRING, generate_tokens


def class_for_describe(token):
    return token.strip().replace(" ", "_").replace("\"","" ).strip(':') + "(object)"
    


def method_for_it(token):
    return token.strip().replace(" ", "_").replace("\"","" ) + "(self)"


def translate(readline):
    result = []
    last_token = None
    for tokenum, value, _, _, _ in generate_tokens(readline):
        if tokenum == NAME and value == 'describe':
            result.append([tokenum, 'class'])
        elif tokenum == NAME and value == 'it':
            result.append([tokenum, 'def'])
        elif tokenum == STRING and last_token == 'it':
            result.extend(([tokenum, value.replace(' ', '_')[1:-1],],
                           [OP, '('],
                           [NAME, 'self'],
                           [OP, ')'],))
        elif tokenum == NAME and last_token == 'describe':
            result.extend(([NAME, value+'Spec'],
                           [OP, '('],
                           [NAME, 'object'],
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
    utf8=encodings.search_function('utf8') # Assume utf8 encoding
    return codecs.CodecInfo(
        name='jargon',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
        streamreader=StreamReader,
        streamwriter=utf8.streamwriter)


codecs.register(search_function)


