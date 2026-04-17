from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag_deprecation import FlagDeprecation
from ..flag_descriptors import FlagBitDescriptorDeprecated

from .helpers import FlagDeprecationCountTrigger


def _assert_fields_set(flag_descriptor):
    """
    Asserts whether the given flag descriptor has all of its fields set.
    
    Parameters
    ----------
    flag_descriptor : ``FlagBitDescriptorDeprecated``
        The flag descriptor to check.
    """
    vampytest.assert_instance(flag_descriptor, FlagBitDescriptorDeprecated)
    vampytest.assert_instance(flag_descriptor.deprecation, FlagDeprecation)
    vampytest.assert_instance(flag_descriptor.shift, int)
    vampytest.assert_instance(flag_descriptor.mask, int)
    vampytest.assert_instance(flag_descriptor.flag_name, str)
    vampytest.assert_instance(flag_descriptor.type_name, str)


def test__flag_descriptors__new():
    """
    Tests whether ``FlagBitDescriptorDeprecated.__new__`` works as intended.
    """
    shift = 2
    type_name = 'koishi'
    flag_name = 'Kokoro'
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    flag_descriptor = FlagBitDescriptorDeprecated(shift, type_name, flag_name, deprecation)
    _assert_fields_set(flag_descriptor)
    
    vampytest.assert_eq(flag_descriptor.shift, shift)
    vampytest.assert_eq(flag_descriptor.mask, 1 << shift)
    vampytest.assert_eq(flag_descriptor.type_name, type_name)
    vampytest.assert_eq(flag_descriptor.flag_name, flag_name)
    vampytest.assert_eq(flag_descriptor.deprecation, deprecation)


def test__FlagBitDescriptorDeprecated__get__type():
    """
    Tests whether ``FlagBitDescriptorDeprecated.__get__`` works as intended.
    
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
    
    flag_descriptor = FlagBitDescriptorDeprecated(shift, type_name, flag_name, deprecation)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    
    vampytest.assert_instance(output, FlagBitDescriptorDeprecated)
    vampytest.assert_is(output, flag_descriptor)
    vampytest.assert_eq(deprecation.triggered, 0)


def _iter_options__get_instance():
    yield 0, 6, False
    yield 1, 6, True


@vampytest._(vampytest.call_from(_iter_options__get_instance()).returning_last())
def test__FlagBitDescriptorDeprecated__get__instance(shift, instance):
    """
    Tests whether ``FlagBitDescriptorDeprecated.__get__`` works as intended.
    
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
    
    flag_descriptor = FlagBitDescriptorDeprecated(shift, type_name, flag_name, deprecation)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(deprecation.triggered, 1)
    return output


def test__FlagBitDescriptorDeprecated__repr():
    """
    Tests whether ``FlagBitDescriptorDeprecated.__repr__`` works as intended.
    """
    shift = 2
    type_name = 'koishi'
    flag_name = 'Kokoro'
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    flag_descriptor = FlagBitDescriptorDeprecated(shift, type_name, flag_name, deprecation)
    
    output = repr(flag_descriptor)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(flag_descriptor).__name__, output)
    vampytest.assert_in(f'name = {flag_descriptor.name!r}', output)
    vampytest.assert_in(f'shift = {shift!r}', output)
    vampytest.assert_in(f'deprecation = {deprecation!r}', output)


def _iter_options__eq():
    shift = 2
    type_name = 'koishi'
    flag_name = 'Kokoro'
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    keyword_parameters = {
        'shift': shift,
        'type_name': type_name,
        'flag_name': flag_name,
        'deprecation': deprecation,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'shift': 10,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'type_name': 'satori',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flag_name': 'orin',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'deprecation': FlagDeprecation(
                'satori',
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            ),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__FlagBitDescriptorDeprecated__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``FlagBitDescriptorDeprecated.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    flag_descriptor_0 = FlagBitDescriptorDeprecated(**keyword_parameters_0)
    flag_descriptor_1 = FlagBitDescriptorDeprecated(**keyword_parameters_1)
    
    output = flag_descriptor_0 == flag_descriptor_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__properties():
    shift = 2
    type_name = 'koishi'
    flag_name = 'Kokoro'
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    keyword_parameters = {
        'shift': shift,
        'type_name': type_name,
        'flag_name': flag_name,
        'deprecation': deprecation,
    }
    
    yield (
        keyword_parameters,
        FlagBitDescriptorDeprecated.name,
        'name',
        f'{type_name}.{flag_name}',
    )


@vampytest._(vampytest.call_from(_iter_options__properties()).returning_last())
def test__FlagBitDescriptorDeprecated__properties(keyword_parameters, property, case_name):
    """
    Check whether ``FlagBitDescriptorDeprecated`` properties work.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    property : ``Property``
        Property to use.
    
    case_name : `str`
        The cases name. Here because python cant write `__repr__` lmeow.
    
    Returns
    -------
    output : `object`
    """
    flag_descriptor = FlagBitDescriptorDeprecated(**keyword_parameters)
    return property.fget(flag_descriptor)
