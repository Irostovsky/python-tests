from unittest import TestCase
from unittest.mock import patch


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


class ProcessorFactoryTestCase(TestCase):

    def test_str_processor_static(self, ):
        with patch('tests.test_abstract_factory_mock.StringProcessor') as mock:
            mock.return_value = 'some_value'
            actual = ProcessorFactoryStatic.build(foo='string')
            self.assertEqual(actual, 'some_value')
            mock.assert_called_with(foo='string')

    def test_str_processor_dynamic_init(self):
        with patch.object(StringProcessor, "__init__", return_value=None) as mock:
            actual = ProcessorFactoryDynamic.build(foo='string')
            self.assertTrue(isinstance(actual, StringProcessor))
            mock.assert_called_with(foo='string')

    def test_str_processor_dynamic_new(self):
        with patch('tests.test_abstract_factory_mock.BaseProcessor.__new__') as mock:
            mock.return_value = 'some_value'
            actual = ProcessorFactoryDynamic.build(foo='string')
            self.assertEqual(actual, 'some_value')
            mock.assert_called_with(StringProcessor, foo='string')

    # def test_int_processor_static(self):
    #     with patch('tests.test_abstract_factory_mock.IntProcessor') as mock:
    #         mock.return_value = 'some_value'
    #         actual = ProcessorFactoryStatic.build(foo=123)
    #         self.assertEqual(actual, 'some_value')
    #         mock.assert_called_with(foo=123)
