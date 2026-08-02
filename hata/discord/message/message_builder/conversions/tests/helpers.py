class TestType():
    __slots__ = ('name',)
    
    def __new__(cls, name):
        self = object.__new__(cls)
        self.name = name
        return self
