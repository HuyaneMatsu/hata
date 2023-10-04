__all__ = ('EntitlementOwnerType', 'EntitlementType',)

from ...bases import Preinstance as P, PreinstancedBase


class EntitlementType(PreinstancedBase):
    """
    Represents an entitlement's type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    value : `int`
        The Discord side identifier value of the entitlement type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``EntitlementType``) items
        Stores the created entitlement type instances. This container is accessed when translating a Discord
        entitlement type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The entitlement types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the entitlement types.
    
    Every predefined entitlement type can be accessed as class attribute as well:
    +---------------------------+---------------------------+-------+
    | Class attribute name      | Name                      | Value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
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


class EntitlementOwnerType(PreinstancedBase):
    """
    Represents an entitlement's owner's type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    value : `int`
        The Discord side identifier value of the entitlement's owner's type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``EntitlementOwnerType``) items
        Stores the created entitlement owner type instances. This container is accessed when translating a Discord
        entitlement owner type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The entitlement owner types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the entitlement owner types.
    
    Every predefined entitlement owner type can be accessed as class attribute as well:
    +---------------------------+---------------------------+-------+
    | Class attribute name      | Name                      | Value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | guild                     | guild                     | 1     |
    +---------------------------+---------------------------+-------+
    | user                      | user                      | 2     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    guild = P(1, 'guild')
    user = P(2, 'user')
