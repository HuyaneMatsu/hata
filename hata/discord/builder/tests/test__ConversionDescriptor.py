from types import FunctionType

import vampytest

from ..builder_base import BuilderBase
from ..descriptor import ConversionDescriptor
from ..conversion import Conversion

from .helpers import _create_default_conversion


def _assert_fields_set(descriptor):
    """
    Asserts whether ``ConversionDescriptor`` has its fields set.
    
    Parameters
    ----------
    descriptor : ``ConversionDescriptor``
        The descriptor to test. 
    """
    vampytest.assert_instance(descriptor, ConversionDescriptor)
    vampytest.assert_instance(descriptor.attribute_name, str, nullable = True)
    vampytest.assert_instance(descriptor.conversion, Conversion)
    vampytest.assert_instance(descriptor.getter, FunctionType)
    vampytest.assert_instance(descriptor.output_conversion, Conversion)
    vampytest.assert_instance(descriptor.setter, FunctionType)


def _test_attribute_requester(attribute_name):
    try:
        return getattr(BuilderBase, attribute_name)
    except AttributeError as exception:
        raise RuntimeError from exception


def test__ConversionDescriptor__new():
    """
    Tests whether ``ConversionDescriptor.__new__`` works as intended.
    """
    attribute_name = 'koishi'
    conversion = _create_default_conversion()
    
    descriptor = ConversionDescriptor(attribute_name, conversion, _test_attribute_requester)
    
    _assert_fields_set(descriptor)
    
    vampytest.assert_eq(descriptor.attribute_name, attribute_name)
    vampytest.assert_is(descriptor.conversion, conversion)
    vampytest.assert_is(descriptor.getter, BuilderBase._getter_none)
    vampytest.assert_is(descriptor.output_conversion, conversion)
    vampytest.assert_is(descriptor.setter, BuilderBase._setter_none)
    

def test__ConversionDescriptor__set():
    """
    Tests whether ``ConversionDescriptor.__set__`` works as intended.
    """
    def set_validator(value):
        yield value
        return
    
    setter_called = False
    
    def setter(input_instance, input_conversion, input_value):
        nonlocal instance
        nonlocal conversion
        nonlocal value
        nonlocal setter_called
        
        vampytest.assert_is(instance, input_instance)
        vampytest.assert_is(conversion, input_conversion)
        vampytest.assert_is(value, input_value)
        setter_called = True
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        if attribute_name == '_setter_none':
            return setter
        
        if attribute_name == '_getter_none':
            return lambda *p: None
        
        raise RuntimeError
        
    
    conversion = _create_default_conversion({
        'set_validator': set_validator,
    })
    
    descriptor = ConversionDescriptor(None, conversion, attribute_requester)
    
    instance = BuilderBase()
    
    value = object()
    
    descriptor.__set__(instance, value)
    
    vampytest.assert_true(setter_called)


def test__ConversionDescriptor__get():
    """
    Tests whether ``ConversionDescriptor.__get__`` works as intended.
    """
    def get_processor(value):
        return value + 1
    
    
    getter_called = False
    
    
    def getter(input_instance, input_conversion):
        nonlocal instance
        nonlocal conversion
        nonlocal value
        nonlocal getter_called
        
        vampytest.assert_is(instance, input_instance)
        vampytest.assert_is(conversion, input_conversion)
        getter_called = True
        return conversion.get_processor(value)
    
    
    def attribute_requester(attribute_name):
        nonlocal getter
        if attribute_name == '_setter_none':
            return lambda *p: None
        
        if attribute_name == '_getter_none':
            return getter
            
        raise RuntimeError
    
    
    conversion = _create_default_conversion({
        'get_processor': get_processor,
    })
    
    descriptor = ConversionDescriptor(None, conversion, attribute_requester)
    
    instance = BuilderBase()
    
    value = 2
    
    output = descriptor.__get__(instance, type(instance))
    
    vampytest.assert_true(getter_called)
    vampytest.assert_eq(output, get_processor(value))


def test__ConversionDescriptor__raise_type_error():
    """
    Tests whether ``ConversionDescriptor.raise_type_error`` works as intended.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    
    
    conversion = _create_default_conversion()
    descriptor = ConversionDescriptor(None, conversion, attribute_requester)
    
    with vampytest.assert_raises(TypeError):
        descriptor.raise_type_error(None, 123)


def test__ConversionDescriptor__repr():
    """
    Tests whether ``ConversionDescriptor.__repr__`` works as intended.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    
    
    attribute_name = 'mister'
    
    conversion = _create_default_conversion()
    descriptor = ConversionDescriptor(attribute_name, conversion, attribute_requester)
    
    output = repr(descriptor)
    
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in('conversion', output)
    vampytest.assert_in(repr(conversion), output)
    
    vampytest.assert_in(attribute_name, output)
    vampytest.assert_in(repr(attribute_name), output)
