import vampytest

from ..descriptor import ConversionDescriptor
from ..serialization_configuration import SerializationConfiguration

from .helpers import _create_default_conversion


def _assert_fields_set(serialization_configuration):
    """
    Asserts whether every field of the serialization configuration are set correctly.
    
    Parameters
    ----------
    serialization_configuration : ``SerializationConfiguration``
        The serialization configuration to check.
    """
    vampytest.assert_instance(serialization_configuration, SerializationConfiguration)
    vampytest.assert_instance(serialization_configuration.conversions, tuple)
    vampytest.assert_instance(serialization_configuration.defaults, bool)


def test__SerializationConfiguration__new():
    """
    Tests whether ``SerializationConfiguration.__new__`` works as intended.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    

    conversion_0 = _create_default_conversion({
        'sort_priority': 3
    })
    descriptor_0 = ConversionDescriptor(None, conversion_0, attribute_requester)
    
    conversion_1 = _create_default_conversion({
        'sort_priority': 2,
    })
    descriptor_1 = ConversionDescriptor(None, conversion_1, attribute_requester)
    
    serialization_configuration = SerializationConfiguration([descriptor_0, descriptor_1], True)
    _assert_fields_set(serialization_configuration)
    
    
    vampytest.assert_eq(serialization_configuration.conversions, (conversion_1, conversion_0))
    vampytest.assert_eq(serialization_configuration.defaults, True)
    

def test__SerializationConfiguration__repr():
    """
    Tests whether ``SerializationConfiguration.__repr__`` works as intended.
    """
    def setter(input_instance, input_conversion, input_value):
        pass
    
    
    def attribute_requester(attribute_name):
        nonlocal setter
        return setter
    

    conversion_0 = _create_default_conversion({
        'sort_priority': 3
    })
    descriptor_0 = ConversionDescriptor(None, conversion_0, attribute_requester)
    
    conversion_1 = _create_default_conversion({
        'sort_priority': 2,
    })
    descriptor_1 = ConversionDescriptor(None, conversion_1, attribute_requester)
    
    serialization_configuration = SerializationConfiguration([descriptor_0, descriptor_1], True)
    
    output = repr(serialization_configuration)
    vampytest.assert_instance(output, str)
