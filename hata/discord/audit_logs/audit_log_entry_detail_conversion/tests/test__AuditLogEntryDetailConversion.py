from types import FunctionType, MethodType

import vampytest

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion


def _test_function_0(value):
    return 6


def _test_function_1(value):
    return value


def _test_function_2(value):
    return value * 2


def _test_function_3(value):
    return 7


def _assert_fields_set(conversion):
    """
    Asserts whether fields are set of the given conversion.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryDetailConversion``
        The conversion to check.
    """
    vampytest.assert_instance(conversion, AuditLogEntryDetailConversion)
    vampytest.assert_instance(conversion.field_key, str)
    vampytest.assert_instance(conversion.field_name, str)
    vampytest.assert_instance(conversion.value_deserializer, FunctionType, MethodType, nullable = True)
    vampytest.assert_instance(conversion.value_serializer, FunctionType, MethodType, nullable = True)
    vampytest.assert_instance(conversion.value_validator, FunctionType, MethodType, nullable = True)


def test__AuditLogEntryDetailConversion__new__minimal_fields():
    """
    Tests whether ``AuditLogEntryDetailConversion.__new__`` works as intended.
    
    Case: Minimal fields.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_key, field_key)
    vampytest.assert_eq(conversion.field_name, field_name)


def test__AuditLogEntryDetailConversion__new__all_fields():
    """
    Tests whether ``AuditLogEntryDetailConversion.__new__`` works as intended.
    
    Case: All fields given.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
        value_deserializer = value_deserializer,
        value_serializer = value_serializer,
        value_validator = value_validator,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_key, field_key)
    vampytest.assert_eq(conversion.field_name, field_name)
    vampytest.assert_is(conversion.value_deserializer, value_deserializer)
    vampytest.assert_is(conversion.value_serializer, value_serializer)
    vampytest.assert_is(conversion.value_validator, value_validator)


def test__AuditLogEntryDetailConversion__repr():
    """
    Tests whether ``AuditLogEntryDetailConversion.__repr__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
        value_deserializer = value_deserializer,
        value_serializer = value_serializer,
        value_validator = value_validator,
    )
    
    vampytest.assert_instance(repr(conversion), str)


def test__AuditLogEntryDetailConversion__hash():
    """
    Tests whether ``AuditLogEntryDetailConversion.__repr__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
        value_deserializer = value_deserializer,
        value_serializer = value_serializer,
        value_validator = value_validator,
    )
    
    vampytest.assert_instance(hash(conversion), int)


def test__AuditLogEntryDetailConversion__eq():
    """
    Tests whether ``AuditLogEntryDetailConversion.__eq__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    
    keyword_parameters = {
        'field_key': field_key,
        'field_name': field_name,
        'value_deserializer': value_deserializer,
        'value_serializer': value_serializer,
        'value_validator': value_validator,
    }
    
    conversion = AuditLogEntryDetailConversion(**keyword_parameters)
    vampytest.assert_eq(conversion, conversion)
    vampytest.assert_ne(conversion, object())
    
    for field_name, field_value in (
        ('field_key', 'Kaenbyou'),
        ('field_name', 'Rin'),
        ('value_deserializer', _test_function_3),
        ('value_serializer', _test_function_3),
        ('value_validator', _test_function_3),
    ):
        test_conversion = AuditLogEntryDetailConversion(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(conversion, test_conversion)


def test__AuditLogEntryDetailConversion__set_value_deserializer():
    """
    Tests whether ``AuditLogEntryDetailConversion.set_value_deserializer`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_value_deserializer(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.value_deserializer, function)


def test__AuditLogEntryDetailConversion__set_value_serializer():
    """
    Tests whether ``AuditLogEntryDetailConversion.set_value_serializer`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_value_serializer(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.value_serializer, function)


def test__AuditLogEntryDetailConversion__set_value_validator():
    """
    Tests whether ``AuditLogEntryDetailConversion.set_value_validator`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_value_validator(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.value_validator, function)
