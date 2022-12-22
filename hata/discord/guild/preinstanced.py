__all__ = (
    'ContentFilterLevel', 'GuildFeature', 'GuildJoinRequestStatus', 'HubType', 'MFA', 'MessageNotificationLevel',
    'NsfwLevel', 'VerificationLevel'
)

from ..bases import Preinstance as P, PreinstancedBase


class VerificationLevel(PreinstancedBase):
    """
    Represents Discord's verification level.
    
    Attributes
    ----------
    name : `str`
        The default name of the verification level.
    value : `int`
        The discord side identifier value of the verification level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VerificationLevel``) items
        Stores the predefined ``VerificationLevel``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The verification levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the verification levels.
    
    Every predefined verification level can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | low                   | low       | 1     |
    +-----------------------+-----------+-------+
    | medium                | medium    | 2     |
    +-----------------------+-----------+-------+
    | high                  | high      | 3     |
    +-----------------------+-----------+-------+
    | extreme               | extreme   | 4     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    low = P(1, 'low')
    medium = P(2, 'medium')
    high = P(3, 'high')
    extreme = P(4, 'extreme')



class ContentFilterLevel(PreinstancedBase):
    """
    Represents Discord's content filter level.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the content filter level.
    name : `str`
        The default name of the content filter level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ContentFilterLevel``) items
        Stores the predefined content filter levels. This container is accessed when translating a Discord side
        identifier of a content filter level. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `int`
        The verification filter levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the content filter levels.
    
    Every predefined content filter level is also stored as a class attribute:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | disabled              | disabled  | 0     |
    +-----------------------+-----------+-------+
    | no_role               | no_role   | 1     |
    +-----------------------+-----------+-------+
    | everyone              | everyone  | 2     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    disabled = P(0, 'disabled')
    no_role = P(1, 'no_role')
    everyone = P(2, 'everyone')



