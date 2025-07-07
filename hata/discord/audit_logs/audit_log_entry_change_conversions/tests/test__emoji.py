import vampytest

from ....emoji.emoji.fields import validate_available, validate_name, validate_role_ids

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    value_deserializer_ids, value_deserializer_name, value_serializer_ids, value_serializer_name
)

from ..emoji import AVAILABLE_CONVERSION, EMOJI_CONVERSIONS, NAME_CONVERSION, ROLE_IDS_CONVERSION


def test__EMOJI_CONVERSIONS():
    """
    Tests whether `EMOJI_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(EMOJI_CONVERSIONS)
    vampytest.assert_eq(
        {*EMOJI_CONVERSIONS.iter_field_keys()},
        {'available', 'name', 'roles'},
    )


# ---- available ----

def test__AVAILABLE_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(AVAILABLE_CONVERSION)
    vampytest.assert_is(AVAILABLE_CONVERSION.value_serializer, None)
    vampytest.assert_is(AVAILABLE_CONVERSION.value_validator, validate_available)


def _iter_options__available__value_deserializer():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__available__value_deserializer()).returning_last())
def test__AVAILABLE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `AVAILABLE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    output = AVAILABLE_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, bool)
    return output


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- role_ids ----

def test__ROLE_IDS_CONVERSION__generic():
    """
    Tests whether ``ROLE_IDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ROLE_IDS_CONVERSION)
    vampytest.assert_is(ROLE_IDS_CONVERSION.value_deserializer, value_deserializer_ids)
    vampytest.assert_is(ROLE_IDS_CONVERSION.value_serializer, value_serializer_ids)
    vampytest.assert_is(ROLE_IDS_CONVERSION.value_validator, validate_role_ids)
