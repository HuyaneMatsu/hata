import vampytest

from ..builder_base import _filter_descriptors_listing
from ..descriptor import ConversionDescriptor

from .helpers import _create_default_conversion


def test__filter_descriptors_listing__filtering():
    """
    Tests whether ``_filter_descriptors_listing`` works as intended.
    
    Case: Filtering.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    
    
    def set_listing_identifier(value):
        yield value
        return
    
    
    conversion_0 = _create_default_conversion({
        'name': 'koishi',
    })
    descriptor_0 = ConversionDescriptor(None, conversion_0, attribute_requester)
    
    conversion_1 = _create_default_conversion({
        'name': 'satori',
        'set_listing_identifier': set_listing_identifier,
    })
    descriptor_1 = ConversionDescriptor(None, conversion_1, attribute_requester)
    
    conversion_descriptors = [descriptor_0, descriptor_1]
    
    output = _filter_descriptors_listing(conversion_descriptors)
    
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, ConversionDescriptor)
    
    vampytest.assert_eq(len(output), 1)
    
    
    descriptor = output[0]
    vampytest.assert_is(descriptor, descriptor_1)


def test__filter_descriptors_listing__sorting():
    """
    Tests whether ``_filter_descriptors_listing`` works as intended.
    
    Case: Sorting.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    
    
    def set_listing_identifier(value):
        yield value
        return
    
    
    conversion_0 = _create_default_conversion()
    conversion_0.name = 'koishi'
    conversion_0.set_listing_identifier = set_listing_identifier
    conversion_0.sort_priority = 2
    descriptor_0 = ConversionDescriptor(None, conversion_0, attribute_requester)
    
    conversion_1 = _create_default_conversion()
    conversion_1.name = 'satori'
    conversion_1.set_listing_identifier = set_listing_identifier
    conversion_1.sort_priority = 1
    descriptor_1 = ConversionDescriptor(None, conversion_1, attribute_requester)
    
    conversion_descriptors = [descriptor_0, descriptor_1]
    
    output = _filter_descriptors_listing(conversion_descriptors)
    
    vampytest.assert_instance(output, list)
    
    for element in output:
        vampytest.assert_instance(element, ConversionDescriptor)
    
    vampytest.assert_eq(len(output), 2)
    
    
    descriptor = output[0]
    vampytest.assert_is(descriptor, descriptor_1)

    descriptor = output[1]
    vampytest.assert_is(descriptor, descriptor_0)
