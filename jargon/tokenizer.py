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
#    result = [(NAME, 'import'),
#              (NAME, 'unittest'),
#              (NEWLINE, '\n')]
    last_token = None
    for tokenum, value, _, _, _ in generate_tokens(readline):
        if tokenum == NAME and value == 'describe':
            result.append([tokenum, 'class'])
        elif tokenum == NAME and value == 'it':
            result.append([tokenum, 'def'])
#        elif tokenum == NAME and value == 'before_each':
#            result.extend([(tokenum, 'setUp'),
#                           (OP, '('),
#                           (NAME, 'self'),
#                           (OP, ')')])
#        elif tokenum == NAME and value == 'after_each':
#            result.extend([(tokenum, 'tearDown'),
#                           (OP, '('),
#                           (NAME, 'self'),
#                           (OP, ')')])
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

#def translate(readline):
#    previous_name = ""
#    for type, name,_,_,_ in tokenize.generate_tokens(readline):
#        if type == tokenize.NAME and name =='describe':
#            yield tokenize.NAME, 'class'
#        elif type == 3 and previous_name == 'describe':
#            yield 3, class_for_describe(name)
#        elif type == tokenize.NAME and name =='it':
#            yield tokenize.NAME, 'def'
#        elif type == 3 and previous_name == 'it': 
#            yield 3, method_for_it(name)
#        else:
#            yield type,name
#        previous_name = name
            


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


