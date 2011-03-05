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
        for root, dirs, files in os.walk(self.path):
            for item in files:
                absolute_path = os.path.join(root, item)
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


