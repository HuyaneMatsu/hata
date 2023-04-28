__all__ = ()

from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, entity_id_array_parser_factory, entity_id_parser_factory,
    force_string_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, default_entity_putter_factory, entity_id_putter_factory, force_string_putter_factory,
    optional_entity_id_array_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator, entity_id_array_validator_factory, entity_id_validator_factory
)
from ...role import Role
from ...user import ClientUserBase, User, ZEROUSER

from .constants import NAME_ALLOWED_CHARACTERS, NAME_LENGTH_MAX, NAME_LENGTH_MIN

# animated

parse_animated = bool_parser_factory('animated', False)
put_animated_into = bool_optional_putter_factory('animated', False)
validate_animated = bool_validator_factory('animated', False)

# available

parse_available = bool_parser_factory('available', True)
put_available_into = bool_optional_putter_factory('available', True)
validate_available = bool_validator_factory('available', True)

# guild_id

validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('emoji_id')

# managed

parse_managed = bool_parser_factory('managed', False)
put_managed_into = bool_optional_putter_factory('managed', False)
validate_managed = bool_validator_factory('managed', False)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')


def validate_name(name):
    """
    Validates the given emoji name.
    
    Parameters
    ----------
    name : `None`, `str`
        Emoji name to validate.
    
    Returns
    -------
    name : `str`
        The validated name.
    
    Raises
    ------
    TypeError
        - If `name`'s type is incorrect.
    ValueError
        - if `name`'s value is incorrect.
    """
    if name is None:
        return ''
    
    if not isinstance(name, str):
        raise TypeError(
            f'`name` can be `None`, `str`, got {name.__class__.__name__} ;{name!r}.'
        )
    
    validated_name = ''.join(NAME_ALLOWED_CHARACTERS.findall(name))
    
    name_length = len(validated_name)
    if (name_length < NAME_LENGTH_MIN) or (name_length > NAME_LENGTH_MAX):
        raise ValueError(
            f'`name` length can be >= {NAME_LENGTH_MIN} and <= {NAME_LENGTH_MAX}, got {name_length}; '
            f'validated_name = {validated_name}; input_name = {name!r}'
        )
    
    return validated_name


# require_colons

parse_require_colons = bool_parser_factory('require_colons', True)
put_require_colons_into = bool_optional_putter_factory('require_colons', True)
validate_require_colons = bool_validator_factory('require_colons', True)

# role_ids

parse_role_ids = entity_id_array_parser_factory('roles')
put_role_ids_into = optional_entity_id_array_optional_putter_factory('roles')
validate_role_ids = entity_id_array_validator_factory('role_ids', Role)

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user_into = default_entity_putter_factory('user', ClientUserBase, ZEROUSER)
validate_user = default_entity_validator('user', ClientUserBase, default = ZEROUSER)
