# coding: konira

from konira import tokenizer


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
        assert self.valid("a. doted. string.") == "it_a_doted_string"
