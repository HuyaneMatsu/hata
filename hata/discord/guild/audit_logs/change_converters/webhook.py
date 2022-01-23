__all__ = ()

from .shared import convert_icon, convert_nothing, convert_snowflake


WEBHOOK_CONVERTERS = {
    'avatar_hash': convert_icon,
    'channel_id': convert_snowflake,
    'id': convert_snowflake,
    'name': convert_nothing,
}
