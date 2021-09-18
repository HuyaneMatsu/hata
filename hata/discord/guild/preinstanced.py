__all__ = ('AuditLogEvent', 'ContentFilterLevel', 'GuildFeature', 'MFA', 'MessageNotificationLevel', 'NsfwLevel',
    'VerificationLevel', 'VerificationScreenStepType', 'VoiceRegion', )

import warnings

from ...backend.export import export
from ...backend.utils import class_property
from ..bases import PreinstancedBase, Preinstance as P


class AuditLogEvent(PreinstancedBase):
    """
    Represents the event type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    name : `str`
        The name of audit log event.
    value : `int`
        The Discord side identifier value of the audit log event.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``AuditLogEvent``) items
        Stores the predefined ``AuditLogEvent`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The audit log events' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the audit log events
    
    Every predefined audit log event can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | guild_update              | guild_update              |  1    |
    +---------------------------+---------------------------+-------+
    | channel_create            | channel_create            | 10    |
    +---------------------------+---------------------------+-------+
    | channel_update            | channel_update            | 11    |
    +---------------------------+---------------------------+-------+
    | channel_delete            | channel_delete            | 12    |
    +---------------------------+---------------------------+-------+
    | channel_overwrite_create  | channel_overwrite_create  | 13    |
    +---------------------------+---------------------------+-------+
    | channel_overwrite_update  | channel_overwrite_update  | 14    |
    +---------------------------+---------------------------+-------+
    | channel_overwrite_delete  | channel_overwrite_delete  | 15    |
    +---------------------------+---------------------------+-------+
    | member_kick               | member_kick               | 20    |
    +---------------------------+---------------------------+-------+
    | member_prune              | member_prune              | 21    |
    +---------------------------+---------------------------+-------+
    | member_ban_add            | member_ban_add            | 22    |
    +---------------------------+---------------------------+-------+
    | member_ban_remove         | member_ban_remove         | 23    |
    +---------------------------+---------------------------+-------+
    | member_update             | member_update             | 24    |
    +---------------------------+---------------------------+-------+
    | member_role_update        | member_role_update        | 25    |
    +---------------------------+---------------------------+-------+
    | member_move               | member_move               | 26    |
    +---------------------------+---------------------------+-------+
    | member_disconnect         | member_disconnect         | 27    |
    +---------------------------+---------------------------+-------+
    | bot_add                   | bot_add                   | 28    |
    +---------------------------+---------------------------+-------+
    | role_create               | role_create               | 30    |
    +---------------------------+---------------------------+-------+
    | role_update               | role_update               | 31    |
    +---------------------------+---------------------------+-------+
    | role_delete               | role_delete               | 32    |
    +---------------------------+---------------------------+-------+
    | invite_create             | invite_create             | 40    |
    +---------------------------+---------------------------+-------+
    | invite_update             | invite_update             | 41    |
    +---------------------------+---------------------------+-------+
    | invite_delete             | invite_delete             | 42    |
    +---------------------------+---------------------------+-------+
    | webhook_create            | webhook_create            | 50    |
    +---------------------------+---------------------------+-------+
    | webhook_update            | webhook_update            | 51    |
    +---------------------------+---------------------------+-------+
    | webhook_delete            | webhook_delete            | 52    |
    +---------------------------+---------------------------+-------+
    | emoji_create              | emoji_create              | 60    |
    +---------------------------+---------------------------+-------+
    | emoji_update              | emoji_update              | 61    |
    +---------------------------+---------------------------+-------+
    | emoji_delete              | emoji_delete              | 62    |
    +---------------------------+---------------------------+-------+
    | message_delete            | message_delete            | 72    |
    +---------------------------+---------------------------+-------+
    | message_bulk_delete       | message_bulk_delete       | 73    |
    +---------------------------+---------------------------+-------+
    | message_pin               | message_pin               | 74    |
    +---------------------------+---------------------------+-------+
    | message_unpin             | message_unpin             | 75    |
    +---------------------------+---------------------------+-------+
    | integration_create        | integration_create        | 80    |
    +---------------------------+---------------------------+-------+
    | integration_update        | integration_update        | 81    |
    +---------------------------+---------------------------+-------+
    | integration_delete        | integration_delete        | 82    |
    +---------------------------+---------------------------+-------+
    | sticker_create            | sticker_create            | 90    |
    +---------------------------+---------------------------+-------+
    | sticker_update            | sticker_update            | 91    |
    +---------------------------+---------------------------+-------+
    | sticker_delete            | sticker_delete            | 92    |
    +---------------------------+---------------------------+-------+
    | scheduled_event_create    | scheduled_event_create    | 100   |
    +---------------------------+---------------------------+-------+
    | scheduled_event_update    | scheduled_event_update    | 101   |
    +---------------------------+---------------------------+-------+
    | scheduled_event_delete    | scheduled_event_delete    | 102   |
    +---------------------------+---------------------------+-------+
    | thread_create             | thread_create             | 110   |
    +---------------------------+---------------------------+-------+
    | thread_update             | thread_update             | 111   |
    +---------------------------+---------------------------+-------+
    | thread_delete             | thread_delete             | 112   |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    # predefined
    guild_update = P(1, 'guild_update')
    
    channel_create = P(10, 'channel_create')
    channel_update = P(11, 'channel_update')
    channel_delete = P(12, 'channel_delete')
    channel_overwrite_create = P(13, 'channel_overwrite_create')
    channel_overwrite_update = P(14, 'channel_overwrite_update')
    channel_overwrite_delete = P(15, 'channel_overwrite_delete')
    
    member_kick = P(20, 'member_kick')
    member_prune = P(21, 'member_prune')
    member_ban_add = P(22, 'member_ban_add')
    member_ban_remove = P(23, 'member_ban_remove')
    member_update = P(24, 'member_update')
    member_role_update = P(25, 'member_role_update')
    member_move = P(26, 'member_move')
    member_disconnect = P(27, 'member_disconnect')
    bot_add = P(28, 'member_role_update')
    
    role_create = P(30, 'role_create')
    role_update = P(31, 'role_update')
    role_delete = P(32, 'role_delete')
    
    invite_create = P(40, 'invite_create')
    invite_update = P(41, 'invite_update')
    invite_delete = P(42, 'invite_delete')
    
    webhook_create = P(50, 'webhook_create')
    webhook_update = P(51, 'webhook_update')
    webhook_delete = P(52, 'webhook_delete')
    
    emoji_create = P(60, 'emoji_create')
    emoji_update = P(61, 'emoji_update')
    emoji_delete = P(62, 'emoji_delete')
    
    message_delete = P(72, 'message_delete')
    message_bulk_delete = P(73, 'message_bulk_delete')
    message_pin = P(74, 'message_pin')
    message_unpin = P(75, 'message_unpin')
    
    integration_create = P(80, 'integration_create')
    integration_update = P(81, 'integration_update')
    integration_delete = P(82, 'integration_delete')
    
    sticker_create = P(90, 'sticker_create')
    sticker_update = P(91, 'sticker_update')
    sticker_delete = P(92, 'sticker_delete')
    
    scheduled_event_create = P(100, 'scheduled_event_create')
    scheduled_event_update = P(101, 'scheduled_event_update')
    scheduled_event_delete = P(102, 'scheduled_event_delete')
    
    thread_create = P(110, 'thread_create')
    thread_update = P(111, 'thread_update')
    thread_delete = P(112, 'thread_delete')


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
        Stores the predefined ``VerificationLevel`` instances. These can be accessed with their `value` as key.
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


@export
class VoiceRegion(PreinstancedBase):
    """
    Represents Discord's voice regions.
    
    Attributes
    ----------
    custom : `bool`
        Whether the voice region is custom (used for events, etc.).
    deprecated : `bool`
        Whether the voice region is deprecated.
    value : `str`
        The unique identifier of the voice region.
    name : `str`
        The default name of the voice region.
    vip : `bool`
        Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``VoiceRegion``) items
        Stores the created ``VoiceRegion`` instances.
    VALUE_TYPE : `type` = `str`
        The voice regions' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the voice regions.
    
    Each predefined voice region is also stored as a class attribute:
    
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | Class attribute name  | value         | name              | deprecated    | vip       | custom    |
    +=======================+===============+===================+===============+===========+===========+
    | brazil                | brazil        | Brazil            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | dubai                 | dubai         | Dubai             | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | eu_central            | eu-central    | Central Europe    | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | eu_west               | eu-west       | Western Europe    | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | europe                | europe        | Europe            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | hongkong              | hongkong      | Hong Kong         | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | india                 | india         | India             | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | japan                 | japan         | Japan             | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | russia                | russia        | Russia            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | singapore             | singapore     | Singapore         | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | africa_south          | southafrica   | South Africa      | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | sydney                | sydney        | Sydney            | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_central            | us-central    | US Central        | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_east               | us-east       | US East           | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_south              | us-south      | US South          | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | us_west               | us-west       | US West           | False         | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | amsterdam             | amsterdam     | Amsterdam         | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | frankfurt             | frankfurt     | Frankfurt         | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | london                | london        | London            | True          | False     | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | vip_us_east           | vip-us-east   | VIP US West       | False         | True      | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | vip_us_west           | vip-us-west   | VIP US East       | False         | True      | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    | vip_amsterdam         | vip-amsterdam | VIP Amsterdam     | True          | True      | False     |
    +-----------------------+---------------+-------------------+---------------+-----------+-----------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ('custom', 'deprecated', 'vip',)
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a voice region from the given id and stores it at class's `.INSTANCES`.
        
        Called by `.get` when no voice region was found with the given id.
        
        Parameters
        ----------
        id_ : `str`
            The identifier of the voice region.
        
        Returns
        -------
        self : ``VoiceRegion``
        """
        name_parts = value.split('-')
        for index in range(len(name_parts)):
            name_part = name_parts[index]
            if len(name_part) < 4:
                name_part = name_part.upper()
            else:
                name_part = name_part.capitalize()
            name_parts[index] = name_part
        
        name = ' '.join(name_parts)
        
        self = object.__new__(cls)
        self.name = name
        self.value = value
        self.deprecated = False
        self.vip = value.startswith('vip-')
        self.custom = True
        self.INSTANCES[value] = self
        return self
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a voice region from the given data and stores it at the class's `.INSTANCES`.
        
        If the voice region already exists returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received voice region data.

        Returns
        -------
        self : ``VoiceRegion``
        """
        value = data['id']
        try:
            return cls.INSTANCES[value]
        except KeyError:
            pass
        
        self = object.__new__(cls)
        self.name = data['name']
        self.value = value
        self.deprecated = data['deprecated']
        self.vip = data['vip']
        self.custom = data['custom']
        self.INSTANCES[value] = self
        
        return self
    
    def __init__(self, value, name, deprecated, vip):
        """
        Creates a new voice region with the given parameters and stores it at the class's `.INSTANCES`.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the voice region.
        name : `str`
            The voice region's name.
        deprecated : `bool`
            Whether the voice region is deprecated.
        name : `str`
            The default name of the voice region.
        vip : `bool`
            Whether the voice region can be used only by guilds with `VIP_REGIONS` feature.
        """
        self.name = name
        self.value = value
        self.deprecated = deprecated
        self.vip = vip
        self.custom = False
        self.INSTANCES[value] = self
    
    # predefined
    
    # normal
    brazil = P('brazil', 'Brazil', False, False)
    dubai = P('dubai', 'Dubai', False, False)
    eu_central = P('eu-central', 'Central Europe', False, False)
    eu_west = P('eu-west', 'Western Europe', False, False)
    europe = P('europe', 'Europe', False, False)
    hongkong = P('hongkong', 'Hong Kong', False, False)
    india = P('india', 'India', False, False)
    japan = P('japan', 'Japan', False, False)
    russia = P('russia', 'Russia', False, False)
    singapore = P('singapore', 'Singapore', False, False)
    africa_south = P('southafrica', 'South Africa', False, False)
    sydney = P('sydney', 'Sydney', False, False)
    us_central = P('us-central', 'US Central', False, False)
    us_east = P('us-east', 'US East', False, False)
    us_south = P('us-south', 'US South', False, False)
    us_west = P('us-west', 'US West', False, False)
    # deprecated
    amsterdam = P('amsterdam', 'Amsterdam', True, False)
    frankfurt = P('frankfurt', 'Frankfurt', True, False)
    london = P('london', 'London', True, False)
    # vip
    vip_us_east = P('vip-us-west', 'VIP US West', False, True)
    vip_us_west = P('vip-us-east', 'VIP US East', False, True)
    # vip + deprecated
    vip_amsterdam = P('vip-amsterdam', 'VIP Amsterdam', True, True)


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
        The verification filer levels' values' type.
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
        Stores the predefined ``GuildFeature`` instances.
    VALUE_TYPE : `type` = `str`
        The guild features' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the guild features. Guild features have the same value as name, so at their case it is not
        applicable.
    
    Every predefined guild feature can be accessed as class attribute as well:
    
    +-------------------------------+-----------------------------------+-----------------------------------+
    | Class attribute names         | name                              | value                             |
    +===============================+===================================+===================================+
    | animated_icon                 | animated icon                     | ANIMATED_ICON                     |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | announcement_channels         | announcement channels             | NEWS                              |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | banner                        | banner                            | BANNER                            |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | commerce                      | commerce                          | COMMERCE                          |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | community                     | community                         | COMMUNITY                         |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | discoverable                  | discoverable                      | DISCOVERABLE                      |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | discoverable_disabled         | discoverable disabled             | DISCOVERABLE_DISABLED             |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | discoverable_enabled_before   | discoverable enabled before       | ENABLED_DISCOVERABLE_BEFORE       |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | featurable                    | featurable                        | FEATURABLE                        |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | hub                           | hub                               | HUB                               |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | invite_splash                 | invite splash                     | INVITE_SPLASH                     |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | member_list_disabled          | member list disabled              | MEMBER_LIST_DISABLED              |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | monetization_enabled          | monetization enabled              | MONETIZATION_ENABLED              |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | more_emoji                    | more emoji                        | MORE_EMOJI                        |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | more_sticker                  | more sticker                      | MORE_STICKERS                     |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | new_thread_permissions        | new thread permissions            | NEW_THREAD_PERMISSIONS            |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | partnered                     | partnered                         | PARTNERED                         |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | public                        | public                            | PUBLIC                            |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | preview_enabled               | preview enabled                   | PREVIEW_ENABLED                   |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | public_disabled               | public disabled                   | PUBLIC_DISABLED                   |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | private_threads               | private threads                   | PRIVATE_THREADS                   |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | relay_enabled                 | relay enabled                     | RELAY_ENABLED                     |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | role_icons                    | role icons                        | ROLE_ICONS                        |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | role_subscriptions_enabled    | role subscriptions enabled        | ROLE_SUBSCRIPTIONS_ENABLED        |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | thread_archive_seven_day      | thread archive seven day          | SEVEN_DAY_THREAD_ARCHIVE          |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | thread_archive_three_day      | thread archive three day          | THREE_DAY_THREAD_ARCHIVE          |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | threads_enabled               | threads enabled                   | THREADS_ENABLED                   |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | threads_enabled_testing       | threads enabled testing           | THREADS_ENABLED_TESTING           |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | ticket_events_enabled         | ticket events enabled             | TICKETED_EVENTS_ENABLED           |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | vanity_invite                 | vanity invite                     | VANITY_URL                        |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | verified                      | verified                          | VERIFIED                          |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | vip voice regions             | vip voice regions                 | VIP_REGIONS                       |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | welcome_screen_enabled        | welcome screen enabled            | WELCOME_SCREEN_ENABLED            |
    +-------------------------------+-----------------------------------+-----------------------------------+
    | verification_screen_enabled   | verification screen enabled       | MEMBER_VERIFICATION_GATE_ENABLED  |
    +-------------------------------+-----------------------------------+-----------------------------------+
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
    animated_icon = P('ANIMATED_ICON', 'animated icon')
    announcement_channels = P('NEWS', 'announcement channels')
    banner = P('BANNER', 'banner')
    commerce = P('COMMERCE', 'commerce')
    community = P('COMMUNITY', 'community')
    discoverable = P('DISCOVERABLE', 'discoverable')
    discoverable_disabled = P('DISCOVERABLE_DISABLED', 'discoverable disabled')
    discoverable_enabled_before = P('ENABLED_DISCOVERABLE_BEFORE', 'discoverable enabled before')
    featurable = P('FEATURABLE', 'featurable')
    hub = P('HUB', 'hub')
    invite_splash = P('INVITE_SPLASH', 'invite splash')
    member_list_disabled = P('MEMBER_LIST_DISABLED', 'member list disabled')
    monetization_enabled = P('MONETIZATION_ENABLED', 'monetization enabled')
    more_emoji = P('MORE_EMOJI', 'more emoji')
    more_sticker = P('MORE_STICKERS', 'more sticker')
    new_thread_permissions = P('NEW_THREAD_PERMISSIONS', 'new thread permissions')
    partnered = P('PARTNERED', 'partnered')
    preview_enabled = P('PREVIEW_ENABLED', 'preview enabled')
    private_threads = P('PRIVATE_THREADS', 'private threads')
    public = P('PUBLIC', 'public')
    public_disabled = P('PUBLIC_DISABLED', 'public disabled')
    relay_enabled = P('RELAY_ENABLED', 'relay enabled')
    role_icons = P('ROLE_ICONS', 'role icons')
    role_subscriptions_enabled = P('ROLE_SUBSCRIPTIONS_ENABLED', 'role subscriptions enabled')
    thread_archive_seven_day = P('SEVEN_DAY_THREAD_ARCHIVE', 'thread archive seven day')
    thread_archive_three_day = P('THREE_DAY_THREAD_ARCHIVE', 'thread archive three day')
    threads_enabled = P('THREADS_ENABLED', 'threads enabled')
    threads_enabled_testing = P('THREADS_ENABLED_TESTING', 'threads enabled testing')
    ticket_events_enabled = P('TICKETED_EVENTS_ENABLED', 'ticket events enabled')
    vanity_invite = P('VANITY_URL', 'vanity invite')
    verification_screen_enabled = P('MEMBER_VERIFICATION_GATE_ENABLED', 'verification screen enabled')
    verified = P('VERIFIED', 'verified')
    vip_voice_regions = P('VIP_REGIONS', 'vip_voice_regions')
    welcome_screen_enabled = P('WELCOME_SCREEN_ENABLED', 'welcome screen enabled')
    
    
    @class_property
    def vanity(cls):
        """
        ``.vanity`` is deprecated, please use ``.vanity_invite`` instead. Will be removed in 2021 September.
        """
        warnings.warn(
            f'`{cls.__name__}.vanity` is deprecated, and will be removed in 2021 September. '
            f'Please use `{cls.__name__}.vanity_invite` instead.',
            FutureWarning)
        
        return cls.vanity_invite
    
    
    @class_property
    def welcome_screen(cls):
        """
        ``.welcome_screen`` is deprecated, please use ``.welcome_screen_enabled`` instead. Will be removed in 2021
        November.
        """
        warnings.warn(
            f'`{cls.__name__}.welcome_screen` is deprecated, and will be removed in 2021 November. '
            f'Please use `{cls.__name__}.welcome_screen_enabled` instead.',
            FutureWarning)
        
        return cls.welcome_screen_enabled
    
    
    @class_property
    def verification_screen(cls):
        """
        ``.verification_screen`` is deprecated, please use ``.verification_screen_enabled`` instead. Will be removed in 2021
        November.
        """
        warnings.warn(
            f'`{cls.__name__}.verification_screen` is deprecated, and will be removed in 2021 November. '
            f'Please use `{cls.__name__}.verification_screen_enabled` instead.',
            FutureWarning)
        
        return cls.verification_screen_enabled
    
    
    @class_property
    def vip(cls):
        """
        ``.vip`` is deprecated, please use ``.vip_voice_regions`` instead. Will be removed in 2021
        November.
        """
        warnings.warn(
            f'`{cls.__name__}.vip` is deprecated, and will be removed in 2021 November. '
            f'Please use `{cls.__name__}.vip_voice_regions` instead.',
            FutureWarning)
        
        return cls.vip_voice_regions
    
    
    @class_property
    def news(cls):
        """
        ``.news`` is deprecated, please use ``.announcement_channels`` instead. Will be removed in 2021
        November.
        """
        warnings.warn(
            f'`{cls.__name__}.news` is deprecated, and will be removed in 2021 November. '
            f'Please use `{cls.__name__}.announcement_channels` instead.',
            FutureWarning)
        
        return cls.announcement_channels




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
        Stores the predefined ``NsfwLevel`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The nsfw level' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the nsfw levels.
    
    Every predefined nsfw level can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | explicit              | explicit          | 1     |
    +-----------------------+-------------------+-------+
    | safe                  | safe              | 2     |
    +-----------------------+-------------------+-------+
    | age_restricted        | age_restricted    | 3     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    explicit = P(1, 'explicit')
    safe = P(2, 'safe')
    age_restricted = P(2, 'age_restricted')


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



class VerificationScreenStepType(PreinstancedBase):
    """
    Represents a type of a ``VerificationScreenStep``.

    Attributes
    ----------
    value : `str`
        The Discord side identifier value of the verification step types.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VerificationScreenStepType``) items
        Stores the predefined ``VerificationScreenStepType`` instances.
    VALUE_TYPE : `type` = `str`
        The verification screen steps' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the verification screen step types.Verification screen step types have the
        same value as name, so at their case it is not applicable.
    
    Every predefined verification screen step type can be accessed as class attribute as well:
    
    +-----------------------+-------+
    | Class attribute names | Value |
    +=======================+=======+
    | rules                 | TERMS |
    +-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new verification screen type with the given value.
        
        Parameters
        ----------
        value : `str`
            The verification screen type's identifier value.
        
        Returns
        -------
        self : ``VerificationScreenStepType``
            The verification screen type.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value
        self.INSTANCES[value] = self
        return self
    
    def __repr__(self):
        """Returns the representation of the verification screen type."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    rules = P('TERMS', 'rules')
