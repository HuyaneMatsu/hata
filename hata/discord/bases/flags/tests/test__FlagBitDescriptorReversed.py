import vampytest

from ..flag_descriptors import FlagBitDescriptorReversed


def test__FlagBitDescriptorReversed__get__type():
    """
    Tests whether ``FlagBitDescriptorReversed.__get__`` works as intended.
    
    Case: from type.
    """
    shift = 2
    type_name = 'koishi'
    flag_name = 'Kokoro'
    instance = None
    instance_type = int
    
    flag_descriptor = FlagBitDescriptorReversed(shift, type_name, flag_name)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    
    vampytest.assert_instance(output, FlagBitDescriptorReversed)
    vampytest.assert_is(output, flag_descriptor)


def _iter_options__get_instance():
    yield 0, 6, True
    yield 1, 6, False


@vampytest._(vampytest.call_from(_iter_options__get_instance()).returning_last())
def test__FlagBitDescriptorReversed__get__instance(shift, instance):
    """
    Tests whether ``FlagBitDescriptorReversed.__get__`` works as intended.
    
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
    
    flag_descriptor = FlagBitDescriptorReversed(shift, type_name, flag_name)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    vampytest.assert_instance(output, bool)
    return output
