__all__ = ('IntegrationExpireBehavior',)

from ...bases import Preinstance as P, PreinstancedBase


class IntegrationExpireBehavior(PreinstancedBase, value_type = int):
    """
    Represents an ``IntegrationDetail``'s expire behavior.
    
    Attributes
    ----------
    name : `str`
        The name of the integration expire behavior.
    
    value : `int`
        The Discord side identifier value of the integration expire behavior.
    
    Type Attributes
    ---------------
    Every predefined expire behavior can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
    +=======================+===============+=======+
    | remove_role           | remove_role   | 0     |
    +-----------------------+---------------+-------+
    | kick                  | kick          | 1     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    remove_role = P(0, 'remove_role')
    kick = P(1, 'kick')
