from types import FunctionType

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
    vampytest.assert_instance(conversion.get_converter, FunctionType)
    vampytest.assert_instance(conversion.put_converter, FunctionType)
    vampytest.assert_instance(conversion.validator, FunctionType)


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
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
        get_converter = get_converter,
        put_converter = put_converter,
        validator = validator,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_key, field_key)
    vampytest.assert_eq(conversion.field_name, field_name)
    vampytest.assert_is(conversion.get_converter, get_converter)
    vampytest.assert_is(conversion.put_converter, put_converter)
    vampytest.assert_is(conversion.validator, validator)


def test__AuditLogEntryDetailConversion__repr():
    """
    Tests whether ``AuditLogEntryDetailConversion.__repr__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
        get_converter = get_converter,
        put_converter = put_converter,
        validator = validator,
    )
    
    vampytest.assert_instance(repr(conversion), str)


def test__AuditLogEntryDetailConversion__hash():
    """
    Tests whether ``AuditLogEntryDetailConversion.__repr__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
        get_converter = get_converter,
        put_converter = put_converter,
        validator = validator,
    )
    
    vampytest.assert_instance(hash(conversion), int)


def test__AuditLogEntryDetailConversion__eq():
    """
    Tests whether ``AuditLogEntryDetailConversion.__eq__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    keyword_parameters = {
        'field_key': field_key,
        'field_name': field_name,
        'get_converter': get_converter,
        'put_converter': put_converter,
        'validator': validator,
    }
    
    conversion = AuditLogEntryDetailConversion(**keyword_parameters)
    vampytest.assert_eq(conversion, conversion)
    vampytest.assert_ne(conversion, object())
    
    for field_name, field_value in (
        ('field_key', 'Kaenbyou'),
        ('field_name', 'Rin'),
        ('get_converter', _test_function_3),
        ('put_converter', _test_function_3),
        ('validator', _test_function_3),
    ):
        test_conversion = AuditLogEntryDetailConversion(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(conversion, test_conversion)


def test__AuditLogEntryDetailConversion__set_get_converter():
    """
    Tests whether ``AuditLogEntryDetailConversion.set_get_converter`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_get_converter(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.get_converter, function)


def test__AuditLogEntryDetailConversion__set_put_converter():
    """
    Tests whether ``AuditLogEntryDetailConversion.set_put_converter`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_put_converter(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.put_converter, function)


def test__AuditLogEntryDetailConversion__set_validator():
    """
    Tests whether ``AuditLogEntryDetailConversion.set_validator`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    
    conversion = AuditLogEntryDetailConversion(
        field_key,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_validator(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.validator, function)
