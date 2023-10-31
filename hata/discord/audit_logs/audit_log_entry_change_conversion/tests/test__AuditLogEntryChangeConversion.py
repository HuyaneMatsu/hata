from types import FunctionType

import vampytest

from ...audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_REMOVAL

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion


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
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to check.
    """
    vampytest.assert_instance(conversion, AuditLogEntryChangeConversion)
    vampytest.assert_instance(conversion.field_key, str)
    vampytest.assert_instance(conversion.field_name, str)
    vampytest.assert_instance(conversion.flags, int)
    vampytest.assert_instance(conversion.get_converter, FunctionType)
    vampytest.assert_instance(conversion.put_converter, FunctionType)
    vampytest.assert_instance(conversion.validator, FunctionType)


def test__AuditLogEntryChangeConversion__new__minimal_fields():
    """
    Tests whether ``AuditLogEntryChangeConversion.__new__`` works as intended.
    
    Case: Minimal fields.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_key, field_key)
    vampytest.assert_eq(conversion.field_name, field_name)
    vampytest.assert_eq(conversion.flags, flags)


def test__AuditLogEntryChangeConversion__new__all_fields():
    """
    Tests whether ``AuditLogEntryChangeConversion.__new__`` works as intended.
    
    Case: All fields given.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
        get_converter = get_converter,
        put_converter = put_converter,
        validator = validator,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_key, field_key)
    vampytest.assert_eq(conversion.field_name, field_name)
    vampytest.assert_eq(conversion.flags, flags)
    vampytest.assert_is(conversion.get_converter, get_converter)
    vampytest.assert_is(conversion.put_converter, put_converter)
    vampytest.assert_is(conversion.validator, validator)


def test__AuditLogEntryChangeConversion__repr():
    """
    Tests whether ``AuditLogEntryChangeConversion.__repr__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
        get_converter = get_converter,
        put_converter = put_converter,
        validator = validator,
    )
    
    vampytest.assert_instance(repr(conversion), str)


def test__AuditLogEntryChangeConversion__hash():
    """
    Tests whether ``AuditLogEntryChangeConversion.__repr__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
        get_converter = get_converter,
        put_converter = put_converter,
        validator = validator,
    )
    
    vampytest.assert_instance(hash(conversion), int)


def test__AuditLogEntryChangeConversion__eq():
    """
    Tests whether ``AuditLogEntryChangeConversion.__eq__`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    get_converter = _test_function_0
    put_converter = _test_function_1
    validator = _test_function_2
    
    keyword_parameters = {
        'field_key': field_key,
        'field_name': field_name,
        'flags': flags,
        'get_converter': get_converter,
        'put_converter': put_converter,
        'validator': validator,
    }
    
    conversion = AuditLogEntryChangeConversion(**keyword_parameters)
    vampytest.assert_eq(conversion, conversion)
    vampytest.assert_ne(conversion, object())
    
    for field_name, field_value in (
        ('field_key', 'Kaenbyou'),
        ('field_name', 'Rin'),
        ('flags', FLAG_IS_REMOVAL),
        ('get_converter', _test_function_3),
        ('put_converter', _test_function_3),
        ('validator', _test_function_3),
    ):
        test_conversion = AuditLogEntryChangeConversion(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(conversion, test_conversion)


def test__AuditLogEntryChangeConversion__set_get_converter():
    """
    Tests whether ``AuditLogEntryChangeConversion.set_get_converter`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
    )
    
    function = _test_function_3
    
    output = conversion.set_get_converter(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.get_converter, function)


def test__AuditLogEntryChangeConversion__set_put_converter():
    """
    Tests whether ``AuditLogEntryChangeConversion.set_put_converter`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
    )
    
    function = _test_function_3
    
    output = conversion.set_put_converter(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.put_converter, function)


def test__AuditLogEntryChangeConversion__set_validator():
    """
    Tests whether ``AuditLogEntryChangeConversion.set_validator`` works as intended.
    """
    field_key = 'koishi'
    field_name = 'komeiji'
    flags = FLAG_IS_ADDITION
    
    conversion = AuditLogEntryChangeConversion(
        field_key,
        field_name,
        flags,
    )
    
    function = _test_function_3
    
    output = conversion.set_validator(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.validator, function)
