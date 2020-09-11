﻿# -*- coding: utf-8 -*-
__all__ = ('DiscoveryCategory', 'Guild', 'GuildDiscovery', 'GuildEmbed', 'GuildFeature', 'GuildPreview', 'GuildWidget',
    'GuildWidgetChannel', 'GuildWidgetUser', 'SystemChannelFlag', 'WelcomeChannel', 'WelcomeScreen', )

import re, reprlib

from ..env import CACHE_PRESENCE
from ..backend.dereaddons_local import cached_property, _spaceholder, DOCS_ENABLED
from ..backend.futures import Task

from .bases import DiscordEntity, ReverseFlagBase, IconSlot, ICON_TYPE_NONE
from .client_core import GUILDS, DISCOVERY_CATEGORIES, CHANNELS, KOKORO
from .others import EMOJI_NAME_RP, VoiceRegion, Status, VerificationLevel, MessageNotificationLevel, MFA, \
    ContentFilterLevel, DISCORD_EPOCH_START, DATETIME_FORMAT_CODE
from .user import User, PartialUser, VoiceState, UserBase, ZEROUSER
from .role import Role
from .channel import CHANNEL_TYPES, ChannelCategory, ChannelText
from .http import URLS
from .permission import Permission
from .activity import Activity, ActivityUnknown
from .emoji import Emoji, PartialEmoji
from .webhook import Webhook, WebhookRepr
from .oauth2 import parse_preferred_locale, DEFAULT_LOCALE
from .preconverters import preconvert_snowflake, preconvert_str

from . import ratelimit

VoiceClient = NotImplemented

LARGE_LIMIT = 250 #can be between 50 and 250

EMOJI_UPDATE_NEW    = 0
EMOJI_UPDATE_DELETE = 1
EMOJI_UPDATE_EDIT   = 2

class GuildFeature(object):
    """
    Represents the event type of an ``AuditLogEntry``.

    Attributes
    ----------
    value : `int`
        The Discord side identificator value of the guild feature.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``GuildFeature``) items
        Stores the predefined ``GuildFeature`` instances.
    
    Every predefined guild feature can be accessed as class attribute as well:
    
    +-------------------------------+-------------------------------+
    | Class attribute names         | Value                         |
    +===============================+===============================+
    | animated_icon                 | ANIMATED_ICON                 |
    +-------------------------------+-------------------------------+
    | banner                        | BANNER                        |
    +-------------------------------+-------------------------------+
    | commerce                      | COMMERCE                      |
    +-------------------------------+-------------------------------+
    | community                     | COMMUNITY                     |
    +-------------------------------+-------------------------------+
    | discoverable                  | DISCOVERABLE                  |
    +-------------------------------+-------------------------------+
    | enabled_discoverable_before   | ENABLED_DISCOVERABLE_BEFORE   |
    +-------------------------------+-------------------------------+
    | featurable                    | FEATURABLE                    |
    +-------------------------------+-------------------------------+
    | member_list_disabled          | MEMBER_LIST_DISABLED          |
    +-------------------------------+-------------------------------+
    | more_emoji                    | MORE_EMOJI                    |
    +-------------------------------+-------------------------------+
    | news                          | NEWS                          |
    +-------------------------------+-------------------------------+
    | partnered                     | PARTNERED                     |
    +-------------------------------+-------------------------------+
    | public                        | PUBLIC                        |
    +-------------------------------+-------------------------------+
    | public_disabled               | PUBLIC_DISABLED               |
    +-------------------------------+-------------------------------+
    | relay_enabled                 | RELAY_ENABLED                 |
    +-------------------------------+-------------------------------+
    | invite_splash                 | INVITE_SPLASH                 |
    +-------------------------------+-------------------------------+
    | vanity                        | VANITY_URL                    |
    +-------------------------------+-------------------------------+
    | verified                      | VERIFIED                      |
    +-------------------------------+-------------------------------+
    | vip                           | VIP_REGIONS                   |
    +-------------------------------+-------------------------------+
    | welcome_screen                | WELCOME_SCREEN_ENABLED        |
    +-------------------------------+-------------------------------+
    """
    # class related
    INSTANCES = {}
    
    @classmethod
    def get(cls, value):
        """
        Accessed to get a guild feature from `.INSTANCES` by it's `value`. If no predefined guild feature is found,
        creates a new one.
        
        Parameters
        ----------
        value : `str`
            The identificator value of the guild feature.
        
        Returns
        -------
        guild_feature : ``GuildFeature``
        """
        try:
            guild_feature = cls.INSTANCES[value]
        except KeyError:
            guild_feature = cls(value)
        
        return guild_feature
    
    # object related
    __slots__ = ('value',)
    
    def __init__(self, value):
        """
        Creates a new guild feature and stores it at `.INSTANCES`.
        
        Parameters
        ----------
        value : `str`
            The identificator value of the guild feature.
        """
        self.value = value
        self.INSTANCES[value] = self
    
    def __str__(self):
        """Returns the guild feature's value."""
        return self.value
    
    name = property(__str__)
    if DOCS_ENABLED:
        name.__doc__ = (
        """
        Returns the guild feature's value.
        
        Returns
        -------
        name : `str`
        """)
    
    def __repr__(self):
        """Returns the representation of the guild feature."""
        return f'{self.__class__.__name__}(value={self.value!r})'
    
    def __gt__(self, other):
        """Whether this feature's value is greater than the other's."""
        if type(self) is type(other):
            return self.value > other.value
        if isinstance(other, str):
            return self.value > other
        return NotImplemented
    
    def __ge__(self, other):
        """Whether this feature's value is greater or equal than the other's."""
        if type(self) is type(other):
            return self.value >= other.value
        if isinstance(other, str):
            return self.value >= other
        return NotImplemented
    
    def __eq__(self, other):
        """Whether this feature's value is equal to the other's."""
        if type(self) is type(other):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return NotImplemented
    
    def __ne__(self, other):
        """Whether this feature's value is not equal to the other's."""
        if type(self) is type(other):
            return self.value != other.value
        if isinstance(other, str):
            return self.value != other
        return NotImplemented
    
    def __le__(self, other):
        """Whether this feature's value is lower or equal than the other's."""
        if type(self) is type(other):
            return self.value <= other.value
        if isinstance(other, str):
            return self.value <= other
        return NotImplemented
    
    def __lt__(self, other):
        """Whether this feature's value is lower than the other's."""
        if type(self) is type(other):
            return self.value < other.value
        if isinstance(other, str):
            return self.value < other
        return  NotImplemented
    
    def __hash__(self):
        return hash(self.value)
    
    # predefined
    animated_icon               = NotImplemented
    banner                      = NotImplemented
    commerce                    = NotImplemented
    discoverable                = NotImplemented
    enabled_discoverable_before = NotImplemented
    featurable                  = NotImplemented
    member_list_disabled        = NotImplemented
    more_emoji                  = NotImplemented
    news                        = NotImplemented
    partnered                   = NotImplemented
    public                      = NotImplemented
    public_disabled             = NotImplemented
    relay_enabled               = NotImplemented
    invite_splash               = NotImplemented
    vanity                      = NotImplemented
    verified                    = NotImplemented
    vip                         = NotImplemented
    welcome_screen              = NotImplemented


GuildFeature.animated_icon              = GuildFeature('ANIMATED_ICON')
GuildFeature.banner                     = GuildFeature('BANNER')
GuildFeature.commerce                   = GuildFeature('COMMERCE')
GuildFeature.community                  = GuildFeature('COMMUNITY')
GuildFeature.discoverable               = GuildFeature('DISCOVERABLE')
GuildFeature.enabled_discoverable_before= GuildFeature('ENABLED_DISCOVERABLE_BEFORE')
GuildFeature.featurable                 = GuildFeature('FEATURABLE')
GuildFeature.member_list_disabled       = GuildFeature('MEMBER_LIST_DISABLED')
GuildFeature.more_emoji                 = GuildFeature('MORE_EMOJI')
GuildFeature.news                       = GuildFeature('NEWS')
GuildFeature.partnered                  = GuildFeature('PARTNERED')
GuildFeature.public                     = GuildFeature('PUBLIC')
GuildFeature.public_disabled            = GuildFeature('PUBLIC_DISABLED')
GuildFeature.relay_enabled              = GuildFeature('RELAY_ENABLED')
GuildFeature.invite_splash              = GuildFeature('INVITE_SPLASH')
GuildFeature.vanity                     = GuildFeature('VANITY_URL')
GuildFeature.verified                   = GuildFeature('VERIFIED')
GuildFeature.vip                        = GuildFeature('VIP_REGIONS')
GuildFeature.welcome_screen             = GuildFeature('WELCOME_SCREEN_ENABLED')

COMMUNITY_FEATURES = {GuildFeature.community, GuildFeature.discoverable, GuildFeature.public}

class SystemChannelFlag(ReverseFlagBase):
    """
    The flags of a ``Guild``'s system channel.
    
    For Discord these flags tell, what ``MessageType`-s are not sent to the guild's system channel, but the wrapper
    reverses this behaviour.
    
    There are also predefined ``SystemChannelFlag``-s:
    
    +-----------------------+-----------------------+
    | Class attribute name  | value                 |
    +=======================+=======================+
    | NONE                  | ActivityFlag(0b11)    |
    +-----------------------+-----------------------+
    | ALL                   | ActivityFlag(0b00)    |
    +-----------------------+-----------------------+
    """
    __keys__ = {
        'welcome': 0,
        'boost'  : 1,
            }
    
    @property
    def none(self):
        """
        Whether the flag not allows any system messages at the respective system channel.
        
        Returns
        -------
        none : `bool`
        """
        return (self == self.NONE)
    
    @property
    def all(self):
        """
        Whether the flag allows all the system messages at the respective system channel.
        
        Returns
        -------
        none : `bool`
        """
        return (self == self.ALL)
    
    NONE = NotImplemented
    ALL  = NotImplemented

SystemChannelFlag.NONE = SystemChannelFlag(0b11)
SystemChannelFlag.ALL  = SystemChannelFlag(0b00)

class GuildEmbed(object):
    """
    Represents a guild's embed.
    
    Attributes
    ----------
    channel : ``Channeltext``
        The respective guild's embed channel.
    enabled : `bool`
        Whether respective guild's embed is enabled.
    guild : ``Guild``
        The guild of the guild embed.
    """
    __slots__ = ('channel', 'enabled', 'guild',)
    def __init__(self, data, guild):
        """
        Creates a new guild embed.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild embed data received from Discord.
        guild : ``Guild``
            The guild of the guild embed.
        """
        self.guild = guild
        self.enabled = guild.embed_enabled = data['enabled']
        channel_id = data['channel_id']
        if (channel_id is not None):
            channel = guild.channels.get(int(channel_id))
        else:
            channel = None
        self.channel = guild.embed_channel=channel
    
    @classmethod
    def from_guild(cls, guild):
        """
        Creates a guild embed directly from a ``Guild``.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild to create the guild embed from.
        
        Returns
        -------
        guild_embed : ``GuildEmbed``
        """
        self = object.__new__(cls)
        self.enabled = guild.embed_enabled
        self.channel = guild.embed_channel
        self.guild = guild
        return self

    def __repr__(self):
        """Returns the representation of the guild embed."""
        return f'<{self.__class__.__name__} of guild {self.guild!r}>'

