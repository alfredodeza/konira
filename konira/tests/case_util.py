from konira import util


describe "name convertion":


    it "replaces underscore with whitespace":
        name = "a_white_space_string"
        assert util.name_convertion(name) == 'A white space string'


    it "removes whitespaces from outer string":
        name = " a_white_space_string "
        assert util.name_convertion(name) == 'a white space string'


    it "removes case from a name string":
        name = "Case_foo_bar"
        assert util.name_convertion(name) == 'foo bar'


    it "does not remove case if not uppercase":
        name = "case_foo_bar"
        assert util.name_convertion(name) == 'Case foo bar'



describe "get class name":


    it "returns itself when it str does not start with case":
        name = "a string"
        assert util.get_class_name(name) == name 


    it "returns none when does not start with Case":
        name = """<class '_stdout_messages_for_the_command_line'>"""
        assert util.get_class_name(name) == None
        

    it "parses correctly when a valid class name is sent":
        name = """<class 'Case_stdout_messages_for_the_command_line'>"""
        assert util.get_class_name(name) == 'Case_stdout_messages_for_the_command_line'



#describe "stop watch":
#
#
#    it "returns no more than 5 chars":
#        swatch = util.StopWatch()
#        assert len(swatch.elapsed()) == 5
#
