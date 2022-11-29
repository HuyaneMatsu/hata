__all__ = ('TeamMemberPermission', 'TeamMembershipState')

from ...bases import Preinstance as P, PreinstancedBase


class TeamMembershipState(PreinstancedBase):
    """
    Represents a ``TeamMember``'s state at a ``Team``.
    
    Attributes
    ----------
    name : `str`
        The name of state.
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


class TeamMemberPermission(PreinstancedBase):
    """
    Represents a permission of a ``TeamMember``.
    
    Attributes
    ----------
    name : `str`
        The name of permission.
    value : `str`
        The Discord side identifier value of the team member permission.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``TeamMemberPermission``) items
        Stores the created team member permission instances. This container is accessed when translating a Discord
        team member permission's value to it's representation.
    VALUE_TYPE : `type` = `str`
        The team member permissions' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the team member permissions.
    
    Every predefined team member permission can be accessed as class attribute as well:
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | `''`  |
    +-----------------------+-----------+-------+
    | admin                 | admin     | `'*'` |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    admin = P('*', 'admin')
