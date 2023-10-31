__all__ = ()

from ...bases import Icon
from ...user.user.fields import validate_name
from ...user.user.user_base import USER_AVATAR
from ...webhook.webhook.fields import validate_channel_id

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name


# ---- avatar ----

AVATAR_CONVERSION = AuditLogEntryChangeConversion(
    'avatar_hash',
    'avatar',
    FLAG_IS_MODIFICATION,
    get_converter = Icon.from_base_16_hash,
    put_converter = Icon.as_base_16_hash,
    validator = USER_AVATAR.validate_icon,
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


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- Construct ----

WEBHOOK_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVATAR_CONVERSION,
    CHANNEL_ID_CONVERSION,
    NAME_CONVERSION,
)
