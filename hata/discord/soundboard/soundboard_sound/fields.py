__all__ = ()

from ...emoji import Emoji, create_emoji_from_exclusive_data, put_exclusive_emoji_data_into
from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, float_parser_factory, force_string_parser_factory,
    nullable_entity_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    float_optional_putter_factory, force_string_putter_factory, nullable_entity_optional_putter_factory,
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, float_conditional_validator_factory,
    force_string_validator_factory, nullable_entity_validator_factory
)
from ...user import ClientUserBase, User

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN


# Unused fields:
# id -> use `sound_id`. Redundant with `sound_id`.
# override_path -> only present in builtin sounds. Redundant with `name`.

# available

parse_available = bool_parser_factory('available', True)
put_available_into = bool_optional_putter_factory('available', True)
validate_available = bool_validator_factory('available', True)

# emoji

def parse_emoji(data):
    """
    Parses out the `emoji` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Channel data.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return create_emoji_from_exclusive_data(data)



def put_emoji_into(emoji, data, defaults):
    """
    Puts the `emoji`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The forum tag's emoji.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (emoji is not None):
        put_exclusive_emoji_data_into(emoji, data)
    
    return data


validate_emoji = nullable_entity_validator_factory('emoji', Emoji)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# id

parse_id = entity_id_parser_factory('sound_id')
put_id_into = entity_id_putter_factory('sound_id')
validate_id = entity_id_validator_factory('sound_id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# user

parse_user = nullable_entity_parser_factory('user', User)
put_user_into = nullable_entity_optional_putter_factory('user', ClientUserBase, force_include_internals = True)
validate_user = nullable_entity_validator_factory('user', ClientUserBase)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)

# volume

parse_volume = float_parser_factory('volume', 1.0)
put_volume_into = float_optional_putter_factory('volume', 1.0)
validate_volume = float_conditional_validator_factory(
    'volume',
    1.0,
    lambda volume : volume >= 0.0 and volume <= 1.0,
    '>= 0.0 and <= 1.0',
)
