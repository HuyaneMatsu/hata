__all__ = ()


from ...field_parsers import (
    int_parser_factory,
    nullable_string_parser_factory, entity_id_parser_factory
)
from ...field_putters import (
    int_putter_factory,
    entity_id_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, int_conditional_validator_factory,
    nullable_string_validator_factory
)
from .constants import NONCE_LENGTH_MAX
from ..guild import Guild
from ...user import User, ClientUserBase
from scarletio import set_docs
from ....env import CACHE_PRESENCE
from ...core import GUILDS

# chunk_count

parse_chunk_count = int_parser_factory('chunk_count', 0)
put_chunk_count_into = int_putter_factory('chunk_count')
validate_chunk_count = int_conditional_validator_factory(
    'chunk_count',
    0,
    lambda chunk_count : chunk_count >= 0,
    '>= 0',
)

# chunk_index

parse_chunk_index = int_parser_factory('chunk_index', 0)
put_chunk_index_into = int_putter_factory('chunk_index')
validate_chunk_index = int_conditional_validator_factory(
    'chunk_index',
    0,
    lambda chunk_index : chunk_index >= 0,
    '>= 0',
)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# nonce

parse_nonce = nullable_string_parser_factory('nonce')
put_nonce_into = url_optional_putter_factory('nonce')
validate_nonce = nullable_string_validator_factory('nonce', 0, NONCE_LENGTH_MAX)

# users

def parse_users__cache_presence(data, guild_id = 0):
    users = []
    guild = GUILDS.get(guild_id, None)
    guild_profile_datas = data.get('members', None)
    
    if guild is None:
        if (guild_profile_datas is not None):
            for guild_profile_data in guild_profile_datas:
                user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id, strong_cache = False)
                users.append(user)
    
    else:
        guild_users = guild.users
        
        if (guild_profile_datas is not None):
            for guild_profile_data in guild_profile_datas:
                user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id, strong_cache = False)
                guild_users[user.id] = user
                users.append(user)
        
        presence_datas = data.get('presences', None)
        if (presence_datas is not None):
            for presence_data in presence_datas:
                user_id = int(presence_data['user']['id'])
                try:
                    user = guild_users[user_id]
                except KeyError:
                    pass
                else:
                    user._update_presence(presence_data)
    
    return users


def parse_users__no_cache_presence(data, guild_id = 0):
    users = []
    guild = GUILDS.get(guild_id, None)
    guild_profile_datas = data.get('members', None)
    
    if guild is None:
        if (guild_profile_datas is not None):
            for guild_profile_data in guild_profile_datas:
                user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id, strong_cache = False)
                users.append(user)
    else:
        guild_users = guild.users
        
        if (guild_profile_datas is not None):
            for guild_profile_data in guild_profile_datas:
                user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id, strong_cache = False)
                guild_users[user.id] = user
                users.append(user)
    
    return users


if CACHE_PRESENCE:
    parse_users = parse_users__cache_presence
else:
    parse_users = parse_users__no_cache_presence


set_docs(
    parse_users,
    """
    Parses the guild's users from the given data.
    
    > Used when presence caching is enabled.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    users : `dict<int, ClientUserBase>`
        The guild's users.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    users : `list<ClientUserBase>
        Returns `users` parameter.
    """
)


def put_users_into(users, data, defaults, *, guild_id = 0):
    """
    Puts the given `users` into the given `data` json serializable object.
    
    Parameters
    ----------
    users : `list` of ``ClientUserBase``
        Resolved users.
    data : `dict` of (`str`, `object`) items
        Interaction resolved data.
    defaults : `bool`
        Whether default fields values should be included as well.
    guild_id : `int` = `0`, Optional (keyword only)
        The guild's identifier.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    guild_profiles_datas = []
    
    if guild_id:
        for user in users:
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            guild_profile_data = guild_profile.to_data(defaults = defaults, include_internals = True)
            guild_profile_data['user'] = user.to_data(defaults = defaults, include_internals = True)
            guild_profiles_datas.append(guild_profile_data)
            continue
    
    data['members'] = guild_profiles_datas
    
    return data


def validate_users(users):
    """
    Validates the given users.
    
    Parameters
    ----------
    users : `None`, `iterable` of ``ClientUserBase``
        The users to validate.
    
    Returns
    -------
    users : `list` of ``ClientUserBase``
    
    Raises
    ------
    TypeError
        - If `users`'s type is incorrect.
    """
    validated_users = []
    
    if users is None:
        return validated_users
        
    if (getattr(users, '__iter__', None) is None):
        raise TypeError(
            f'`users` can be `None`,`iterable` of `{ClientUserBase.__name__}` elements, '
            f'got {users.__class__.__name__}; {users!r}.'
        )
    
    for user in users:
        if not isinstance(user, ClientUserBase):
            raise TypeError(
                f'`users` elements can be `{ClientUserBase.__name__}`, got {user.__class__.__name__}; '
                f'{user!r}; users = {users!r}.'
            )
        
        validated_users.append(user)
    
    return validated_users
