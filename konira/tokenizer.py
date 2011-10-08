from tokenize           import NAME, OP, STRING, generate_tokens
import re



def quote_remover(string):
    _string = string.replace(",", "").replace(".", "")
    return _string.replace("'", "")


def valid_method_name(token):
    transform = token.strip().replace(" ", "_").replace("\"","" )
    return "it_%s" % quote_remover(transform)


def valid_class_name(token):
    transform = token.strip().replace(" ", "_").replace("\"","" )
    return "Case_%s" % quote_remover(transform)


def valid_raises(value):
    if not value:
        return True
    whitespace = re.compile(r'^\s*$')
    if whitespace.match(value):
        return True
    return False


def process_name(result, value, last_token, tokenum, last_type, descr_obj, last_kw):
    # From Describe to class - includes inheritance
    if value == 'describe':
        last_kw = 'describe'
        result.extend(([tokenum, 'class'],))

    elif last_type == OP and last_kw == 'describe':
        if descr_obj:
            result.extend(([NAME, value],
                           [OP, ')'],))
            last_kw   = None
            descr_obj = False

    # Skip if Constructors
    elif value == 'skip':
        result.extend(([tokenum, 'def'],))

    elif last_token == 'skip' and value == 'if':
        result.extend(([tokenum, '_skip_if'],
                       [OP, '('],
                       [NAME, 'self'],
                       [OP, ')']))

    # Before Constructors
    elif value == 'before':
        result.extend(([tokenum, 'def'],))

    elif last_token == 'before':
        result.extend(([tokenum, '_before_%s' % value],
                       [OP, '('],
                       [NAME, 'self'],
                       [OP, ')']))

    # After Constructors
    elif value == 'after':
        result.extend(([tokenum, 'def'],))

    elif last_token == 'after':
        result.extend(([tokenum, '_after_%s' % value],
                       [OP, '('],
                       [NAME, 'self'],
                       [OP, ')']))

    # From it to def
    elif value == 'it':
        result.extend(([tokenum, 'def'],))
    elif last_token == 'it':
        result.extend(([tokenum, valid_method_name(value)],
                       [OP, '('],
                       [NAME, 'self'],
                       [OP, ')'],))

    # From raises to with konira.tools.raises
    elif value == 'raises' and valid_raises(last_token):
        result.extend(([tokenum, 'with konira.tools.raises'],))

    elif last_token == 'raises':
        result.extend(([OP, '('],
                       [NAME, value],
                       [OP, ')'],))

    # From let to attribute
    elif value == 'let':
        result.extend(([tokenum, ''],))

    elif last_token == 'let':
        result.pop()
        result.extend(([tokenum, '_let_%s' % value],))

    else:
        result.append([tokenum, value])

    return result, descr_obj, last_kw



def process_string(result, value, last_token, tokenum, last_type, descr_obj, last_kw):
    if last_token == 'describe':
        last_kw   = 'describe'
        descr_obj = True
        result.extend(([NAME, valid_class_name(value)],))

    elif last_kw == 'describe':
        if descr_obj:
            result.extend(([OP, '('],
                           [NAME, 'object'],
                           [OP, ')'],
                           [OP, ':'],))
            last_kw   = None
            descr_obj = False

    elif last_token == 'it':
        result.extend(([tokenum, valid_method_name(value)],
                       [OP, '('],
                       [NAME, 'self'],
                       [OP, ')'],))

    else:
        result.append([tokenum, value])

    return result, descr_obj, last_kw



def process_operator(result, value, last_token, tokenum, last_type, descr_obj, last_kw):
    if value == ',' and last_type == STRING and last_kw == 'describe':
        if descr_obj:
            result.extend(([OP, '('],))
            last_kw   = 'describe'
            descr_obj = True

    elif last_type == STRING and last_kw == 'describe':
        if descr_obj:
            result.extend(([OP, '('],
                           [NAME, 'object'],
                           [OP, ')'],
                           [OP, ':'],))
            last_kw   = None
            descr_obj = False

    else:
        result.append([tokenum, value])

    return result, descr_obj, last_kw



def process_default(result, value, last_token, tokenum, last_type, descr_obj, last_kw):
    result.append([tokenum, value])
    return result, descr_obj, last_kw


# The dispatchers holds the tokenizer mappings, allowing
# to cut a huge if/elseif chaing that slows us down.
dispatcher={NAME: process_name, STRING: process_string, OP: process_operator}



def translate(readline):
    result     = []
    last_kw    = None
    last_token = None
    last_type  = None
    descr_obj  = False

    for tokenum, value, _, _, _ in generate_tokens(readline):
        process = dispatcher.get(tokenum, process_default)

        result, descr_obj, last_kw = process(result, value, last_token, tokenum, last_type, descr_obj, last_kw)

        last_token = value
        last_type  = tokenum

    return result
