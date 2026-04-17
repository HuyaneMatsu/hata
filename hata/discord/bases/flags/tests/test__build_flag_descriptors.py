from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag_deprecation import FlagDeprecation
from ..flag_descriptors import (
    FlagBitDescriptor, FlagBitDescriptorDeprecated, FlagBitDescriptorReversed, FlagBitDescriptorReversedDeprecated,
    FlagDescriptor
)
from ..flag_meta import _build_flag_descriptors


def _iter_options():
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    yield (
        'hey_mister',
        False,
        {
            ('koishi', FlagDescriptor(4)),
            ('satori', FlagDescriptor(5, deprecation = deprecation)),
        },
        {
            FlagBitDescriptor(4, 'hey_mister', 'koishi'),
            FlagBitDescriptorDeprecated(5, 'hey_mister', 'satori', deprecation),
        }
    )
    
    yield (
        'hey_mister',
        True,
        {
            ('koishi', FlagDescriptor(4)),
            ('satori', FlagDescriptor(5, deprecation = deprecation)),
        },
        {
            FlagBitDescriptorReversed(4, 'hey_mister', 'koishi'),
            FlagBitDescriptorReversedDeprecated(5, 'hey_mister', 'satori', deprecation),
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_flag_descriptors(type_name, reverse_descriptors, accumulated_flag_descriptors):
    """
    Tests whether ``_build_flag_descriptors`` works as intended.
    Parameters
    ----------
    type_name : `str`
        The created class's name.
    
    reverse_descriptors : `bool`
        Whether the descriptors should be reversed.
    
    accumulated_flag_descriptors : `set<(str, FlagDescriptor)>`
        Flag descriptors.
    
    Returns
    -------
    output : `set<FlagBitDescriptor>`
    """
    output = _build_flag_descriptors(type_name, reverse_descriptors, accumulated_flag_descriptors)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, FlagBitDescriptor)
    return {*output}
