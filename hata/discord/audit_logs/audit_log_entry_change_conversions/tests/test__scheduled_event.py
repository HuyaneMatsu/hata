from datetime import datetime as DateTime

import vampytest

from ....bases import Icon
from ....scheduled_event import (
    PrivacyLevel, ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation, ScheduledEventEntityType,
    ScheduledEventStatus
)
from ....scheduled_event.scheduled_event.fields import (
    validate_channel_id, validate_description, validate_end, validate_entity_id, validate_entity_type, validate_name,
    validate_privacy_level, validate_sku_ids, validate_start, validate_status
)
from ....scheduled_event.scheduled_event.scheduled_event import SCHEDULED_EVENT_IMAGE
from ....scheduled_event.scheduled_event_entity_metadata.fields import validate_location
from ....utils import datetime_to_timestamp

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversion
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_deserializer_ids, value_deserializer_name, value_serializer_description,
    value_serializer_id, value_serializer_ids, value_serializer_name
)

from ..scheduled_event import (
    CHANNEL_ID_CONVERSION, DESCRIPTION_CONVERSION, END_CONVERSION, ENTITY_ID_CONVERSION, ENTITY_METADATA_CONVERSION,
    ENTITY_TYPE_CONVERSION, IMAGE_CONVERSION, LOCATION_CONVERSION, NAME_CONVERSION, PRIVACY_LEVEL_CONVERSION,
    SCHEDULED_EVENT_CONVERSIONS, SKU_IDS_CONVERSION, START_CONVERSION, STATUS_CONVERSION
)


def test__SCHEDULED_EVENT_CONVERSIONS():
    """
    Tests whether `SCHEDULED_EVENT_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(SCHEDULED_EVENT_CONVERSIONS)
    vampytest.assert_eq(
        {*SCHEDULED_EVENT_CONVERSIONS.iter_field_keys()},
        {
            'channel_id', 'description', 'entity_id', 'entity_metadata', 'entity_type', 'image_hash', 'location',
            'name', 'privacy_level', 'scheduled_end_time', 'scheduled_start_time', 'sku_ids', 'status',
        },
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


# ---- description ----

def test__DESCRIPTION_CONVERSION__generic():
    """
    Tests whether ``DESCRIPTION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DESCRIPTION_CONVERSION)
    vampytest.assert_is(DESCRIPTION_CONVERSION.value_deserializer, value_deserializer_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.value_serializer, value_serializer_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.value_validator, validate_description)


# ---- entity_id ----

def test__ENTITY_ID_CONVERSION__generic():
    """
    Tests whether ``ENTITY_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ENTITY_ID_CONVERSION)
    vampytest.assert_is(ENTITY_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(ENTITY_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(ENTITY_ID_CONVERSION.value_validator, validate_entity_id)


# ---- entity_metadata ----

def test__ENTITY_METADATA_CONVERSION__generic():
    """
    Tests whether ``ENTITY_METADATA_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ENTITY_METADATA_CONVERSION)


def _iter_options__entity_metadata__value_deserializer():
    yield None, None
    metadata = ScheduledEventEntityMetadataLocation(location = 'koishi')
    yield metadata.to_data(defaults = True), metadata


@vampytest._(vampytest.call_from(_iter_options__entity_metadata__value_deserializer()).returning_last())
def test__ENTITY_METADATA_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `ENTITY_METADATA_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | ScheduledEventEntityMetadataBase`
    """
    return ENTITY_METADATA_CONVERSION.value_deserializer(input_value)


def _iter_options__entity_metadata__value_serializer():
    yield None, None
    
    metadata = ScheduledEventEntityMetadataLocation(location = 'koishi')
    yield metadata, metadata.to_data(defaults = True)


@vampytest._(vampytest.call_from(_iter_options__entity_metadata__value_serializer()).returning_last())
def test__ENTITY_METADATA_CONVERSION__value_serializer(input_value):
    """
    Tests whether `ENTITY_METADATA_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | ScheduledEventEntityMetadataBase`
        Processed value.
    
    Returns
    -------
    output : `None | dict<str, object>`
    """
    return ENTITY_METADATA_CONVERSION.value_serializer(input_value)


def _iter_options__entity_metadata__value_validator__passing():
    yield None, None
    
    metadata = ScheduledEventEntityMetadataLocation(location = 'koishi')
    yield metadata, metadata


def _iter_options__entity_metadata__value_validator__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__entity_metadata__value_validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__entity_metadata__value_validator__type_error()).raising(TypeError))
def test__ENTITY_METADATA_CONVERSION__value_validator(input_value):
    """
    Tests whether `ENTITY_METADATA_CONVERSION.value_validator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ScheduledEventEntityMetadataBase`
    
    Raises
    ------
    TypeError
    """
    return ENTITY_METADATA_CONVERSION.value_validator(input_value)


# ---- entity_type ----

def test__ENTITY_TYPE_CONVERSION__generic():
    """
    Tests whether ``ENTITY_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ENTITY_TYPE_CONVERSION)
    vampytest.assert_is(ENTITY_TYPE_CONVERSION.value_validator, validate_entity_type)


