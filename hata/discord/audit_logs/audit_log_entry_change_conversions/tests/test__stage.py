import vampytest

from ....scheduled_event import PrivacyLevel
from ....stage.stage.fields import validate_privacy_level, validate_topic

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_description, value_serializer_description

from ..stage import PRIVACY_LEVEL_CONVERSION, STAGE_CONVERSIONS, TOPIC_CONVERSION


def test__STAGE_CONVERSIONS():
    """
    Tests whether `STAGE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(STAGE_CONVERSIONS)
    vampytest.assert_eq(
        {*STAGE_CONVERSIONS.iter_field_keys()},
        {'privacy_level', 'topic'},
    )


# ---- privacy_level ----

def test__PRIVACY_LEVEL_CONVERSION__generic():
    """
    Tests whether ``PRIVACY_LEVEL_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(PRIVACY_LEVEL_CONVERSION)
    vampytest.assert_is(PRIVACY_LEVEL_CONVERSION.value_validator, validate_privacy_level)


def _iter_options__privacy_level__value_deserializer():
    yield None, PrivacyLevel.none
    yield PrivacyLevel.public.value, PrivacyLevel.public


@vampytest._(vampytest.call_from(_iter_options__privacy_level__value_deserializer()).returning_last())
def test__PRIVACY_LEVEL_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `PRIVACY_LEVEL_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``PrivacyLevel``
    """
    return PRIVACY_LEVEL_CONVERSION.value_deserializer(input_value)


def _iter_options__privacy_level__value_serializer():
    yield PrivacyLevel.none, PrivacyLevel.none.value
    yield PrivacyLevel.public, PrivacyLevel.public.value


@vampytest._(vampytest.call_from(_iter_options__privacy_level__value_serializer()).returning_last())
def test__PRIVACY_LEVEL_CONVERSION__value_serializer(input_value):
    """
    Tests whether `PRIVACY_LEVEL_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``PrivacyLevel``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return PRIVACY_LEVEL_CONVERSION.value_serializer(input_value)


# ---- topic ----

def test__TOPIC_CONVERSION__generic():
    """
    Tests whether ``TOPIC_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TOPIC_CONVERSION)
    vampytest.assert_is(TOPIC_CONVERSION.value_deserializer, value_deserializer_description)
    vampytest.assert_is(TOPIC_CONVERSION.value_serializer, value_serializer_description)
    vampytest.assert_is(TOPIC_CONVERSION.value_validator, validate_topic)
