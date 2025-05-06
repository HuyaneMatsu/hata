__all__ = (
    'ApplicationDiscoverabilityState', 'ApplicationEventWebhookEventType', 'ApplicationEventWebhookState',
    'ApplicationExplicitContentFilterLevel', 'ApplicationIntegrationType', 'ApplicationInteractionEventType',
    'ApplicationInteractionVersion', 'ApplicationInternalGuildRestriction', 'ApplicationMonetizationState',
    'ApplicationRPCState', 'ApplicationStoreState', 'ApplicationType', 'ApplicationVerificationState'
)

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationDiscoverabilityState(PreinstancedBase, value_type = int):
    """
    Represents an application's discoverability state.
    
    Attributes
    ----------
    name : `str`
        The name of the application discoverability state.
    
    value : `int`
        The Discord side identifier value of the application discoverability state.
        
    Type Attributes
    ---------------
    Every predefined application discoverability state can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | ineligible                | ineligible                | 1     |
    +---------------------------+---------------------------+-------+
    | not_discoverable          | not discoverable          | 2     |
    +---------------------------+---------------------------+-------+
    | discoverable              | discoverable              | 3     |
    +---------------------------+---------------------------+-------+
    | featurable                | featurable                | 4     |
    +---------------------------+---------------------------+-------+
    | blocked                   | blocked                   | 5     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    ineligible = P(1, 'ineligible')
    not_discoverable = P(2, 'not discoverable')
    discoverable = P(3, 'discoverable')
    featurable = P(4, 'featurable')
    blocked = P(5, 'blocked')


class ApplicationEventWebhookEventType(PreinstancedBase, value_type = str):
    """
    Represents an application's event webhook event type.
    
    Attributes
    ----------
    name : `str`
        The name of the application event webhook event type.
    
    value : `str`
        The Discord side identifier value of the application event webhook event type.
        
    Type Attributes
    ---------------
    Every predefined application event webhook event type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+---------------------------+
    | Type attribute name       | name                      | value                     |
    +===========================+===========================+===========================+
    | application_authorization | application authorization | 'APPLICATION_AUTHORIZED'  |
    +---------------------------+---------------------------+---------------------------+
    | entitlement_create        | entitlement create        | 'ENTITLEMENT_CREATE'      |
    +---------------------------+---------------------------+---------------------------+
    | quest_enrollment          | quest enrollment          | 'QUEST_USER_ENROLLMENT'   |
    +---------------------------+---------------------------+---------------------------+
    """
    __slots__ = ()
    
    # predefined
    application_authorization = P('APPLICATION_AUTHORIZED', 'application authorization')
    entitlement_create = P('ENTITLEMENT_CREATE', 'entitlement create')
    quest_enrollment = P('QUEST_USER_ENROLLMENT', 'quest enrollment')


class ApplicationEventWebhookState(PreinstancedBase, value_type = int):
    """
    Represents an application's event webhook state.
    
    Attributes
    ----------
    name : `str`
        The name of the application event webhook state.
    
    value : `int`
        The Discord side identifier value of the application event webhook state.
        
    Type Attributes
    ---------------
    Every predefined application event webhook state can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | disabled                  | disabled                  | 1     |
    +---------------------------+---------------------------+-------+
    | enabled                   | enabled                   | 2     |
    +---------------------------+---------------------------+-------+
    | auto_disabled             | auto-disabled             | 3     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    disabled = P(1, 'disabled')
    enabled = P(2, 'enabled')
    auto_disabled = P(3, 'auto-disabled')


class ApplicationExplicitContentFilterLevel(PreinstancedBase, value_type = int):
    """
    Represents an application's explicit content filter level.
    
    Attributes
    ----------
    name : `str`
        The name of the application explicit content filter level.
    
    value : `int`
        The Discord side identifier value of the application explicit content filter level.
        
    Type Attributes
    ---------------
    Every predefined application explicit content filter level can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | filtered                  | filtered                  | 1     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    filtered = P(1, 'filtered')


class ApplicationIntegrationType(PreinstancedBase, value_type = int):
    """
    Represents how an application can be integrated.
    
    Attributes
    ----------
    name : `str`
        The name of the application integration type.
    
    value : `int`
        The Discord side identifier value of the application integration type.
        
    Type Attributes
    ---------------
    Every predefined application integration type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | guild_install             | guild install             | 0     |
    +---------------------------+---------------------------+-------+
    | user_install              | user install              | 1     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    guild_install = P(0, 'guild install')
    user_install = P(1, 'user install')


class ApplicationInteractionEventType(PreinstancedBase, value_type = str):
    """
    Represents an application's interaction event type.
    
    Attributes
    ----------
    name : `str`
        The name of the application interaction event type.
    
    value : `str`
        The Discord side identifier value of the application interaction event type.
        
    Type Attributes
    ---------------
    Every predefined application interaction event type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | `''`  |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P('', 'none')


class ApplicationInteractionVersion(PreinstancedBase, value_type = int):
    """
    Represents an application interaction version.
    
    Attributes
    ----------
    name : `str`
        The name of the application interaction version.
    
    value : `int`
        The Discord side identifier value of the application interaction version.
    
    Type Attributes
    ---------------
    Every predefined application interaction version can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | every                     | every                     | 1     |
    +---------------------------+---------------------------+-------+
    | selective                 | selective                 | 2     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    every = P(1, 'every')
    selective = P(2, 'selective')


