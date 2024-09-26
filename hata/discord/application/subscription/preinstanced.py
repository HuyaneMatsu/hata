__all__ = ('SubscriptionStatus',)

from ...bases import Preinstance as P, PreinstancedBase


class SubscriptionStatus(PreinstancedBase):
    """
    Represents a subscription's status.
    
    Attributes
    ----------
    name : `str`
        The name of the subscription status.
    value : `int`
        The identifier value the subscription status.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SubscriptionStatus``) items
        Stores the predefined ``SubscriptionStatus``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The subscription status' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the subscription statuses.
    
    Every predefined subscription status can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | active                | active        | 0     |
    +-----------------------+---------------+-------+
    | ending                | ending        | 1     |
    +-----------------------+---------------+-------+
    | inactive              | inactive      | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    active = P(0, 'active')
    ending = P(1, 'ending')
    inactive = P(2, 'inactive')
