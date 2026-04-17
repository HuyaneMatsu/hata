import vampytest

from ..descriptor import _conversion_descriptor_sort_key, ConversionDescriptor

from .helpers import _create_default_conversion


def test__conversion_descriptor_sort_key():
    """
    Tests whether ``_conversion_descriptor_sort_key`` works as intended.
    """
    sort_priority = 2
    conversion = _create_default_conversion({
        'sort_priority': sort_priority,
    })
    
    attribute_name = 'koishi'
    
    def attribute_requester(input_attribute_name):
        return lambda *p: None
    
    conversion_descriptor = ConversionDescriptor(attribute_name, conversion, attribute_requester)
    
    output = _conversion_descriptor_sort_key(conversion_descriptor)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, sort_priority)
