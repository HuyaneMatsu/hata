__all__ = (
    'ApplicationDiscoverabilityState', 'ApplicationEventWebhookEventType', 'ApplicationEventWebhookState',
    'ApplicationExplicitContentFilterLevel', 'ApplicationIntegrationType', 'ApplicationInteractionEventType',
    'ApplicationInteractionVersion', 'ApplicationInternalGuildRestriction', 'ApplicationMonetizationState',
    'ApplicationRPCState', 'ApplicationStoreState', 'ApplicationType', 'ApplicationVerificationState'
)

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationDiscoverabilityState(PreinstancedBase):
    """
    Represents an application's discoverability state.
    
    Attributes
    ----------
    name : `str`
        The name of the application discoverability state.
    value : `int`
        The Discord side identifier value of the application discoverability state.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationDiscoverabilityState``) items
        Stores the created application discoverability state instances. This container is accessed when translating a
        Discord application discoverability state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application discoverability states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application discoverability states.
    
    Every predefined application discoverability state can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    ineligible = P(1, 'ineligible')
    not_discoverable = P(2, 'not discoverable')
    discoverable = P(3, 'discoverable')
    featurable = P(4, 'featurable')
    blocked = P(5, 'blocked')


class ApplicationEventWebhookEventType(PreinstancedBase):
    """
    Represents an application's event webhook event type.
    
    Attributes
    ----------
    name : `str`
        The name of the application event webhook event type.
    
    value : `str`
        The Discord side identifier value of the application event webhook event type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationDiscoverabilityState``) items
        Stores the created application event webhook event type instances. This container is accessed when translating a
        Discord application event webhook event type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application event webhook event types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application event webhook event types.
    
    Every predefined application event webhook event type can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+---------------------------+
    | Class attribute name      | name                      | value                     |
    +===========================+===========================+===========================+
    | application_authorization | application authorization | 'APPLICATION_AUTHORIZED'  |
    +---------------------------+---------------------------+---------------------------+
    | entitlement_create        | entitlement create        | 'ENTITLEMENT_CREATE'      |
    +---------------------------+---------------------------+---------------------------+
    | quest_enrollment          | quest enrollment          | 'QUEST_USER_ENROLLMENT'   |
    +---------------------------+---------------------------+---------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    application_authorization = P('APPLICATION_AUTHORIZED', 'application authorization')
    entitlement_create = P('ENTITLEMENT_CREATE', 'entitlement create')
    quest_enrollment = P('QUEST_USER_ENROLLMENT', 'quest enrollment')


class ApplicationEventWebhookState(PreinstancedBase):
    """
    Represents an application's event webhook state.
    
    Attributes
    ----------
    name : `str`
        The name of the application event webhook state.
    
    value : `int`
        The Discord side identifier value of the application event webhook state.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationDiscoverabilityState``) items
        Stores the created application event webhook state instances. This container is accessed when translating a
        Discord application event webhook state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application event webhook states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application event webhook states.
    
    Every predefined application event webhook state can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    disabled = P(1, 'disabled')
    enabled = P(2, 'enabled')
    auto_disabled = P(3, 'auto-disabled')


class ApplicationExplicitContentFilterLevel(PreinstancedBase):
    """
    Represents an application's explicit content filter level.
    
    Attributes
    ----------
    name : `str`
        The name of the application explicit content filter level.
    value : `int`
        The Discord side identifier value of the application explicit content filter level.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationExplicitContentFilterLevel``) items
        Stores the created application explicit content filter level instances. This container is accessed when translating a
        Discord application explicit content filter level's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application explicit content filter levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application explicit content filter levels.
    
    Every predefined application explicit content filter level can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | filtered                  | filtered                  | 1     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    filtered = P(1, 'filtered')


class ApplicationIntegrationType(PreinstancedBase):
    """
    Represents how an application can be integrated.
    
    Attributes
    ----------
    name : `str`
        The name of the application integration type.
    value : `int`
        The Discord side identifier value of the application integration type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationIntegrationType``) items
        Stores the created application integration type instances. This container is accessed when translating a
        Discord application integration type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application integration types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application integration types.
    
    Every predefined application integration type can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | guild_install             | guild install             | 0     |
    +---------------------------+---------------------------+-------+
    | user_install              | user install              | 1     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    guild_install = P(0, 'guild install')
    user_install = P(1, 'user install')


class ApplicationInteractionEventType(PreinstancedBase):
    """
    Represents an application's interaction event type.
    
    Attributes
    ----------
    name : `str`
        The name of the application interaction event type.
    value : `int`
        The Discord side identifier value of the application interaction event type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationInteractionEventType``) items
        Stores the created application interaction event type instances. This container is accessed when translating a
        Discord application interaction event type's value to it's representation.
    VALUE_TYPE : `type` = `str`
        The application interaction event types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application interaction event types.
    
    Every predefined application interaction event type can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | `''`  |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    none = P('', 'none')


