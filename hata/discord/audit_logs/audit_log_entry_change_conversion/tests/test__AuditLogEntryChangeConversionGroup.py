import vampytest

from ...audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_REMOVAL

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ..audit_log_entry_change_conversion_group import AuditLogEntryChangeConversionGroup


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
    vampytest.assert_instance(group.get_converters, dict)
    vampytest.assert_instance(group.put_converters, dict)
    vampytest.assert_instance(group.validators, dict)


def test__AuditLogEntryChangeConversionGroup__new():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__new__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion('komeiji', 'koishi', FLAG_IS_ADDITION, validator = _test_function_0)
    conversion_1 = AuditLogEntryChangeConversion('kkhta', 'koishi', FLAG_IS_REMOVAL, get_converter = _test_function_0)
    conversion_2 = AuditLogEntryChangeConversion('kaenbyou', 'rin', FLAG_IS_ADDITION, put_converter = _test_function_0)
    
    conversions = [conversion_0, conversion_1, conversion_2]
    
    group = AuditLogEntryChangeConversionGroup(*conversions)
    _assert_fields_set(group)
    
    vampytest.assert_eq(group.conversions, tuple(conversions))
    vampytest.assert_eq(
        group.get_converters,
        {
            conversion_0.field_key: (conversion_0.field_name, conversion_0.flags, conversion_0.get_converter),
            conversion_1.field_key: (conversion_1.field_name, conversion_1.flags, conversion_1.get_converter),
            conversion_2.field_key: (conversion_2.field_name, conversion_2.flags, conversion_2.get_converter),
        },
    )
    vampytest.assert_eq(
        group.put_converters,
        {
            (conversion_0.field_name, conversion_0.flags): (conversion_0.field_key, conversion_0.put_converter),
            (conversion_1.field_name, conversion_1.flags): (conversion_1.field_key, conversion_1.put_converter),
            (conversion_2.field_name, conversion_2.flags): (conversion_2.field_key, conversion_2.put_converter),
        },
    )
    vampytest.assert_eq(
        group.validators,
        {
            (conversion_0.field_name, conversion_0.flags): conversion_0.validator,
            (conversion_1.field_name, conversion_1.flags): conversion_1.validator,
            (conversion_2.field_name, conversion_2.flags): conversion_2.validator,
        },
    )


def test__AuditLogEntryChangeConversionGroup__repr():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__repr__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion('komeiji', 'koishi', FLAG_IS_ADDITION, validator = _test_function_0)
    group = AuditLogEntryChangeConversionGroup(conversion_0)
    
    vampytest.assert_instance(repr(group), str)


def test__AuditLogEntryChangeConversionGroup__hash():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__hash__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion('komeiji', 'koishi', FLAG_IS_ADDITION, validator = _test_function_0)
    group = AuditLogEntryChangeConversionGroup(conversion_0)
    
    vampytest.assert_instance(hash(group), int)


def test__AuditLogEntryChangeConversionGroup__eq():
    """
    Tests whether ``AuditLogEntryChangeConversionGroup.__eq__`` works as intended.
    """
    conversion_0 = AuditLogEntryChangeConversion('komeiji', 'koishi', FLAG_IS_ADDITION, validator = _test_function_0)
    conversion_1 = AuditLogEntryChangeConversion('kkhta', 'koishi', FLAG_IS_REMOVAL, get_converter = _test_function_0)
    
    group = AuditLogEntryChangeConversionGroup(conversion_0)
    vampytest.assert_eq(group, group)
    vampytest.assert_ne(group, object())
    
    test_group = AuditLogEntryChangeConversionGroup(conversion_1)
    vampytest.assert_ne(group, test_group)
