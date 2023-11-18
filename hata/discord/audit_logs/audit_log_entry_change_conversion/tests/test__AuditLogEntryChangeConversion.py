from types import FunctionType, MethodType

import vampytest


from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion


def _test_function_0(value):
    return 6


def _test_function_1(value):
    return value


def _test_function_2(value):
    return value * 2


def _test_function_3(value):
    return True


def _test_function_4(value):
    return False


def _test_change_deserializer_0(conversion, entry):
    return
    yield


def _test_change_deserializer_1(conversion, entry):
    return 12
    yield

def _test_change_serializer_0(conversion, data):
    return
    yield


def _test_change_serializer_1(conversion, data):
    return 32
    yield


def _test_value_merger_0(value_0, value_1):
    return 1


def _test_value_merger_1(value_0, value_1):
    return 2


def _assert_fields_set(conversion):
    """
    Asserts whether fields are set of the given conversion.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to check.
    """
    vampytest.assert_instance(conversion, AuditLogEntryChangeConversion)
    vampytest.assert_instance(conversion.change_deserialization_key_pre_check, FunctionType, MethodType, nullable = True)
    vampytest.assert_instance(conversion.change_deserializer, FunctionType, MethodType)
    vampytest.assert_instance(conversion.change_serializer, FunctionType, MethodType)
    vampytest.assert_instance(conversion.field_keys, tuple, nullable = True)
    vampytest.assert_instance(conversion.field_name, str)
    vampytest.assert_instance(conversion.value_deserializer, FunctionType, MethodType, nullable = True)
    vampytest.assert_instance(conversion.value_merger, FunctionType, MethodType, nullable = True)
    vampytest.assert_instance(conversion.value_serializer, FunctionType, MethodType, nullable = True)
    vampytest.assert_instance(conversion.value_validator, FunctionType, MethodType, nullable = True)


def test__AuditLogEntryChangeConversion__new__minimal_fields():
    """
    Tests whether ``AuditLogEntryChangeConversion.__new__`` works as intended.
    
    Case: Minimal fields.
    """
    field_keys = ('koishi', )
    field_name = 'komeiji'
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_keys, field_keys)
    vampytest.assert_eq(conversion.field_name, field_name)


def test__AuditLogEntryChangeConversion__new__all_fields():
    """
    Tests whether ``AuditLogEntryChangeConversion.__new__`` works as intended.
    
    Case: All fields given.
    """
    field_keys = ('koishi',)
    field_name = 'komeiji'
    
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    change_deserializer = _test_change_deserializer_0
    change_serializer = _test_change_serializer_0
    change_deserialization_key_pre_check = _test_function_3
    value_merger = _test_value_merger_0
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
        change_deserialization_key_pre_check = change_deserialization_key_pre_check,
        change_deserializer = change_deserializer,
        change_serializer = change_serializer,
        value_deserializer = value_deserializer,
        value_merger = value_merger,
        value_serializer = value_serializer,
        value_validator = value_validator,
    )
    
    _assert_fields_set(conversion)
    
    vampytest.assert_eq(conversion.field_keys, field_keys)
    vampytest.assert_eq(conversion.field_name, field_name)
    vampytest.assert_is(conversion.change_deserialization_key_pre_check, change_deserialization_key_pre_check)
    vampytest.assert_is(conversion.change_deserializer, change_deserializer)
    vampytest.assert_is(conversion.change_serializer, change_serializer)
    vampytest.assert_is(conversion.value_deserializer, value_deserializer)
    vampytest.assert_is(conversion.value_merger, value_merger)
    vampytest.assert_is(conversion.value_serializer, value_serializer)
    vampytest.assert_is(conversion.value_validator, value_validator)


def test__AuditLogEntryChangeConversion__repr():
    """
    Tests whether ``AuditLogEntryChangeConversion.__repr__`` works as intended.
    """
    field_keys = ('koishi',)
    field_name = 'komeiji'
    
    change_deserialization_key_pre_check = _test_function_3
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    change_deserializer = _test_change_deserializer_0
    change_serializer = _test_change_serializer_0
    value_merger = _test_value_merger_0
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
        change_deserialization_key_pre_check = change_deserialization_key_pre_check,
        change_deserializer = change_deserializer,
        change_serializer = change_serializer,
        value_deserializer = value_deserializer,
        value_merger = value_merger,
        value_serializer = value_serializer,
        value_validator = value_validator,
    )
    
    vampytest.assert_instance(repr(conversion), str)


