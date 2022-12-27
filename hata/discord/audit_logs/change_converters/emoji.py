__all__ = ()

from .shared import convert_nothing, convert_snowflake_array


EMOJI_CONVERTERS = {
    'available': convert_nothing,
    'name': convert_nothing,
    'role_ids': convert_snowflake_array,
}
