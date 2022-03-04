__all__ = ()

from .shared import convert_nothing, convert_snowflake


INVITE_CONVERTERS = {
    'channel_id': convert_snowflake,
    'code': convert_nothing,
    'inviter_id': convert_snowflake,
    'max_age': convert_nothing,
    'max_uses': convert_nothing,
    'temporary': convert_nothing,
    'uses': convert_nothing,
}
