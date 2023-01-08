__all__ = ()

from ...emoji import Emoji
from ...field_parsers import (
    entity_id_parser_factory, force_string_parser_factory, int_parser_factory, nullable_string_parser_factory,
    preinstanced_array_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, force_string_putter_factory, int_putter_factory, nullable_string_putter_factory,
    preinstanced_array_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, int_conditional_validator_factory,
    nullable_string_validator_factory, preinstanced_array_validator_factory
)
from ...sticker import Sticker

from .constants import DESCRIPTION_LENGTH_MAX, NAME_LENGTH_MAX

# approximate_online_count

parse_approximate_online_count = int_parser_factory('approximate_presence_count', 0)
put_approximate_online_count_into = int_putter_factory('approximate_presence_count')
validate_approximate_online_count = int_conditional_validator_factory(
    'approximate_online_count',
    0,
    lambda approximate_online_count : approximate_online_count >= 0,
    '>= 0',
)

# approximate_user_count

parse_approximate_user_count = int_parser_factory('approximate_member_count', 0)
put_approximate_user_count_into = int_putter_factory('approximate_member_count')
validate_approximate_user_count = int_conditional_validator_factory(
    'approximate_user_count',
    0,
    lambda approximate_user_count : approximate_user_count >= 0,
    '>= 0',
)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# emojis

def parse_emojis(data, entities, guild_id):
    """
    Parses the `emojis` field out from the given guild preview data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Guild preview data.
    entities : `dict` of (`int`, ``Emoji``) items
        The entity container to populate.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    entities : `dict` of (`int`, ``Emoji``) items
    """
    emoji_datas = data.get('emojis', None)
    if emoji_datas is None:
        return entities
    
    if entities:
        entity_cache = [*entities.values()]
        entities.clear()
    
    for emoji_data in emoji_datas:
        emoji = Emoji.from_data(emoji_data, guild_id)
        entities[emoji.id] = emoji
    
    return entities


def put_emojis_into(entities, data, defaults):
    """
    Puts the given emojis to the guild preview data.
    
    Parameters
    ----------
    entities : `dict` of (`int`, ``Emoji``) items
        Emojis to put into the given data.
    data : `dict` of (`str`, `object`) items
        Guild preview data.
    defaults : `bool`
        Whether values with their default fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['emojis'] = [
        entity.to_data(defaults = defaults, include_internals = True) for entity in sorted(entities.values())
    ]
    return data


def validate_emojis(emojis):
    """
    Validates the given emojis.
    
    Parameters
    ----------
    emojis : `None`, `iterable` of ``Emoji``
        The emojis to validate.
    
    Returns
    -------
    emojis : `dict` of (`int`, ``Emoji``) items
        The validated emojis.
    
    Raises
    ------
    TypeError
        - If `emojis` is not `None`, `iterable` of ``Emoji``.
        - If `emojis` contains a non-``Emoji`` element. 
    """
    validated_emojis = {}
    
    if emojis is None:
        return validated_emojis
    
    if getattr(type(emojis), '__iter__', None) is None:
        raise TypeError(
            f'`emojis` can be `None` ot `iterable` of `{Emoji.__name__}`, '
            f'got {emojis.__class__.__name__}; {emojis!r}.'
        )
    
    for emoji in emojis:
        if not isinstance(emoji, Emoji):
            raise TypeError(
                f'`emoji` can contain `{Emoji.__name__}` elements, got {emoji.__class__.__name__}; {emoji!r}; '
                f'emojis = {emojis!r}.'
            )
        
        validated_emojis[emoji.id] = emoji
    
    return validated_emojis

# features

parse_features = preinstanced_array_parser_factory('features', NotImplemented, include = 'GuildFeature')
put_features_into = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', NotImplemented, include = 'GuildFeature')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id', NotImplemented, include = 'Guild')

# stickers

def parse_stickers(data, entities):
    """
    Parses the `stickers` field out from the given guild preview data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Guild preview data.
    entities : `dict` of (`int`, ``Sticker``) items
        The entity container to populate.
    
    Returns
    -------
    entities : `dict` of (`int`, ``Sticker``) items
    """
    sticker_datas = data.get('stickers', None)
    if sticker_datas is None:
        return entities
    
    if entities:
        entity_cache = [*entities.values()]
        entities.clear()
    
    for sticker_data in sticker_datas:
        sticker = Sticker.from_data(sticker_data)
        entities[sticker.id] = sticker
    
    return entities


def put_stickers_into(entities, data, defaults):
    """
    Puts the given stickers to the guild preview data.
    
    Parameters
    ----------
    entities : `dict` of (`int`, ``Sticker``) items
        Stickers to put into the given data.
    data : `dict` of (`str`, `object`) items
        Guild preview data.
    defaults : `bool`
        Whether values with their default fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['stickers'] = [
        entity.to_data(defaults = defaults, include_internals = True) for entity in sorted(entities.values())
    ]
    return data


def validate_stickers(stickers):
    """
    Validates the given stickers.
    
    Parameters
    ----------
    stickers : `None`, `iterable` of ``Sticker``
        The stickers to validate.
    
    Returns
    -------
    stickers : `dict` of (`int`, ``Sticker``) items
        The validated stickers.
    
    Raises
    ------
    TypeError
        - If `stickers` is not `None`, `iterable` of ``Sticker``.
        - If `stickers` contains a non-``Sticker`` element. 
    """
    validated_stickers = {}
    
    if stickers is None:
        return validated_stickers
    
    if getattr(type(stickers), '__iter__', None) is None:
        raise TypeError(
            f'`stickers` can be `None` ot `iterable` of `{Sticker.__name__}`, '
            f'got {stickers.__class__.__name__}; {stickers!r}.'
        )
    
    for sticker in stickers:
        if not isinstance(sticker, Sticker):
            raise TypeError(
                f'`sticker` can contain `{Sticker.__name__}` elements, got {sticker.__class__.__name__}; {sticker!r}; '
                f'stickers = {stickers!r}.'
            )
        
        validated_stickers[sticker.id] = sticker
    
    return validated_stickers

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', 0, NAME_LENGTH_MAX)