class GuildWidgetUser(DiscordEntity):
    """
    Represents an user object sent with a ``GuildWidget``'s data.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the guild widget user. Can be between `0` and `99`.
    activity_name : `None` or `str`
        The guild widget user's activity's name if applicable.
    avatar_url : `str` or `None`
        The guild widget user's avatar url if applicable.
    discriminator : `int`
        The guild widget user's discriminator.
    name : `str`
        The guild widget user's name.
    status : ``Status``
        The guild widget user's status.
    """
    __slots__ = ('activity_name', 'avatar_url', 'discriminator', 'name', 'status')
    
    def __init__(self, data):
        """
        Creates a new guild widget user from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild widget user data received with ``GuildWidget``'s.
        """
        self.name = data['username']
        self.id = int(data['id'])
        self.discriminator = int(data['discriminator'])
        self.avatar_url = data['avatar_url']
        self.status = Status.INSTANCES[data['status']]
        try:
            activity_data = data['game']
        except KeyError:
            activity_name = None
        else:
            activity_name = activity_data['name']
        
        self.activity_name = activity_name
    
    @property
    def full_name(self):
        """
        The user's name with it's discriminator.
        
        Returns
        -------
        full_name : `str`
        """
        return f'{self.name}#{self.discriminator:0>4}'
    
    @property
    def mention(self):
        """
        The mention of the user.
        
        Returns
        -------
        mention : `str`
        """
        return f'<@{self.id}>'
    
    @property
    def mention_nick(self):
        """
        The mention to the user's nick.
        
        Returns
        -------
        mention : `str`
        
        Notes
        -----
        It actually has nothing to do with the user's nickname > <.
        """
        return f'<@!{self.id}>'
    
    def __str__(self):
        """Returns the name of the guild widget user."""
        return self.name
    
    def __repr__(self):
        """Returns the representation of the guild widget user."""
        return f'<{self.__class__.__name__} name={self.full_name!r} ({self.id})>'

class GuildWidgetChannel(DiscordEntity):
    """
    Represents a ``GuildWidget``'s channel.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the guild widget channel.
    name : `str`
        The channel's name.
    position : `int`
        The channel's position.
    """
    __slots__  = ('name', 'position')
    
    def __init__(self, data):
        """
        Creates a new guild widget channel from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild widget channel data received with ``GuildWidget``'s.
        """
        self.id = int(data['id'])
        self.name = data['name']
        self.position = data['name']
    
    @property
    def mention(self):
        """
        The channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
    
    def __str__(self):
        """Returns the guild widget channel's name."""
        return self.name
    
    def __repr__(self):
        """Returns the guild widget channel's representation."""
        return f'<{self.__class__.__name__} name={self.name} ({self.id})>'
    
    def __gt__(self, other):
        """
        Whether this guild widget channel has greater (visible) position than the other at their respective guild.
        """
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id > other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __ge__(self, other):
        """
        Whether this guild widget channel has greater or equal (visible) position than the other at their respective
        guild.
        """
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id >= other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __le__(self, other):
        """
        Whether this guild widget channel has lower or equal (visible) position than the other at their respective
        guild.
        """
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id <= other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __lt__(self, other):
        """
        Whether this guild widget channel has lower (visible) position than the other at their respective guild.
        """
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id < other.id:
                    return True
            
            return False
        
        return NotImplemented

class GuildWidget(DiscordEntity):
    """
    Represents a ``Guild``'s widget.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`) items
        Internal cache used by cached properties.
    _data : `dict` of (`str`, `Any`) items
        The data sent by Discord and used by the cached properties of the guild widget instances.
    guild : ``Guild``
        The owner guild of the widget.
    """
    __slots__ = ('_cache', '_data', 'guild',)
    
    def __init__(self, data):
        """
        Creates a new guild widget.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The requested guild widget data.
        """
        self.guild = Guild.precreate(int(data['id']), name=data['name'])
        self._data = data
        self._cache = {}
    
    json_url = property(URLS.guild_widget_json_url)
    
    @property
    def id(self):
        """
        The unique identificator number of the guild widget's guild.
        
        Returns
        -------
        id : `int`
        """
        return self.guild.id
    
    @property
    def name(self):
        """
        The name of the guild widget's guild.
        
        Returns
        -------
        name : `str`
        """
        return self.guild.name
    
    @property
    def invite_url(self):
        """
        The guild widget's invite url if applicable.
        
        Returns
        -------
        invite_url : `str` or `None`
        """
        return self._data.get('instant_invite')
    
    @property
    def online_count(self):
        """
        Estimated online count of the respective guild.
        
        Returns
        -------
        online_count : `int`
        """
        return self._data['presence_count']
    
    @cached_property
    def users(self):
        """
        Online users received with the guild widget.
        
        Returns
        -------
        users : `list` of ``GuildWidgetUser``
        """
        return [GuildWidgetUser(GWU_data) for GWU_data in self._data['members']]

    @cached_property
    def channels(self):
        """
        Voice channels received with the guild widget.
        
        Returns
        -------
        users : `list` of ``GuildWidgetChannel``
        """
        return [GuildWidgetChannel(GWC_data) for GWC_data in self._data['channels']]
    
    def __repr__(self):
        """Returns the representation of the guild widget."""
        return f'<{self.__class__.__name__} of guild {self.guild.name}>'

#we need to ignore client adding, because clients count to being not
#partial. If a guild is not partial it wont get update on Guild.__new__
def PartialGuild(data):
    """
    Creates a partial guild from partial guild data.
    
    Parameters
    ----------
    data : `None` or `dict` of (`str`, `Any`) items
        Partial channel data received from Discord.
    
    Returns
    -------
    channel : `None` or ``Guild`` instance
        The created partial guild, or `None`, if no data was received.
    """
    if (data is None) or (not data):
        return None
    guild_id = int(data['id'])
    try:
        return GUILDS[guild_id]
    except KeyError:
        pass
    
    guild = object.__new__(Guild)
    GUILDS[guild_id] = guild
    guild.id = guild_id
    
    # do not use pop, at later versions the received data might be read-only.
    try:
        available = not data['unavailable']
    except KeyError:
        available = True
        restricted_data_limit = 2
    else:
        restricted_data_limit = 3
    
    guild.available = available
    
    # set default values
    guild._boosters = None
    guild._cache_perm = None
    guild.afk_channel = None
    guild.afk_timeout = 0
    guild.channels = {}
    guild.roles = {}
    #available set up
    guild.banner_type = ICON_TYPE_NONE
    guild.banner_hash = 0
    guild.booster_count = -1
    guild.clients = []
    guild.content_filter = ContentFilterLevel.disabled
    # description will be set down
    guild.embed_channel = None
    guild.embed_enabled = False
    guild.emojis = {}
    guild.features = []
    # icon_type will be set down
    # icon_hash will be set down
    # id is set up
    guild.is_large = False
    guild.max_presences = 25000
    guild.max_users = 250000
    guild.max_video_channel_users = 25
    guild.message_notification = MessageNotificationLevel.only_mentions
    guild.mfa = MFA.none
    # name will be set down
    guild.owner = ZEROUSER
    guild.preferred_locale = DEFAULT_LOCALE
    guild.premium_tier = 0
    guild.public_updates_channel = None
    guild.region = VoiceRegion.eu_central
    guild.rules_channel = None
    # invite_splash_type will be set down
    # invite_splash_hash will be set down
    guild.system_channel = None
    guild.system_channel_flags = SystemChannelFlag.NONE
    guild.user_count = 1
    guild.users = {}
    guild.vanity_code = None
    guild.verification_level = VerificationLevel.none
    guild.voice_states = {}
    guild.webhooks = {}
    guild.webhooks_uptodate = False
    guild.widget_channel = None
    guild.widget_enabled = False
    
    if len(data) < restricted_data_limit:
        guild.name = ''
        guild.icon_type = ICON_TYPE_NONE
        guild.icon_hash = 0
        guild.invite_splash_type = ICON_TYPE_NONE
        guild.invite_splash_hash = 0
        guild.discovery_splash_type = ICON_TYPE_NONE
        guild.discovery_splash_hash = 0
        guild.description = None
    else:
        guild.name = data.get('name','')
        guild._set_icon(data)
        guild._set_invite_splash(data)
        guild._set_discovery_splash(data)
        guild.description=data.get('description',None)
        
        try:
            verification_level = data['verification_level']
        except KeyError:
            pass
        else:
            guild.verification_level = VerificationLevel.INSTANCES[verification_level]
        
        try:
            features = data['features']
        except KeyError:
            guild.features.clear()
        else:
            features = [GuildFeature.get(feature) for feature in features]
            features.sort()
            guild.features = features
    
    return guild

