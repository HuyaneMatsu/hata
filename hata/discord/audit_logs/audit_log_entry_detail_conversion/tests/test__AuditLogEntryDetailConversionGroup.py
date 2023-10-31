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
    vampytest.assert_instance(group.get_converters, dict)
    vampytest.assert_instance(group.put_converters, dict)
    vampytest.assert_instance(group.validators, dict)


def test__AuditLogEntryDetailConversionGroup__new():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__new__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', validator = _test_function_0)
    conversion_1 = AuditLogEntryDetailConversion('kkhta', 'koishi', get_converter = _test_function_0)
    conversion_2 = AuditLogEntryDetailConversion('kaenbyou', 'rin', put_converter = _test_function_0)
    
    conversions = [conversion_0, conversion_1, conversion_2]
    
    group = AuditLogEntryDetailConversionGroup(*conversions)
    _assert_fields_set(group)
    
    vampytest.assert_eq(group.conversions, tuple(conversions))
    vampytest.assert_eq(
        group.get_converters,
        {
            conversion_0.field_key: (conversion_0.field_name, conversion_0.get_converter),
            conversion_1.field_key: (conversion_1.field_name, conversion_1.get_converter),
            conversion_2.field_key: (conversion_2.field_name, conversion_2.get_converter),
        },
    )
    vampytest.assert_eq(
        group.put_converters,
        {
            conversion_0.field_name: (conversion_0.field_key, conversion_0.put_converter),
            conversion_2.field_name: (conversion_2.field_key, conversion_2.put_converter),
        },
    )
    vampytest.assert_eq(
        group.validators,
        {
            conversion_0.field_name: conversion_0.validator,
            conversion_2.field_name: conversion_2.validator,
        },
    )


def test__AuditLogEntryDetailConversionGroup__repr():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__repr__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', validator = _test_function_0)
    group = AuditLogEntryDetailConversionGroup(conversion_0)
    
    vampytest.assert_instance(repr(group), str)


def test__AuditLogEntryDetailConversionGroup__hash():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__hash__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', validator = _test_function_0)
    group = AuditLogEntryDetailConversionGroup(conversion_0)
    
    vampytest.assert_instance(hash(group), int)


def test__AuditLogEntryDetailConversionGroup__eq():
    """
    Tests whether ``AuditLogEntryDetailConversionGroup.__eq__`` works as intended.
    """
    conversion_0 = AuditLogEntryDetailConversion('komeiji', 'koishi', validator = _test_function_0)
    conversion_1 = AuditLogEntryDetailConversion('kkhta', 'koishi', get_converter = _test_function_0)
    
    group = AuditLogEntryDetailConversionGroup(conversion_0)
    vampytest.assert_eq(group, group)
    vampytest.assert_ne(group, object())
    
    test_group = AuditLogEntryDetailConversionGroup(conversion_1)
    vampytest.assert_ne(group, test_group)
