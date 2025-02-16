__all__ = ()

from ...field_parsers import force_string_parser_factory, nullable_string_parser_factory
from ...field_putters import force_string_putter_factory, url_optional_putter_factory
from ...field_validators import (
    default_entity_validator_factory, force_string_validator_factory, nullable_string_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER, create_partial_user_from_id

from .constants import NONCE_LENGTH_MAX, SESSION_ID_LENGTH_MAX, SESSION_ID_LENGTH_MIN


# nonce

parse_nonce = nullable_string_parser_factory('nonce')
put_nonce = url_optional_putter_factory('nonce')
validate_nonce = nullable_string_validator_factory('nonce', 0, NONCE_LENGTH_MAX)

# session_id

parse_session_id = force_string_parser_factory('session_id')
put_session_id = force_string_putter_factory('session_id')
validate_session_id = force_string_validator_factory('session_id', SESSION_ID_LENGTH_MIN, SESSION_ID_LENGTH_MAX)

# user

def parse_user(data, guild_id = 0):
    """
    Parses out a user from the given reaction create or delete event data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Reaction event data.
    
    guild_id : `int` = `0`, Optional
        The guild's identifier where the event is from.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    if guild_id:
        try:
            guild_profile_data = data['member']
        except KeyError:
            pass
        else:
            user_data = guild_profile_data['user']
            return User.from_data(user_data, guild_profile_data, int(guild_id))
    
    return create_partial_user_from_id(int(data['user_id']))


def put_user(user, data, defaults, *, guild_id = 0):
    """
    Puts the given user's representation into the given reaction event data.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to serialize.
    data : `dict<str, object>`
        Reaction event data.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild's identifier where the event is from.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['user_id'] = str(user.id)
    
    if guild_id:
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            guild_profile_data = guild_profile.to_data(defaults = defaults, include_internals = True)
            guild_profile_data['user'] = user.to_data(defaults = defaults, include_internals = True)
            
            data['member'] = guild_profile_data
    
    return data


validate_user = default_entity_validator_factory('user', ClientUserBase, default = ZEROUSER)
