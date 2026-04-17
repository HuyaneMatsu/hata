__all__ = ('TeamMemberRole', 'TeamMembershipState',)

from ...bases import Preinstance as P, PreinstancedBase


class TeamMembershipState(PreinstancedBase, value_type = int):
    """
    Represents a ``TeamMember``'s state at a ``Team``.
    
    Attributes
    ----------
    name : `str`
        The name of the state.
    
    value : `int`
        The Discord side identifier value of the team membership state.
        
    Type Attributes
    ---------------
    Every predefined team membership state can be accessed as type attribute as well:
    +-----------------------+-----------+-------+
    | Type attribute name   | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | invited               | invited   | 1     |
    +-----------------------+-----------+-------+
    | accepted              | accepted  | 2     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    invited = P(1, 'invited')
    accepted = P(2, 'accepted')


class TeamMemberRole(PreinstancedBase, value_type = str):
    """
    Represents a role of a ``TeamMember``.
    
    Attributes
    ----------
    name : `str`
        The name of role.
    
    value : `str`
        The Discord side identifier value of the team member role.
        
    Type Attributes
    ---------------
    Every predefined team member role can be accessed as type attribute as well:
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
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
    __slots__ = ()
    
    # predefined
    admin = P('admin', 'admin')
    developer = P('developer', 'developer')
    owner = P('owner', 'owner')
    read_only = P('read_only', 'read_only')
    none = P('', 'none')
