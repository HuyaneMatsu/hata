import vampytest

from ..builder_base import _create_conversion_descriptors, BuilderBase
from ..descriptor import ConversionDescriptor

from .helpers import _create_default_conversion


def test__create_conversion_descriptors():
    """
    Tests whether ``_create_conversion_descriptors`` works as intended.
    """
    type_name = 'yuuka'
    base_types = (BuilderBase,)
    type_attributes = {}
    
    conversion_0 = _create_default_conversion({
        'name': 'koishi',
    })
    conversion_1 = _create_default_conversion({
        'name': 'satori',
    })
    
    default_conversions = [conversion_0]
    assigned_conversions = {'mister': conversion_1}
    
    output = _create_conversion_descriptors(
        type_name, base_types, type_attributes, default_conversions, assigned_conversions
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, ConversionDescriptor)
    
    vampytest.assert_eq(len(output), 2)
    
    descriptor = output[0]
    vampytest.assert_is(descriptor.attribute_name, None)
    vampytest.assert_is(descriptor.conversion, conversion_0)
    
    descriptor = output[1]
    vampytest.assert_is(descriptor.attribute_name, 'mister')
    vampytest.assert_is(descriptor.conversion, conversion_1)