class ApplicationInteractionVersion(PreinstancedBase):
    """
    Represents an application interaction version.
    
    Attributes
    ----------
    name : `str`
        The name of the application interaction version.
    value : `int`
        The Discord side identifier value of the application interaction version.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationInteractionVersion``) items
        Stores the created application interaction version instances. This container is accessed when translating a
        Discord application interaction version's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application interaction versions' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application interaction versions.
    
    Every predefined application interaction version can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | every                     | every                     | 1     |
    +---------------------------+---------------------------+-------+
    | selective                 | selective                 | 2     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    every = P(1, 'every')
    selective = P(2, 'selective')


class ApplicationInternalGuildRestriction(PreinstancedBase):
    """
    Represents an application's internal guild restriction.
    
    > Note that could not find anything about this.
    
    Attributes
    ----------
    name : `str`
        The name of the application internal guild restriction.
    value : `int`
        The Discord side identifier value of the application internal guild restriction.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationInternalGuildRestriction``) items
        Stores the created application internal guild restriction instances. This container is accessed when
        translating a Discord application internal guild restriction's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application internal guild restrictions' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application internal guild restrictions.
    
    Every predefined application internal guild restriction can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | restricted                | restricted                | 1     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    restricted = P(1, 'restricted')


class ApplicationMonetizationState(PreinstancedBase):
    """
    Represents an application's monetization state.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the monetization state.
    name : `str`
        The default name of the monetization state.
    enabled : `bool`
        Whether monetization is enabled.
    locked : `bool`
        Whether monetization actions are locked.
    settable : `bool`
        Whether the monetization state can be set.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``ApplicationMonetizationState``) items
        Stores the predefined monetization states. This container is accessed when translating a Discord side
        identifier of a monetization state. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `state` = `str`
        The monetization states' values' state.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the monetization states.
    
    Every predefined monetization state is also stored as a class attribute:
    
    +-----------------------+-----------------------+-----------+-----------+-----------+-----------+
    | Class attribute name  | Name                  | Value     | Enabled   | Locked    | Settable  |
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
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new monetization state with the given value.
        
        Parameters
        ----------
        value : `int`
            The monetization state's identifier value.
        
        Returns
        -------
        self : `instance<cls>`
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.enabled = False
        self.locked = False
        self.settable = False
        
        return self
    
    
    def __init__(self, value, name, enabled, locked, settable):
        """
        Creates a monetization state and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the monetization state.
        name : `str`
            The default name of the monetization state.
        enabled : `bool`
            Whether monetization is enabled.
        locked : `bool`
            Whether monetization actions are locked.
        settable : `bool`
            Whether the monetization state can be set.
        """
        self.value = value
        self.name = name
        self.enabled = enabled
        self.locked = locked
        self.settable = settable
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', False, False, False)
    disabled = P(1, 'disabled', False, False, True)
    provisional = P(2, 'provisional', True, False, True)
    rejected = P(3, 'rejected', False, True, False)
    approved = P(4, 'approved', True, False, False)
    blocked = P(5, 'blocked', False, True, False)


class ApplicationRPCState(PreinstancedBase):
    """
    Represents an application rpc state.
    
    Attributes
    ----------
    name : `str`
        The name of the application rpc state.
    value : `int`
        The Discord side identifier value of the application rpc state.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationRPCState``) items
        RPCs the created application rpc state instances. This container is accessed when translating a
        Discord application rpc state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application rpc states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application rpc states.
    
    Every predefined application rpc state can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    not_submitted = P(1, 'not submitted')
    submitted = P(2, 'submitted')
    approved = P(3, 'approved')
    rejected = P(4, 'rejected')


class ApplicationStoreState(PreinstancedBase):
    """
    Represents an application store state.
    
    Attributes
    ----------
    name : `str`
        The name of the application store state.
    value : `int`
        The Discord side identifier value of the application store state.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationStoreState``) items
        Stores the created application store state instances. This container is accessed when translating a
        Discord application store state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application store states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application store states.
    
    Every predefined application store state can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    no_license = P(1, 'no license')
    license = P(2, 'license')
    submitted = P(3, 'submitted')
    approved = P(4, 'approved')
    rejected = P(5, 'rejected')


class ApplicationType(PreinstancedBase):
    """
    Represents an application type.
    
    Attributes
    ----------
    name : `str`
        The name of the application type.
    value : `int`
        The Discord side identifier value of the application type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationType``) items
        Stores the created application type instances. This container is accessed when translating a Discord
        application type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application types.
    
    Every predefined application type can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    game = P(1, 'game')
    music = P(2, 'music')
    ticketed_event = P(3, 'ticketed event')
    guild_role_subscription = P(4, 'guild role subscription')


class ApplicationVerificationState(PreinstancedBase):
    """
    Represents an application's verification state.
    
    Attributes
    ----------
    name : `str`
        The name of the application verification state.
    value : `int`
        The Discord side identifier value of the application verification state.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationVerificationState``) items
        Stores the created application verification state instances. This container is accessed when translating a
        Discord application verification state's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application verification states' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application verification states.
    
    Every predefined application verification state can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    ineligible = P(1, 'ineligible')
    not_submitted = P(2, 'not submitted')
    submitted = P(3, 'submitted')
    approved = P(4, 'approved')
    blocked = P(5, 'blocked')
