__all__ = ()

from ...bases import Icon
from ...scheduled_event import (
    PrivacyLevel, ScheduledEventEntityMetadataBase, ScheduledEventEntityType, ScheduledEventStatus
)
from ...scheduled_event.scheduled_event.fields import (
    validate_channel_id, validate_description, validate_end, validate_entity_id, validate_entity_type, validate_name,
    validate_privacy_level, validate_sku_ids, validate_start, validate_status
)
from ...scheduled_event.scheduled_event.scheduled_event import SCHEDULED_EVENT_IMAGE
from ...scheduled_event.scheduled_event_entity_metadata.fields import validate_location
from ...scheduled_event.scheduled_event_entity_metadata.utils import try_get_scheduled_event_metadata_type_from_data
from ...utils import datetime_to_timestamp, timestamp_to_datetime

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_deserializer_ids, value_deserializer_name, value_serializer_description,
    value_serializer_id, value_serializer_ids, value_serializer_name
)


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('channel_id',),
    'channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_channel_id,
)


# ---- description ----

DESCRIPTION_CONVERSION = AuditLogEntryChangeConversion(
    ('description',),
    'description',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_description,
)


# ---- entity_id ----

ENTITY_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('entity_id',),
    'entity_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_entity_id,
)


# ---- entity_metadata ----

ENTITY_METADATA_CONVERSION = AuditLogEntryChangeConversion(
    ('entity_metadata',),
    'entity_metadata',
)

@ENTITY_METADATA_CONVERSION.set_value_deserializer
def entity_metadata_value_deserializer(value):
    if value is not None:
        metadata_type = try_get_scheduled_event_metadata_type_from_data(value)
        if metadata_type is None:
            value = None
        else:
            value = metadata_type.from_data(value)
    
    return value


@ENTITY_METADATA_CONVERSION.set_value_serializer
def entity_metadata_value_serializer(value):
    if value is not None:
        value = value.to_data(defaults = True)
    return value


@ENTITY_METADATA_CONVERSION.set_value_validator
def entity_metadata_value_validator(value):
    if value is None or isinstance(value, ScheduledEventEntityMetadataBase):
        return value
    
    raise TypeError(
        f'`entity_metadata` can be `None`, `{ScheduledEventEntityMetadataBase.__name__}`, '
        f'got {type(value).__name__}; {value!r}.'
    )


# ---- entity_type ----

ENTITY_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('entity_type',),
    'entity_type',
    value_validator = validate_entity_type,
)


@ENTITY_TYPE_CONVERSION.set_value_deserializer
def entity_type_value_deserializer(value):
    return ScheduledEventEntityType(value)


@ENTITY_TYPE_CONVERSION.set_value_serializer
def entity_type_value_serializer(value):
    return value.value


# ---- image ----

IMAGE_CONVERSION = AuditLogEntryChangeConversion(
    ('image_hash',),
    'image',
    value_deserializer = Icon.from_base_16_hash,
    value_serializer = Icon.as_base_16_hash.fget,
    value_validator = SCHEDULED_EVENT_IMAGE.validate_icon,
)


# ---- location ----

LOCATION_CONVERSION = AuditLogEntryChangeConversion(
    ('location',),
    'location',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_location,
)

# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- privacy_level ----

PRIVACY_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    ('privacy_level',),
    'privacy_level',
    value_validator = validate_privacy_level,
)


@PRIVACY_LEVEL_CONVERSION.set_value_deserializer
def privacy_level_value_deserializer(value):
    return PrivacyLevel(value)


@PRIVACY_LEVEL_CONVERSION.set_value_serializer
def privacy_level_value_serializer(value):
    return value.value


# ---- end ----

END_CONVERSION = AuditLogEntryChangeConversion(
    ('scheduled_end_time',),
    'end',
    value_validator = validate_end,
)


# ---- start ----

START_CONVERSION = AuditLogEntryChangeConversion(
    ('scheduled_start_time',),
    'start',
    value_validator = validate_start,
)

# ----

@END_CONVERSION.set_value_deserializer
@START_CONVERSION.set_value_deserializer
def date_time_converter_get(value):
    if (value is not None):
        value = timestamp_to_datetime(value)
    return value

@END_CONVERSION.set_value_serializer
@START_CONVERSION.set_value_serializer
def date_time_converter_put(value):
    if (value is not None):
        value = datetime_to_timestamp(value)
    return value


# ---- sku_ids ----

SKU_IDS_CONVERSION = AuditLogEntryChangeConversion(
    ('sku_ids',),
    'sku_ids',
    value_deserializer = value_deserializer_ids,
    value_serializer = value_serializer_ids,
    value_validator = validate_sku_ids,
)


# ---- status ----

STATUS_CONVERSION = AuditLogEntryChangeConversion(
    ('status',),
    'status',
    value_validator = validate_status,
)


@STATUS_CONVERSION.set_value_deserializer
def status_value_deserializer(value):
    return ScheduledEventStatus(value)


@STATUS_CONVERSION.set_value_serializer
def status_value_serializer(value):
    return value.value


# ---- Construct ----

SCHEDULED_EVENT_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    CHANNEL_ID_CONVERSION,
    DESCRIPTION_CONVERSION,
    ENTITY_ID_CONVERSION,
    ENTITY_METADATA_CONVERSION,
    ENTITY_TYPE_CONVERSION,
    IMAGE_CONVERSION,
    LOCATION_CONVERSION,
    NAME_CONVERSION,
    PRIVACY_LEVEL_CONVERSION,
    END_CONVERSION,
    START_CONVERSION,
    SKU_IDS_CONVERSION,
    STATUS_CONVERSION,
)
