__all__ = ('IntegrationExpireBehavior',)

from ...bases import Preinstance as P, PreinstancedBase


class IntegrationExpireBehavior(PreinstancedBase):
    """
    Represents an ``IntegrationDetail``'s expire behavior.
    
    Attributes
    ----------
    name : `str`
        The name of the integration expire behavior.
    value : `int`
        The Discord side identifier value of the integration expire behavior.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``IntegrationExpireBehavior``) items
        Stores the predefined ``IntegrationExpireBehavior``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The integration expire behavior' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the integration expire behaviors.
    
    Every predefined expire behavior can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | remove_role           | remove_role   | 0     |
    +-----------------------+---------------+-------+
    | kick                  | kick          | 1     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    remove_role = P(0, 'remove_role')
    kick = P(1, 'kick')
