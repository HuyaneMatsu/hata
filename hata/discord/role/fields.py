__all__ = ()

from ..color import Color
from ..field_parsers import (
    bool_parser_factory, flag_parser_factory, force_string_parser_factory, int_parser_factory,
    nullable_functional_parser_factor
)
from ..field_putters import (
    bool_optional_putter_factory, flag_optional_putter_factory, force_string_putter_factory, int_putter_factory,
    nullable_functional_optional_putter_factory, string_flag_putter_factory
)
from ..field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory, nullable_entity_conditional_validator_factory, preinstanced_validator_factory
)
from ..permission import Permission
from ..permission.utils import PERMISSION_KEY

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .preinstanced import RoleManagerType

# color

parse_color = flag_parser_factory('color', Color)
put_color_into = flag_optional_putter_factory('color', Color())
validate_color = flag_validator_factory('color', Color)

# manager_id

validate_manager_id = entity_id_validator_factory('manager_id')

# manager_type

validate_manager_type = preinstanced_validator_factory('manager_type', RoleManagerType)

# manager id & type

def parse_manager(data):
    """
    Parses out ``Role.manager_id`` and ``Role.manager_type` fields from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Role data.
    
    Returns
    -------
    manager_type : ``RoleManagerType``
        If the role is manager, defined by what type of entity is the role is managed.
    
    manager_id : `int`
         If the role is managed, then it's manager's id if applicable.
    """    
    while True:
        if not data.get('managed', False):
            manager_type = RoleManagerType.none
            manager_id = 0
            break
        
        try:
            role_tag_data = data['tags']
        except KeyError:
            manager_type = RoleManagerType.unset
            manager_id = 0
            break
        
        try:
            manager_id = role_tag_data['bot_id']
        except KeyError:
            pass
        else:
            manager_type = RoleManagerType.bot
            manager_id = int(manager_id)
            break
        
        if 'premium_subscriber' in role_tag_data:
            manager_type = RoleManagerType.booster
            manager_id = 0
            break
        
        try:
            manager_id = role_tag_data['integration_id']
        except KeyError:
            pass
        else:
            manager_type = RoleManagerType.integration
            manager_id = int(manager_id)
            break
        
        manager_type = RoleManagerType.unknown
        manager_id = 0
        break
    
    return manager_type, manager_id


def put_manager_into(manager, data, defaults):
    """
    Puts the role's manager into the given data.
    
    Parameters
    ----------
    manager : `tuple` of (``RoleManagerType``, `int`)
        The role's manager as a tuple containing it's identifier and type.
    
    data : `dict` of (`str`, `Any`) items
        Role data.
    
    defaults : `bool`
        Whether default field values should be put into `data` as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    manager_type, manager_id = manager
    
    # No goto? LOLK
    while True:
        managed = manager_type is not RoleManagerType.none
        if defaults or managed:
            data['managed'] = managed
        
        if manager_type is RoleManagerType.bot:
            role_manager_data = {'bot_id': str(manager_id)}
        
        elif manager_type is RoleManagerType.booster:
            role_manager_data = {'premium_subscriber': None}
        
        elif manager_type is RoleManagerType.integration:
            role_manager_data = {'integration_id': str(manager_id)}
        
        else:
            break
        
        data['tags'] = role_manager_data
        break
    
    return data


def validate_manager(manager):
    """
    Validates the given manager value.
    
    Parameters
    ----------
    manager : `None`, `tuple` (``RoleManagerType``, `int`)
        Role manager tuple containing it's identifier and type.
    
    Returns
    -------
    manager_type : ``RoleManagerType``
        If the role is manager, defined by what type of entity is the role is managed.
    
    manager_id : `int`
         If the role is managed, then it's manager's id if applicable.
    
    Raises
    ------
    TypeError
        - If `manager`'s type is invalid.
    """
    if manager is None:
        return 0, RoleManagerType.none
    
    if (not isinstance(manager, tuple)) or (len(manager) != 2):
        raise TypeError(
            f'`manager` can be `None` or `tuple` (of length 2 as manager_type & manager_id), got '
            f'{manager.__class__.__name__}; {manager!r}.'
        )
    
    manager_type, manager_id = manager
    manager_type = validate_manager_type(manager_type)
    manager_id = validate_manager_id(manager_id)
    
    return manager_type, manager_id

# mentionable

parse_mentionable = bool_parser_factory('mentionable', False)
put_mentionable_into = bool_optional_putter_factory('mentionable', False)
validate_mentionable = bool_validator_factory('mentionable')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# permissions

parse_permissions = flag_parser_factory(PERMISSION_KEY, Permission)
put_permissions_into = string_flag_putter_factory(PERMISSION_KEY)
validate_permissions = flag_validator_factory(PERMISSION_KEY, Permission)

# position

parse_position = int_parser_factory('position', 0)
put_position_into = int_putter_factory('position')
validate_position = int_conditional_validator_factory(
    'position',
    0,
    lambda position : position >= 0,
    '>= 0',
)

# separated

parse_separated = bool_parser_factory('hoist', False)
put_separated_into = bool_optional_putter_factory('hoist', False)
validate_separated = bool_validator_factory('separated')

# unicode_emoji

parse_unicode_emoji = nullable_functional_parser_factor(
    'unicode_emoji', NotImplemented, include = 'create_unicode_emoji'
)
put_unicode_emoji_into = nullable_functional_optional_putter_factory('unicode_emoji', lambda emoji: emoji.unicode)
validate_unicode_emoji = nullable_entity_conditional_validator_factory(
    'unicode_emoji', NotImplemented, lambda emoji: emoji.is_unicode_emoji(), 'unicode emoji', include = 'Emoji'
)
