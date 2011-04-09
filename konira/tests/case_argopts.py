# coding: konira

from konira import argopts


describe "parsing arguments":


    it "removes the first item in the list always":
        parser = argopts.ArgOpts([])
        parser.parse_args(['foo'])
        assert parser.args == []


    it "matches an option in arguments":
        parser = argopts.ArgOpts(['--foo'])
        parser.parse_args(['/bin/konira', '--foo'])
        assert parser.args  == ['--foo']
        assert parser.match == ['--foo']


    it "matches arguments with no values":
        parser = argopts.ArgOpts(['--foo'])
        parser.parse_args(['/bin/konira', '--foo'])
        assert parser._arg_count['--foo'] == 0
        assert parser._count_arg[0]       == '--foo'


    it "matches arguments with values":
        parser = argopts.ArgOpts(['--foo'])
        parser.parse_args(['/bin/konira', '--foo', 'BAR'])
        assert parser.match               == ['--foo']
        assert parser._arg_count['--foo'] == 0
        assert parser._count_arg[1]       == 'BAR'


    it "matches valid configured options only":
        parser = argopts.ArgOpts(['--fuuu'])
        parser.parse_args(['/bin/konira', '--foo', '--meh'])
        assert parser.match == []

    
    it "matches mixed values and arguments":
        parser = argopts.ArgOpts(['--foo', '--bar'])
        parser.parse_args(['/bin/konira', '--foo', 'FOO', '--bar'])
        assert parser.match == ['--foo', '--bar']
        assert parser._arg_count['--foo'] == 0
        assert parser._arg_count['--bar'] == 2
        assert parser._count_arg[1]       == 'FOO'
        assert parser._count_arg.get(3)   == None



describe "get values from arguments":


    before each:
        self.parser = argopts.ArgOpts(['--foo'])
        self.parser.parse_args(['/bin/konira', '--foo', 'BAR', '--bar'])


    it "returns a valid value from a matching argument":
        assert self.parser.get_value('--foo') == 'BAR'


    it "returns None when an argument does not exist":
        assert self.parser.get_value('--meh') == None


    it "returns None when an argument does not have a value":
        assert self.parser.get_value('--bar') == None
