__all__ = ('AuditLogEvent', 'ContentFilterLevel', 'GuildFeature', 'MFA', 'MessageNotificationLevel', 'NsfwLevel',
    'VerificationLevel', 'VerificationScreenStepType', 'VoiceRegion', )

from ...backend.export import export
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
    | INVITE_delete             | INVITE_delete             | 42    |
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
    invite_delete = P(42, 'INVITE_delete')
    
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
        voice_region : ``VoiceRegion``
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
    
    +-------------------------------+-----------------------------------+
    | Class attribute names         | Value                             |
    +===============================+===================================+
    | animated_icon                 | ANIMATED_ICON                     |
    +-------------------------------+-----------------------------------+
    | banner                        | BANNER                            |
    +-------------------------------+-----------------------------------+
    | commerce                      | COMMERCE                          |
    +-------------------------------+-----------------------------------+
    | community                     | COMMUNITY                         |
    +-------------------------------+-----------------------------------+
    | discoverable                  | DISCOVERABLE                      |
    +-------------------------------+-----------------------------------+
    | discoverable_disabled         | DISCOVERABLE_DISABLED             |
    +-------------------------------+-----------------------------------+
    | discoverable_enabled_before   | ENABLED_DISCOVERABLE_BEFORE       |
    +-------------------------------+-----------------------------------+
    | featurable                    | FEATURABLE                        |
    +-------------------------------+-----------------------------------+
    | member_list_disabled          | MEMBER_LIST_DISABLED              |
    +-------------------------------+-----------------------------------+
    | more_emoji                    | MORE_EMOJI                        |
    +-------------------------------+-----------------------------------+
    | news                          | NEWS                              |
    +-------------------------------+-----------------------------------+
    | partnered                     | PARTNERED                         |
    +-------------------------------+-----------------------------------+
    | public                        | PUBLIC                            |
    +-------------------------------+-----------------------------------+
    | public_disabled               | PUBLIC_DISABLED                   |
    +-------------------------------+-----------------------------------+
    | relay_enabled                 | RELAY_ENABLED                     |
    +-------------------------------+-----------------------------------+
    | invite_splash                 | INVITE_SPLASH                     |
    +-------------------------------+-----------------------------------+
    | vanity                        | VANITY_URL                        |
    +-------------------------------+-----------------------------------+
    | verified                      | VERIFIED                          |
    +-------------------------------+-----------------------------------+
    | vip                           | VIP_REGIONS                       |
    +-------------------------------+-----------------------------------+
    | welcome_screen                | WELCOME_SCREEN_ENABLED            |
    +-------------------------------+-----------------------------------+
    | verification_screen           | MEMBER_VERIFICATION_GATE_ENABLED  |
    +-------------------------------+-----------------------------------+
    | preview_enabled               | PREVIEW_ENABLED                   |
    +-------------------------------+-----------------------------------+
    | ticket_events_enabled         | TICKETED_EVENTS_ENABLED           |
    +-------------------------------+-----------------------------------+
    | monetization_enabled          | MONETIZATION_ENABLED              |
    +-------------------------------+-----------------------------------+
    | more_sticker                  | MORE_STICKERS                     |
    +-------------------------------+-----------------------------------+
    | thread_archive_3_day          | THREE_DAY_THREAD_ARCHIVE          |
    +-------------------------------+-----------------------------------+
    | thread_archive_7_day          | SEVEN_DAY_THREAD_ARCHIVE          |
    +-------------------------------+-----------------------------------+
    | private_threads               | PRIVATE_THREADS                   |
    +-------------------------------+-----------------------------------+
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
        self.name = value
        self.INSTANCES[value] = self
        return self
    
    
    # predefined
    animated_icon = P('ANIMATED_ICON', 'animated_icon')
    banner = P('BANNER', 'banner')
    commerce = P('COMMERCE', 'commerce')
    community = P('COMMUNITY', 'community')
    discoverable = P('DISCOVERABLE', 'discoverable')
    discoverable_disabled = P('DISCOVERABLE_DISABLED', 'discoverable_disabled')
    discoverable_enabled_before = P('ENABLED_DISCOVERABLE_BEFORE', 'discoverable_enabled_before')
    featurable = P('FEATURABLE', 'featurable')
    member_list_disabled = P('MEMBER_LIST_DISABLED', 'member_list_disabled')
    more_emoji = P('MORE_EMOJI', 'more_emoji')
    news = P('NEWS', 'news')
    partnered = P('PARTNERED', 'partnered')
    public = P('PUBLIC', 'public')
    public_disabled = P('PUBLIC_DISABLED', 'public_disabled')
    relay_enabled = P('RELAY_ENABLED', 'relay_enabled')
    invite_splash = P('INVITE_SPLASH', 'invite_splash')
    vanity = P('VANITY_URL', 'vanity')
    verified = P('VERIFIED', 'verified')
    vip = P('VIP_REGIONS', 'vip')
    welcome_screen = P('WELCOME_SCREEN_ENABLED', 'welcome_screen')
    verification_screen = P('MEMBER_VERIFICATION_GATE_ENABLED', 'verification_screen')
    preview_enabled = P('PREVIEW_ENABLED', 'preview_enabled')
    ticket_events_enabled = P('TICKETED_EVENTS_ENABLED', 'ticket_events_enabled')
    monetization_enabled = P('MONETIZATION_ENABLED', 'monetization_enabled')
    more_sticker = P('MORE_STICKERS', 'more_sticker')
    thread_archive_3_day = P('THREE_DAY_THREAD_ARCHIVE', 'thread_archive_3_day')
    thread_archive_7_day = P('SEVEN_DAY_THREAD_ARCHIVE', 'thread_archive_7_day')
    private_threads = P('PRIVATE_THREADS', 'private_threads')


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
