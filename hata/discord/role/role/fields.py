__all__ = ()

from ...color import Color
from ...field_parsers import (
    bool_parser_factory, flag_parser_factory, force_string_parser_factory, int_parser_factory,
    nullable_functional_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, flag_optional_putter_factory, force_string_putter_factory, int_putter_factory,
    nullable_functional_optional_putter_factory, string_flag_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator, flag_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory, nullable_entity_conditional_validator_factory, preinstanced_validator_factory
)
from ...permission import Permission
from ...permission.constants import PERMISSION_KEY

from ..role_manager_metadata import RoleManagerMetadataBase
from ..role_manager_metadata.constants import BOOSTER_KEY, BOT_ID_KEY, INTEGRATION_ID_KEY, SUBSCRIPTION_LISTING_ID_KEY

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN, ROLE_MANAGER_DEFAULT
from .preinstanced import RoleManagerType

# color

parse_color = flag_parser_factory('color', Color)
put_color_into = flag_optional_putter_factory('color', Color())
validate_color = flag_validator_factory('color', Color)

# manager_metadata

validate_manager_metadata = default_entity_validator('manager_metadata', RoleManagerMetadataBase, ROLE_MANAGER_DEFAULT)

# manager_type

validate_manager_type = preinstanced_validator_factory('manager_type', RoleManagerType)

# manager type & metadata

def parse_manager(data):
    """
    Parses out ``Role.manager_id`` and ``Role.manager_type` fields from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Role data.
    
    Returns
    -------
    manager_type : ``RoleManagerType``
        If the role is manager, defined by what type of entity is the role is managed.
    
    manager_metadata : ``RoleManagerMetadataBase``
         Metadata about the role's manager.
    """
    managed = data.get('managed', False)
    manager_data = data.get('tags', None)
    
    while True:
        if (not managed):
            manager_type = RoleManagerType.none
            break
        
        if (manager_data is None) or (not manager_data):
            manager_type = RoleManagerType.unset
            break
        
        if BOT_ID_KEY in manager_data:
            manager_type = RoleManagerType.bot
            break
        
        if BOOSTER_KEY in manager_data:
            manager_type = RoleManagerType.booster
            break
        
        if SUBSCRIPTION_LISTING_ID_KEY in manager_data:
            manager_type = RoleManagerType.integration
            break
        
        if INTEGRATION_ID_KEY in manager_data:
            manager_type = RoleManagerType.integration
            break
        
        manager_type = RoleManagerType.unknown
        break
    
    metadata_type = manager_type.metadata_type
    if metadata_type is RoleManagerMetadataBase:
        manager_metadata = ROLE_MANAGER_DEFAULT
    else:
        manager_metadata = metadata_type.from_data(manager_data)
    
    return manager_type, manager_metadata


def put_manager_into(manager, data, defaults):
    """
    Puts the role's manager into the given data.
    
    Parameters
    ----------
    manager : `tuple` (``RoleManagerType``, ``RoleManagerMetadataBase``)
        The role's manager as a tuple containing it's identifier and type.
    
    data : `dict` of (`str`, `object`) items
        Role data.
    
    defaults : `bool`
        Whether default field values should be put into `data` as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    manager_type, manager_metadata = manager
    
    managed = manager_type is not RoleManagerType.none
    if defaults or managed:
        data['managed'] = managed
        data['tags'] = manager_metadata.to_data(defaults = defaults)
    
    return data


def validate_manager(manager):
    """
    Validates the given manager value.
    
    Parameters
    ----------
    manager : `None`, `tuple` (``RoleManagerType``, ``RoleManagerMetadataBase``)
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
        - `manager_type` - `manager_metadata` mismatch.
    """
    if manager is None:
        return RoleManagerType.none, ROLE_MANAGER_DEFAULT
    
    if (not isinstance(manager, tuple)) or (len(manager) != 2):
        raise TypeError(
            f'`manager` can be `None` or `tuple` (of length 2 as manager_type & manager_metadata), got '
            f'{manager.__class__.__name__}; {manager!r}.'
        )
    
    manager_type, manager_metadata = manager
    manager_type = validate_manager_type(manager_type)
    manager_metadata = validate_manager_metadata(manager_metadata)
    
    expected_manager_metadata_type = manager_type.metadata_type
    received_manager_metadata_type = type(manager_metadata)
    
    if received_manager_metadata_type is RoleManagerMetadataBase:
        if expected_manager_metadata_type is not RoleManagerMetadataBase:
            manager_metadata = expected_manager_metadata_type()
    
    else:
        if received_manager_metadata_type is not expected_manager_metadata_type:
            raise TypeError(
                f'`manager_metadata` should be `{expected_manager_metadata_type.__name__}` instance, got '
                f'{received_manager_metadata_type.__name__}, {manager_metadata!r}.'
            )
    
    return manager_type, manager_metadata


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

parse_unicode_emoji = nullable_functional_parser_factory(
    'unicode_emoji', NotImplemented, include = 'create_unicode_emoji'
)
put_unicode_emoji_into = nullable_functional_optional_putter_factory('unicode_emoji', lambda emoji: emoji.unicode)
validate_unicode_emoji = nullable_entity_conditional_validator_factory(
    'unicode_emoji', NotImplemented, lambda emoji: emoji.is_unicode_emoji(), 'unicode emoji', include = 'Emoji'
)
