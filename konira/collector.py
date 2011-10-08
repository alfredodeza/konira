from __future__ import with_statement
from konira.tokenizer import translate
import tokenize
import os
import re


class FileCollector(list):


    def __init__(self, path, config={}):
        self.user_match       = config.get('collect-match')
        self.case_insensitive = config.get('collect-ci')
        self.path             = path
        self._collect()


    @property
    def valid_module_name(self):
        fallback = re.compile(r'case[_a-z]\w*\.py$', re.IGNORECASE)
        if not self.user_match:
            return fallback
        else:
            try:
                if self.case_insensitive:
                    return re.compile(self.user_match, re.IGNORECASE)
                return re.compile(self.user_match)
            except Exception, msg:
                raise SystemExit('Could not compile regex, error was: %s' % msg)


    def _collect(self):
        if os.path.isfile(self.path):
            self.append(self.path)
            return

        # Local is faster
        walk = os.walk
        join = os.path.join
        path = self.path
        levels_deep = 0

        for root, dirs, files in walk(path):
            levels_deep += 1

            # Start checking for Python packages after 3 levels
            if levels_deep > 2:
                if not '__init__.py' in files:
                    continue
            for item in files:
                absolute_path = join(root, item)
                if not self.valid_module_name.match(item):
                    continue
                self.append(absolute_path)



def globals_from_file(filename):
    _file = open(filename)
    data  = tokenize.untokenize(translate(_file.readline))
    compiled = compile(data, filename, "exec")
    globals_ = {}
    exec(compiled, globals_)
    return globals_



