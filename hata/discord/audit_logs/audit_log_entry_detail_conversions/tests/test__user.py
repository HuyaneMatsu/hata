import vampytest

from ....integration import IntegrationType
from ....user.voice_state.fields import validate_channel_id

from ...conversion_helpers.converters import get_converter_id, put_converter_id

from ..user import (
    CHANNEL_ID_CONVERSION, COUNT_CONVERSION, DELETE_MESSAGE_DURATION_CONVERSION, INTEGRATION_TYPE_CONVERSION,
    USER_CONVERSIONS
)


def test__USER_CONVERSIONS():
    """
    Tests whether `USER_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*USER_CONVERSIONS.get_converters.keys()},
        {'delete_message_seconds', 'delete_message_days', 'count', 'integration_type', 'channel_id'},
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- count ----

def _iter_options__count__get_converter():
    count = 123
    yield 0, 0
    yield count, count
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__count__get_converter()).returning_last())
def test__COUNT_CONVERSION__get_converter(input_value):
    """
    Tests whether `COUNT_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return COUNT_CONVERSION.get_converter(input_value)


def _iter_options__count__put_converter():
    count = 123
    yield 0, 0
    yield count, count


@vampytest._(vampytest.call_from(_iter_options__count__put_converter()).returning_last())
def test__COUNT_CONVERSION__put_converter(input_value):
    """
    Tests whether `COUNT_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return COUNT_CONVERSION.put_converter(input_value)


def _iter_options__count__validator__passing():
    count = 1123
    yield 0, 0
    yield count, count


def _iter_options__count__validator__type_error():
    yield 12.6


def _iter_options__count__validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__count__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__count__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__count__validator__value_error()).raising(ValueError))
def test__COUNT_CONVERSION__validator(input_value):
    """
    Tests whether `COUNT_CONVERSION.validator` works as intended.
    
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
    return COUNT_CONVERSION.validator(input_value)


# ---- delete_message_duration ----

def _iter_options__delete_message_duration__get_converter():
    delete_message_duration = 123
    yield 0, 0
    yield delete_message_duration, delete_message_duration
    yield None, 0


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


# ---- integration_type ----

def _iter_options__integration_type__get_converter():
    yield None, IntegrationType.none
    yield IntegrationType.discord.value, IntegrationType.discord


@vampytest._(vampytest.call_from(_iter_options__integration_type__get_converter()).returning_last())
def test__INTEGRATION_TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `INTEGRATION_TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``IntegrationType``
    """
    return INTEGRATION_TYPE_CONVERSION.get_converter(input_value)


def _iter_options__integration_type__put_converter():
    yield IntegrationType.none, IntegrationType.none.value
    yield IntegrationType.discord, IntegrationType.discord.value


@vampytest._(vampytest.call_from(_iter_options__integration_type__put_converter()).returning_last())
def test__INTEGRATION_TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `INTEGRATION_TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``IntegrationType``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return INTEGRATION_TYPE_CONVERSION.put_converter(input_value)


def _iter_options__integration_type__validator__passing():
    yield IntegrationType.discord, IntegrationType.discord
    yield IntegrationType.discord.value, IntegrationType.discord


def _iter_options__integration_type__validator__type_error():
    yield 12.6
    yield 12


def _iter_options__integration_type__validator__value_error():
    yield 'pudding'


@vampytest._(vampytest.call_from(_iter_options__integration_type__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__integration_type__validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__integration_type__validator__value_error()).raising(ValueError))
def test__INTEGRATION_TYPE_CONVERSION__validator(input_value):
    """
    Tests whether `INTEGRATION_TYPE_CONVERSION.validator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``IntegrationType``
    
    Raises
    ------
    TypeError
    ValueError
    """
    return INTEGRATION_TYPE_CONVERSION.validator(input_value)
