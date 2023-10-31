import vampytest

from ..guild import DELETE_MESSAGE_DURATION_CONVERSION, GUILD_CONVERSIONS, USERS_REMOVED_CONVERSION


def test__GUILD_CONVERSIONS():
    """
    Tests whether `GUILD_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*GUILD_CONVERSIONS.get_converters.keys()},
        {'delete_message_seconds', 'delete_message_days', 'members_removed'}
    )


# ---- delete_message_duration ----

def _iter_options__delete_message_duration__get_converter():
    delete_message_duration = 123
    yield 0, 0
    yield delete_message_duration, delete_message_duration


@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__get_converter()).returning_last())
def test__DELETE_MESSAGE_DURATION_CONVERSION__get_converter(input_value):
    """
    Tests whether `DELETE_MESSAGE_DURATION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return DELETE_MESSAGE_DURATION_CONVERSION.get_converter(input_value)


def _iter_options__delete_message_duration__put_converter():
    delete_message_duration = 123
    yield 0, 0
    yield delete_message_duration, delete_message_duration


@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__put_converter()).returning_last())
def test__DELETE_MESSAGE_DURATION_CONVERSION__put_converter(input_value):
    """
    Tests whether `DELETE_MESSAGE_DURATION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return DELETE_MESSAGE_DURATION_CONVERSION.put_converter(input_value)


def _iter_options__delete_message_duration__validator__passing():
    delete_message_duration = 1123
    yield 0, 0
    yield delete_message_duration, delete_message_duration


def _iter_options__delete_message_duration__validator__type_error():
    yield 12.6


def _iter_options__delete_message_duration__validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__validator__value_error()).raising(ValueError))
def test__DELETE_MESSAGE_DURATION_CONVERSION__validator(input_value):
    """
    Tests whether `DELETE_MESSAGE_DURATION_CONVERSION.validator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return DELETE_MESSAGE_DURATION_CONVERSION.validator(input_value)


# ---- users_removed ----

def _iter_options__users_removed__get_converter():
    users_removed = 123
    yield 0, 0
    yield users_removed, users_removed


@vampytest._(vampytest.call_from(_iter_options__users_removed__get_converter()).returning_last())
def test__USERS_REMOVED_CONVERSION__get_converter(input_value):
    """
    Tests whether `USERS_REMOVED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return USERS_REMOVED_CONVERSION.get_converter(input_value)


def _iter_options__users_removed__put_converter():
    users_removed = 123
    yield 0, 0
    yield users_removed, users_removed


@vampytest._(vampytest.call_from(_iter_options__users_removed__put_converter()).returning_last())
def test__USERS_REMOVED_CONVERSION__put_converter(input_value):
    """
    Tests whether `USERS_REMOVED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return USERS_REMOVED_CONVERSION.put_converter(input_value)


def _iter_options__users_removed__validator__passing():
    users_removed = 1123
    yield 0, 0
    yield users_removed, users_removed


def _iter_options__users_removed__validator__type_error():
    yield 12.6


def _iter_options__users_removed__validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__users_removed__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__users_removed__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__users_removed__validator__value_error()).raising(ValueError))
def test__USERS_REMOVED_CONVERSION__validator(input_value):
    """
    Tests whether `USERS_REMOVED_CONVERSION.validator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return USERS_REMOVED_CONVERSION.validator(input_value)
