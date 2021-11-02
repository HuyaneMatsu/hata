__all__ = ('create_partial_role_from_id', 'cr_p_role_object', 'parse_role', 'parse_role_mention')

from ...backend.export import export

from ..core import ROLES
from ..color import Color
from ..permission import Permission
from ..permission.permission import PERMISSION_NONE
from ..utils import random_id, ROLE_MENTION_RP, ID_RP
from ..bases import ICON_TYPE_NONE

from .preinstanced import RoleManagerType
from .role import Role

ROLE_MANAGER_TYPE_NONE = RoleManagerType.none

@export
def create_partial_role_from_id(role_id):
    """
    Creates a partial role from the given `role_id`. If the role already exists returns that instead.
    
    Parameters
    ----------
    role_id : `int`
        The unique identifier number of the role.
    
    Returns
    -------
    role : ``Role``
    """
    try:
        return ROLES[role_id]
    except KeyError:
        pass
    
    role = Role._create_empty(role_id)
    ROLES[role_id] = role
    
    return role

def cr_p_role_object(name, role_id=None, color=Color(), separated=False, position=0, permissions=Permission(),
        managed=False, mentionable=False):
    """
    Creates a json serializable object representing a ``Role``.
    
    Parameters
    ----------
    name : `str`
        The name of the role.
    role_id : `None` or `int`,`optional
        The role's unique identifier number. If given as `None`, then a random `id` will be generated.
    color : ``Color``, Optional
        The role's color. Defaults to `Color(0)`
    separated : `bool`, Optional
        Users show up in separated groups by their highest `separated` role. Defaults to `False`.
    position : `int`, Optional
        The role's position at the guild. Defaults to `0`.
    permissions : ``Permission``, Optional
        The permissions of the users having the role.
    managed : `bool`, Optional
        Whether the role is managed by an integration.
    mentionable : `bool`, Optional
        Whether the role can be mentioned.
    
    Returns
    -------
    role_data : `dict` of (`str`, `Any`) items
    """
    if role_id is None:
        role_id = random_id()
    
    return {
        'id': role_id,
        'name': name,
        'color': color,
        'hoist': separated,
        'position': position,
        'permissions': permissions,
        'managed': managed,
        'mentionable': mentionable,
    }


def parse_role_mention(text):
    """
    If the text is a role mention, returns the respective role if found.
    
    Parameters
    ----------
    text : `str`
       The text to parse the role out from.
    
    Returns
    -------
    role : `None` or ``Role``
        The found role if any.
    """
    parsed = ROLE_MENTION_RP.fullmatch(text)
    if parsed is None:
        return
    
    role_id = int(parsed.group(1))
    return ROLES.get(role_id, None)


def parse_role(text, message=None):
    """
    Tries to parse a role out from the given text.
    
    Parameters
    ----------
    text : `str`
        The text to parse the role out.
    message : `None` or ``Message``, Optional
        Context for name based parsing.
    
    Returns
    -------
    role : `None` or ``Role``
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
