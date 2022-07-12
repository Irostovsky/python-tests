class BaseProcessor:
    def __init__(self, foo):
        self.foo = foo


class StringProcessor(BaseProcessor):
    foo_type = str


class IntProcessor(BaseProcessor):
    foo_type = int


class ProcessorFactoryDynamic:

    @classmethod
    def build(cls, foo):
        clazz = [subclass for subclass in BaseProcessor.__subclasses__() if subclass.foo_type == type(foo)][0]
        return clazz(foo=foo)


class ProcessorFactoryStatic:

    @classmethod
    def build(cls, foo):
        if type(foo) == str:
            return StringProcessor(foo=foo)
        return IntProcessor(foo=foo)
