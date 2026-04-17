import vampytest

from ..builder_base import _filter_descriptors_typed
from ..descriptor import ConversionDescriptor

from .helpers import _create_default_conversion


def test__filter_descriptors_typed():
    """
    Tests whether ``_filter_descriptors_typed`` works as intended.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    
    set_type_0 = int
    set_type_1 = str
    
    conversion_0 = _create_default_conversion()
    descriptor_0 = ConversionDescriptor(None, conversion_0, attribute_requester)
    
    conversion_1 = _create_default_conversion({
        'set_type': set_type_0,
        'sort_priority': 2,
    })
    descriptor_1 = ConversionDescriptor(None, conversion_1, attribute_requester)
    
    conversion_2 = _create_default_conversion({
        'set_type': set_type_1,
        'sort_priority': 1,
    })
    descriptor_2 = ConversionDescriptor(None, conversion_2, attribute_requester)
    
    conversion_descriptors = [descriptor_0, descriptor_1, descriptor_2]
    
    output = _filter_descriptors_typed(conversion_descriptors)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    descriptors_typed, descriptors_typed_ordered = output 
    
    # descriptors_typed
    vampytest.assert_instance(descriptors_typed, dict)
    for key, value in descriptors_typed.items():
        vampytest.assert_instance(key, type)
        vampytest.assert_instance(value, ConversionDescriptor)
    
    descriptors_typed = sorted(descriptors_typed.items(), key = lambda item: item[0].__name__)
    
    vampytest.assert_eq(len(descriptors_typed), 2)
    
    key, descriptor = descriptors_typed[0]
    vampytest.assert_is(key, set_type_0)
    vampytest.assert_is(descriptor, descriptor_1)
    
    key, descriptor = descriptors_typed[1]
    vampytest.assert_is(key, set_type_1)
    vampytest.assert_is(descriptor, descriptor_2)
    
    # descriptors_typed_ordered
    vampytest.assert_instance(descriptors_typed_ordered, list)
    for value in descriptors_typed_ordered:
        vampytest.assert_instance(value, ConversionDescriptor)
    
    vampytest.assert_eq(len(descriptors_typed_ordered), 2)
    vampytest.assert_eq(
        descriptors_typed_ordered,
        [descriptor_2, descriptor_1],
    )
