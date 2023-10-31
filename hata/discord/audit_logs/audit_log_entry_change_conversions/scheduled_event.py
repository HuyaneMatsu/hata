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

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    get_converter_description, get_converter_id, get_converter_ids, get_converter_name, put_converter_description,
    put_converter_id, put_converter_ids, put_converter_name
)


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'channel_id',
    'channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_channel_id,
)


# ---- description ----

DESCRIPTION_CONVERSION = AuditLogEntryChangeConversion(
    'description',
    'description',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_description,
)


# ---- entity_id ----

ENTITY_ID_CONVERSION = AuditLogEntryChangeConversion(
    'entity_id',
    'entity_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_entity_id,
)


# ---- entity_metadata ----

ENTITY_METADATA_CONVERSION = AuditLogEntryChangeConversion(
    'entity_metadata',
    'entity_metadata',
    FLAG_IS_MODIFICATION,
)

@ENTITY_METADATA_CONVERSION.set_get_converter
def entity_metadata_get_converter(value):
    if value is not None:
        metadata_type = try_get_scheduled_event_metadata_type_from_data(value)
        if metadata_type is None:
            value = None
        else:
            value = metadata_type.from_data(value)
    
    return value


@ENTITY_METADATA_CONVERSION.set_put_converter
def entity_metadata_put_converter(value):
    if value is not None:
        value = value.to_data(defaults = True)
    return value


@ENTITY_METADATA_CONVERSION.set_validator
def entity_metadata_validator(value):
    if value is None or isinstance(value, ScheduledEventEntityMetadataBase):
        return value
    
    raise TypeError(
        f'`entity_metadata` can be `None`, `{ScheduledEventEntityMetadataBase.__name__}`, '
        f'got {type(value).__name__}; {value!r}.'
    )


# ---- entity_type ----

ENTITY_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'entity_type',
    'entity_type',
    FLAG_IS_MODIFICATION,
    validator = validate_entity_type,
)


@ENTITY_TYPE_CONVERSION.set_get_converter
def entity_type_get_converter(value):
    return ScheduledEventEntityType.get(value)


@ENTITY_TYPE_CONVERSION.set_put_converter
def entity_type_put_converter(value):
    return value.value


# ---- image ----

IMAGE_CONVERSION = AuditLogEntryChangeConversion(
    'image',
    'image',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = SCHEDULED_EVENT_IMAGE.validate_icon,
)


# ---- location ----

LOCATION_CONVERSION = AuditLogEntryChangeConversion(
    'location',
    'location',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_location,
)

# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- privacy_level ----

PRIVACY_LEVEL_CONVERSION = AuditLogEntryChangeConversion(
    'privacy_level',
    'privacy_level',
    FLAG_IS_MODIFICATION,
    validator = validate_privacy_level,
)


@PRIVACY_LEVEL_CONVERSION.set_get_converter
def privacy_level_get_converter(value):
    return PrivacyLevel.get(value)


@PRIVACY_LEVEL_CONVERSION.set_put_converter
def privacy_level_put_converter(value):
    return value.value


# ---- end ----

END_CONVERSION = AuditLogEntryChangeConversion(
    'scheduled_end_time',
    'end',
    FLAG_IS_MODIFICATION,
    validator = validate_end,
)


# ---- start ----

START_CONVERSION = AuditLogEntryChangeConversion(
    'scheduled_start_time',
    'start',
    FLAG_IS_MODIFICATION,
    validator = validate_start,
)

# ----

@END_CONVERSION.set_get_converter
@START_CONVERSION.set_get_converter
def date_time_converter_get(value):
    if (value is not None):
        value = timestamp_to_datetime(value)
    return value

@END_CONVERSION.set_put_converter
@START_CONVERSION.set_put_converter
def date_time_converter_put(value):
    if (value is not None):
        value = datetime_to_timestamp(value)
    return value


# ---- sku_ids ----

SKU_IDS_CONVERSION = AuditLogEntryChangeConversion(
    'sku_ids',
    'sku_ids',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_ids,
    put_converter = put_converter_ids,
    validator = validate_sku_ids,
)


# ---- status ----

STATUS_CONVERSION = AuditLogEntryChangeConversion(
    'status',
    'status',
    FLAG_IS_MODIFICATION,
    validator = validate_status,
)


@STATUS_CONVERSION.set_get_converter
def status_get_converter(value):
    return ScheduledEventStatus.get(value)


@STATUS_CONVERSION.set_put_converter
def status_put_converter(value):
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
