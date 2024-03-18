import vampytest

from ..builder_base import _filter_descriptors_keyword
from ..descriptor import ConversionDescriptor

from .helpers import _create_default_conversion


def test__filter_descriptors_keyword():
    """
    Tests whether ``_filter_descriptors_keyword`` works as intended.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    
    
    def set_validator(value):
        yield value
        return
    
    
    conversion_0 = _create_default_conversion({
        'name': 'koishi',
    })
    descriptor_0 = ConversionDescriptor(None, conversion_0, attribute_requester)
    
    conversion_1 = _create_default_conversion({
        'name': 'satori',
        'name_aliases': ('orin',), 
        'set_validator': set_validator,
    })
    descriptor_1 = ConversionDescriptor(None, conversion_1, attribute_requester)
    
    conversion_descriptors = [descriptor_0, descriptor_1]
    
    output = _filter_descriptors_keyword(conversion_descriptors)
    
    vampytest.assert_instance(output, dict)
    
    for key, element in output.items():
        vampytest.assert_instance(key, str)
        vampytest.assert_instance(element, ConversionDescriptor)
    
    output = sorted(output.items())
    
    vampytest.assert_eq(len(output), 2)
    
    key, descriptor = output[0]
    vampytest.assert_eq(key, 'orin')
    vampytest.assert_is(descriptor, descriptor_1)

    key, descriptor = output[1]
    vampytest.assert_eq(key, 'satori')
    vampytest.assert_is(descriptor, descriptor_1)
