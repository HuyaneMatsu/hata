__all__ = ()

from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, entity_id_parser_factory, force_string_parser_factory,
    int_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, default_entity_putter_factory, entity_id_optional_putter_factory,
    entity_id_putter_factory, force_string_putter_factory, int_putter_factory, nullable_string_putter_factory, 
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator, entity_id_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory, nullable_string_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

from .constants import (
    DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN, NAME_LENGTH_MAX, NAME_LENGTH_MIN, SORT_VALUE_DEFAULT,
    SORT_VALUE_MAX, SORT_VALUE_MIN
)
from .preinstanced import StickerFormat, StickerType

# available

parse_available = bool_parser_factory('available', True)
put_available_into = bool_optional_putter_factory('available', True)
validate_available = bool_validator_factory('available', True)

# description 

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX)

# format

parse_format = preinstanced_parser_factory('format_type', StickerFormat, StickerFormat.none)
put_format_into = preinstanced_putter_factory('format_type')
validate_format = preinstanced_validator_factory('format', StickerFormat)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# pack_id

parse_pack_id = entity_id_parser_factory('pack_id')
put_pack_id_into = entity_id_optional_putter_factory('pack_id')
validate_pack_id = entity_id_validator_factory('pack_id', NotImplemented, include = 'StickerPack')

# sort_value

parse_sort_value = int_parser_factory('sort_value', SORT_VALUE_DEFAULT)
put_sort_value_into = int_putter_factory('sort_value')
validate_sort_value = int_conditional_validator_factory(
    'sort_value',
    SORT_VALUE_MIN,
    (lambda sort_value: sort_value >= SORT_VALUE_MIN and sort_value <= SORT_VALUE_MAX),
    f'>= {SORT_VALUE_MIN} and <= {SORT_VALUE_MAX},'
)

# tags

def parse_tags(data):
    """
    Parses out sticker tags from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Sticker data
    
    Returns
    -------
    tags : `None`, `frozenset` of `str`
    """
    raw_tags = data.get('tags', None)
    if (raw_tags is None) or (not raw_tags):
        tags = None
    else:
        tags = frozenset(raw_tags.split(', '))

    return tags


def put_tags_into(tags, data, defaults):
    """
    Puts the sticker tags into the given json serializable dictionary.
    
    Parameters
    ----------
    tags : `None`, `frozenset` of `str`
        Sticker tags.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if tags is None:
        raw_tags = ''
    else:
        raw_tags = ', '.join(tags)
    data['tags'] = raw_tags
    return data


def validate_tags(tags):
    """
    Validates the given sticker tags.
    
    Parameters
    ----------
    tags : `None`, `str`, `iterable` of `str`
        Sticker tags to validate.
    
    Returns
    -------
    tags : `None`, `frozenset` of `str`
    
    Raises
    ------
    TypeError
        - If `tags`'s value or structure is incorrect.
    """
    if tags is None:
        return tags
    
    if isinstance(tags, str):
        if not tags:
            return None
        
        return frozenset(tags.split(', '))
    
    if getattr(type(tags), '__iter__', None) is None:
        raise TypeError(
            f'`tags` can be `None`, `str`, `iterable` of `str`, got {type(tags).__name__}; {tags!r}.'
        )
    
    validated_tags = None
    
    for tag in tags:
        if not isinstance(tag, str):
            raise TypeError(
                f'`tags` can contain `str` instances, got {tag.__class__.__name__}; {tag!r}; tags = {tags!r}.'
            )
        
        if validated_tags is None:
            validated_tags = set()
        
        validated_tags.add(tag)
    
    if (validated_tags is not None):
        return frozenset(tags)

# type

parse_type = preinstanced_parser_factory('type', StickerType, StickerType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('sticker_type', StickerType)

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user_into = default_entity_putter_factory('user', ClientUserBase, ZEROUSER)
validate_user = default_entity_validator('user', ClientUserBase, default = ZEROUSER)
