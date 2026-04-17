from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..flag_deprecation import FlagDeprecation
from ..flag_descriptors import FlagDescriptor, NAME_UNKNOWN


def _assert_fields_set(flag_descriptor):
    """
    Asserts whether the given flag descriptor has all of its fields set.
    
    Parameters
    ----------
    flag_descriptor : ``FlagDescriptor``
        The flag descriptor to check.
    """
    vampytest.assert_instance(flag_descriptor, FlagDescriptor)
    vampytest.assert_instance(flag_descriptor.deprecation, FlagDeprecation, nullable = True)
    vampytest.assert_instance(flag_descriptor.shift, int)


def test__flag_descriptors__new():
    """
    Tests whether ``FlagDescriptor.__new__`` works as intended.
    """
    shift = 5
    deprecation = FlagDeprecation('koishi', DateTime(2016, 5, 1, tzinfo = TimeZone.utc))
    
    flag_descriptor = FlagDescriptor(shift, deprecation = deprecation)
    _assert_fields_set(flag_descriptor)
    
    vampytest.assert_eq(flag_descriptor.shift, shift)
    vampytest.assert_eq(flag_descriptor.deprecation, deprecation)


def test__flag_descriptors__new__deprecation_disallowed():
    """
    Tests whether ``FlagDescriptor.__new__`` works as intended.
    
    Case: deprecation disallowed.
    """
    shift = 5
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 1, tzinfo = TimeZone.utc),
        trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 4000),
    )
    
    flag_descriptor = FlagDescriptor(shift, deprecation = deprecation)
    _assert_fields_set(flag_descriptor)
    
    vampytest.assert_eq(flag_descriptor.shift, shift)
    vampytest.assert_eq(flag_descriptor.deprecation, None)


def test__FlagDescriptor__get__instance():
    """
    Tests whether ``FlagDescriptor.__get__`` works as intended.
    
    Case: from instance.
    """
    shift = 1
    instance = 3
    instance_type = int
    
    flag_descriptor = FlagDescriptor(shift)
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__FlagDescriptor__repr():
    """
    Tests whether ``FlagDescriptor.__repr__`` works as intended.
    """
    shift = 1
    deprecation = FlagDeprecation('koishi', DateTime(2016, 5, 1, tzinfo = TimeZone.utc))
    
    flag_descriptor = FlagDescriptor(shift, deprecation = deprecation)
    
    output = repr(flag_descriptor)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(flag_descriptor).__name__, output)
    vampytest.assert_in(f'deprecation = {deprecation!r}', output)
    vampytest.assert_in(f'name = {flag_descriptor.name!r}', output)
    vampytest.assert_in(f'shift = {shift!r}', output)


def _iter_options__eq():
    shift = 2
    deprecation = FlagDeprecation('koishi', DateTime(2016, 5, 1, tzinfo = TimeZone.utc))
    
    keyword_parameters = {
        'shift': shift,
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
            'deprecation': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__FlagDescriptor__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``FlagDescriptor.__eq__`` works as intended.
    
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
    flag_descriptor_0 = FlagDescriptor(**keyword_parameters_0)
    flag_descriptor_1 = FlagDescriptor(**keyword_parameters_1)
    
    output = flag_descriptor_0 == flag_descriptor_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__properties():
    shift = 2
    
    keyword_parameters = {
        'shift': shift,
    }
    
    yield (
        keyword_parameters,
        FlagDescriptor.flag_name,
        'flag_name',
        NAME_UNKNOWN,
    )
    
    yield (
        keyword_parameters,
        FlagDescriptor.type_name,
        'type_name',
        NAME_UNKNOWN,
    )
    
    yield (
        keyword_parameters,
        FlagDescriptor.mask,
        'mask',
        1 << 2,
    )
    
    yield (
        keyword_parameters,
        FlagDescriptor.name,
        'name',
        f'{NAME_UNKNOWN}.{NAME_UNKNOWN}',
    )


@vampytest._(vampytest.call_from(_iter_options__properties()).returning_last())
def test__FlagDescriptor__properties(keyword_parameters, property, case_name):
    """
    Check whether ``FlagDescriptor`` properties work.
    
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
    flag_descriptor = FlagDescriptor(**keyword_parameters)
    return property.fget(flag_descriptor)
