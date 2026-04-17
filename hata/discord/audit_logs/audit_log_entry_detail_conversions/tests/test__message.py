import vampytest

from ....message.message.fields import validate_channel_id, validate_id

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_id, value_serializer_id

from ..message import CHANNEL_ID_CONVERSION, COUNT_CONVERSION, ID_CONVERSION, MESSAGE_CONVERSIONS


def test__MESSAGE_CONVERSIONS():
    """
    Tests whether `MESSAGE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(MESSAGE_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in MESSAGE_CONVERSIONS.conversions},
        {'channel_id', 'count', 'message_id'}
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
    output = COUNT_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, int)
    return output


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
    output = COUNT_CONVERSION.value_validator(input_value)
    vampytest.assert_instance(output, int)
    return output


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ID_CONVERSION)
    vampytest.assert_is(ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(ID_CONVERSION.value_validator, validate_id)
