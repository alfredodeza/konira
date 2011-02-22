from encodings          import utf_8
import codecs
import cStringIO
import encodings
import tokenize



def class_for_describe(token):
    return token.strip().replace(" ", "_").replace("\"","" ).strip(':') + "(object)"
    


def method_for_it(token):
    return token.strip().replace(" ", "_").replace("\"","" ) + "(self)"


def to_verify(line):
    clean_line = line.strip()
    code = clean_line.split('verify')[1].strip()
    left    = code.split()[0]
    operand = code.split()[1]
    right   = code.split()[2]
    return 'verify(%s, %s, %s)' % (left, operand, right)



def translate(readline):
    previous_name = ""
    for type, name,_,_,_ in tokenize.generate_tokens(readline):
        if type == tokenize.NAME and name =='describe':
            yield tokenize.NAME, 'class'
        elif type == 3 and previous_name == 'describe':
            yield 3, class_for_describe(name)
        elif type == tokenize.NAME and name =='it':
            yield tokenize.NAME, 'def'
        elif type == 3 and previous_name == 'it': 
            yield 3, method_for_it(name)
        else:
            yield type,name
        previous_name = name
            


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


