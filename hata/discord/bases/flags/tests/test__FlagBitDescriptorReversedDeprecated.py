from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag_descriptors import FlagBitDescriptorReversedDeprecated

from .helpers import FlagDeprecationCountTrigger


def test__FlagBitDescriptorReversedDeprecated__get__type():
    """
    Tests whether ``FlagBitDescriptorReversedDeprecated.__get__`` works as intended.
    
    Case: from type.
    """
    shift = 2
    type_name = 'koishi'
    flag_name = 'Kokoro'
    instance = None
    instance_type = int
    deprecation = FlagDeprecationCountTrigger(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    flag_descriptor = FlagBitDescriptorReversedDeprecated(shift, type_name, flag_name, deprecation)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    
    vampytest.assert_instance(output, FlagBitDescriptorReversedDeprecated)
    vampytest.assert_is(output, flag_descriptor)
    vampytest.assert_eq(deprecation.triggered, 0)


def _iter_options__get_instance():
    yield 0, 6, True
    yield 1, 6, False


@vampytest._(vampytest.call_from(_iter_options__get_instance()).returning_last())
def test__FlagBitDescriptorReversedDeprecated__get__instance(shift, instance):
    """
    Tests whether ``FlagBitDescriptorReversedDeprecated.__get__`` works as intended.
    
    Case: from instance.
    
    Parameters
    ----------
    shift : `int`
        Shift value to test with.
    
    instance : `int`
        Instance value to test on.
    
    Returns
    -------
    output : `bool`
    """
    type_name = 'koishi'
    flag_name = 'Kokoro'
    instance_type = int
    deprecation = FlagDeprecationCountTrigger(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    flag_descriptor = FlagBitDescriptorReversedDeprecated(shift, type_name, flag_name, deprecation)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(deprecation.triggered, 1)
    return output
