

class ArgOpts(object):


    def __init__(self, options):
        self.options    = options
        self.help       = ['-h', '--h', '--help', 'help']
        self.version    = ['--version', 'version']
        self._arg_count = {}
        self._count_arg = {}
        

    def parse_args(self, argv):
        self.args = argv[1:]
        self.match = [i for i in argv if i in self.options]
        for count, argument in enumerate(self.args):
            self._arg_count[argument] = count
            self._count_arg[count]    = argument


    def get_value(self, opt):
        count = self._arg_count.get(opt)
        if count == None:
            return None
        value = self._count_arg.get(count+1)
        return value


    def has(self, opt):
        if type(opt) == list:
            for i in opt:
                if i in self._arg_count.keys():
                    return True
            return False
        if opt in self._arg_count.keys():
            return True
        return False


    def catches_help(self):
        if [i for i in self.args if i in self.help]:
            return True
        return False


    def catches_version(self):
        if [i for i in self.args if i in self.version]:
            return True
        return False