def _iter_options__entity_type__value_deserializer():
    yield None, ScheduledEventEntityType.none
    yield ScheduledEventEntityType.location.value, ScheduledEventEntityType.location


@vampytest._(vampytest.call_from(_iter_options__entity_type__value_deserializer()).returning_last())
def test__ENTITY_TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `ENTITY_TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``ScheduledEventEntityType``
    """
    return ENTITY_TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__entity_type__value_serializer():
    yield ScheduledEventEntityType.none, ScheduledEventEntityType.none.value
    yield ScheduledEventEntityType.location, ScheduledEventEntityType.location.value


@vampytest._(vampytest.call_from(_iter_options__entity_type__value_serializer()).returning_last())
def test__ENTITY_TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `ENTITY_TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``ScheduledEventEntityType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return ENTITY_TYPE_CONVERSION.value_serializer(input_value)


# ---- image ----

def test__IMAGE_CONVERSION__generic():
    """
    Tests whether ``IMAGE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(IMAGE_CONVERSION)
    vampytest.assert_eq(IMAGE_CONVERSION.value_deserializer, Icon.from_base_16_hash)
    vampytest.assert_eq(IMAGE_CONVERSION.value_serializer, Icon.as_base_16_hash.fget)
    vampytest.assert_eq(IMAGE_CONVERSION.value_validator, SCHEDULED_EVENT_IMAGE.validate_icon)


# ---- location ----

def test__LOCATION_CONVERSION__generic():
    """
    Tests whether ``LOCATION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(LOCATION_CONVERSION)
    vampytest.assert_is(LOCATION_CONVERSION.value_deserializer, value_deserializer_description)
    vampytest.assert_is(LOCATION_CONVERSION.value_serializer, value_serializer_description)
    vampytest.assert_is(LOCATION_CONVERSION.value_validator, validate_location)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


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


# ---- end ----

def test__END_CONVERSION__generic():
    """
    Tests whether ``END_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(END_CONVERSION)
    vampytest.assert_is(END_CONVERSION.value_validator, validate_end)


# ---- start ----

def test__START_CONVERSION__generic():
    """
    Tests whether ``START_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(START_CONVERSION)
    vampytest.assert_is(START_CONVERSION.value_validator, validate_start)


# ----


def _iter_options__date_time__value_deserializer():
    date_time = DateTime(2016, 5, 14)
    
    yield END_CONVERSION, datetime_to_timestamp(date_time), date_time
    yield END_CONVERSION, None, None
    yield START_CONVERSION, datetime_to_timestamp(date_time), date_time
    yield START_CONVERSION, None, None


@vampytest._(vampytest.call_from(_iter_options__date_time__value_deserializer()).returning_last())
def test__DATE_TIME_CONVERSION__value_deserializer(conversion, input_value):
    """
    Tests whether `START_CONVERSION.value_deserializer` and `END_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to test.
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return conversion.value_deserializer(input_value)


def _iter_options__date_time__value_serializer():
    date_time = DateTime(2016, 5, 14)
    
    yield END_CONVERSION, date_time, datetime_to_timestamp(date_time)
    yield END_CONVERSION, None, None
    yield START_CONVERSION, date_time, datetime_to_timestamp(date_time)
    yield START_CONVERSION, None, None


@vampytest._(vampytest.call_from(_iter_options__date_time__value_serializer()).returning_last())
def test__DATE_TIME_CONVERSION__value_serializer(conversion, input_value):
    """
    Tests whether `START_CONVERSION.value_serializer` and `END_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to test.
    input_value : `None | DateTime`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    return conversion.value_serializer(input_value)


# ---- sku_ids ----

def test__SKU_IDS_CONVERSION__generic():
    """
    Tests whether ``SKU_IDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(SKU_IDS_CONVERSION)
    vampytest.assert_is(SKU_IDS_CONVERSION.value_deserializer, value_deserializer_ids)
    vampytest.assert_is(SKU_IDS_CONVERSION.value_serializer, value_serializer_ids)
    vampytest.assert_is(SKU_IDS_CONVERSION.value_validator, validate_sku_ids)


# ---- status ----

def test__STATUS_CONVERSION__generic():
    """
    Tests whether ``STATUS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(STATUS_CONVERSION)
    vampytest.assert_is(STATUS_CONVERSION.value_validator, validate_status)


def _iter_options__status__value_deserializer():
    yield None, ScheduledEventStatus.none
    yield ScheduledEventStatus.active.value, ScheduledEventStatus.active


@vampytest._(vampytest.call_from(_iter_options__status__value_deserializer()).returning_last())
def test__STATUS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `STATUS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``ScheduledEventStatus``
    """
    return STATUS_CONVERSION.value_deserializer(input_value)


def _iter_options__status__value_serializer():
    yield ScheduledEventStatus.none, ScheduledEventStatus.none.value
    yield ScheduledEventStatus.active, ScheduledEventStatus.active.value


@vampytest._(vampytest.call_from(_iter_options__status__value_serializer()).returning_last())
def test__STATUS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `STATUS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``ScheduledEventStatus``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return STATUS_CONVERSION.value_serializer(input_value)
