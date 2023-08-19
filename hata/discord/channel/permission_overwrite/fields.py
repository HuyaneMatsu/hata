__all__ = ()

from scarletio import include

from ...bases import maybe_snowflake
from ...field_parsers import entity_id_parser_factory, flag_parser_factory
from ...field_putters import entity_id_putter_factory, preinstanced_putter_factory, string_flag_putter_factory
from ...field_validators import entity_id_validator_factory, flag_validator_factory, preinstanced_validator_factory
from ...permission import Permission
from ...permission.constants import PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY

from .helpers import get_permission_overwrite_key_value
from .preinstanced import PermissionOverwriteTargetType


Role = include('Role')
ClientUserBase = include('ClientUserBase')

# allow

parse_allow = flag_parser_factory(PERMISSION_ALLOW_KEY, Permission)
put_allow_into = string_flag_putter_factory(PERMISSION_ALLOW_KEY)
validate_allow = flag_validator_factory('allow', Permission)

# deny

parse_deny = flag_parser_factory(PERMISSION_DENY_KEY, Permission)
put_deny_into = string_flag_putter_factory(PERMISSION_DENY_KEY)
validate_deny = flag_validator_factory('deny', Permission)

# target

def put_target_into(target, data, defaults, *, include_internals = False):
    """
    Puts the `target` field of ``PermissionOverwrite`` to the given data.
    
    The `target` value must come from ``validate_target``.
    
    Parameters
    ----------
    target : `tuple` (`int`, ``PermissionOverwriteTargetType``)
        Permission overwrite `target-id`, `target_type` pair.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    include_internals : `bool` = `False`, Optional (Keyword only)
        Whether internal fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    target_id, target_type = target
    
    if include_internals:
        data['id'] = str(target_id) if target_id else None
    
    if (target_type is not PermissionOverwriteTargetType.unknown):
        data['type'] = target_type.value
    
    return data


def validate_target(target):
    """
    Validates the `target` field of ``PermissionOverwrite``. target is a mixed representation of `target_id` and
    `target_type`.
    
    Parameters
    ----------
    target : ``Role``, ``ClientUserBase``, `int`
        The permission overwrite's target or it's identifier.
    
    Returns
    -------
    target_id : `int`
        The permission overwrite target's identifier.
    target_type : ``PermissionOverwriteTargetType``
        The permission overwrite's type.
    
    Raises
    ------
    TypeError
        - If `target`'s type is unexpected.
    """
    # target_id
    if isinstance(target, Role):
        target_id = target.id
        target_type = PermissionOverwriteTargetType.role
    
    elif isinstance(target, ClientUserBase):
        target_id = target.id
        target_type = PermissionOverwriteTargetType.user
    
    else:
        target_id = maybe_snowflake(target)
        if (target_id is None):
            raise TypeError(
                f'`target` can be `int`, `{Role.__name__}`, `{ClientUserBase.__name__}`, got '
                f'{target.__class__.__name__}; {target!r}.'
            )
        
        target_type = PermissionOverwriteTargetType.unknown
    
    return target_id, target_type

# target_id

parse_target_id = entity_id_parser_factory('id')
put_target_id_into = entity_id_putter_factory('id')
validate_target_id = entity_id_validator_factory('target_id')

# target_type

def parse_target_type(data):
    """
    Parses out ``PermissionOverwrite.target_type`` from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Permission overwrite data.
    
    Returns
    -------
    target_type : ``PermissionOverwriteTargetType``
    """
    return PermissionOverwriteTargetType.get(get_permission_overwrite_key_value(data))


put_target_type_into = preinstanced_putter_factory('type')
validate_target_type = preinstanced_validator_factory('target_type', PermissionOverwriteTargetType)