def test__AuditLogEntryChangeConversion__hash():
    """
    Tests whether ``AuditLogEntryChangeConversion.__repr__`` works as intended.
    """
    field_keys = ('koishi',)
    field_name = 'komeiji'
    
    change_deserialization_key_pre_check = _test_function_3
    change_deserializer = _test_change_deserializer_0
    change_serializer = _test_change_serializer_0
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    value_merger = _test_value_merger_0
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
        change_deserialization_key_pre_check = change_deserialization_key_pre_check,
        change_deserializer = change_deserializer,
        change_serializer = change_serializer,
        value_deserializer = value_deserializer,
        value_merger = value_merger,
        value_serializer = value_serializer,
        value_validator = value_validator,
    )
    
    vampytest.assert_instance(hash(conversion), int)


def test__AuditLogEntryChangeConversion__eq():
    """
    Tests whether ``AuditLogEntryChangeConversion.__eq__`` works as intended.
    """
    field_keys = ('koishi',)
    field_name = 'komeiji'
    
    change_deserialization_key_pre_check = _test_function_3
    change_deserializer = _test_change_deserializer_0
    change_serializer = _test_change_serializer_0
    value_deserializer = _test_function_0
    value_serializer = _test_function_1
    value_validator = _test_function_2
    value_merger = _test_value_merger_0
    
    keyword_parameters = {
        'change_deserialization_key_pre_check': change_deserialization_key_pre_check,
        'field_keys': field_keys,
        'field_name': field_name,
        'change_deserializer': change_deserializer,
        'change_serializer': change_serializer,
        'value_deserializer': value_deserializer,
        'value_serializer': value_serializer,
        'value_validator': value_validator,
        'value_merger': value_merger,
    }
    
    conversion = AuditLogEntryChangeConversion(**keyword_parameters)
    vampytest.assert_eq(conversion, conversion)
    vampytest.assert_ne(conversion, object())
    
    for field_name, field_value in (
        ('field_keys', ('Kaenbyou',)),
        ('field_name', 'Rin'),
        ('change_deserialization_key_pre_check', _test_function_4),
        ('change_deserializer', _test_change_deserializer_1),
        ('change_serializer', _test_change_serializer_1),
        ('value_deserializer', _test_function_3),
        ('value_serializer', _test_function_3),
        ('value_validator', _test_function_3),
        ('value_merger', _test_value_merger_1),
    ):
        test_conversion = AuditLogEntryChangeConversion(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(conversion, test_conversion)


def test__AuditLogEntryChangeConversion__set_value_deserializer():
    """
    Tests whether ``AuditLogEntryChangeConversion.set_value_deserializer`` works as intended.
    """
    field_keys = ('koishi',)
    field_name = 'komeiji'
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_value_deserializer(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.value_deserializer, function)


def test__AuditLogEntryChangeConversion__set_value_serializer():
    """
    Tests whether ``AuditLogEntryChangeConversion.set_value_serializer`` works as intended.
    """
    field_keys = ('koishi', )
    field_name = 'komeiji'
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_value_serializer(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.value_serializer, function)


def test__AuditLogEntryChangeConversion__set_value_validator():
    """
    Tests whether ``AuditLogEntryChangeConversion.set_value_validator`` works as intended.
    """
    field_keys = ('koishi', )
    field_name = 'komeiji'
    
    conversion = AuditLogEntryChangeConversion(
        field_keys,
        field_name,
    )
    
    function = _test_function_3
    
    output = conversion.set_value_validator(function)
    vampytest.assert_is(output, function)
    vampytest.assert_is(conversion.value_validator, function)


def _iter_options__iter_field_keys():
    yield None, []
    yield ('koishi',), ['koishi']
    yield ('komeiji', 'koishi'), ['komeiji', 'koishi']


@vampytest._(vampytest.call_from(_iter_options__iter_field_keys()).returning_last())
def test__AuditLogEntryChangeConversion__iter_field_keys(field_keys):
    """
    Tests whether ``AuditLogEntryChangeConversion.iter_field_keys`` works as intended.
    
    Parameters
    ----------
    field_keys : `None | tuple<str>`
        Field keys to use.
    
    Returns
    -------
    output : `list<str>`
    """
    conversion = AuditLogEntryChangeConversion(field_keys, '')
    return [*conversion.iter_field_keys()]


def _iter_options__get_field_key():
    yield None, 0, None
    yield ('komeiji', 'koishi'), -1, None
    yield ('komeiji', 'koishi'), 0, 'komeiji'
    yield ('komeiji', 'koishi'), 1, 'koishi'
    yield ('komeiji', 'koishi'), 2, None


@vampytest._(vampytest.call_from(_iter_options__get_field_key()).returning_last())
def test__AuditLogEntryChangeConversion__get_field_key(field_keys, index):
    """
    Tests whether ``AuditLogEntryChangeConversion.get_field_key`` works as intended.
    
    Parameters
    ----------
    field_keys : `None | tuple<str>`
        Field keys to use.
    index : `int`
        Index to get.
    
    Returns
    -------
    output : `None | str`
    """
    conversion = AuditLogEntryChangeConversion(field_keys, '')
    return conversion.get_field_key(index)


def _iter_options__should_add_as_key_based_deserializer():
    yield None, None, False
    yield ('komeiji',), None, True
    yield None, _test_function_3, False
    yield ('komeiji',), _test_function_3, False


@vampytest._(vampytest.call_from(_iter_options__should_add_as_key_based_deserializer()).returning_last())
def test__AuditLogEntryChangeConversion__should_add_as_key_based_deserializer(
    field_keys, change_deserialization_key_pre_check
):
    """
    Tests whether ``AuditLogEntryChangeConversion.should_add_as_key_based_deserializer`` works as intended.
    
    Parameters
    ----------
    field_keys : `None | tuple<str>`
        Field keys to use.
    change_deserialization_key_pre_check : `None | FunctionType | MethodType`
        In case the deserialization is not key matched, this can be used to match the keys instead.
        
    Returns
    -------
    output : `bool`
    """
    conversion = AuditLogEntryChangeConversion(
        field_keys, '', change_deserialization_key_pre_check = change_deserialization_key_pre_check,
    )
    return conversion.should_add_as_key_based_deserializer()


def _iter_options__should_add_as_key_pre_check_deserializer():
    yield None, None, False
    yield ('komeiji',), None, False
    yield None, _test_function_3, True
    yield ('komeiji',), _test_function_3, True


@vampytest._(vampytest.call_from(_iter_options__should_add_as_key_pre_check_deserializer()).returning_last())
def test__AuditLogEntryChangeConversion__should_add_as_key_pre_check_deserializer(
    field_keys, change_deserialization_key_pre_check
):
    """
    Tests whether ``AuditLogEntryChangeConversion.should_add_as_key_pre_check_deserializer`` works as intended.
    
    Parameters
    ----------
    field_keys : `None | tuple<str>`
        Field keys to use.
    change_deserialization_key_pre_check : `None | FunctionType | MethodType`
        In case the deserialization is not key matched, this can be used to match the keys instead.
        
    Returns
    -------
    output : `bool`
    """
    conversion = AuditLogEntryChangeConversion(
        field_keys, '', change_deserialization_key_pre_check = change_deserialization_key_pre_check
    )
    return conversion.should_add_as_key_pre_check_deserializer()


def _iter_options__should_add_by_field_name():
    yield '', False
    yield 'koishi', True


@vampytest._(vampytest.call_from(_iter_options__should_add_by_field_name()).returning_last())
def test__AuditLogEntryChangeConversion__should_add_by_field_name(field_name):
    """
    Tests whether ``AuditLogEntryChangeConversion.should_add_by_field_name`` works as intended.
    
    Parameters
    ----------
    field_keys : `str`
        Field name to use.
        
    Returns
    -------
    output : `bool`
    """
    conversion = AuditLogEntryChangeConversion(None, field_name)
    return conversion.should_add_by_field_name()