class GuildFeature(PreinstancedBase):
    """
    Represents a ``Guild``'s feature.
    
    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the guild feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``GuildFeature``) items
        Stores the predefined ``GuildFeature``-s.
    VALUE_TYPE : `type` = `str`
        The guild features' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the guild features. Guild features have the same value as name, so at their case it is not
        applicable.
    
    Every predefined guild feature can be accessed as class attribute as well:
    
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | Class attribute names                 | name                                  | value                                     |
    +=======================================+=======================================+===========================================+
    | application_command_permissions_v2    | application command permissions v2    | APPLICATION_COMMAND_PERMISSIONS_V2        |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | animated_banner                       | animated banner                       | ANIMATED_BANNER                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | animated_icon                         | animated icon                         | ANIMATED_ICON                             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | announcement_channels                 | announcement channels                 | NEWS                                      |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | auto_moderation_enabled               | auto moderation enabled               | AUTO_MODERATION                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | banner                                | banner                                | BANNER                                    |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | burst_reactions                       | burst reactions                       | BURST_REACTIONS                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | channel_banners                       | channel banners                       | CHANNEL_BANNER                            |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | channel_highlights                    | channel highlights                    | CHANNEL_HIGHLIGHTS                        |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | channel_highlights_disabled           | channel highlights disabled           | CHANNEL_HIGHLIGHTS_DISABLED               |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | commerce                              | commerce                              | COMMERCE                                  |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | creator_store_page                    | creator store page                    | CREATOR_STORE_PAGE                        |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | creator_monetizable                   | creator monetizable                   | CREATOR_MONETIZABLE                       |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | creator_monetizable_disabled          | creator monetizable disabled          | CREATOR_MONETIZABLE_DISABLED              |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | creator_monetizable_restricted        | creator monetizable restricted        | CREATOR_MONETIZABLE_RESTRICTED            |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | creator_monetizable_premium_service   | creator monetizable premium service   | CREATOR_MONETIZABLE_WHITEGLOVE            |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | creator_monetizable_temporarily       | creator monetizable temporarily       | CREATOR_MONETIZABLE_PROVISIONAL           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | community                             | community                             | COMMUNITY                                 |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | developer_support_guild               | developer support guild               | DEVELOPER_SUPPORT_SERVER                  |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | discoverable                          | discoverable                          | DISCOVERABLE                              |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | discoverable_disabled                 | discoverable disabled                 | DISCOVERABLE_DISABLED                     |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | discoverable_enabled_before           | discoverable enabled before           | ENABLED_DISCOVERABLE_BEFORE               |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | embedded_activities_experiment        | embedded activities experiment        | EXPOSED_TO_ACTIVITIES_WTP_EXPERIMENT      |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | featurable                            | featurable                            | FEATURABLE                                |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | has_directory_entry                   | has directory entry                   | HAS_DIRECTORY_ENTRY                       |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | home_override                         | home override                         | GUILD_HOME_OVERRIDE                       |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | home_test                             | home test                             | GUILD_HOME_TEST                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | hub                                   | hub                                   | HUB                                       |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | internal_employee_only                | internal employee only                | INTERNAL_EMPLOYEE_ONLY                    |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | invite_splash                         | invite splash                         | INVITE_SPLASH                             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | invites_disabled                      | invites disabled                      | INVITES_DISABLED                          |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | linked_to_hub                         | linked to hub                         | LINKED_TO_HUB                             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | marketplaces_connection_roles         | marketplaces connection roles         | MARKETPLACES_CONNECTION_ROLES             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | member_list_disabled                  | member list disabled                  | MEMBER_LIST_DISABLED                      |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | monetization_enabled                  | monetization enabled                  | MONETIZATION_ENABLED                      |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | more_emoji                            | more emoji                            | MORE_EMOJI                                |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | more_sticker                          | more sticker                          | MORE_STICKERS                             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | new_thread_permissions                | new thread permissions                | NEW_THREAD_PERMISSIONS                    |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | onboarding                            | onboarding                            | GUILD_ONBOARDING                          |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | onboarding_ever_enabled               | onboarding evert enabled              | GUILD_ONBOARDING_EVER_ENABLED             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | onboarding_has_prompts                | onboarding has prompts                | GUILD_ONBOARDING_HAS_PROMPTS              |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | partnered                             | partnered                             | PARTNERED                                 |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | preview_enabled                       | preview enabled                       | PREVIEW_ENABLED                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | private_threads                       | private threads                       | PRIVATE_THREADS                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | public                                | public                                | PUBLIC                                    |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | public_disabled                       | public disabled                       | PUBLIC_DISABLED                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | raid_alerts_enabled                   | raid alerts enabled                   | RAID_ALERTS_ENABLED                       |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | relay_enabled                         | relay enabled                         | RELAY_ENABLED                             |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | role_icons                            | role icons                            | ROLE_ICONS                                |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | role_subscriptions_enabled            | role subscriptions enabled            | ROLE_SUBSCRIPTIONS_ENABLED                |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | role_subscription_purchasable         | role subscription purchasable         | ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | text_in_stage_enabled                 | text in stage enabled                 | TEXT_IN_STAGE_ENABLED                     |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | text_in_voice_enabled                 | text in voice enabled                 | TEXT_IN_VOICE_ENABLED                     |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | thread_archive_seven_day              | thread archive seven day              | SEVEN_DAY_THREAD_ARCHIVE                  |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | thread_archive_three_day              | thread archive three day              | THREE_DAY_THREAD_ARCHIVE                  |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | threads_enabled                       | threads enabled                       | THREADS_ENABLED                           |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | threads_enabled_testing               | threads enabled testing               | THREADS_ENABLED_TESTING                   |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | thread_limit_increased                | thread limit increased                | INCREASED_THREAD_LIMIT                    |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | ticket_events_enabled                 | ticket events enabled                 | TICKETED_EVENTS_ENABLED                   |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | vanity_invite                         | vanity invite                         | VANITY_URL                                |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | verified                              | verified                              | VERIFIED                                  |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | vip_voice_regions                     | vip voice regions                     | VIP_REGIONS                               |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | welcome_screen_enabled                | welcome screen enabled                | WELCOME_SCREEN_ENABLED                    |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    | verification_screen_enabled           | verification screen enabled           | MEMBER_VERIFICATION_GATE_ENABLED          |
    +---------------------------------------+---------------------------------------+-------------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new guild feature with the given value.
        
        Parameters
        ----------
        value : `str`
            The guild feature's identifier value.
        
        Returns
        -------
        self : ``GuildFeature``
            The created guild feature.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value.lower().replace('_', ' ')
        self.INSTANCES[value] = self
        return self
    
    
    # predefined
    application_command_permissions_v2 = P('APPLICATION_COMMAND_PERMISSIONS_V2', 'application command permissions v2')
    animated_banner = P('ANIMATED_BANNER', 'animated banner')
    animated_icon = P('ANIMATED_ICON', 'animated icon')
    announcement_channels = P('NEWS', 'announcement channels')
    auto_moderation_enabled = P('AUTO_MODERATION', 'auto moderation enabled')
    banner = P('BANNER', 'banner')
    burst_reactions = P('BURST_REACTIONS', 'burst reactions')
    channel_banners = P('CHANNEL_BANNER', 'channel banners')
    channel_highlights = P('CHANNEL_HIGHLIGHTS', 'channel highlights')
    channel_highlights_disabled = P('CHANNEL_HIGHLIGHTS_DISABLED', 'channel highlights disabled')
    commerce = P('COMMERCE', 'commerce')
    creator_store_page = P('CREATOR_STORE_PAGE', 'creator store page')
    creator_monetizable = P('CREATOR_MONETIZABLE', 'creator monetizable')
    creator_monetizable_disabled = P('CREATOR_MONETIZABLE_DISABLED', 'creator monetizable disabled')
    creator_monetizable_restricted = P('CREATOR_MONETIZABLE_RESTRICTED', 'creator monetizable restricted')
    creator_monetizable_premium_service = P('CREATOR_MONETIZABLE_WHITEGLOVE', 'creator monetizable premium service')
    creator_monetizable_temporarily = P('CREATOR_MONETIZABLE_PROVISIONAL', 'creator monetizable temporarily')
    community = P('COMMUNITY', 'community')
    developer_support_guild = P('DEVELOPER_SUPPORT_SERVER', 'developer support guild')
    discoverable = P('DISCOVERABLE', 'discoverable')
    discoverable_disabled = P('DISCOVERABLE_DISABLED', 'discoverable disabled')
    embedded_activities_experiment = P('EXPOSED_TO_ACTIVITIES_WTP_EXPERIMENT', 'embedded activities experiment')
    discoverable_enabled_before = P('ENABLED_DISCOVERABLE_BEFORE', 'discoverable enabled before')
    featurable = P('FEATURABLE', 'featurable')
    has_directory_entry = P('HAS_DIRECTORY_ENTRY', 'has directory_entry')
    home_override = P('GUILD_HOME_OVERRIDE', 'home override')
    home_test = P('GUILD_HOME_TEST', 'home test')
    hub = P('HUB', 'hub')
    internal_employee_only = P('INTERNAL_EMPLOYEE_ONLY', 'internal employee only')
    invite_splash = P('INVITE_SPLASH', 'invite splash')
    invites_disabled = P('INVITES_DISABLED', 'invites disabled')
    linked_to_hub = P('LINKED_TO_HUB', 'linked to hub')
    marketplaces_connection_roles = P('MARKETPLACES_CONNECTION_ROLES', 'marketplaces connection roles')
    member_list_disabled = P('MEMBER_LIST_DISABLED', 'member list disabled')
    monetization_enabled = P('MONETIZATION_ENABLED', 'monetization enabled')
    more_emoji = P('MORE_EMOJI', 'more emoji')
    more_sticker = P('MORE_STICKERS', 'more sticker')
    new_thread_permissions = P('NEW_THREAD_PERMISSIONS', 'new thread permissions')
    onboarding = P('GUILD_ONBOARDING', 'onboarding')
    onboarding_ever_enabled  = P('GUILD_ONBOARDING_EVER_ENABLED', 'onboarding evert enabled')
    onboarding_has_prompts  = P('GUILD_ONBOARDING_HAS_PROMPTS', 'onboarding has prompts')
    partnered = P('PARTNERED', 'partnered')
    preview_enabled = P('PREVIEW_ENABLED', 'preview enabled')
    private_threads = P('PRIVATE_THREADS', 'private threads')
    public = P('PUBLIC', 'public')
    public_disabled = P('PUBLIC_DISABLED', 'public disabled')
    raid_alerts_enabled = P('RAID_ALERTS_ENABLED', 'raid alerts enabled')
    relay_enabled = P('RELAY_ENABLED', 'relay enabled')
    role_icons = P('ROLE_ICONS', 'role icons')
    role_subscriptions_enabled = P('ROLE_SUBSCRIPTIONS_ENABLED', 'role subscriptions enabled')
    role_subscription_purchasable = P('ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE', 'role subscription purchasable')
    text_in_stage_enabled = P('TEXT_IN_STAGE_ENABLED', 'text in stage enabled')
    text_in_voice_enabled = P('TEXT_IN_VOICE_ENABLED', 'text in voice enabled')
    thread_archive_seven_day = P('SEVEN_DAY_THREAD_ARCHIVE', 'thread archive seven day')
    thread_archive_three_day = P('THREE_DAY_THREAD_ARCHIVE', 'thread archive three day')
    threads_enabled = P('THREADS_ENABLED', 'threads enabled')
    threads_enabled_testing = P('THREADS_ENABLED_TESTING', 'threads enabled testing')
    thread_limit_increased = P('INCREASED_THREAD_LIMIT', 'thread limit increased')
    ticket_events_enabled = P('TICKETED_EVENTS_ENABLED', 'ticket events enabled')
    vanity_invite = P('VANITY_URL', 'vanity invite')
    verification_screen_enabled = P('MEMBER_VERIFICATION_GATE_ENABLED', 'verification screen enabled')
    verified = P('VERIFIED', 'verified')
    vip_voice_regions = P('VIP_REGIONS', 'vip_voice_regions')
    welcome_screen_enabled = P('WELCOME_SCREEN_ENABLED', 'welcome screen enabled')


class NsfwLevel(PreinstancedBase):
    """
    Represents a guild's nsfw level.
    
    Attributes
    ----------
    name : `str`
        The name of the nsfw filter level.
    value : `int`
        The identifier value the nsfw filter level
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``NsfwLevel``) items
        Stores the predefined ``NsfwLevel``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The nsfw level' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the nsfw levels.
    
    Every predefined nsfw level can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+-------+
    | Class attribute name  | Name              | Value | nsfw  |
    +=======================+===================+=======+=======+
    | none                  | none              | 0     | False |
    +-----------------------+-------------------+-------+-------+
    | explicit              | explicit          | 1     | True  |
    +-----------------------+-------------------+-------+-------+
    | safe                  | safe              | 2     | False |
    +-----------------------+-------------------+-------+-------+
    | age_restricted        | age_restricted    | 3     | True  |
    +-----------------------+-------------------+-------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('nsfw', )
    
    def __init__(self, value, name, nsfw):
        """
        Creates a new nsfw level instance.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value of the nsfw level.
        name : `str`
            The nsfw level name.
        nsfw : `bool`
            Whether the nsfw level refers to being actually nsfw.
        """
        self.value = value
        self.name = name
        self.nsfw = nsfw
        
        self.INSTANCES[value] = self
    
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new nsfw level from the given value
        
        Parameters
        ----------
        value : `int`
            The nsfw level's identifier value.
        
        Returns
        -------
        self : ``NsfwLevel``
            The created nsfw level.
        """
        self = object.__new__(cls)
        
        self.value = value
        self.name = ''
        self.nsfw = True
        self.INSTANCES[value] = self
        
        return self
    
    
    def __repr__(self):
        """Returns the nsfw level's representation."""
        return f'{self.__class__.__name__}(value = {self.value!r}, name = {self.name!r}, nsfw = {self.nsfw!r})'
    
    
    none = P(0, 'none', False)
    explicit = P(1, 'explicit', True)
    safe = P(2, 'safe', False)
    age_restricted = P(2, 'age_restricted', True)


