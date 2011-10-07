from konira.util import StringIO
from konira    import tokenizer


describe "quote remover":


    before each:
        self.remover = tokenizer.quote_remover


    it "removes commas from strings":
        assert self.remover("a,separated,string") == "aseparatedstring"


    it "removes commas respecting whitespace":
        assert self.remover("a, separated, string") == "a separated string"


    it "removes single quotes from strings":
        assert self.remover("a ' string '") == "a  string "


    it "removes a combination of commas and quotes":
        assert self.remover("a, 'string',") == "a string"


    it "removes dots from strings":
        assert self.remover("a. dotted. string.") == "a dotted string"


    it "respects camel case strings":
        assert self.remover("a Camel Case string") == "a Camel Case string"



describe "valid method names":


    before each:
        self.valid = tokenizer.valid_method_name


    it "replaces whitespace with underscores":
        assert self.valid("a name with underscores") == "it_a_name_with_underscores"


    it "removes double quotes from strings":
        assert self.valid('a double \"quoted\" string') == "it_a_double_quoted_string"


    it "removes commas from strings":
        assert self.valid('a ,in a string,') == "it_a_in_a_string"


    it "removes commas quotes and double quotes from strings":
        assert self.valid('a \", in a string\'') == 'it_a__in_a_string'


    it "removes dots from strings":
        assert self.valid("a. dotted. string.") == "it_a_dotted_string"


    it "respects camel case from strings":
        assert self.valid("a CamelCase string") == "it_a_CamelCase_string"



describe "valid class names":


    before each:
        self.valid = tokenizer.valid_class_name


    it "replaces whitespace with underscores":
        assert self.valid("a string with whitespace") == "Case_a_string_with_whitespace"


    it "removes double quotes from strings":
        assert self.valid("a string\"") == "Case_a_string"


    it "removes dots and commas from strings":
        assert self.valid("a. string, \'") == "Case_a_string_"


    it "removes single quotes from strings":
        assert self.valid("\'single quote") == "Case_single_quote"


    it "respects camel case in strings":
        assert self.valid("my Test") == "Case_my_Test"



describe "valid raises detection":


    before each:
        self.valid = tokenizer.valid_raises


    it "is True when the value is None":
        assert self.valid(None) == True


    it "is True when the value is an empty string":
        assert self.valid(" ") == True


    it "is false when the value has a character at the start":
        assert self.valid("d ") == False


    it "is false when the value has a character at the end":
        assert self.valid("   d") == False


    it "is true when there are non whitespace chars":
        assert self.valid("\n ") == True


    it "is true when an empty string is passed":
        assert self.valid("") == True



describe "translate dsl into valid Python":
    

    before each:
        self.translate = tokenizer.translate
        self.line      = StringIO


    it "never do implicit imports":
        line = self.line('').readline
        assert self.translate(line) == [[0, '']]

    
    it "translates describe into a class":
        line = self.line('describe "my test class":\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'class'
        assert result[1][1]   == 'Case_my_test_class'
        assert result[2][1]   == '('
        assert result[3][1]   == 'object'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''
        

    it "translates an it to a def":
        line = self.line('it "should test my method":\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == 'it_should_test_my_method'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates a describe with inheritance":
        line = self.line('describe "my test class", Foo:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'class'
        assert result[1][1]   == 'Case_my_test_class'
        assert result[2][1]   == '('
        assert result[3][1]   == 'Foo'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates a describe with inheritance regardless of space":
        line = self.line('describe "my test class",Foo:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'class'
        assert result[1][1]   == 'Case_my_test_class'
        assert result[2][1]   == '('
        assert result[3][1]   == 'Foo'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates a describe with inheritance with a lot of whitespace":
        line = self.line('describe "my test class"    ,          Foo:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'class'
        assert result[1][1]   == 'Case_my_test_class'
        assert result[2][1]   == '('
        assert result[3][1]   == 'Foo'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates skip if constructors":
        line = self.line('skip if:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == '_skip_if'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates before all constructors":
        line = self.line('before all:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == '_before_all'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates before each constructors":
        line = self.line('before each:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == '_before_each'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates after each constructors":
        line = self.line('after each:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == '_after_each'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates after all constructors":
        line = self.line('after all:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == '_after_all'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates raises into with statements":
        line = self.line('raises IOError: foo()')
        result = self.translate(line.readline)
        assert len(result) == 9
        assert result[0][1]   == 'with konira.tools.raises'
        assert result[1][1]   == '('
        assert result[2][1]   == 'IOError'
        assert result[3][1]   == ')'
        assert result[4][1]   == ':'
        assert result[5][1]   == 'foo'
        assert result[6][1]   == '('
        assert result[7][1]   == ')'
        assert result[8][1]   == ''


    it "does not translate a regular class":
        line = self.line('class Foo(object):\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'class'
        assert result[1][1]   == 'Foo'
        assert result[2][1]   == '('
        assert result[3][1]   == 'object'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "does not translate a regular method":
        line = self.line('def foo(self):\n pass')
        result = self.translate(line.readline)
        assert len(result) == 11
        assert result[0][1]   == 'def'
        assert result[1][1]   == 'foo'
        assert result[2][1]   == '('
        assert result[3][1]   == 'self'
        assert result[4][1]   == ')'
        assert result[5][1]   == ':'
        assert result[6][1]   == '\n'
        assert result[7][1]   == ' '
        assert result[8][1]   == 'pass'
        assert result[9][1]   == ''
        assert result[10][1]  == ''


    it "translates let into a valid method":
        line = self.line('let foo = True')
        result = self.translate(line.readline)
        assert len(result)  == 4
        assert result[0][1] == '_let_foo'
        assert result[1][1] == '='
        assert result[2][1] == 'True'
        assert result[3][1] == ''
