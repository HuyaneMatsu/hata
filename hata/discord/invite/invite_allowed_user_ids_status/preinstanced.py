__all__ = ()

from ...bases import Preinstance as P, PreinstancedBase


class InviteAllowedUserIdsStatusStatus(PreinstancedBase, value_type = int):
    """
    Represents an invite allowed user identifiers status's status.
    
    Attributes
    ----------
    name : `str`
        The name of the invite allowed user identifiers status.
    
    value : `int`
        The Discord side identifier value of the invite allowed user identifiers status.
        
    Type Attributes
    ---------------
    Every predefined invite allowed user identifiers status can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | processing                | processing                | 1     |
    +---------------------------+---------------------------+-------+
    | completed                 | completed                 | 2     |
    +---------------------------+---------------------------+-------+
    | failed                    | auto-failed               | 3     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    processing = P(1, 'processing')
    completed = P(2, 'completed')
    failed = P(3, 'failed')
