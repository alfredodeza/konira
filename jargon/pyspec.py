class _MethodWrap:
    def __init__(self, instance, value):
        self.instance = instance
        self.func = value
        
    def __call__(self):
        return self.func(self.instance())
    
    def should_be(self, dado):
        return self.func(self.instance()) == dado

