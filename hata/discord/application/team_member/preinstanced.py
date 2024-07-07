__all__ = ('TeamMemberRole', 'TeamMembershipState',)

from ...bases import Preinstance as P, PreinstancedBase


class TeamMembershipState(PreinstancedBase):
    """
    Represents a ``TeamMember``'s state at a ``Team``.
    
    Attributes
    ----------
    name : `str`
        The name of the state.
    value : `int`
        The Discord side identifier value of the team membership state.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``TeamMembershipState``) items
        Stores the created team membership state instances. This container is accessed when translating a Discord
        team membership state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The team membership states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the team membership states.
    
    Every predefined team membership state can be accessed as class attribute as well:
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | invited               | invited   | 1     |
    +-----------------------+-----------+-------+
    | accepted              | accepted  | 2     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    invited = P(1, 'invited')
    accepted = P(2, 'accepted')


class TeamMemberRole(PreinstancedBase):
    """
    Represents a role of a ``TeamMember``.
    
    Attributes
    ----------
    name : `str`
        The name of role.
    value : `str`
        The Discord side identifier value of the team member role.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``TeamMemberRole``) items
        Stores the created team member role instances. This container is accessed when translating a Discord
        team member role's value to it's representation.
    VALUE_TYPE : `type` = `str`
        The team member roles' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the team member roles.
    
    Every predefined team member role can be accessed as class attribute as well:
    +-----------------------+---------------+---------------+
    | Class attribute name  | name          | value         |
    +=======================+===============+===============+
    | admin                 | admin         | `'admin'`     |
    +-----------------------+---------------+---------------+
    | developer             | developer     | `'developer'` |
    +-----------------------+---------------+---------------+
    | owner                 | owner         | `'owner'`     |
    +-----------------------+---------------+---------------+
    | read_only             | read_only     | `'read_only'` |
    +-----------------------+---------------+---------------+
    | none                  | none          | `''`          |
    +-----------------------+---------------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    admin = P('admin', 'admin')
    developer = P('developer', 'developer')
    owner = P('owner', 'owner')
    read_only = P('read_only', 'read_only')
    none = P('', 'none')