class ApplicationInternalGuildRestriction(PreinstancedBase, value_type = int):
    """
    Represents an application's internal guild restriction.
    
    > Note that could not find anything about this.
    
    Attributes
    ----------
    name : `str`
        The name of the application internal guild restriction.
    
    value : `int`
        The Discord side identifier value of the application internal guild restriction.
    
    Type Attributes
    ---------------
    Every predefined application internal guild restriction can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | restricted                | restricted                | 1     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    restricted = P(1, 'restricted')


class ApplicationMonetizationState(PreinstancedBase, value_type = int):
    """
    Represents an application's monetization state.
    
    Attributes
    ----------
    enabled : `bool`
        Whether monetization is enabled.
    
    locked : `bool`
        Whether monetization actions are locked.
    
    name : `str`
        The default name of the monetization state.
    
    settable : `bool`
        Whether the monetization state can be set.
    
    value : `int`
        The Discord side identifier value of the monetization state.
    
    Type Attributes
    ---------------
    Every predefined monetization state is also stored as a type attribute:
    
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | Type attribute name   | Name                  | Value     | Enabled   | Locked    | Settable  |
    +=======================+=======================+===========+===========+===========+===========+
    | none                  | none                  | 0         | `False`   | `False`   | `False`   |
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | disabled              | disabled              | 1         | `False`   | `False`   | `True`    |
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | provisional           | provisional           | 2         | `True`    | `False`   | `True`    |
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | rejected              | rejected              | 3         | `False`   | `True`    | `False`   |
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | approved              | approved              | 4         | `True`    | `False`   | `False`   |
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | blocked               | blocked               | 5         | `False`   | `True`    | `False`   |
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    """
    __slots__ = ('enabled', 'locked', 'settable')
    
    def __new__(cls, value, name = None, enabled = False, locked = False, settable = False):
        """
        Creates a monetization state.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the monetization state.
        
        name : `None | str` = `None`, Optional
            The default name of the monetization state.
        
        enabled : `bool` = `False`, Optional
            Whether monetization is enabled.
        
        locked : `bool` = `False`, Optional
            Whether monetization actions are locked.
        
        settable : `bool` = `False`, Optional
            Whether the monetization state can be set.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.enabled = enabled
        self.locked = locked
        self.settable = settable
        return self
    
    # predefined
    none = P(0, 'none', False, False, False)
    disabled = P(1, 'disabled', False, False, True)
    provisional = P(2, 'provisional', True, False, True)
    rejected = P(3, 'rejected', False, True, False)
    approved = P(4, 'approved', True, False, False)
    blocked = P(5, 'blocked', False, True, False)


class ApplicationRPCState(PreinstancedBase, value_type = int):
    """
    Represents an application rpc state.
    
    Attributes
    ----------
    name : `str`
        The name of the application rpc state.
    
    value : `int`
        The Discord side identifier value of the application rpc state.
    
    Type Attributes
    ---------------
    Every predefined application rpc state can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | not_submitted             | not submitted             | 1     |
    +---------------------------+---------------------------+-------+
    | submitted                 | submitted                 | 2     |
    +---------------------------+---------------------------+-------+
    | approved                  | approved                  | 3     |
    +---------------------------+---------------------------+-------+
    | rejected                  | rejected                  | 4     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    not_submitted = P(1, 'not submitted')
    submitted = P(2, 'submitted')
    approved = P(3, 'approved')
    rejected = P(4, 'rejected')


class ApplicationStoreState(PreinstancedBase, value_type = int):
    """
    Represents an application store state.
    
    Attributes
    ----------
    name : `str`
        The name of the application store state.
    
    value : `int`
        The Discord side identifier value of the application store state.
    
    Type Attributes
    ---------------
    Every predefined application store state can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | no_license                | no license                | 1     |
    +---------------------------+---------------------------+-------+
    | license                   | license                   | 2     |
    +---------------------------+---------------------------+-------+
    | submitted                 | submitted                 | 3     |
    +---------------------------+---------------------------+-------+
    | approved                  | approved                  | 4     |
    +---------------------------+---------------------------+-------+
    | rejected                  | rejected                  | 5     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    no_license = P(1, 'no license')
    license = P(2, 'license')
    submitted = P(3, 'submitted')
    approved = P(4, 'approved')
    rejected = P(5, 'rejected')


class ApplicationType(PreinstancedBase, value_type = int):
    """
    Represents an application type.
    
    Attributes
    ----------
    name : `str`
        The name of the application type.
    
    value : `int`
        The Discord side identifier value of the application type.
        
    Type Attributes
    ---------------
    Every predefined application type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | game                      | game                      | 1     |
    +---------------------------+---------------------------+-------+
    | music                     | music                     | 2     |
    +---------------------------+---------------------------+-------+
    | ticketed_event            | ticketed event            | 3     |
    +---------------------------+---------------------------+-------+
    | guild_role_subscription   | guild role subscription   | 4     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    game = P(1, 'game')
    music = P(2, 'music')
    ticketed_event = P(3, 'ticketed event')
    guild_role_subscription = P(4, 'guild role subscription')


class ApplicationVerificationState(PreinstancedBase, value_type = int):
    """
    Represents an application's verification state.
    
    Attributes
    ----------
    name : `str`
        The name of the application verification state.
    
    value : `int`
        The Discord side identifier value of the application verification state.
    
    Type Attributes
    ---------------
    Every predefined application verification state can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | ineligible                | ineligible                | 1     |
    +---------------------------+---------------------------+-------+
    | not_submitted             | not submitted             | 2     |
    +---------------------------+---------------------------+-------+
    | submitted                 | submitted                 | 3     |
    +---------------------------+---------------------------+-------+
    | approved                  | approved                  | 4     |
    +---------------------------+---------------------------+-------+
    | blocked                   | blocked                   | 5     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    ineligible = P(1, 'ineligible')
    not_submitted = P(2, 'not submitted')
    submitted = P(3, 'submitted')
    approved = P(4, 'approved')
    blocked = P(5, 'blocked')