class MessageNotificationLevel(PreinstancedBase):
    """
    Represents the default message notification level of a ``Guild``.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the message notification level.
    name : `str`
        The default name of the message notification level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageNotificationLevel``) items
        Stores the predefined message notification levels. This container is accessed when translating message
        notification level's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The notification levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the notification levels.
    
    Each predefined message notification level can also be accessed as a class attribute:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | all_messages          | all_messages  | 0     |
    +-----------------------+---------------+-------+
    | only_mentions         | only_mentions | 1     |
    +-----------------------+---------------+-------+
    | no_message            | no_messages   | 2     |
    +-----------------------+---------------+-------+
    | null                  | null          | 3     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    all_messages = P(0, 'all_messages')
    only_mentions = P(1, 'only_mentions')
    no_messages = P(2, 'no_messages')
    null = P(3, 'null')


class MFA(PreinstancedBase):
    """
    Represents Discord's Multi-Factor Authentication's levels.
    
    Attributes
    ----------
    name : `str`
        The default name of the MFA level.
    value : `int`
        The Discord side identifier value of the MFA level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MFA``) items
        Stores the predefined MFA level. This container is accessed when converting an MFA level's value to
        it's wrapper side representation.
    VALUE_TYPE : `type` = `int`
        The mfa levels' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the mfa levels.
    
    Each predefined MFA can also be accessed as class attribute:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | elevated              | elevated  | 1     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # Predefined
    none = P(0, 'none')
    elevated = P(1, 'elevated')


