class MyBaseClass:
    def __init__(self, value):
        self.value = value


class TimesFive(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 2


class Foo(TimesFive, PlusTwo):
    pass


if __name__ == '__main__':
    foo = Foo(5)
    print(foo.value)
    print(foo.__class__.mro())
    assert foo.value == 35
