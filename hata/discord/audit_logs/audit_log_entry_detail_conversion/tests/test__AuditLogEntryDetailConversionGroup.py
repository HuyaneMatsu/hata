import vampytest

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion
from ..audit_log_entry_detail_conversion_group import AuditLogEntryDetailConversionGroup


def _test_function_0(value):
    return 6


def _assert_fields_set(group):
    """
    Asserts whether fields are set of the given conversion group.
    
    Parameters
    ----------
    group : ``AuditLogEntryDetailConversionGroup``
        The group pto assert.
    """
    vampytest.assert_instance(group, AuditLogEntryDetailConversionGroup)
    vampytest.assert_instance(group.conversions, tuple)
    vampytest.assert_instance(group.key_to_conversion, dict, nullable = True)
    vampytest.assert_instance(group.name_to_conversion, dict, nullable = True)


def test__AuditLogEntryDetailConversionGroup__new():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__new__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', value_validator = _test_function_0)
    conversion_1 = AuditLogEntryDetailConversion('kkhta', 'koishi', value_deserializer = _test_function_0)
    conversion_2 = AuditLogEntryDetailConversion('kaenbyou', 'rin', value_serializer = _test_function_0)
    
    conversions = [conversion_0, conversion_1, conversion_2]
    
    group = AuditLogEntryDetailConversionGroup(*conversions)
    _assert_fields_set(group)
    
    vampytest.assert_eq(group.conversions, tuple(conversions))
    vampytest.assert_eq(
        group.key_to_conversion,
        {
            conversion_0.field_key: conversion_0,
            conversion_1.field_key: conversion_1,
            conversion_2.field_key: conversion_2,
        },
    )
    vampytest.assert_eq(
        group.name_to_conversion,
        {
            conversion_1.field_name: conversion_1,
            conversion_2.field_name: conversion_2,
        },
    )


def test__AuditLogEntryDetailConversionGroup__repr():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__repr__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', value_validator = _test_function_0)
    group = AuditLogEntryDetailConversionGroup(conversion_0)
    
    vampytest.assert_instance(repr(group), str)


def test__AuditLogEntryDetailConversionGroup__hash():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__hash__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', value_validator = _test_function_0)
    group = AuditLogEntryDetailConversionGroup(conversion_0)
    
    vampytest.assert_instance(hash(group), int)


def test__AuditLogEntryDetailConversionGroup__eq():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__eq__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', value_validator = _test_function_0)
    conversion_1 = AuditLogEntryDetailConversion('kkhta', 'koishi', value_deserializer = _test_function_0)
    
    group = AuditLogEntryDetailConversionGroup(conversion_0)
    vampytest.assert_eq(group, group)
    vampytest.assert_ne(group, object())
    
    test_group = AuditLogEntryDetailConversionGroup(conversion_1)
    vampytest.assert_ne(group, test_group)



def _iter_options__get_conversion_for_key():
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi')
    conversion_1 = AuditLogEntryDetailConversion('kkhta', 'koishi')
    conversion_2 = AuditLogEntryDetailConversion('satori', 'okuu')
    
    yield AuditLogEntryDetailConversionGroup(), 'koishi', None
    yield AuditLogEntryDetailConversionGroup(conversion_0), 'koishi', None
    yield AuditLogEntryDetailConversionGroup(conversion_0), 'komeiji', conversion_0
    yield AuditLogEntryDetailConversionGroup(conversion_0), 'satori', None
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1), 'koishi', None
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1), 'kkhta', conversion_1
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1, conversion_2), 'satori', conversion_2
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1, conversion_2), '202311170000', None


@vampytest._(vampytest.call_from(_iter_options__get_conversion_for_key()).returning_last())
def test__AuditLogEntryDetailConversionGroup__get_conversion_for_key(group, key):
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.get_conversion_for_key`` works as intended.
    
    Parameters
    ----------
    group : ``AuditLogEntryDetailConversionGroup``
        The group to iterate its keys of.
    
    Returns
    -------
    conversion : `None | AuditLogEntryDetailConversion`
    """
    return group.get_conversion_for_key(key)


def _iter_options__get_conversion_for_name():
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi')
    conversion_1 = AuditLogEntryDetailConversion('kkhta', 'koishi')
    conversion_2 = AuditLogEntryDetailConversion('satori', 'okuu')
    
    yield AuditLogEntryDetailConversionGroup(), 'koishi', None
    yield AuditLogEntryDetailConversionGroup(conversion_0), 'koishi', conversion_0
    yield AuditLogEntryDetailConversionGroup(conversion_0), 'komeiji', None
    yield AuditLogEntryDetailConversionGroup(conversion_0), 'satori', None
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1), 'koishi', conversion_1
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1), 'kkhta', None
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1, conversion_2), 'okuu', conversion_2
    yield AuditLogEntryDetailConversionGroup(conversion_0, conversion_1, conversion_2), '202311170000', None


@vampytest._(vampytest.call_from(_iter_options__get_conversion_for_name()).returning_last())
def test__AuditLogEntryDetailConversionGroup__get_conversion_for_name(group, name):
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.get_conversion_for_name`` works as intended.
    
    Parameters
    ----------
    group : ``AuditLogEntryDetailConversionGroup``
        The group to iterate its names of.
    
    Returns
    -------
    conversion : `None | AuditLogEntryDetailConversion`
    """
    return group.get_conversion_for_name(name)
