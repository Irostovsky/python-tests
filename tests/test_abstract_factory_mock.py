import unittest
from unittest import TestCase
from unittest.mock import patch


class BaseProcessor:
    def __init__(self, foo):
        self.foo = foo


class StringProcessor(BaseProcessor):
    foo_type = str


class IntProcessor(BaseProcessor):
    foo_type = int


class ProcessorFactory:

    @classmethod
    def build(cls, foo):
        # Tests failed:
        clazz = [subclass for subclass in BaseProcessor.__subclasses__() if subclass.foo_type == type(foo)][0]
        return clazz(foo=foo)

        # Tests work:
        # if type(foo) == str:
        #     return StringProcessor(foo=foo)
        # return IntProcessor(foo=foo)


class MyTest(TestCase):

    @patch('tests.test_abstract_factory_mock.StringProcessor')
    def test_str_processor(self, mock):
        mock.return_value = 'some_value'
        actual = ProcessorFactory.build(foo='string')
        self.assertEqual(actual, 'some_value')
        mock.assert_called_with(foo='string')

    @patch('tests.test_abstract_factory_mock.IntProcessor')
    def test_int_processor(self, mock):
        mock.return_value = 'some_value'
        actual = ProcessorFactory.build(foo=123)
        self.assertEqual(actual, 'some_value')
        mock.assert_called_with(foo=123)


# To run tests:
# python -m unittest tests/test_abstract_factory_mock.py
if __name__ == '__main__':
    unittest.main()
