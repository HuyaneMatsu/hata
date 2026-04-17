__all__ = ('EntitlementOwnerType', 'EntitlementSourceType', 'EntitlementType',)

from ...bases import Preinstance as P, PreinstancedBase


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


class EntitlementSourceType(PreinstancedBase, value_type = int):
    """
    Represents an entitlement's source's type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    
    value : `int`
        The Discord side identifier value of the entitlement's source's type.
        
    Type Attributes
    ---------------
    Every predefined entitlement source type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | Name                      | Value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | quest_reward              | quest reward              | 1     |
    +---------------------------+---------------------------+-------+
    | developer_gift            | developer gift            | 2     |
    +---------------------------+---------------------------+-------+
    | invoice                   | invoice                   | 3     |
    +---------------------------+---------------------------+-------+
    | reverse_trial             | reverse trial             | 4     |
    +---------------------------+---------------------------+-------+
    | user_gift                 | user gift                 | 5     |
    +---------------------------+---------------------------+-------+
    | guild_enhancement         | guild enhancement         | 6     |
    +---------------------------+---------------------------+-------+
    | first_party_promotion     | first party promotion     | 7     |
    +---------------------------+---------------------------+-------+
    | fraction_premium_giveaway | fraction premium giveaway | 8     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    quest_reward = P(1, 'quest reward')
    developer_gift = P(2, 'developer gift')
    invoice = P(3, 'invoice')
    reverse_trial = P(4, 'reverse trial')
    user_gift = P(5, 'user gift')
    guild_enhancement = P(6, 'guild enhancement')
    first_party_promotion = P(7, 'first party promotion')
    fraction_premium_giveaway = P(8, 'fractional premium giveaway')


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
    
    +-------------------------------+-------------------------------+-------+
    | Type attribute name           | Name                          | Value |
    +===============================+===============================+=======+
    | none                          | none                          | 0     |
    +-------------------------------+-------------------------------+-------+
    | purchase                      | purchase                      | 1     |
    +-------------------------------+-------------------------------+-------+
    | premium_subscription          | premium subscription          | 2     |
    +-------------------------------+-------------------------------+-------+
    | developer_gift                | developer gift                | 3     |
    +-------------------------------+-------------------------------+-------+
    | test_mode_purchase            | test mode purchase            | 4     |
    +-------------------------------+-------------------------------+-------+
    | free_purchase                 | free purchase                 | 5     |
    +-------------------------------+-------------------------------+-------+
    | user_gift                     | user gift                     | 6     |
    +-------------------------------+-------------------------------+-------+
    | premium_purchase              | premium purchase              | 7     |
    +-------------------------------+-------------------------------+-------+
    | application_subscription      | application subscription      | 8     |
    +-------------------------------+-------------------------------+-------+
    | free_staff_purchase           | free staff purchase           | 9     |
    +-------------------------------+-------------------------------+-------+
    | quest_reward                  | quest reward                  | 10    |
    +-------------------------------+-------------------------------+-------+
    | fractional_redemption         | fractional redemption         | 11    |
    +-------------------------------+-------------------------------+-------+
    | virtual_currency_redemption   | virtual currency redemption   | 12    |
    +-------------------------------+-------------------------------+-------+
    | guild_enhancement             | guild enhancement             | 13    |
    +-------------------------------+-------------------------------+-------+
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
    free_staff_purchase = P(9, 'free staff purchase')
    quest_reward = P(10, 'quest reward')
    fractional_redemption = P(11, 'fractional redemption')
    virtual_currency_redemption = P(12, 'virtual currency redemption')
    guild_enhancement = P(13, 'guild enhancement')
