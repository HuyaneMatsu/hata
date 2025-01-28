__all__ = ('EntitlementOwnerType', 'EntitlementType',)

from ...bases import Preinstance as P, PreinstancedBase


class EntitlementType(PreinstancedBase, value_type = int):
    """
    Represents an entitlement's type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    
    value : `int`
        The Discord side identifier value of the entitlement type.
    
    Type Attributes
    ---------------
    Every predefined entitlement type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | Name                      | Value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | purchase                  | purchase                  | 1     |
    +---------------------------+---------------------------+-------+
    | premium_subscription      | premium subscription      | 2     |
    +---------------------------+---------------------------+-------+
    | developer_gift            | developer gift            | 3     |
    +---------------------------+---------------------------+-------+
    | test_mode_purchase        | test mode purchase        | 4     |
    +---------------------------+---------------------------+-------+
    | free_purchase             | free purchase             | 5     |
    +---------------------------+---------------------------+-------+
    | user_gift                 | user gift                 | 6     |
    +---------------------------+---------------------------+-------+
    | premium_purchase          | premium purchase          | 7     |
    +---------------------------+---------------------------+-------+
    | application_subscription  | application subscription  | 8     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    purchase = P(1, 'purchase')
    premium_subscription = P(2, 'premium subscription')
    developer_gift = P(3, 'developer gift')
    test_mode_purchase = P(4, 'test mode purchase')
    free_purchase = P(5, 'free purchase')
    user_gift = P(6, 'user gift')
    premium_purchase = P(7, 'premium purchase')
    application_subscription = P(8, 'application subscription')


class EntitlementOwnerType(PreinstancedBase, value_type = int):
    """
    Represents an entitlement's owner's type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    
    value : `int`
        The Discord side identifier value of the entitlement's owner's type.
        
    Type Attributes
    ---------------
    Every predefined entitlement owner type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | Name                      | Value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | guild                     | guild                     | 1     |
    +---------------------------+---------------------------+-------+
    | user                      | user                      | 2     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    guild = P(1, 'guild')
    user = P(2, 'user')