#discord does not sends `embed_channel`, `embed_enabled`, `widget_channel`,
#`widget_enabled`, `max_presences`, `max_users` correctly and thats sad.
class Guild(DiscordEntity, immortal=True):
    """
    Represents a Discord guild (or server).
    
    Attributes
    ----------
    _boosters : `None` or `list` of (``User`` or ``Client``) objects
        Cached slot for the boosters of the guild.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    afk_channel : `None` or ``ChannelVoice``
        The afk channel of the guild if it has.
    afk_timeout : `int`
        The afk timeout at the `afk_channel`. Can be `60`, `300`, `900`, `1800`, `3600` in seconds.
    available : `bool`
        Whether the guild is available.
    banner_hash : `int`
        The guild's banner's hash in `uint128`.
    banner_type : ``IconType``
        The guild's banner's type.
    booster_count : `int`
        The total number of boosts of the guild.
    channels : `dict` of (`int`, ``ChannelGuildBase`` instance) items
        The channels of the guild stored in `channel_id` - `channel` relation.
    clients : `list` of ``Client``
        The loaded clients, who are the member of the guild. If no clients are member of a guild, it is partial.
    content_filter : ``ContentFilterLevel``
        The explicit content filter level of the guild.
    description : `str` or `None`
        Description of the guild. The guild must be a Community guild.
    discovery_splash_hash : `int`
        The guild's discovery splashe's hash in `uint128`. The guild must be a discoverable.
    discovery_splash_type : ``IconType``
        The guild's discovery splashe's type.
    embed_channel : `None` or ``ChannelText``
        The channel to where the guild's embed widget will generate the invite to.
    embed_enabled : `bool`
        If the guild embeddable. Linked to ``.embed_channel``.
    emojis : `dict` of (`int`, ``Emoji``) items
        The emojis of the guild stored in `emoji_id` - `emoji` relation.
    features : `list` of ``GuildFeature``
        The guild's features.
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    icon_type : ``IconType``
        The guild's icon's type.
    invite_splash_hash : `int`
        The guild's invite splashe's hash in `uint128`. The guild must have `INVITE_SPLASH` feature.
    invite_splash_type : ``IconType``
        The guild's invite splashe's type.
    is_large : `bool`
        Whether the guild is considered as a large one.
    max_presences : `int`
        The maximal amount of presences for the guild.
    max_users : `int`
        The maximal amount of users for the guild.
    max_video_channel_users : `int`
        The maximal amaunt of users in a video channel(?).
    message_notification : ``MessageNotificationLevel``
        The message notification level of the guild.
    mfa : ``MFA``
        The required Multi-factor authentication level for the guild.
    name : `str`
        The name of the guild.
    owner : ``User`` or ``Client``
        The owner of the guild. At some cases it can be set as `ZEROUSER` as well.
    preferred_locale : `str`
        The preferred language of the guild. The guild must be a Community guild, defaults to `'en-US'`.
    premium_tier : `int`
        The premium tier of the guild. More subs = higher tier.
    public_updates_channel : `None` or ``ChannelText``
        The channel where the guild's public upddates should go. The guild must be a Community guild.
    region : ``VoiceRegion``
        The voice region of the guild.
    roles : `dict` of (`int`, ``Role``) items
        The roles of the guild stored in `role_id` - `role` relation.
    rules_channel : `None` or ``ChannelText``
        The channel where the rules of a public guild's should be. The guild must be a Community guild.
    system_channel : `None` or ``ChannelText``
        The channel where the system messages are sent.
    system_channel_flags : ``SystemChannelFlag``
        Describe which type of messages are sent automatically to the system channel.
    user_count : `int`
        The amount of users at the guild.
    users : `dict` of (`int`, (``User`` or ``Client``)) items
        The users at the guild stored within `user_id` - `user` relation.
    vanity_code : `None` or `str`
        The guild's vanity invite's code if it has.
    verification_level : ``VerificationLevel``
        The minimal verification needed to join to guild.
    voice_states : `dict` of (`int`, ``VoiceState``) items
        Each user at a voice channel is represented by a ``VoiceState`` object. voice state are stored in
        `respecitve user's id` - `voice state` relation.
    webhooks : `dict` of (`int`, ``Webhook``) items
        The guild's webhooks if requested in `webhook_id` - `webhook` relation. This container is updated when a new
        request is done.
    webhooks_uptodate : `bool`
        Whether the guild's `.webhooks` containr is up-to-date. If it is, then instead of requesting new webhooks, that
        container is accessed.
    widget_channel : `None` or ``ChannelText``
        The channel for the guild's widget.
    widget_enabled : `bool`
        Whether the guild's widget is enabled. Linked to ``.widget_channel``.
    
    Notes
    -----
    When a guild is loaded first time, some of it's attrbiutes might not reflect their real value. These are the
    following:
    - ``.embed_channel``
    - ``.embed_enabled``
    - ``.max_presences``
    - ``.max_users``
    - ``.widget_channel``
    - ``.widget_enabled``
    """
    __slots__ = ('_boosters', '_cache_perm', 'afk_channel', 'afk_timeout', 'available', 'booster_count', 'channels',
        'clients', 'content_filter', 'description', 'embed_channel', 'embed_enabled', 'emojis', 'features',
        'has_animated_icon', 'is_large', 'max_presences', 'max_users', 'max_video_channel_users',
        'message_notification', 'mfa', 'name', 'owner', 'preferred_locale', 'premium_tier', 'public_updates_channel',
        'region', 'roles', 'roles', 'rules_channel', 'system_channel', 'system_channel_flags', 'user_count', 'users',
        'vanity_code', 'verification_level', 'voice_states', 'webhooks', 'webhooks_uptodate', 'widget_channel',
        'widget_enabled')
    
    banner = IconSlot('banner', 'banner', URLS.guild_banner_url, URLS.guild_banner_url_as)
    icon = IconSlot('icon', 'icon', URLS.guild_icon_url, URLS.guild_icon_url_as)
    invite_splash = IconSlot('invite_splash', 'splash', URLS.guild_invite_splash_url, URLS.guild_invite_splash_url_as)
    discovery_splash = IconSlot('discovery_splash', 'discovery_splash', URLS.guild_discovery_splash_url, URLS.guild_discovery_splash_url_as)
    
    def __new__(cls, data, client):
        """
        Tries to find the guild from the already existing ones. If it can not find, creates a new one. If the found
        guild is partial (or freshly created), sets it's attributes from the given `data`. If the the guild is not
        added to the client's guild profiles yet, adds it, and the client to the guilds's `.clients` as well.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild data.
        client : ``Client``
            The client who received the guild's data.
        
        Returns
        -------
        guild : ``Guild``
        """
        guild_id = int(data['id'])
        
        try:
            guild = GUILDS[guild_id]
            update = (not guild.clients)
        except KeyError:
            guild = object.__new__(cls)
            GUILDS[guild_id] = guild
            guild.id = guild_id
            
            guild.clients = []
            guild.users = {}
            guild.emojis = {}
            guild.voice_states = {}
            guild.roles = {}
            guild.channels = {}
            guild.features = []
            guild.webhooks = {}
            guild.webhooks_uptodate = False
            guild._cache_perm = None
            guild._boosters = None
            
            update = True
        
        guild.available = (not data.get('unavailable',False))
        
        if update:
            guild.user_count = data.get('member_count',1)
            guild.booster_count = -1
            
            try:
                guild.is_large = data['large']
            except KeyError:
                guild.is_large = (guild.user_count>=LARGE_LIMIT)
            
            try:
                role_datas = data['roles']
            except KeyError:
                pass
            else:
                for role_data in role_datas:
                    Role(role_data, guild)
            
            try:
                emoji_datas = data['emojis']
            except KeyError:
                pass
            else:
                emojis = guild.emojis
                for emoji_data in emoji_datas:
                    emoji = Emoji(emoji_data,guild)
                    emojis[emoji.id] = emoji
            
            try:
                channel_datas = data['channels']
            except KeyError:
                pass
            else:
                later = []
                for channel_data in channel_datas:
                    channel_type = CHANNEL_TYPES[channel_data['type']]
                    if channel_type is ChannelCategory:
                        channel_type(channel_data, client, guild)
                    else:
                        later.append((channel_type, channel_data),)
                for channel_type,channel_data in later:
                    channel_type(channel_data, client, guild)
            
            guild._update_no_return(data)
            
            if CACHE_PRESENCE:
                try:
                    user_datas = data['members']
                except KeyError:
                    pass
                else:
                    for user_data in user_datas:
                        User(user_data, guild)
                #if user caching is disabled, then presence caching is too.
                try:
                    presence_data = data['presences']
                except KeyError:
                    pass
                else:
                    guild._apply_presences(presence_data)
            
            try:
                voice_state_datas = data['voice_states']
            except KeyError:
                pass
            else:
                for voice_state_data in voice_state_datas:
                    user = PartialUser(int(voice_state_data['user_id']))
                    if user.id in guild.voice_states:
                        continue
                    
                    channel_id = voice_state_data.get('channel_id', None)
                    if channel_id is None:
                        continue
                    channel = guild.channels[int(channel_id)]
                    
                    guild.voice_states[user.id] = VoiceState(voice_state_data, channel)
        
        if (not CACHE_PRESENCE):
            #we get information about the client here
            try:
                user_datas = data['members']
            except KeyError:
                pass
            else:
                for user_data in user_datas:
                    User._bypass_no_cache(user_data, guild)
        
        if client not in guild.clients:
            try:
                ghost_state = guild.voice_states[client.id]
            except KeyError:
                pass
            else:
                Task(VoiceClient._kill_ghost(client, ghost_state.channel), KOKORO)
            guild.clients.append(client)
        
        return guild
    
    @classmethod
    def precreate(cls, guild_id, **kwargs):
        """
        Precreates the guild with the given parameters. Precreated guilds ar picked up when a guild's data is rceived
        with the same id.
        
        First tries to find whether a guild exists with the given id. If it does and it is partial, updates it with the
        given parameters, else it creates a new one.
        
        Parameters
        ----------
        guild_id : `snowflake`
            The guild's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the guild.
        
        Other Parameters
        ----------------
        name : `str`
            The guild's ``.name``.
        banner : `int`
            The guild's ``.banner``.
        invite_splash : `int`
            The guild's ``.invite_splash``.
        discovery_splash : `int`
            The guild's ``.discovery_splash``.
        icon : `int`
            The guild's ``.icon``.
        has_animated_icon : `bool`
            Whether the guild's icon is animated.
        
        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        guild_id = preconvert_snowflake(guild_id, 'guild_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name', name))
            
            cls.icon.preconvert(kwargs, processable)
            cls.banner.preconvert(kwargs, processable)
            cls.invite_splash.preconvert(kwargs, processable)
            cls.discovery_splash.preconvert(kwargs, processable)
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            guild = object.__new__(cls)
            guild._boosters = None
            guild._cache_perm = None
            guild.afk_channel = None
            guild.afk_timeout = 0
            guild.channels = {}
            guild.roles = {}
            guild.available = False
            guild.banner_hash = 0
            guild.banner_type = ICON_TYPE_NONE
            guild.booster_count = -1
            guild.clients = []
            guild.content_filter = ContentFilterLevel.disabled
            guild.description = None
            guild.discovery_splash_hash = 0
            guild.discovery_splash_type = ICON_TYPE_NONE
            guild.embed_channel = None
            guild.embed_enabled = False
            guild.emojis = {}
            guild.features = []
            guild.has_animated_icon = False
            guild.icon_hash = 0
            guild.icon_type = ICON_TYPE_NONE
            guild.id = guild_id
            guild.is_large = False
            guild.max_presences = 25000
            guild.max_users = 250000
            guild.max_video_channel_users = 25
            guild.message_notification = MessageNotificationLevel.only_mentions
            guild.mfa = MFA.none
            guild.name = ''
            guild.owner = ZEROUSER
            guild.preferred_locale = DEFAULT_LOCALE
            guild.premium_tier = 0
            guild.public_updates_channel = None
            guild.region = VoiceRegion.eu_central
            guild.rules_channel = None
            guild.invite_splash_hash = 0
            guild.invite_splash_type = ICON_TYPE_NONE
            guild.system_channel = None
            guild.system_channel_flags = SystemChannelFlag.NONE
            guild.user_count = 1
            guild.users = {}
            guild.vanity_code = None
            guild.verification_level = VerificationLevel.none
            guild.voice_states = {}
            guild.webhooks = {}
            guild.webhooks_uptodate = False
            guild.widget_channel = None
            guild.widget_enabled = False
            GUILDS[guild_id] = guild
        else:
            if guild.clients:
                return guild
        
        if (processable is not None):
            for item in processable:
                setattr(guild, *item)
        
        return guild
    
    def __str__(self):
        """Returns the guild's name."""
        return self.name
    
    def __repr__(self):
        """Returns the guild's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}{"" if self.clients else " (partial)"}>'
    
    def __format__(self, code):
        """
        Formats the guild in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        channel : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```
        >>> from hata import Guild, now_as_id
        >>> guild = Guild.precreate(now_as_id(), name='GrassGrass')
        >>> guild
        <Guild name='GrassGrass', id=713718885970345984 (partial)>
        >>> # no code stands for str(guild).
        >>> f'{guild}'
        'GrassGrass'
        >>> # 'c' stands for created at.
        >>> f'{guild:c}'
        '2020.05.23-11:44:02'
        ```
        """
        if not code:
            return self.name
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    embed_url = URLS.guild_embed_url
    widget_url = URLS.guild_widget_url
    
    def _update_embed(self, data):
        """
        On requesting a guild's embed it's respective attributes get updated.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild embed's data received from Discord.
        """
        self.embed_enabled = data.get('enabled', False)
        
        channel_id = data.get('id')
        if channel_id is None:
            embed_channel = None
        else:
            embed_channel = self.channels[int(channel_id)]
        self.embed_channel = embed_channel
    
    @property
    def embed(self):
        """
        Returns the guild's embed based on the guild's current embed information.
        
        Returns
        -------
        guild_embed : ``GuildEmbed``
        """
        return GuildEmbed.from_guild(self)

    def _delete(self, client):
        """
        When a client leaves (gets kicked or banned) from a guild, this method is called. If the guild loses it's last
        active client, then the it's references are cleared.
        
        Parameters
        ----------
        client : ``Client``
            The client, who left the guild.
        """
        clients = self.clients
        
        try:
            clients.remove(client)
        except ValueError:
            pass
        
        if clients:
            return
        
        for category in self.channel_list:
            if type(category) is ChannelCategory:
                for channel in category.channel_list:
                    channel._delete()
            category._delete()
        
        for emoji in list(self.emojis.values()):
            emoji._delete()
        
        self.voice_states.clear()
        
        users = self.users
        for user in users.values():
            if type(user) is User:
                del user.guild_profiles[self]
        
        users.clear()
        
        for role in self.role_list:
            role._delete()
        
        self.webhooks.clear()
        self.webhooks_uptodate = False
        self._boosters = None
    
    def _update_voice_state(self, data, user):
        """
        Called by dispatch event. Updates the voice state of the `user` with the given `data`.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Data received from Discord.
        user : ``User`` or ``Client``
            The user, who's voice state is updated.
        
        Returns
        -------
        changes : `None` or `tuple` (``VoiceState``, `str`, (`None` or `dict` of (`str`, `Any`) items))
            If the user's ``VoiceState`` is already deleteted or updated the method returns `None`. If it is not, then
            returns 3 objects, which describe what changed:
            
            +-------+-------------------+-------------------------------------------+
            | Index | Respective name   | Type                                      |
            +=======+===================+===========================================+
            | 0     | voice_state       | ``VoiceState``                            |
            +-------+-------------------+-------------------------------------------+
            | 1     | action            | `str`                                     |
            +-------+-------------------+-------------------------------------------+
            | 2     | old_attributes    | `None` or `dict` of (`str`, `Any`) items  |
            +-------+-------------------+-------------------------------------------+
            
            Action values can be the following:
            +-------------------+-------+
            | Respective name   | Value |
            +===================+=======+
            | leave             | `'l'` |
            +-------------------+-------+
            | join              | `'j'` |
            +-------------------+-------+
            | update            | `'u'` |
            +-------------------+-------+
            
            If action value is update (`'u'`), then `old_attributes` is returned as a `dict` conatining the changed
            attributes in `attribute-name` - `old-value` relation. All item at the returned dictionary is optional.
            +---------------+-------------------+
            | Keys          | Values            |
            +===============+===================+
            | channel       | ``ChannelVoice``  |
            +---------------+-------------------+
            | deaf          | `str`             |
            +---------------+-------------------+
            | mute          | `bool`            |
            +---------------+-------------------+
            | self_deaf     | `bool`            |
            +---------------+-------------------+
            | self_mute     | `bool`            |
            +---------------+-------------------+
            | self_stream   | `bool`            |
            +---------------+-------------------+
            | self_video    | `bool`            |
            +---------------+-------------------+
        """
        while True:
            channel_id = data.get('channel_id')
            if channel_id is None:
                try:
                    state = self.voice_states.pop(user.id)
                except KeyError:
                    return
                
                old_attributes = None
                action = 'l'
                break
            
            channel = self.channels[int(channel_id)]
            
            try:
                state = self.voice_states[user.id]
            except KeyError:
                state = self.voice_states[user.id] = VoiceState(data, channel)
                old_attributes = None
                action = 'j'
                break
            
            old_attributes = state._update(data,channel)
            if old_attributes:
                action = 'u'
                break
            
            old_attributes = None
            return
        
        return state, action, old_attributes
    
    def _update_voice_state_restricted(self, data, user):
        """
        Familiar to ``._update_voice_state``, but does not calculate changes and just returns a representation of the
        action.
        
        Returns `None` if nothing happened, `_spaceholder` at the case of leave, or at the case of join or update the
        channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Data received from Discord.
        user : ``User`` or ``Client``
            The user, who's voice state is updated.
        
        Returns
        -------
        changes : `None`, `_spaceholder`, ``ChannelVoice``
        """
        channel_id = data.get('channel_id')
        if channel_id is None:
            try:
                state = self.voice_states.pop(user.id)
            except KeyError:
                return
            return _spaceholder
        
        channel = self.channels[int(channel_id)]
        
        try:
            state = self.voice_states[user.id]
        except KeyError:
            self.voice_states[user.id] = VoiceState(data,channel)
            return channel
        
        state._update_no_return(data,channel)
        return channel
    
    @property
    def text_channels(self):
        """
        Returns the text channels of the guild. Announcement channels are not included.
        
        Returns
        -------
        channels : `list` of ``ChannelText``
        """
        return [channel for channel in self.channels.values() if channel.type==0]

    @property
    def voice_channels(self):
        """
        Returns the voice channels of the guild.
        
        Returns
        -------
        channels : `list` of ``ChannelVoice``
        """
        return [channel for channel in self.channels.values() if channel.type==2]

    @property
    def category_channels(self):
        """
        Returns the category channels of the guild.
        
        Returns
        -------
        channels : `list` of ``ChannelCategory``
        """
        return [channel for channel in self.channels.values() if channel.type==4]

    @property
    def announcement_channels(self):
        """
        Returns the announcemet channels of the guild.
        
        Returns
        -------
        channels : `list` of ``ChannelText``
        """
        return [channel for channel in self.channels.values() if channel.type==5]

    @property
    def store_channels(self):
        """
        Returns the store channels of the guild.
        
        Returns
        -------
        channels : `list` of ``ChannelStore``
        """
        return [channel for channel in self.channels.values() if channel.type==6]
    
    @property
    def thread_channels(self):
        """
        Returns the thread channels of the guild.
        
        Returns
        -------
        channels : `list` of ``ChannelThread``
        """
        return [channel for channel in self.channels.values() if channel.type==9]
    
    @property
    def messageable_channels(self):
        """
        Returns the message able channels of the guild.
        
        Returns
        -------
        channels : `list` of ``ChannelText``
        """
        return [channel for channel in self.channels.values() if channel.type in (0, 5)]
    
    @property
    def default_role(self):
        """
        Returns the default role of the guild (`@everyone`).
        
        Might return `None` at the case of partial guilds.
        
        Returns
        -------
        default_role : `None` or `Role``
        """
        return self.roles.get(self.id)
    
    @property
    def partial(self):
        """
        Returns whether the guild is partial.
        
        A guild is partial, if it has no active clients.
        
        Returns
        -------
        partial : `bool`
        """
        return (not self.clients)
    
    def _sync(self, data):
        """
        Syncs the guild with the requested guild data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild data.
        """
        try:
            is_large = data['large']
        except KeyError:
            is_large = (self.user_count>=LARGE_LIMIT)
        self.is_large = is_large
        
        self._update_no_return(data)
        
        try:
            role_datas = data['roles']
        except KeyError:
            pass
        else:
            self._sync_roles(role_datas)
        
        try:
            emoji_datas = data['emojis']
        except KeyError:
            pass
        else:
            self._sync_emojis(emoji_datas)

##        #sadly we dont get voice states with guild_get
##        try:
##            voice_state_datas=data['voice_states']
##        except KeyError:
##            self.voice_states.clear()
##        else:
##            old_voice_states=self.voice_states
##            new_voice_states=self.voice_states={}
##
##            for voice_state_data in voice_state_datas:
##                user=PartialUser(int(voice_state_data['user_id']))
##
##                channel_id=voice_state_data.get('channel_id',None)
##                if channel_id is None:
##                    continue
##                channel=self.channels[int(channel_id)]
##
##                try:
##                    voice_state=old_voice_states[user.id]
##                except KeyError:
##                    new_voice_states[user.id]=VoiceState(voice_state_data,channel)
##                    continue
##
##                voice_state._update_no_return(voice_state_data,channel)
##                new_voice_states[user.id]=voice_state

    def _apply_presences(self, data):
        """
        Applies the presences to the guild user's. Called when the guild is created or if a user chunk is received if
        presence caching is enabled.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Guild's users' presences' data.
        """
        users = self.users
        for presence in data:
            user_id = int(presence['user']['id'])
            try:
                user = users[user_id]
            except KeyError:
                pass
            else:
                user.status = Status.INSTANCES[presence['status']]
                user.statuses = presence['client_status']
                user.activities = [Activity(activity_data) for activity_data in presence['activities']]
    
    def _sync_channels(self, data):
        """
        Syncs the guild's channels with the given guild channel datas.
        
        Parameters
        ----------
        data `list` of (`dict` of (`str`, `Any`) items)
            Received guild channel datas.
        """
        channels = self.channels
        old_ids = set(channels)
        
        later = []
        for channel_data in data:
            channel_type = CHANNEL_TYPES[channel_data['type']]
            if channel_type is ChannelCategory:
                #categories
                channel = channel_type(channel_data, None, self)
                channel_id = channel.id
                try:
                    old_ids.remove(channel_id)
                except KeyError:
                    pass
                else:
                    #old channel -> update
                    channel._update_no_return(channel_data)
            else:
                later.append((channel_type, channel_data),)
        
        #non category channels
        for channel_type, channel_data in later:
            channel = channel_type(channel_data, None, self)
            channel_id = channel.id
            try:
                old_ids.remove(channel_id)
            except KeyError:
                pass
            else:
                #old channel -> update
                channel._update_no_return(channel_data)
        #deleting
        for channel_id in old_ids:
            channels[channel_id]._delete()
    
    def _sync_roles(self, data):
        """
        Syncs the guild's roles with the given guild role datas.
        
        Parameters
        ----------
        data `list` of (`dict` of (`str`, `Any`) items)
            Received guild role datas.
        """
        roles = self.roles
        old_ids = set(roles)
        # every new role can cause mass switchings at the role orders, can it mess up the order tho?
        for role_data in data:
            role = Role(role_data, self)
            try:
                old_ids.remove(role.id)
                role._update_no_return(role_data)
            except KeyError:
                pass
        
        for role_id in old_ids:
            roles[role_id]._delete()
    
    def get_user(self, name, default=None):
        """
        Tries to find the a user with the given name at the guild. Returns the first matched one.
        
        The search order is the following:
        - `full_name`
        - `name`
        - `nick`
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``User``, ``Client`` or `default`
        """
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name = name[:-5]
                for user in users.values():
                    if (user.discriminator == discriminator) and (user.name == name):
                        return user
        
        if len(name) > 32:
            return default
        
        for user in users.values():
            if user.name == name:
                return user
        
        for user in users.values():
            nick = user.guild_profiles[self].nick
            if nick is None:
                continue
            
            if nick == name:
                return user
        
        return default
    
    def get_user_like(self, name, default=None):
        """
        Searches a user, who's name or nick starts with the given string and returns the first find. Also matches full
        name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``User``, ``Client`` or `default`
        """
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users.values():
                    if (user.discriminator == discriminator) and (user.name == name_):
                        return user
        
        if len(name) > 32:
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        for user in self.users.values():
            if (pattern.match(user.name) is not None):
                return user
            
            nick = user.guild_profiles[self].nick
            
            if nick is None:
                continue
            
            if pattern.match(nick) is None:
                continue
            
            return user
        
        return default
    
    def get_users_like(self, name):
        """
        Searches the users, who's name or nick start with the given string.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        result = []
        if (not 1 < len(name) < 38):
            return result
        
        users = self.users
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users.values():
                    if (user.discriminator == discriminator) and (user.name == name_):
                        result.append(user)
                        break
        
        if len(name) > 32:
            return result
        
        pattern = re.compile(re.escape(name), re.I)
        for user in self.users.values():
            if pattern.match(user.name) is None:
                nick = user.guild_profiles[self].nick
                if nick is None:
                    continue
                
                if pattern.match(nick) is None:
                    continue
            
            result.append(user)
        return result
    
    def get_users_like_ordered(self, name):
        """
        Searches the users, who's name or nick start with the given string. At the orders them at the same ways, as
        Discord orders them when requesting guild member chunk.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        to_sort = []
        if (not 1 < len(name) < 33):
            return to_sort
        
        pattern = re.compile(re.escape(name), re.I)
        for user in self.users.values():
            profile = user.guild_profiles[self]
            if pattern.match(user.name) is None:
                nick = profile.nick
                if nick is None:
                    continue
                
                if pattern.match(nick) is None:
                    continue
            
            joined_at = profile.joined_at
            
            if joined_at is None:
                joined_at = user.created_at
            
            to_sort.append((joined_at, user))
        
        if not to_sort:
            return to_sort
        
        to_sort.sort(key=lambda x: x[0])
        return [x[1] for x in to_sort]
    
    def get_emoji(self, name, default=None):
        """
        Searches an emoji of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        emoji : ``Emoji`` or `default`
        """
        emoji = EMOJI_NAME_RP.fullmatch(name)
        if emoji is None:
            return default
        
        name = emoji.groups()[0]
        for emoji in self.emojis.values():
            if emoji.name == name:
                return emoji
        
        return default
    
    def get_emoji_like(self, name, default=None):
        """
        Searches an emoji of the guild, whats name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        emoji : ``Emoji`` or `default`
        """
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 32):
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        
        accurate_emoji = default
        accurate_name_length = 33
        
        for emoji in self.emojis.values():
            emoji_name = emoji.name
            name_length = len(emoji_name)
            if name_length > accurate_name_length:
                continue
            
            if pattern.match(emoji_name) is None:
                continue
            
            if name_length < accurate_name_length:
                accurate_emoji = emoji
                accurate_name_length = name_length
            
            if (name_length == target_name_length) and (name == emoji_name):
                return emoji
            
            continue
        
        return accurate_emoji
    
    def get_channel(self, name, default=None):
        """
        Searches a channel of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no channel was found. Defaults to `None`.
        
        Returns
        -------
        channel : ``ChannelGuildBase`` instance or `default`
        """
        if name.startswith('#'):
            name = name[1:]
        
        for channel in self.channels.values():
            if channel.display_name == name:
                return channel
        
        for channel in self.channels.values():
            if channel.name == name:
                return channel
        
        return default
    
    def get_channel_like(self, name, default=None, type_=None):
        """
        Searches a channel of the guild, whats name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no channel was found. Defaults to `None`.
        type_ : `None`, `type`, `tuple` of `type`, Optional
            Whether only specific channel type instances are accepted.
        
        Returns
        -------
        channel : ``ChannelGuildBase`` instance or `default`
        """
        if name.startswith('#'):
            name = name[1:]
        
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 100):
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        
        accurate_channel = default
        accurate_name_length = 101
        
        for channel in self.channels.values():
            if (type_ is not None) and (not isinstance(channel, type_)):
                continue
            
            channel_name = channel.name
            name_length = len(channel_name)
            if name_length > accurate_name_length:
                continue
            
            if pattern.match(channel_name) is None:
                continue

            if name_length < accurate_name_length:
                accurate_channel = channel
                accurate_name_length = name_length
            
            # Compare with display name
            if (name_length == target_name_length) and (name == channel.display_name):
                return channel
            
            continue
        
        return accurate_channel
    
    def get_role(self, name, default=None):
        """
        Searches a role of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no role was found. Defaults to `None`.
        
        Returns
        -------
        role : ``Role`` or `default`
        """
        for role in self.roles.values():
            if role.name == name:
                return role
        
        return default
    
    def get_role_like(self, name, default=None):
        """
        Searches a role of the guild, whats name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no role was found. Defaults to `None`.
        
        Returns
        -------
        role : ``Role`` or `default`
        """
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 32):
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        
        accurate_role = default
        accurate_name_length = 33
        
        for role in self.roles.values():
            role_name = role.name
            name_length = len(role_name)
            if name_length > accurate_name_length:
                continue
            
            if pattern.match(role_name) is None:
                continue
            
            if name_length < accurate_name_length:
                accurate_role = role
                accurate_name_length = name_length
            
            if (name_length == target_name_length) and (name == role_name):
                return role
            
            continue
        
        return accurate_role
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the guild.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        See Also
        --------
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        if user == self.owner:
            return Permission.permission_all
        
        base = self.roles[self.id].permissions
        
        try:
            roles = user.guild_profiles[self].roles
        except KeyError:
            if type(user) in (Webhook, WebhookRepr) and user.guild is self:
                return base
            return Permission.permission_none
        
        if (roles is not None):
            roles.sort()
            for role in roles:
                base |= role.permissions
        
        if Permission.can_administrator(base):
            return Permission.permission_all
        
        return Permission(base)
    
    def cached_permissions_for(self, user):
        """
        Returns the permissions for the given user at the guild. If the user's permissions are not cached, calculates
        and stores them first.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Mainly designed for getting clients' permissions.
        """
        cache_perm = self._cache_perm
        if cache_perm is None:
            self._cache_perm = cache_perm = {}
        else:
            try:
                return cache_perm[user.id]
            except KeyError:
                pass
        
        permissions = self.permissions_for(user)
        cache_perm[user.id] = permissions
        return permissions
    
    def _update(self, data):
        """
        Updates the guild and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------------------+-------------------------------+
        | Keys                      | Values                        |
        +===========================+===============================+
        | afk_channel               | `None` or ``ChannelVoice`     |
        +---------------------------+-------------------------------+
        | afk_timeout               | `int`                         |
        +---------------------------+-------------------------------+
        | available                 | `bool`                        |
        +---------------------------+-------------------------------+
        | banner                    | ``Icon``                      |
        +---------------------------+-------------------------------+
        | booster_count             | `int`                         |
        +---------------------------+-------------------------------+
        | content_filter            | ``ContentFilterLevel``        |
        +---------------------------+-------------------------------+
        | description               | `None` or `str`               |
        +---------------------------+-------------------------------+
        | discovery_splash          | ``Icon``                      |
        +---------------------------+-------------------------------+
        | embed_channel             | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | embed_enabled             | `bool`                        |
        +---------------------------+-------------------------------+
        | features                  | `list` of ``GuildFeature``    |
        +---------------------------+-------------------------------+
        | icon                      | ``Icon``                      |
        +---------------------------+-------------------------------+
        | invite_splash             | ``Icon``                      |
        +---------------------------+-------------------------------+
        | max_presences             | `int`                         |
        +---------------------------+-------------------------------+
        | max_users                 | `int`                         |
        +---------------------------+-------------------------------+
        | max_video_channel_users   | `int`                         |
        +---------------------------+-------------------------------+
        | message_notification      | ``MessageNotificationLevel``  |
        +---------------------------+-------------------------------+
        | mfa                       | ``MFA``                       |
        +---------------------------+-------------------------------+
        | name                      | `str`                         |
        +---------------------------+-------------------------------+
        | owner                     | ``User`` or ``Client``        |
        +---------------------------+-------------------------------+
        | preferred_locale          | `str`                         |
        +---------------------------+-------------------------------+
        | premium_tier              | `int`                         |
        +---------------------------+-------------------------------+
        | public_updates_channel    | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | region                    | ``VoiceRegion``               |
        +---------------------------+-------------------------------+
        | rules_channel             | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | system_channel            | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | system_channel_flags      | ``SystemChannelFlag``         |
        +---------------------------+-------------------------------+
        | vanity_code               | `None` or `str`               |
        +---------------------------+-------------------------------+
        | verification_level        | ``VerificationLevel``         |
        +---------------------------+-------------------------------+
        | widget_channel            | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | widget_enabled            | `bool`                        |
        +---------------------------+-------------------------------+
        """
        old_attributes = {}
        
        #ignoring 'roles'
        #ignoring 'emojis'
        #ignoring 'members'
        #ignoring 'presence'
        #ignoring 'channels'
        #ignoring 'voice_states'
        #ignoring 'member_count'
        #ignoring 'large'
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        self._update_icon(data, old_attributes)
        self._update_invite_splash(data, old_attributes)
        self._update_discovery_splash(data, old_attributes)
        self._update_banner(data, old_attributes)
        
        region = VoiceRegion.get(data['region'])
        if self.region is not region:
            old_attributes['region'] = region
            self.region = region
        
        afk_timeout = data['afk_timeout']
        if self.afk_timeout != afk_timeout:
            old_attributes['afk_timeout'] = self.afk_timeout
            self.afk_timeout = afk_timeout
        
        verification_level = VerificationLevel.INSTANCES[data['verification_level']]
        if self.verification_level is not verification_level:
            old_attributes['verification_level'] = self.verification_level
            self.verification_level = verification_level

        message_notification = MessageNotificationLevel.INSTANCES[data['default_message_notifications']]
        if self.message_notification is not message_notification:
            old_attributes['message_notification'] = self.message_notification
            self.message_notification = message_notification
        
        mfa = MFA.INSTANCES[data['mfa_level']]
        if self.mfa is not mfa:
            old_attributes['mfa'] = self.mfa
            self.mfa = mfa
        
        content_filter = ContentFilterLevel.INSTANCES[data.get('explicit_content_filter', 0)]
        if self.content_filter is not content_filter:
            old_attributes['content_filter'] = self.content_filter
            self.content_filter = content_filter
        
        available = (not data.get('unavailable', False))
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        try:
            features = data['features']
        except KeyError:
            features = []
        else:
            features = [GuildFeature.get(feature) for feature in features]
            features.sort()
        
        if self.features != features:
            old_attributes['features'] = self.features
            self.features = features
        
        system_channel_id = data.get('system_channel_id')
        if system_channel_id is None:
            system_channel = None
        else:
            system_channel = self.channels[int(system_channel_id)]
        
        if self.system_channel is not system_channel:
            old_attributes['system_channel'] = self.system_channel
            self.system_channel = system_channel
        
        try:
            system_channel_flags = SystemChannelFlag(data['system_channel_flags'])
        except KeyError:
            system_channel_flags = SystemChannelFlag.ALL
        
        if self.system_channel_flags != system_channel_flags:
            old_attributes['system_channel_flags'] = self.system_channel_flags
            self.system_channel_flags = system_channel_flags
        
        public_updates_channel_id = data.get('public_updates_channel_id')
        if public_updates_channel_id is None:
            public_updates_channel = None
        else:
            public_updates_channel = self.channels[int(public_updates_channel_id)]
        
        if self.public_updates_channel is not public_updates_channel:
            old_attributes['public_updates_channel'] = self.public_updates_channel
            self.public_updates_channel = public_updates_channel
        
        owner_id = data.get('owner_id')
        if owner_id is None:
            owner = ZEROUSER
        else:
            owner = PartialUser(int(owner_id))
        
        if self.owner != owner:
            old_attributes['owner'] = self.owner
            self.owner = owner
        
        afk_channel_id = data['afk_channel_id']
        if afk_channel_id is None:
            afk_channel = None
        else:
            afk_channel = self.channels[int(afk_channel_id)]
        if self.afk_channel is not afk_channel:
            old_attributes['afk_channel'] = self.afk_channel
            self.afk_channel = afk_channel
        
        widget_enabled = data.get('widget_enabled', False)
        if self.widget_enabled != widget_enabled:
            old_attributes['widget_enabled'] = self.widget_enabled
            self.widget_enabled = widget_enabled
        
        widget_channel_id = data.get('widget_channel_id')
        if widget_channel_id is None:
            widget_channel = None
        else:
            widget_channel = self.channels[int(widget_channel_id)]
        
        if self.widget_channel is not widget_channel:
            old_attributes['widget_channel'] = self.widget_channel
            self.widget_channel = widget_channel
        
        embed_enabled = data.get('embed_enabled', False)
        if self.embed_enabled != embed_enabled:
            old_attributes['embed_enabled'] = self.embed_enabled
            self.embed_enabled = embed_enabled

        embed_channel_id = data.get('embed_channel_id')
        if embed_channel_id is None:
            embed_channel = None
        else:
            embed_channel = self.channels[int(embed_channel_id)]
        
        if self.embed_channel is not embed_channel:
            old_attributes['embed_channel'] = self.embed_channel
            self.embed_channel = embed_channel
        
        rules_channel_id = data.get('rules_channel_id')
        if rules_channel_id is None:
            rules_channel = None
        else:
            rules_channel = self.channels[int(rules_channel_id)]
        
        if self.rules_channel is not rules_channel:
            old_attributes['rules_channel'] = self.rules_channel
            self.rules_channel = rules_channel
        
        description = data.get('description')
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        vanity_code = data.get('vanity_url_code')
        if self.vanity_code != vanity_code:
            old_attributes['vanity_code'] = self.vanity_code
            self.vanity_code = vanity_code
        
        max_users = data.get('max_members')
        if max_users is None:
            max_users = 250000
        if self.max_users != max_users:
            old_attributes['max_users'] = self.max_users
            self.max_users = max_users
        
        max_presences = data.get('max_presences')
        if max_presences is None:
            max_presences = 25000
        if self.max_presences != max_presences:
            old_attributes['max_presences'] = self.max_presences
            self.max_presences = max_presences
        
        max_video_channel_users = data.get('max_video_channel_users', 25)
        if self.max_video_channel_users!=max_video_channel_users:
            old_attributes['max_video_channel_users'] = self.max_video_channel_users
            self.max_video_channel_users = max_video_channel_users
        
        premium_tier=data['premium_tier']
        if self.premium_tier!=premium_tier:
            old_attributes['premium_tier']=self.premium_tier
            self.premium_tier=premium_tier

        booster_count = data.get('premium_subscription_count')
        if booster_count is None:
            booster_count = 0
        
        if self.booster_count != booster_count:
            old_attributes['booster_count'] = self.booster_count
            self.booster_count = booster_count
        
        self._boosters = None
        
        preferred_locale = parse_preferred_locale(data)
        if self.preferred_locale != preferred_locale:
            old_attributes['preferred_locale'] = self.preferred_locale
            self.preferred_locale = preferred_locale
        
        return old_attributes
    
    def _update_no_return(self, data):
        """
        Updates the guild and with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild data received from Discord.
        """
        #ignoring 'roles'
        #ignoring 'emojis'
        #ignoring 'members'
        #ignoring 'presence'
        #ignoring 'channels'
        #ignoring 'voice_states'
        
        self.name = data['name']
        
        self._set_icon(data)
        self._set_invite_splash(data)
        self._set_discovery_splash(data)
        self._set_banner(data)
        
        self.region = VoiceRegion.get(data['region'])
        
        self.afk_timeout = data['afk_timeout']
        
        self.verification_level = VerificationLevel.INSTANCES[data['verification_level']]
        
        self.message_notification = MessageNotificationLevel.INSTANCES[data['default_message_notifications']]
        
        self.mfa = MFA.INSTANCES[data['mfa_level']]
        
        self.content_filter = ContentFilterLevel.INSTANCES[data.get('explicit_content_filter', 0)]

        self.available = (not data.get('unavailable', False))
        
        try:
            features = data['features']
        except KeyError:
            self.features.clear()
        else:
            features = [GuildFeature.get(feature) for feature in features]
            features.sort()
            self.features = features
        
        system_channel_id = data.get('system_channel_id')
        if system_channel_id is None:
            system_channel = None
        else:
            system_channel = self.channels[int(system_channel_id)]
        self.system_channel = system_channel
        
        try:
            system_channel_flags = SystemChannelFlag(data['system_channel_flags'])
        except KeyError:
            system_channel_flags = SystemChannelFlag.ALL
        self.system_channel_flags = system_channel_flags
        
        public_updates_channel_id = data.get('public_updates_channel_id')
        if public_updates_channel_id is None:
            public_updates_channel = None
        else:
            public_updates_channel = self.channels[int(public_updates_channel_id)]
        self.public_updates_channel = public_updates_channel
        
        owner_id = data.get('owner_id')
        if owner_id is None:
            owner = ZEROUSER
        else:
            owner = PartialUser(int(owner_id))
        self.owner = owner
        
        afk_channel_id = data.get('afk_channel_id')
        if afk_channel_id is None:
            afk_channel = None
        else:
            afk_channel = self.channels[int(afk_channel_id)]
        self.afk_channel = afk_channel
        
        self.widget_enabled = data.get('widget_enabled', False)

        widget_channel_id = data.get('widget_channel_id')
        if widget_channel_id is None:
            widget_channel = None
        else:
            widget_channel = self.channels[int(widget_channel_id)]
        self.widget_channel = widget_channel
        
        self.embed_enabled = data.get('embed_enabled', False)

        embed_channel_id = data.get('embed_channel_id')
        if embed_channel_id is None:
            embed_channel = None
        else:
            embed_channel = self.channels[int(embed_channel_id)]
        self.embed_channel = embed_channel
        
        rules_channel_id = data.get('rules_channel_id')
        if rules_channel_id is None:
            rules_channel = None
        else:
            rules_channel = self.channels[int(rules_channel_id)]
        self.rules_channel = rules_channel
        
        self.description = data.get('description')
        
        self.vanity_code = data.get('vanity_url_code')
        
        max_users = data.get('max_members')
        if max_users is None:
            max_users = 250000
        self.max_users = max_users
        
        max_presences = data.get('max_presences')
        if max_presences is None:
            max_presences = 25000
        self.max_presences = max_presences
        
        self.max_video_channel_users = data.get('max_video_channel_users', 25)
        
        self.premium_tier = data['premium_tier']
        
        booster_count = data.get('premium_subscription_count')
        if booster_count is None:
            booster_count = 0
        
        self.booster_count = booster_count
        self._boosters = None
        
        self.preferred_locale = parse_preferred_locale(data)

    def _update_emojis(self, data):
        """
        Updates the emojis with the emojis' data received from Discord and returns all the changes broke down if any
        for each emoji.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Received emoji datas.
        
        Returns
        -------
        changes : `list` of `tuple` (`int`, ``Emoji``, (`None` or `dict` of (`str`, `Any`) items)))
            The changes breaken down for each changed emoji. Each element of the list is a tuple of 3 elements:
            +-------+-------------------+-----------------------------------------------+
            | Index | Respective name   | Type                                          |
            +=======+===================+===============================================+
            | 0     | action            | `int`                                         |
            +-------+-------------------+-----------------------------------------------+
            | 1     | emoji             | ``Emoji``                                     |
            +-------+-------------------+-----------------------------------------------+
            | 2     | old_attributes    | `None` or `dict` of (`str`, `Any`) items      |
            +-------+-------------------+-----------------------------------------------+
            
            Possible actions:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | EMOJI_UPDATE_NEW      | `0`   |
            +-----------------------+-------+
            | EMOJI_UPDATE_DELETE   | `1`   |
            +-----------------------+-------+
            | EMOJI_UPDATE_EDIT     | `2`   |
            +-----------------------+-------+
            
            If action is `EMOJI_UPDATE_EDIT`, then `old_attributes` is passed as a dictionary containing the changed
            attributes in an `attribute-name` - `old-value` relation. Every item in `old_attributes` is optional.
            +-------------------+-------------------------------+
            | Keys              | Values                        |
            +===================+===============================+
            | animated          | `bool`                        |
            +-------------------+-------------------------------+
            | available         | `bool`                        |
            +-------------------+-------------------------------+
            | managed           | `bool`                        |
            +-------------------+-------------------------------+
            | name              | `int`                         |
            +-------------------+-------------------------------+
            | require_colons    | `bool`                        |
            +-------------------+-------------------------------+
            | roles             | `None` or `set` of ``Role``   |
            +-------------------+-------------------------------+
        """
        emojis = self.emojis
        changes = []
        old_ids = set(emojis)
        
        for emoji_data in data:
            emoji_id = int(emoji_data['id'])
            try:
                emoji = emojis[emoji_id]
            except KeyError:
                emoji = Emoji(emoji_data,self)
                emojis[emoji_id] = emoji
                changes.append((EMOJI_UPDATE_NEW,emoji, None),)
            else:
                old_attributes = emoji._update(emoji_data)
                if old_attributes:
                    changes.append((EMOJI_UPDATE_EDIT, emoji, old_attributes),)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            emoji = emojis[emoji_id]
            emoji._delete()
            changes.append((EMOJI_UPDATE_DELETE, emoji, None),)
        
        return changes
    
    def _sync_emojis(self, data):
        """
        Syncs the emojis of the guild with the emoji datas.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Received emoji datas.
        """
        emojis = self.emojis
        old_ids = set(emojis)

        for emoji_data in data:
            emoji_id = int(emoji_data['id'])
            try:
                emoji = emojis[emoji_id]
            except KeyError:
                emoji = Emoji(emoji_data,self)
                emojis[emoji_id] = emoji
            else:
                emoji._update_no_return(emoji_data)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            emoji = emojis[emoji_id]
            emoji._delete()
    
    @property
    def emoji_limit(self):
        """
        The maximal amount of emojis, what the guild can have.
        
        Returns
        -------
        limit : `int`
        """
        limit = (50, 100, 150, 250)[self.premium_tier]
        if limit < 200 and (GuildFeature.more_emoji in self.features):
            limit = 200
        return limit
    
    @property
    def bitrate_limit(self):
        """
        The maximal bitrate for the guild's voice channels.
        
        Returns
        -------
        limit : `int`
        """
        limit = (96000, 128000, 256000, 384000)[self.premium_tier]
        if limit < 128000 and (GuildFeature.vip in self.features):
            limit = 128000
        return limit
    
    @property
    def upload_limit(self):
        """
        The maximal size of files, which can be uploaded to the guild's channels.
        
        Returns
        -------
        limit : `int`
        """
        return (8388608, 8388608, 52428800, 104857600)[self.premium_tier]

    widget_json_url = property(URLS.guild_widget_json_url)
    
    @property
    def boosters(self):
        """
        The boosters of the guild sorted by their subscription date.
        
        These users are queried from the guild's `.users` dictionary, so make sure that is populated before accessing
        the property.
        
        Returns
        -------
        boosters : `list` of (``User`` or ``Client``)
        """
        boosters = self._boosters
        if boosters is None:
            if self.booster_count:
                boosters_ordered = []
                for user in self.users.values():
                    boosts_since = user.guild_profiles[self].boosts_since
                    if boosts_since is None:
                        continue
                    boosters_ordered.append((boosts_since, user),)
                    
                boosters_ordered.sort(key=lambda element: element[0])
                boosters = [element[1] for element in boosters_ordered]
            else:
                boosters=[]
            
            self._boosters = boosters

        return boosters
    
    @property
    def emoji_counts(self):
        """
        Returns the emoji counts of the guild.
        
        Returns
        -------
        normal_static : `int`
            The static emoji count of the guild (excluding managed static).
        normal_animated : `int`
            The animated emoji count of the guild (excluding managed animated).
        managed_static : `int`
            The static managed emoji count of the guild.
        manged_animated : `int`
            The animated managed emoji count of the guild.
        """
        normal_static = 0
        normal_animated = 0
        managed_static = 0
        manged_animated = 0
        
        for emoji in self.emojis.values():
            if emoji.animated:
                if emoji.managed:
                    manged_animated +=1
                else:
                    normal_animated +=1
            else:
                if emoji.managed:
                    managed_static +=1
                else:
                    normal_static +=1
        
        return normal_static, normal_animated, managed_static, manged_animated
    
    @property
    def channel_list(self):
        """
        Returns the channels of the guild in a list in their display order. Note, that channels inside of categories are
        excluded.
        
        Returns
        -------
        channels : `list` of ``ChannelGuildBase`` instances
        """
        return sorted(channel for channel in self.channels.values() if channel.category is self)
    
    @property
    def channel_list_flattened(self):
        """
        Returns the channels of the guild in a list in their display order. Note, that channels inside of categories are
        included as well.
        
        channels : `list` of ``ChannelGuildBase`` instances
        """
        channels = []
        for channel in sorted(channel for channel in self.channels.values() if channel.category is self):
            channels.append(channel)
            if type(channel) is ChannelCategory:
                channels.extend(channel.list_channels)
        
        return channels
    
    @property
    def role_list(self):
        """
        Returns the roles of the guild in their display order.
        
        Returns
        -------
        roles : `list` of ``Role``
        """
        return sorted(self.roles.values())

class GuildPreview(DiscordEntity):
    """
    A preview of a public guild.
    
    Attributes
    ----------
    description : `str` or `None`
        Description of the guild. The guild must have `PUBLIC` feature.
    discovery_splash_hash : `int`
        The guild's discovery splashe's hash in `uint128`. The guild must have `DISCOVERABLE` feature to have
        discovery splash.
    discovery_splash_type : ``Icontype``
        The guild discovery splashe's type.
    emojis : `dict` of (`int`, ``Emoji``) items
        The emojis of the guild stored in `emoji_id` - `emoji` relation.
    features : `list` of ``GuildFeature``
        The guild's features.
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    icon_type : ``IconType``
        The guild's icon's type.
    invite_splash_hash : `int`
        The guild's invite splashe's hash in `uint128`. The guild must have `INVITE_SPLASH` feature.
    invite_splash_type : ``IconType``
        the guild's invite splashe's type.
    name : `str`
        The name of the guild.
    online_count : `int`
        Approximate amount of online users at the guild.
    user_count : `int`
        Approximate amount of users at the guild.
    """
    __slots__ = ('description', 'emojis', 'features', 'name', 'online_count', 'user_count', )
    
    icon = IconSlot('icon', 'icon', URLS.guild_icon_url, URLS.guild_icon_url_as)
    invite_splash = IconSlot('invite_splash', 'splash', URLS.guild_invite_splash_url, URLS.guild_invite_splash_url_as)
    discovery_splash = IconSlot('discovery_splash', 'discovery_splash', URLS.guild_discovery_splash_url, URLS.guild_discovery_splash_url_as)
    
    def __init__(self, data):
        """
        Creates a guild preview from the requested guild preview data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild preview data.
        """
        self.description = data.get('description',None)
        
        self._set_discovery_splash(data)
        
        emojis = {}
        self.emojis = emojis
        try:
            emoji_datas = data['emojis']
        except KeyError:
            pass
        else:
            for emoji_data in emoji_datas:
                emoji = Emoji(emoji_data, None)
                emojis[emoji.id] = emoji
        
        features = []
        self.features = features
        try:
            feature_datas = data['features']
        except KeyError:
            pass
        else:
            for feature_data in feature_datas:
                feature = GuildFeature.get(feature_data)
                features.append(feature)
            
            features.sort()
        
        self._set_icon(data)
        
        self.id = int(data['id'])
        
        self.name = data['name']
        
        self.online_count = data['approximate_presence_count']
        
        self._set_invite_splash(data)
        
        self.user_count = data['approximate_member_count']
    
    def __str__(self):
        """Returns the respective guild's name."""
        return self.name
    
    def __repr__(self):
        """Returns the guild preview's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'
    
    def __format__(self,code):
        """
        Formats the guild preview in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        channel : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```
        >>> from hata import Client, KOKORO
        >>> TOKEN = 'a token goes here'
        >>> client = Client(TOKEN)
        >>> guild_id = 302094807046684672
        >>> guild_preview = KOKORO.run(client.guild_preview(guild_id))
        >>> guild_preview
        <GuildPreview name='MINECRAFT', id=302094807046684672>
        >>> # no code stands for str(guild_preview).
        >>> f'{guild_preview}'
        'MINECRAFT'
        >>> # 'c' stands for created at.
        >>> f'{guild_preview:c}'
        '2017.04.13-14:56:54'
        ```
        """
        if not code:
            return self.name
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')

class GuildDiscovery(object):
    """
    Represent a guild's Discovery settings.
    
    Attributes
    ----------
    emoji_discovery : `bool`
        Whether guild info is shown when the respective guild's emojis are clicked.
    guild : `Guild`
        The represented guild.
    keywords : `None` or (`set` of `str`)
        The set discovery search keywords for the guild.
    primary_category_id : `int`
        The `id` of the primary discovery category of the guild.
    sub_category_ids : `set` of `int`
        Guild Discovery sub-category id-s. Can be maximum 5.
    """
    __slots__ = ('emoji_discovery', 'guild', 'keywords', 'primary_category', 'sub_categories')
    def __init__(self, data, guild):
        """
        Creates a new ``GuildDiscovery`` from the requested data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Requested guild discovery data.
        guild : ``Guild``
            The owner guild.
        """
        self.guild = guild
        
        self._update_no_return(data)
    
    def _update_no_return(self, data):
        """
        Updates the guild discovery object from the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild discovery data.
        """
        self.sub_categories = set(DiscoveryCategory.from_id(category_id) for category_id in data['category_ids'])
        self.emoji_discovery = data['emoji_discoverability_enabled']
        
        keywords = data['keywords']
        if (keywords is not None):
            if keywords :
                keywords  = set(keywords)
            else:
                keywords = None
        self.keywords = keywords
        
        self.primary_category = DiscoveryCategory.from_id(data['primary_category_id'], primary=True)
    
    def __eq__(self, other):
        """Returns whether the two guild dicoveries are the same."""
        if (type(self) is not type(other)):
            return NotImplemented
        
        if (self.guild is not other.guild):
            return False
        
        if (self.primary_category != other.primary_category_id):
            return False
        
        if (self.emoji_discovery != other.emoji_discovery):
            return False
        
        # Leave the set-s last.
        if (self.sub_categories != other.category_ids):
            return False
        
        # Keywords can be `None`.
        if (self.keywords != other.keywords):
            return False
        
        return True
    
    def __hash__(self):
        """Returns the guild discovery's hash value."""
        return self.guild.id
    
    def __repr__(self):
        """Returns the guild discovery's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' of guild ',
                ]
        
        guild = self.guild
        result.append(repr(guild.name))
        result.append(' (')
        result.append(repr(guild.id))
        result.append(')>')
        
        return ''.join(result)

class DiscoveryCategory(DiscordEntity, immortal=True):
    """
    Represents a category of a ``GuildDiscovery``.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the discovery category.
    local_names : `None` or `dict` of (`str`, `str`) items
        The category's name in other langauges.
    name : `str`
        The category's name.
    primary : `bool`
        Whether this category can be set as a guild's primary category.
    
    Class Attributes
    ----------------
    There are predefined discovery categories, which can be accessed as class attributes as well:
    
    +-------------------------------+-------+-------------------------------+-----------+
    | Class attribute name          | id    | name                          | primary   |
    +===============================+=======+===============================+===========+
    | general                       | `0`   | `'General'`                   | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | gaming                        | `1`   | `'Gaming'`                    | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | music                         | `2`   | `'Music'`                     | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | entertainment                 | `3`   | `'Entertainment'`             | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | creative_arts                 | `4`   | `'Creative Arts'`             | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | science_and_tech              | `5`   | `'Science & Tech'`            | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | ducation                      | `6`   | `'Education'`                 | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | sports                        | `7`   | `'Sports'`                    | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | fashion_and_beauty            | `8`   | `'Fashion & Beauty'`          | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | relationships_and_identity    | `9`   | `'Relationships & Identity'`  | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | travel_and_food               | `10`  | `'Travel & Food'`             | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | fitness_and_health            | `11`  | `'Fitness & Health'`          | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | finance                       | `12`  | `'Finance'`                   | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | other                         | `13`  | `'Other'`                     | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | general_chatting              | `14`  | `'General Chatting'`          | `True`    |
    +-------------------------------+-------+-------------------------------+-----------+
    | esports                       | `15`  | `'Esports'`                   | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | anime_and_manga               | `16`  | `'Anime & Manga'`             | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | movies_and_tv                 | `17`  | `'Movies & TV'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | books                         | `18`  | `'Books'`                     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | art                           | `19`  | `'Art'`                       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | writing                       | `20`  | `'Writing'`                   | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | crafts_diy_and_making         | `21`  | `'Crafts, DIY, & Making'`     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | programming                   | `22`  | `'Programming'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | podcasts                      | `23`  | `'Podcasts'`                  | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | tabletop_games                | `24`  | `'Tabletop Games'`            | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | memes                         | `25`  | `'Memes'`                     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | news_and_current_events       | `26`  | `'News & Current Events'`     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | cryptocurrency                | `27`  | `'Cryptocurrency'`            | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | investing                     | `28`  | `'Investing'`                 | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | studying_and_teaching         | `29`  | `'Studying & Teaching'`       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | lfg                           | `30`  | `'LFG'`                       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | customer_support              | `31`  | `'Customer Support'`          | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | theorycraft                   | `32`  | `'Theorycraft'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | events                        | `33`  | `'Events'`                    | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | roleplay                      | `34`  | `'Roleplay'`                  | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | content_creator               | `35`  | `'Content Creator'`           | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | business                      | `36`  | `'Business'`                  | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | local_group                   | `37`  | `'Local Group'`               | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | collaboration                 | `38`  | `'Collaboration'`             | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | fandom                        | `39`  | `'Fandom'`                    | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | wiki_and_guide                | `40`  | `'Wiki & Guide'`              | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | subreddit                     | `42`  | `'Subreddit'`                 | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | emoji                         | `43`  | `'Emoji'`                     | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | comics_and_cartoons           | `44`  | `'Comics & Cartoons'`         | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | mobile                        | `45`  | `'Mobile'`                    | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | console                       | `46`  | `'Console'`                   | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    | charity_and_nonprofit         | `47`  | `'Charity & Nonprofit'`       | `False`   |
    +-------------------------------+-------+-------------------------------+-----------+
    
    Notes
    -----
    Guild discovery objects are weakreferable.
    """
    __slots__ = ('local_names', 'name', 'primary')
    
    @classmethod
    def from_id(cls, category_id, primary=False):
        """
        Tries to find the category by the given id. If exists returns that, else creates a new one.
        
        Parameters
        ----------
        category_id : `int`
            The unique identificator number of the discovery category
        primary : `bool`, Optional
            Whether the catgeory is a primary category.
        
        Returns
        -------
        category : ``DiscoveryCategory``
        """
        try:
            category = DISCOVERY_CATEGORIES[category_id]
        except KeyError:
            category = object.__new__(cls)
            DISCOVERY_CATEGORIES[category_id] = category
            category.id = category_id
            category.name = ''
            category.local_names = None
            category.primary = primary
        
        if primary:
            category.primary = True
        
        return category
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``DiscoveryCategory`` object from the given data. if the discovery category already
        exists returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Discovery category data.
        
        Returns
        -------
        category : ``DiscoveryCategory``
        """
        # Note that even tho id is received as integer, but integers over 32 bits are still received as string.
        category_id = int(data['id'])
        
        try:
            category = DISCOVERY_CATEGORIES[category_id]
        except KeyError:
            category = object.__new__(cls)
            DISCOVERY_CATEGORIES[category_id] = category
            category.id = category_id
        
        category.primary = data['is_primary']
        name_data = data['name']
        category.name = name_data['default']
        
        local_names = name_data.get('localizations')
        if (local_names is not None) and (not local_names):
            local_names = None
        
        category.local_names = local_names
        
        return category
    
    def __init__(self, category_id, name, primary):
        """
        Creates a new discovery catgeory from the given parameters.
        
        Parameters
        ----------
        category_id : `int`
            The unique identificator number of the discovery category.
        name : `str`
            The category's name.
        primary : `bool`
            Whether this category can be set as a guild's primary category.
        """
        self.id = category_id
        self.name = name
        self.primary = primary
        self.local_names = None
        
        DISCOVERY_CATEGORIES[category_id] = self
    
    def created_at(self):
        """
        Returns when the discovery category was created.
        
        Because discovery category id-s are not snowflakes, this method will return the start of the discord epoch.
        
        Returns
        -------
        created_at : `datetime`
        """
        return DISCORD_EPOCH_START
    
    def __str__(self):
        """Returns the discovery category's name."""
        return self.name
    
    def __repr__(self):
        """Returns the discovery category's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self.name),
            ' id=',
            repr(self.id),
                ]
        
        if self.primary:
            result.append(' primary')
        
        result.append('>')
        
        return ''.join(result)
    
    general = NotImplemented
    gaming = NotImplemented
    music = NotImplemented
    entertainment = NotImplemented
    creative_arts = NotImplemented
    science_and_tech = NotImplemented
    education = NotImplemented
    sports = NotImplemented
    fashion_and_beauty = NotImplemented
    relationships_and_identity = NotImplemented
    travel_and_food = NotImplemented
    fitness_and_health = NotImplemented
    finance = NotImplemented
    other = NotImplemented
    general_chatting = NotImplemented
    esports = NotImplemented
    anime_and_manga = NotImplemented
    movies_and_tv = NotImplemented
    books = NotImplemented
    art = NotImplemented
    writing = NotImplemented
    crafts_diy_and_making = NotImplemented
    programming = NotImplemented
    podcasts = NotImplemented
    tabletop_games = NotImplemented
    memes = NotImplemented
    news_and_current_events = NotImplemented
    cryptocurrency = NotImplemented
    investing = NotImplemented
    studying_and_teaching = NotImplemented
    lfg = NotImplemented
    customer_support = NotImplemented
    theorycraft = NotImplemented
    events = NotImplemented
    roleplay = NotImplemented
    content_creator = NotImplemented
    business = NotImplemented
    local_group = NotImplemented
    collaboration = NotImplemented
    fandom = NotImplemented
    wiki_and_guide = NotImplemented
    subreddit = NotImplemented
    emoji = NotImplemented
    comics_and_cartoons = NotImplemented
    mobile = NotImplemented
    console = NotImplemented
    charity_and_nonprofit = NotImplemented

DiscoveryCategory.general = DiscoveryCategory(0, 'General', True)
DiscoveryCategory.gaming = DiscoveryCategory(1, 'Gaming', True)
DiscoveryCategory.music = DiscoveryCategory(2, 'Music', True)
DiscoveryCategory.entertainment = DiscoveryCategory(3, 'Entertainment', True)
DiscoveryCategory.creative_arts = DiscoveryCategory(4, 'Creative Arts', True)
DiscoveryCategory.science_and_tech = DiscoveryCategory(5, 'Science & Tech', True)
DiscoveryCategory.education = DiscoveryCategory(6, 'Education', True)
DiscoveryCategory.sports = DiscoveryCategory(7, 'Sports', True)
DiscoveryCategory.fashion_and_beauty = DiscoveryCategory(8, 'Fashion & Beauty', True)
DiscoveryCategory.relationships_and_identity = DiscoveryCategory(9, 'Relationships & Identity', True)
DiscoveryCategory.travel_and_food = DiscoveryCategory(10, 'Travel & Food', True)
DiscoveryCategory.fitness_and_health = DiscoveryCategory(11, 'Fitness & Health', True)
DiscoveryCategory.finance = DiscoveryCategory(12, 'Finance', True)
DiscoveryCategory.other = DiscoveryCategory(13, 'Other', True)
DiscoveryCategory.general_chatting = DiscoveryCategory(14, 'General Chatting', True)
DiscoveryCategory.esports = DiscoveryCategory(15, 'Esports', False)
DiscoveryCategory.anime_and_manga = DiscoveryCategory(16, 'Anime & Manga', False)
DiscoveryCategory.movies_and_tv = DiscoveryCategory(17, 'Movies & TV', False)
DiscoveryCategory.books = DiscoveryCategory(18, 'Books', False)
DiscoveryCategory.art = DiscoveryCategory(19, 'Art', False)
DiscoveryCategory.writing = DiscoveryCategory(20, 'Writing', False)
DiscoveryCategory.crafts_diy_and_making = DiscoveryCategory(21, 'Crafts, DIY, & Making', False)
DiscoveryCategory.programming = DiscoveryCategory(22, 'Programming', False)
DiscoveryCategory.podcasts = DiscoveryCategory(23, 'Podcasts', False)
DiscoveryCategory.tabletop_games = DiscoveryCategory(24, 'Tabletop Games', False)
DiscoveryCategory.memes = DiscoveryCategory(25, 'Memes', False)
DiscoveryCategory.news_and_current_events = DiscoveryCategory(26, 'News & Current Events', False)
DiscoveryCategory.cryptocurrency = DiscoveryCategory(27, 'Cryptocurrency', False)
DiscoveryCategory.investing = DiscoveryCategory(28, 'Investing', False)
DiscoveryCategory.studying_and_teaching = DiscoveryCategory(29, 'Studying & Teaching', False)
DiscoveryCategory.lfg = DiscoveryCategory(30, 'LFG', False)
DiscoveryCategory.customer_support = DiscoveryCategory(31, 'Customer Support', False)
DiscoveryCategory.theorycraft = DiscoveryCategory(32, 'Theorycraft', False)
DiscoveryCategory.events = DiscoveryCategory(33, 'Events', False)
DiscoveryCategory.roleplay = DiscoveryCategory(34, 'Roleplay', False)
DiscoveryCategory.content_creator = DiscoveryCategory(35, 'Content Creator', False)
DiscoveryCategory.business = DiscoveryCategory(36, 'Business', False)
DiscoveryCategory.local_group = DiscoveryCategory(37, 'Local Group', False)
DiscoveryCategory.collaboration = DiscoveryCategory(38, 'Collaboration', False)
DiscoveryCategory.fandom = DiscoveryCategory(39, 'Fandom', False)
DiscoveryCategory.wiki_and_guide = DiscoveryCategory(40, 'Wiki & Guide', False)
DiscoveryCategory.subreddit = DiscoveryCategory(42, 'Subreddit', False)
DiscoveryCategory.emoji = DiscoveryCategory(43, 'Emoji', False)
DiscoveryCategory.comics_and_cartoons = DiscoveryCategory(44, 'Comics & Cartoons', False)
DiscoveryCategory.mobile = DiscoveryCategory(45, 'Mobile', False)
DiscoveryCategory.console = DiscoveryCategory(46, 'Console', False)
DiscoveryCategory.charity_and_nonprofit = DiscoveryCategory(47, 'Charity & Nonprofit', False)

class WelcomeScreen(object):
    """
    Represents a guild's welcome screen.
    
    Attributes
    ----------
    description : `str`
        Description, of what is the server about.
    welcome_channels : `list` of ``WelcomeChannel``
        The featured channels by the welcome screen.
    """
    __slots__ = ('description', 'welcome_channels', )
    
    def __init__(self, data):
        """
        Creates a new welcome screen instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Welcome screen data.
        """
        self.description = data['description']
        self.welcome_channels = [
            WelcomeChannel(welcome_channel_data) for welcome_channel_data in data['welcome_channels']
                ]
    
    def __repr__(self):
        """Returns the welcome screen's representation."""
        return (f'<{self.__class__.__name__} description={reprlib.repr(self.description)}, welcome_channels='
            f'{self.welcome_channels!r}>')
    
    def __hash__(self):
        """Returns the welcome screen's hash."""
        return hash(self.description) ^ hash(self.welcome_channels)
    
    def __eq__(self, other):
        """Returns whether the two welcome screens are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.description != other.description:
            return False
        
        if self.welcome_channels != other.welcome_channels:
            return False
        
        return True

class WelcomeChannel(object):
    """
    Represents a featured channel by a welcome screen.
    
    Attributes
    ----------
    description : `str`
        The channel's short description.
    channel_id : `int`
        The channel's id.
    emoji : ``Emoji``
        The emoji displayed before the `description`.
    """
    __slots__ = ('description', 'channel_id', 'emoji', )
    def __init__(self, data):
        """
        Creates a new welcome channel instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Welcome channel data.
        """
        self.channel_id = int(data['channel_id'])
        self.description = data['description']
        self.emoji = PartialEmoji(data)
    
    @property
    def channel(self):
        """
        Returns the welcome channel's respective channel.
        """
        channel_id = self.channel_id
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = ChannelText._from_partial_data(None, channel_id, None)
        
        return channel
    
    def __repr__(self):
        """Returns the welcome channel's representation."""
        return (f'<{self.__class__.__name__} channel_id={self.channel_id},  emoji={self.emoji!r}, description='
            f'{reprlib.repr(self.description)}>')
    
    def __hash__(self):
        """Returns the welcome channel's hash."""
        return self.channel_id ^ self.emoji.id ^ hash(self.description)
    
    def __eq__(self, other):
        """Returns whether the two welcome channels are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.channel_id != other.channel_id:
            return False
        
        if (self.emoji is not other.emoji):
            return False
        
        if self.description != other.description:
            return False
        
        return True

ratelimit.Guild = Guild

del URLS
del cached_property
del ActivityUnknown
del UserBase
del ratelimit
del DiscordEntity
del ReverseFlagBase
del IconSlot
del DOCS_ENABLED
