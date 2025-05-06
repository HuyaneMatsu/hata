__all__ = ('SubscriptionStatus',)

from ...bases import Preinstance as P, PreinstancedBase


class SubscriptionStatus(PreinstancedBase, value_type = int):
    """
    Represents a subscription's status.
    
    Attributes
    ----------
    name : `str`
        The name of the subscription status.
    
    value : `int`
        The identifier value the subscription status.
    
    Type Attributes
    ---------------
    Every predefined subscription status can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | Name          | Value |
    +=======================+===============+=======+
    | active                | active        | 0     |
    +-----------------------+---------------+-------+
    | ending                | ending        | 1     |
    +-----------------------+---------------+-------+
    | inactive              | inactive      | 2     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    active = P(0, 'active')
    ending = P(1, 'ending')
    inactive = P(2, 'inactive')
