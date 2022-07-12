from unittest import TestCase
from unittest.mock import patch

from examples.abstract_factory import ProcessorFactoryStatic, StringProcessor, ProcessorFactoryDynamic


class ProcessorFactoryTestCase(TestCase):

    def test_str_processor_static(self, ):
        with patch('examples.abstract_factory.StringProcessor') as mock:
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
        with patch('examples.abstract_factory.BaseProcessor.__new__') as mock:
            mock.return_value = 'some_value'
            actual = ProcessorFactoryDynamic.build(foo='string')
            self.assertEqual(actual, 'some_value')
            mock.assert_called_with(StringProcessor, foo='string')