class GuildJoinRequestStatus(PreinstancedBase):
    """
    Represents the status of a ``GuildJoinRequest``.
    
    Attributes
    ----------
    name : `str`
        The name of the guild join request status.
    value : `str`
        The Discord side identifier value of the guild join request status.
    

    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``GuildJoinRequestStatus``) items
        Stores the predefined ``GuildJoinRequestStatus``-s.
    VALUE_TYPE : `type` = `str`
        The guild join request statuses' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the guild join request statuses. Guild join request statuses have their name generated from
        their value, so at their case it is not applicable.
    
    Every predefined guild join request status can be accessed as class attribute as well:
    
    +-----------------------+-----------+-----------+
    | Class attribute names | Name      | Value     |
    +=======================+===========+===========+
    | approved              | approved  | APPROVED  |
    +-----------------------+-----------+-----------+
    | pending               | pending   | PENDING   |
    +-----------------------+-----------+-----------+
    | rejected              | rejected  | REJECTED  |
    +-----------------------+-----------+-----------+
    | started               | started   | STARTED   |
    +-----------------------+-----------+-----------+
    """
    
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new guild join request status from the given value.
        
        Parameters
        ----------
        value : `str`
            The guild join request status's identifier value.
        
        Returns
        -------
        self : ``GuildJoinRequestStatus``
            The guild join request status.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value.lower().replace('_', ' ')
        self.INSTANCES[value] = self
        return self
    
    def __repr__(self):
        """Returns the representation of the guild join request status."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    approved = P('APPROVED', 'approved')
    pending = P('PENDING', 'pending')
    rejected = P('REJECTED', 'rejected')
    started = P('STARTED', 'started')


class VerificationFieldPlatform(PreinstancedBase):
    """
    Represents the verification field platform of a verification screen.
    
    Attributes
    ----------
    name : `str`
        The name of the verification field platform.
    value : `str`
        The Discord side identifier value of the verification field platform.
    

    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VerificationFieldPlatform``) items
        Stores the predefined ``VerificationFieldPlatform``-s.
    VALUE_TYPE : `type` = `str`
        The verification field platforms' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the verification field platforms. Verification field platforms have their name generated from
        their value, so at their case it is not applicable.
    
    Every predefined verification field platform can be accessed as class attribute as well:
    
    +-----------------------+-----------+-----------+
    | Class attribute names | Name      | Value     |
    +=======================+===========+===========+
    | email                 | email     | email     |
    +-----------------------+-----------+-----------+
    | phone                 | phone     | phone     |
    +-----------------------+-----------+-----------+
    """
    
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new verification field platform from the given value.
        
        Parameters
        ----------
        value : `str`
            The verification field platform's identifier value.
        
        Returns
        -------
        self : ``VerificationFieldPlatform``
            The verification field platform.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value
        self.INSTANCES[value] = self
        return self
    
    def __repr__(self):
        """Returns the representation of the verification field platform."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    email = P('email', 'email')
    phone = P('phone', 'phone')


class HubType(PreinstancedBase):
    """
    Represents Discord's guild's hub type.
    
    Attributes
    ----------
    name : `str`
        The default name of the hub type
    value : `int`
        The Discord side identifier value of the hub type
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``HubType``) items
        Stores the predefined Hub types. This container is accessed when converting an Hub types' value to
        it's wrapper side representation.
    VALUE_TYPE : `type` = `int`
        The hub types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the hub types
    
    Each predefined hub type can also be accessed as class attribute:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | high_school           | high school   | 1     |
    +-----------------------+---------------+-------+
    | college               | college       | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # Predefined
    none = P(0, 'none')
    high_school = P(1, 'high school')
    college = P(2, 'college')
