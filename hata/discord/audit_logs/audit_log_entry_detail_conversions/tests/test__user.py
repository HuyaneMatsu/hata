import vampytest

from ....integration import IntegrationType
from ....integration.integration.fields import validate_type as validate_integration_type
from ....user.voice_state.fields import validate_channel_id

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_id, value_serializer_id

from ..user import (
    CHANNEL_ID_CONVERSION, COUNT_CONVERSION, DELETE_MESSAGE_DURATION_CONVERSION, INTEGRATION_TYPE_CONVERSION,
    USER_CONVERSIONS
)


def test__USER_CONVERSIONS():
    """
    Tests whether `USER_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(USER_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in USER_CONVERSIONS.conversions},
        {'delete_message_seconds', 'delete_message_days', 'count', 'integration_type', 'channel_id'},
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CHANNEL_ID_CONVERSION)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_validator, validate_channel_id)


# ---- count ----

def test__COUNT_CONVERSION__generic():
    """
    Tests whether ``COUNT_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(COUNT_CONVERSION)
    vampytest.assert_is(COUNT_CONVERSION.value_serializer, None)


def _iter_options__count__value_deserializer():
    count = 123
    yield 0, 0
    yield count, count
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__count__value_deserializer()).returning_last())
def test__COUNT_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `COUNT_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return COUNT_CONVERSION.value_deserializer(input_value)


def _iter_options__count__value_validator__passing():
    count = 1123
    yield 0, 0
    yield count, count


def _iter_options__count__value_validator__type_error():
    yield 12.6


def _iter_options__count__value_validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__count__value_validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__count__value_validator__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__count__value_validator__value_error()).raising(ValueError))
def test__COUNT_CONVERSION__value_validator(input_value):
    """
    Tests whether `COUNT_CONVERSION.value_validator` works as intended.
    
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
    return COUNT_CONVERSION.value_validator(input_value)


# ---- delete_message_duration ----

def test__DELETE_MESSAGE_DURATION_CONVERSION__generic():
    """
    Tests whether ``DELETE_MESSAGE_DURATION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DELETE_MESSAGE_DURATION_CONVERSION)
    vampytest.assert_is(DELETE_MESSAGE_DURATION_CONVERSION.value_serializer, None)


def _iter_options__delete_message_duration__value_deserializer():
    delete_message_duration = 123
    yield 0, 0
    yield delete_message_duration, delete_message_duration
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__value_deserializer()).returning_last())
def test__DELETE_MESSAGE_DURATION_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `DELETE_MESSAGE_DURATION_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return DELETE_MESSAGE_DURATION_CONVERSION.value_deserializer(input_value)


def _iter_options__delete_message_duration__value_validator__passing():
    delete_message_duration = 1123
    yield 0, 0
    yield delete_message_duration, delete_message_duration


def _iter_options__delete_message_duration__value_validator__type_error():
    yield 12.6


def _iter_options__delete_message_duration__value_validator__value_error():
    yield -12


@vampytest._(vampytest.call_from(_iter_options__delete_message_duration__value_validator__passing()).returning_last())
@vampytest._(
    vampytest.call_from(_iter_options__delete_message_duration__value_validator__type_error()).raising(TypeError)
)
@vampytest._(
    vampytest.call_from(_iter_options__delete_message_duration__value_validator__value_error()).raising(ValueError)
)
def test__DELETE_MESSAGE_DURATION_CONVERSION__value_validator(input_value):
    """
    Tests whether `DELETE_MESSAGE_DURATION_CONVERSION.value_validator` works as intended.
    
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
    return DELETE_MESSAGE_DURATION_CONVERSION.value_validator(input_value)


# ---- integration_type ----

def test__INTEGRATION_TYPE_CONVERSION__generic():
    """
    Tests whether ``INTEGRATION_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(INTEGRATION_TYPE_CONVERSION)
    # vampytest.assert_is(INTEGRATION_TYPE_CONVERSION.value_deserializer, )
    # vampytest.assert_is(INTEGRATION_TYPE_CONVERSION.value_serializer, )
    vampytest.assert_is(INTEGRATION_TYPE_CONVERSION.value_validator, validate_integration_type)


def _iter_options__integration_type__value_deserializer():
    yield None, IntegrationType.none
    yield IntegrationType.discord.value, IntegrationType.discord


@vampytest._(vampytest.call_from(_iter_options__integration_type__value_deserializer()).returning_last())
def test__INTEGRATION_TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `INTEGRATION_TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``IntegrationType``
    """
    return INTEGRATION_TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__integration_type__value_serializer():
    yield IntegrationType.none, IntegrationType.none.value
    yield IntegrationType.discord, IntegrationType.discord.value


@vampytest._(vampytest.call_from(_iter_options__integration_type__value_serializer()).returning_last())
def test__INTEGRATION_TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `INTEGRATION_TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``IntegrationType``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return INTEGRATION_TYPE_CONVERSION.value_serializer(input_value)
