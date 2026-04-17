import vampytest

from ....soundboard.soundboard_sound.fields import (
    validate_available, validate_emoji, validate_id, validate_name, validate_user_id, validate_volume
)

from ...audit_log_entry_change_conversion.change_deserializers import (
    change_deserializer_deprecation, change_deserializer_flattened_emoji
)
from ...audit_log_entry_change_conversion.change_serializers import change_serializer_flattened_emoji
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...audit_log_entry_change_conversion.value_mergers import value_merger_replace
from ...conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name
)

from ..soundboard_sound import (
    AVAILABLE_CONVERSION, EMOJI_CONVERSION, ID_CONVERSION, ID_CONVERSION_IGNORED, NAME_CONVERSION,
    SOUNDBOARD_SOUND_CONVERSIONS, USER_ID_CONVERSION, VOLUME_CONVERSION
)


def test__SOUNDBOARD_SOUND_CONVERSIONS():
    """
    Tests whether `SOUNDBOARD_SOUND_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(SOUNDBOARD_SOUND_CONVERSIONS)
    vampytest.assert_eq(
        {*SOUNDBOARD_SOUND_CONVERSIONS.iter_field_keys()},
        {'available', 'user_id', 'name', 'volume', 'id', 'sound_id', 'emoji_id', 'emoji_name'},
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
    return AVAILABLE_CONVERSION.value_deserializer(input_value)


# ---- emoji ----


def test__EMOJI_CONVERSION__generic():
    """
    Tests whether ``EMOJI_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EMOJI_CONVERSION)
    vampytest.assert_is(EMOJI_CONVERSION.value_validator, validate_emoji)
    vampytest.assert_is(EMOJI_CONVERSION.change_deserializer, change_deserializer_flattened_emoji)
    vampytest.assert_is(EMOJI_CONVERSION.change_serializer, change_serializer_flattened_emoji)
    vampytest.assert_is(EMOJI_CONVERSION.value_merger, value_merger_replace)


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ID_CONVERSION)
    vampytest.assert_is(ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(ID_CONVERSION.value_validator, validate_id)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- volume ----

def test__VOLUME_CONVERSION__generic():
    """
    Tests whether ``VOLUME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(VOLUME_CONVERSION)
    vampytest.assert_is(VOLUME_CONVERSION.value_serializer, None)
    vampytest.assert_is(VOLUME_CONVERSION.value_validator, validate_volume)


def _iter_options__volume__value_deserializer():
    yield 1.0, 1.0
    yield 0.0, 0.0
    yield None, 1.0


@vampytest._(vampytest.call_from(_iter_options__volume__value_deserializer()).returning_last())
def test__VOLUME_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `VOLUME_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `float`
    """
    return VOLUME_CONVERSION.value_deserializer(input_value)


# ---- user_id ----

def test__USER_ID_CONVERSION__generic():
    """
    Tests whether ``USER_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(USER_ID_CONVERSION)
    vampytest.assert_is(USER_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(USER_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(USER_ID_CONVERSION.value_validator, validate_user_id)


# ---- ignored ----

def _iter_options__ignored():
    yield ID_CONVERSION_IGNORED


@vampytest.call_from(_iter_options__ignored())
def test_ignored(conversion):
    """
    Tests whether the ignored conversions are set up as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to test.
    """
    _assert_conversion_fields_set(conversion)
    vampytest.assert_is(conversion.change_deserializer, change_deserializer_deprecation)
    vampytest.assert_eq(conversion.field_name, '')

