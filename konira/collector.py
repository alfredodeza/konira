import os
import re


class FileCollector(list):


    def __init__(self, path):
        self.path              = path
        self.valid_module_name = re.compile(r'case[_a-z]\w*\.py$', re.IGNORECASE)
        self._collect()


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



def globals_from_execed_file(filename):
    globals_ = {}
    try:
        execfile(filename, globals_)
        return globals_
    except Exception, e:
        raise


