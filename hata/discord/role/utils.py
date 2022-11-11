__all__ = ('create_partial_role_from_id', 'cr_p_role_object', 'parse_role', 'parse_role_mention')

import warnings

from scarletio import export

from ..core import ROLES
from ..utils import ID_RP, ROLE_MENTION_RP

from .role import Role
from .fields import validate_color, put_color_into, validate_mentionable, put_mentionable_into, \
    validate_name, put_name_into, validate_permissions, put_separated_into, \
    put_permissions_into, put_position_into, validate_separated, validate_position


ROLE_FIELD_CONVERTERS = {
    'color': (validate_color, put_color_into),
    'mentionable': (validate_mentionable, put_mentionable_into),
    'name': (validate_name, put_name_into),
    'permissions': (validate_permissions, put_permissions_into),
    'position': (validate_position, put_position_into),
    'separated': (validate_separated, put_separated_into),
}


@export
def create_partial_role_from_id(role_id, guild_id = 0):
    """
    Creates a partial role from the given `role_id`. If the role already exists returns that instead.
    
    Parameters
    ----------
    role_id : `int`
        The unique identifier number of the role.
    guild_id : `int` = `0`, Optional
        The role's guild's identifier.
    
    Returns
    -------
    role : ``Role``
    """
    try:
        return ROLES[role_id]
    except KeyError:
        pass
    
    role = Role._create_empty(role_id, guild_id)
    ROLES[role_id] = role
    
    return role


def cr_p_role_object(name, **keyword_parameters):
    """
    Deprecated, please use `Role(..).to_data(...)` instead.
    
    Will be removed in 2023 February.
    """
    warnings.warn(
        (
            f'`cr_p_role_object` is deprecated and will be removed in 2023 February. '
            f'Please use `Role(..).to_data(...)` instead.'
        ),
        FutureWarning,
        stacklevel = 2,
    )
    return Role(name = name, **keyword_parameters).to_data()


def parse_role_mention(text):
    """
    If the text is a role mention, returns the respective role if found.
    
    Parameters
    ----------
    text : `str`
       The text to parse the role out from.
    
    Returns
    -------
    role : `None`, ``Role``
        The found role if any.
    """
    parsed = ROLE_MENTION_RP.fullmatch(text)
    if parsed is None:
        return
    
    role_id = int(parsed.group(1))
    return ROLES.get(role_id, None)


def parse_role(text, message = None):
    """
    Tries to parse a role out from the given text.
    
    Parameters
    ----------
    text : `str`
        The text to parse the role out.
    
    message : `None`, ``Message`` = `None`, Optional
        Context for name based parsing.
    
    Returns
    -------
    role : `None`, ``Role``
        The found role if any.
    """
    parsed = ID_RP.fullmatch(text)
    if (parsed is not None):
        role_id = int(parsed.group(1))
        try:
            role = ROLES[role_id]
        except KeyError:
            pass
        else:
            return role
    
    role = parse_role_mention(text)
    if (role is not None):
        return role
    
    if (message is not None):
        guild = message.guild
        if (guild is not None):
            role = guild.get_role_like(text)
            if (role is not None):
                return role
    
    return None
