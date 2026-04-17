import vampytest

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ..audit_log_entry_change_conversion_group import AuditLogEntryChangeConversionGroup
from ..key_pre_checks import key_pre_check_id


def _test_function_0(value):
    return 6


def _assert_fields_set(group):
    """
    Asserts whether fields are set of the given conversion group.
    
    Parameters
    ----------
    group : ``AuditLogEntryChangeConversionGroup``
        The group pto assert.
    """
    vampytest.assert_instance(group, AuditLogEntryChangeConversionGroup)
    vampytest.assert_instance(group.conversions, tuple)
    vampytest.assert_instance(group.key_pre_checker_conversions, list, nullable = True)
    vampytest.assert_instance(group.key_to_conversion, dict, nullable = True)
    vampytest.assert_instance(group.name_to_conversion, dict, nullable = True)


def test__AuditLogEntryChangeConversionGroup__new():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__new__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion(('komeiji', 'koishi'), 'koishi')
    conversion_1 = AuditLogEntryChangeConversion(('kkhta', ), 'koishi')
    conversion_2 = AuditLogEntryChangeConversion(('kaenbyou', ), 'rin')
    conversion_3 = AuditLogEntryChangeConversion(None, 'okuu')
    conversion_4 = AuditLogEntryChangeConversion(('aya', ), '')
    conversion_5 = AuditLogEntryChangeConversion(
        'satori', 'satori', change_deserialization_key_pre_check = key_pre_check_id,
    )
    
    conversions = [conversion_0, conversion_1, conversion_2, conversion_3, conversion_4, conversion_5]
    
    group = AuditLogEntryChangeConversionGroup(*conversions)
    _assert_fields_set(group)
    
    vampytest.assert_eq(group.conversions, tuple(conversions))
    vampytest.assert_eq(
        group.key_pre_checker_conversions,
        [
            conversion_5,
        ],
    )
    vampytest.assert_eq(
        group.key_to_conversion,
        {
            conversion_0.field_keys[0]: conversion_0,
            conversion_0.field_keys[1]: conversion_0,
            conversion_1.field_keys[0]: conversion_1,
            conversion_2.field_keys[0]: conversion_2,
            conversion_4.field_keys[0]: conversion_4,
        }
    )
    
    vampytest.assert_eq(
        group.name_to_conversion,
        {
            conversion_1.field_name: conversion_1,
            conversion_2.field_name: conversion_2,
            conversion_3.field_name: conversion_3,
            conversion_5.field_name: conversion_5,
        },
    )


def test__AuditLogEntryChangeConversionGroup__repr():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__repr__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion(('komeiji',), 'koishi', value_validator = _test_function_0)
    group = AuditLogEntryChangeConversionGroup(conversion_0)
    
    vampytest.assert_instance(repr(group), str)


def test__AuditLogEntryChangeConversionGroup__hash():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__hash__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion(('komeiji',), 'koishi', value_validator = _test_function_0)
    group = AuditLogEntryChangeConversionGroup(conversion_0)
    
    vampytest.assert_instance(hash(group), int)


def test__AuditLogEntryChangeConversionGroup__eq():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__eq__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion(('komeiji',), 'koishi', value_validator = _test_function_0)
    conversion_1 = AuditLogEntryChangeConversion(('kkhta',), 'koishi', value_deserializer = _test_function_0)
    
    group = AuditLogEntryChangeConversionGroup(conversion_0)
    vampytest.assert_eq(group, group)
    vampytest.assert_ne(group, object())
    
    test_group = AuditLogEntryChangeConversionGroup(conversion_1)
    vampytest.assert_ne(group, test_group)


def _iter_options__iter_field_keys():
    conversion_0 = AuditLogEntryChangeConversion(('komeiji', 'koishi'), 'koishi')
    conversion_1 = AuditLogEntryChangeConversion(('kkhta', ), 'koishi')
    conversion_2 = AuditLogEntryChangeConversion(None, 'okuu')
    
    yield AuditLogEntryChangeConversionGroup(conversion_0), ['komeiji', 'koishi']
    yield AuditLogEntryChangeConversionGroup(conversion_1), ['kkhta']
    yield AuditLogEntryChangeConversionGroup(conversion_2), []
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1, conversion_2), ['komeiji', 'koishi', 'kkhta']


@vampytest._(vampytest.call_from(_iter_options__iter_field_keys()).returning_last())
def test__AuditLogEntryChangeConversionGroup__iter_field_keys(group):
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.iter_field_keys`` works as intended.
    
    Parameters
    ----------
    group : ``AuditLogEntryChangeConversionGroup``
        The group to iterate its keys of.
    
    Returns
    -------
    output : `list<str>`
    """
    return [*group.iter_field_keys()]


def _iter_options__get_conversion_for_key():
    conversion_0 = AuditLogEntryChangeConversion(('komeiji', 'koishi'), 'koishi')
    conversion_1 = AuditLogEntryChangeConversion(('kkhta', ), 'koishi')
    conversion_2 = AuditLogEntryChangeConversion(
        'satori', 'okuu', change_deserialization_key_pre_check = key_pre_check_id
    )
    
    yield AuditLogEntryChangeConversionGroup(), 'koishi', None
    yield AuditLogEntryChangeConversionGroup(conversion_0), 'koishi', conversion_0
    yield AuditLogEntryChangeConversionGroup(conversion_0), 'komeiji', conversion_0
    yield AuditLogEntryChangeConversionGroup(conversion_0), 'satori', None
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1), 'koishi', conversion_0
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1), 'kkhta', conversion_1
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1, conversion_2), 'satori', None
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1, conversion_2), '202311170000', conversion_2


@vampytest._(vampytest.call_from(_iter_options__get_conversion_for_key()).returning_last())
def test__AuditLogEntryChangeConversionGroup__get_conversion_for_key(group, key):
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.get_conversion_for_key`` works as intended.
    
    Parameters
    ----------
    group : ``AuditLogEntryChangeConversionGroup``
        The group to iterate its keys of.
    
    Returns
    -------
    conversion : `None | AuditLogEntryChangeConversion`
    """
    return group.get_conversion_for_key(key)


def _iter_options__get_conversion_for_name():
    conversion_0 = AuditLogEntryChangeConversion(('komeiji', 'koishi'), 'koishi')
    conversion_1 = AuditLogEntryChangeConversion(('kkhta', ), 'koishi')
    conversion_2 = AuditLogEntryChangeConversion(
        'satori', 'okuu', change_deserialization_key_pre_check = key_pre_check_id
    )
    
    yield AuditLogEntryChangeConversionGroup(), 'koishi', None
    yield AuditLogEntryChangeConversionGroup(conversion_0), 'koishi', conversion_0
    yield AuditLogEntryChangeConversionGroup(conversion_0), 'komeiji', None
    yield AuditLogEntryChangeConversionGroup(conversion_0), 'satori', None
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1), 'koishi', conversion_1
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1), 'kkhta', None
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1, conversion_2), 'okuu', conversion_2
    yield AuditLogEntryChangeConversionGroup(conversion_0, conversion_1, conversion_2), '202311170000', None


@vampytest._(vampytest.call_from(_iter_options__get_conversion_for_name()).returning_last())
def test__AuditLogEntryChangeConversionGroup__get_conversion_for_name(group, name):
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.get_conversion_for_name`` works as intended.
    
    Parameters
    ----------
    group : ``AuditLogEntryChangeConversionGroup``
        The group to iterate its names of.
    
    Returns
    -------
    conversion : `None | AuditLogEntryChangeConversion`
    """
    return group.get_conversion_for_name(name)
