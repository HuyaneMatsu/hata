__all__ = ('create_partial_role_from_id', 'parse_role', 'parse_role_mention')

from functools import partial as partial_func

from scarletio import export

from ...core import ROLES
from ...utils import ID_RP, ROLE_MENTION_RP

from .fields import (
    put_color, put_color_configuration, put_flags, put_mentionable, put_name, put_permissions, put_position,
    put_separated, put_unicode_emoji, validate_color, validate_color_configuration, validate_flags,
    validate_mentionable, validate_name, validate_permissions, validate_position, validate_separated,
    validate_unicode_emoji
)
from .role import ROLE_ICON, Role


ROLE_FIELD_CONVERTERS = {
    'color': (validate_color, put_color),
    'color_configuration': (validate_color_configuration, put_color_configuration),
    'flags': (validate_flags, put_flags),
    'icon': (partial_func(ROLE_ICON.validate_icon, allow_data = True), partial_func(ROLE_ICON.put_into, as_data = True)),
    'mentionable': (validate_mentionable, put_mentionable),
    'name': (validate_name, put_name),
    'permissions': (validate_permissions, put_permissions),
    'position': (validate_position, put_position),
    'separated': (validate_separated, put_separated),
    'unicode_emoji': (validate_unicode_emoji, put_unicode_emoji),
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


def parse_role(text, guild = None):
    """
    Tries to parse a role out from the given text.
    
    Parameters
    ----------
    text : `str`
        The text to parse the role out.
    
    guild : ``None | Guild`` = `None`, Optional
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
    
    if (guild is not None):
        if (guild is not None):
            role = guild.get_role_like(text)
            if (role is not None):
                return role
    
    return None
