# -*- coding: utf-8 -*-
__all__ = ('Attachment', 'EMBED_UPDATE_EMBED_ADD', 'EMBED_UPDATE_EMBED_REMOVE', 'EMBED_UPDATE_NONE',
    'EMBED_UPDATE_SIZE_UPDATE', 'Message', 'MessageActivity', 'MessageActivityType', 'MessageApplication',
    'MessageFlag', 'MessageReference', 'MessageType', 'UnknownCrossMention', )

import re
from datetime import datetime

from ..backend.dereaddons_local import any_to_any, where, cached_property, _spaceholder, BaseMethodDescriptor

from .bases import DiscordEntity, FlagBase
from .http import URLS
from .others import parse_time, CHANNEL_MENTION_RP, time_to_id
from .client_core import MESSAGES, CHANNELS, GUILDS
from .user import ZEROUSER, User
from .emoji import reaction_mapping
from .embed import EmbedCore, EXTRA_EMBED_TYPES
from .webhook import WebhookRepr, PartialWebhook, WebhookType, Webhook
from .role import Role
from .preconverters import preconvert_flag, preconvert_bool, preconvert_snowflake, preconvert_str
from .activity import ActivityStream

from . import ratelimit

Client          = NotImplemented
ChannelBase     = NotImplemented
ChannelTextBase = NotImplemented
ChannelGuildBase= NotImplemented
ChannelText     = NotImplemented
ChannelPrivate  = NotImplemented
ChannelGroup    = NotImplemented

class MessageFlag(FlagBase):
    """
    Bitwise flags of a ``Message``.
    
    The implemented message flags are the following:
    
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | crossposted               | 0                 |
    +---------------------------+-------------------+
    | is_crosspost              | 1                 |
    +---------------------------+-------------------+
    | embeds_suppressed         | 2                 |
    +---------------------------+-------------------+
    | source_message_deleted    | 3                 |
    +---------------------------+-------------------+
    | urgent                    | 4                 |
    +---------------------------+-------------------+
    | has_thread                | 5                 |
    +---------------------------+-------------------+
    """
    __keys__ = {
        'crossposted'           : 0,
        'is_crosspost'          : 1,
        'embeds_suppressed'     : 2,
        'source_message_deleted': 3,
        'urgent'                : 4,
        'has_thread'            : 5,
            }

class MessageActivityType(object):
    """
    Represents a ``MessageActivity``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the message activity type.
    value : `int`
        The Discord side identificator value of the message activity type.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``MessageActivityType``
        Stores the predefined ``MessageActivityType`` instances. These can be accessed with their `value` as index.
    
    Every predefind message activity type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | join                  | join          | 1     |
    +-----------------------+---------------+-------+
    | spectate              | spectate      | 2     |
    +-----------------------+---------------+-------+
    | listen                | listen        | 3     |
    +-----------------------+---------------+-------+
    | watch                 | watch         | 4     |
    +-----------------------+---------------+-------+
    | join_request          | join_request  | 5     |
    +-----------------------+---------------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 6
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self, value, name):
        """
        Creates an ``MessageActivityType`` and stores it at the classe's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the message activity type.
        name : `str`
            The name of the message activity type.
        """
        self.value=value
        self.name=name
        
        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the message activity type's name."""
        return self.name
    
    def __int__(self):
        """Returns the message activity type's value."""
        return self.value
    
    def __repr__(self):
        """Returns the represnetation of the message activity type."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    none         = NotImplemented
    join         = NotImplemented
    spectate     = NotImplemented
    listen       = NotImplemented
    watch        = NotImplemented
    join_request = NotImplemented

MessageActivityType.none         = MessageActivityType(0, 'none')
MessageActivityType.join         = MessageActivityType(1, 'join')
MessageActivityType.spectate     = MessageActivityType(2, 'spectate')
MessageActivityType.listen       = MessageActivityType(3, 'listen')
MessageActivityType.watch        = MessageActivityType(4, 'watch')
MessageActivityType.join_request = MessageActivityType(5, 'join_request')

class MessageActivity(object):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    party_id : `str`
        The message application's party's id. Can be empty string.
    type : ``MessageActivityType``
        The message application's type.
    """
    __slots__ = ('party_id', 'type',)
    def __init__(self, data):
        """
        Creates a new ``MessageActivity`` from message activity data included inside of a ``Message``'s data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message activity data.
        """
        self.party_id=data.get('party_id','')
        self.type=MessageActivityType.INSTANCES[data['type']]

    def __eq__(self, other):
        """Returns whether the two message activitys are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.party_id!=other.party_id:
            return False
        
        return True
    
    def __repr__(self):
        """Returns the message activity's representation."""
        return f'<{self.__class__.__name__} type={self.type.name} ({self.type.value}), party_id={self.party_id!r}>'
    
class Attachment(DiscordEntity):
    """
    Represents an attachment of a ``Message``.
    
    Attributes
    ----------
    id : `int`
        The unique identificcator number of the attachment.
    height : `int`
        The height of the attachment if applicable. Defaults to `0`.
    name : `str`
        The name of th attachment.
    proxy_url : `str`
        Proxied url of the attachment.
    size : `int`
        The attachment's size in bytes,
    url : `str`
        The attachment's url.
    width : `int`
        The attachment's width if applicable. Defaults to `0`.
    """
    __slots__ = ('height', 'name', 'proxy_url', 'size', 'url', 'width',)
    def __init__(self, data):
        """
        Creates an attachment object from the attachment data included inside of a ``Message`'s.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received attachment data.
        """
        self.name       = data['filename']
        self.id         = int(data['id'])
        self.proxy_url  = data['proxy_url']
        self.size       = data['size']
        self.url        = data['url']
        self.height     = data.get('height',0)
        self.width      = data.get('width',0)
    
    def __repr__(self):
        """Returns the representation of the attachment."""
        result = [
            '<',self.__class__.__name__,
            ' id=',repr(self.id),
            ', name=',repr(self.name),
                ]
        
        x=self.width
        y=self.height
        if x and y:
            result.append(', size=')
            result.append(repr(x))
            result.append('x')
            result.append(repr(y))
        
        result.append('>')
        
        return ''.join(result)
        

class MessageApplication(DiscordEntity):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the respective appliaction.
    cover : `int`
        The respective application's cover image's hash in `uin128` if applicable. Set as `0` if the application has
        no cover.
    description : `str`
        The respective application's description.
    icon : `int`
        The respective application's icon's hash in `uint128` if applicable. Set as `0`, if th application has no icon.
    name : `str`
        The respective application's name.
    """
    __slots__ = ('cover', 'description', 'icon', 'name',)
    def __init__(self, data):
        """
        Creates a new ``MessageApplication`` from message application data included inside of a ``Message``'s data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message application data.
        """
        cover = data.get('cover_image',)
        self.cover = 0 if cover is None else int(cover,16)
        self.description = data['description']
        icon=data.get('icon')
        self.icon = 0 if icon is None else int(icon,16)
        self.id = int(data['id'])
        self.name  = data['name']
    
    icon_url=property(URLS.application_icon_url)
    icon_url_as=URLS.application_icon_url_as
    cover_url=property(URLS.application_cover_url)
    cover_url_as=URLS.application_cover_url_as
    
    def __repr__(self):
        """Returns the represnetation of the message application."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'

class MessageReference(object):
    """
    A cross guild reference used as a ``Message``'s `.cross_reference` at crosspost messages.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`) items
        A dictionary used by the object's properties and cached properties.
    """
    __slots__=('_cache',)
    def __init__(self, data):
        """
        Creates a ``MessagReference`` from message reference data included inside of a ``Message``'s.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message reference data.
        """
        self._cache=cache={}
        
        try:
            channel_id=data['channel_id']
        except KeyError:
            channel_id=0
        else:
            channel_id=int(channel_id)
        
        cache['channel_id']=channel_id
        
        try:
            guild_id=data['guild_id']
        except KeyError:
            guild_id=0
        else:
            guild_id=int(guild_id)
            
        cache['guild_id']=guild_id
        
        try:
            message_id=data['message_id']
        except KeyError:
            message_id=0
        else:
            message_id=int(message_id)
            
        cache['message_id']=message_id
    
    @property
    def channel_id(self):
        """
        Returns the referenced message's channel's id. If no `channel_id` was received from Discord, returns `0`.
        
        Returns
        -------
        channel_id : `int`
        """
        return self._cache['channel_id']
    
    @property
    def guild_id(self):
        """
        Returns the referenced message's guild's id. If no `guild_id` was received from Discord, then returns `0`.
        
        Returns
        -------
        guild_id : `int`
        """
        return self._cache['guild_id']
    
    @property
    def message_id(self):
        """
        Returns the referenced message's id. If no `message_id` was received from Discord, then returns `0`.
        
        Returns
        -------
        message_id : `int`
        """
        return self._cache['message_id']
    
    @cached_property
    def channel(self):
        """
        Tries to find the referenced message's channel and return it. If fails on any step, then returns `None`.
        
        Returns
        -------
        channel : `None` or ``ChannelText``
        """
        channel_id=self._cache['channel_id']
        if channel_id==0:
            return None
        
        return CHANNELS.get(channel_id)
    
    @cached_property
    def guild(self):
        """
        Tries to find the referenced message's guild and return it. If fails on any step, then returns `None`.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        guild_id=self._cache['guild_id']
        if guild_id==0:
            return None
        
        return GUILDS.get(guild_id)
    
    @cached_property
    def message(self):
        """
        Tries to find the referenced message and return it. If fails on any step, then returns `None`.
        
        Returns
        -------
        message : `None` or ``Message``
        """
        message_id=self._cache['message_id']
        if message_id==0:
            return
        
        return MESSAGES.get(message_id)
    
    def __repr__(self):
        """Returns the representation of the message reference."""
        return f'<{self.__class__.__name__} channel_id={self._cache["channel_id"]}, guild_id={self._cache["guild_id"]}, message_id={self._cache["message_id"]}>'

class UnknownCrossMention(DiscordEntity):
    """
    Represents an unknown channel mentioned by a cross guild mention. These mentions are stored at ``Message``'s
    `.cross_mentions` instance attribute.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the respective channel.
    guild_id : `int`
        The unique identificator number of the respective channel's guild.
    name : `str`
        The name of the respective channel.
    type : `int`
        The channel type value of the respective channel.
    """
    __slots__ = ('guild_id', 'name', 'type',)
    def __new__(cls, data):
        """
        Tries to find the refernced channel by `id`. If it fails creates and returns an ``UnknownCrossMention``
        instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Cross reference channel mention data.
        
        Returns
        -------
        channel : ``UnknownCrossMention`` or ``ChannelGuildBase`` instance
        """
        channel_id=int(data['id'])
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            channel.id=channel_id
            channel.guild_id=int(data['guild_id'])
            channel.type=data['type']
            channel.name=data['name']
        
        return channel
    
    def __gt__(self,other):
        """Returns whether this unknown cross mention's id is greater than the other's."""
        if (type(other) is not UnknownCrossMention) or (not isinstance(other,ChannelBase)):
            return NotImplemented
        return self.id>other.id
    
    def __ge__(self,other):
        """Returns whether this unknown cross mention's id is greater or equal to the other's."""
        if (type(other) is not UnknownCrossMention) or (not isinstance(other,ChannelBase)):
            return NotImplemented
        return self.id>=other.id
    
    def __eq__(self,other):
        """Returns whether this unknown cross mention's id is equal to the other's."""
        if (type(other) is not UnknownCrossMention) or (not isinstance(other,ChannelBase)):
            return NotImplemented
        return self.id==other.id
    
    def __ne__(self,other):
        """Returns whether this unknown cross mention's id is not equal to the other's."""
        if (type(other) is not UnknownCrossMention) or (not isinstance(other,ChannelBase)):
            return NotImplemented
        return self.id!=other.id
    
    def __le__(self,other):
        """Returns whether this unknown cross mention's id is less or equal to the other's."""
        if (type(other) is not UnknownCrossMention) or (not isinstance(other,ChannelBase)):
            return NotImplemented
        return self.id<=other.id
    
    def __lt__(self,other):
        """Returns whether this unknown cross mention's id is less than the other's."""
        if (type(other) is not UnknownCrossMention) or (not isinstance(other,ChannelBase)):
            return NotImplemented
        return self.id<other.id
    
    def __str__(self):
        """Returns the unknown cross mention's respective channel's name."""
        return self.name
    
    def __format__(self, code):
        """
        Formats the unknown corss mention ina format string. Check ``ChannelBase.__format__`` for availabl format
        codes.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        unknow_cross_mention : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        """
        if not code:
            return self.__str__()
        if code=='m':
            return f'<#{self.id}>'
        if code=='d':
            return self.display_name
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def clients(self):
        """
        Returns the unknown cross mention's respective channel's clients, what is an empty `list` every time.
        
        Returns
        -------
        clients : `list` of ``Client``
        """
        return []
    
    @property
    def display_name(self):
        """
        Returns the unknown cross mention's respective channel's display name.
        
        Returns
        -------
        display_name : `str`
        """
        type_=self.type
        name=self.name
        # Text or Store
        if (type_==0) or (type_==5) or (type_==6):
            return name.lower()
        
        # Voice
        if (type==2):
            return name.capitalize()
        
        # Category
        if (type_==4):
            return name.upper()
        
        # Should not happen
        return name
    
    @property
    def guild(self):
        """
        Returns the unknown cross mention's respective channel's guild, what is `None` every time.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
    @property
    def mention(self):
        """
        The unknown cross mention's respective channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
    
    @property
    def partial(self):
        """
        Unknown cross mentions represent a partial channel, so this property returns `True` every time.
        
        Returns
        -------
        partial : `bool`
        """
        return True

EMBED_UPDATE_NONE = 0
EMBED_UPDATE_SIZE_UPDATE = 1
EMBED_UPDATE_EMBED_ADD = 2
EMBED_UPDATE_EMBED_REMOVE = 3

class Message(DiscordEntity, immortal=True):
    """
    Represents a message from Discord.
    
    id : `int`
        The unique identificator number of the message.
    _channel_mentions : `None` or `list` of (``UnknownCrossMention`` or ``ChannelBase`` instances)
        Cache used by the ``.channel_mentions` property.
    activity : `None` or ``MessageActivity``
        Sent with rich presence related embeds.
    application : `None` or ``MessageApplication``
        Sent with rich presence related embeds.
    attachments : `None` or `list` of ``Attachment``
        Attachments sent with the message.
    author : ``UserBase`` instance
        The author of the message. Can be any user type and if not found, then set as `ZEROUSER`.
    channel : ``ChannelTextBase`` instance
        The channel where the message is sent.
    content : `str`
        The message's content.
    cross_mentions : `None` or `list` of (``UnknownCrossMention`` or ``ChannelBase`` instances)
        Cross guild channel mentions of a crosspost message if applicable. If a channel is not loaded by the wrapper,
        then it will be represented with a ``UnknownCrossMention`` instead.
    cross_reference : `None` or ``MessageReference``
        Cross guild reference to the original message of crospost messages.
    edited : `None` or `datetime`
        The time when the message was edited, or `None` if it was not.
        > Pinning or (un)supressing a mesage will not change it's edited value.
    embeds : `None` or `list` of ``EmbedCore``
        List of embeds included with the message if any.
        > If a message contains links, then those embeds' might not be included with the source payload and those
        > will be added only later.
    everyone_mention : `bool`
        Whether the message contains `@everyone` or `@here`.
    flags : ``MessageFlag``
        The message's flags.
    nonce : `str` or `None`
        A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
        be shown up at the message's received payload as well.
    pinned : `bool`
        Whether the message is pinned.
    reactions : ``reaction_mapping``
        A dictionary like object, which contains the reactions on the message.
    role_mentions : `None` or `list` of ``Role``
        The mentioned roles by the message if any.
    tts : `bool`
        Whether the message is "text to speech".
    type : ``MessageType``
        The type of the message.
    user_mentions : `None` or `list` of (``Client`` or ``User``)
        The mentioned users by the message if any.
    """
    __slots__ = ('_channel_mentions', 'activity', 'application', 'attachments', 'author', 'channel', 'content',
        'cross_mentions', 'cross_reference', 'edited', 'embeds', 'everyone_mention', 'flags', 'nonce', 'pinned',
        'reactions', 'role_mentions', 'tts', 'type', 'user_mentions',)
    
    def __new__(cls, data, channel):
        """
        A message should not be created with `.__new__` method, but should be created through a channel method, or
        by ``Message.custom``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        channel : ``ChanneltextBase`` instance
            Source channel.
        
        Raises
        ------
        RuntimeError
            Message should not be created like this.
        """
        raise RuntimeError(f'`{cls.__name__}` should not be created like this.')
    
    @classmethod
    def _create_unlinked(cls, message_id, data, channel):
        """
        Creates an unlinked message.
        
        Parameters
        ----------
        message_id : `int`
            The message's unique identificator number.
        data : `dict` of (`str`, `Any`) items
            Message data.
        channel : ``ChanneltextBase`` instance
            Source channel.
        
        Returns
        -------
        self : ``Message``
        """
        self = object.__new__(cls)
        self.id = message_id
        self._finish_init(data, channel)
        return self
    
    def _finish_init(self, data, channel):
        """
        This method is called after a message object is created and it's id is set. Fills up the message's attributes
        from the given message data and stores the message at `MESSAGES` weak value dictionary.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        channel : ``ChanneltextBase`` instance
            Source channel.
        """
        self.channel=channel
        guild=channel.guild
        webhook_id=data.get('webhook_id',None)
        author_data=data.get('author',None)
        if webhook_id is None:
            self.cross_reference=None
            self.cross_mentions=None
            if author_data is None:
                self.author=ZEROUSER
            else:
                try:
                     author_data['member']=data['member']
                except KeyError:
                    pass
                self.author=User(author_data,guild)
        else:
            webhook_id=int(webhook_id)
            cross_reference_data=data.get('message_reference',None)
            is_cross=(cross_reference_data is not None)
            if is_cross:
                self.cross_reference=MessageReference(cross_reference_data)
                
                cross_mention_datas=data.get('mention_channels',None)
                if cross_mention_datas is None:
                    cross_mentions=None
                else:
                    cross_mentions=[UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas]
                    cross_mentions.sort()
                self.cross_mentions=cross_mentions
                webhook_type=WebhookType.server
            else:
                self.cross_reference=None
                self.cross_mentions=None
                webhook_type=WebhookType.bot
            
            if author_data is None:
                self.author=PartialWebhook(webhook_id,'',type_=webhook_type)
            else:
                self.author=WebhookRepr(author_data,webhook_id,type_=webhook_type,channel=channel)
        
        self.reactions=reaction_mapping(data.get('reactions',None))
        
        try:
            application_data=data['application']
        except KeyError:
            self.application=None
        else:
            self.application=MessageApplication(application_data)
        
        try:
            activity_data=data['activity']
        except KeyError:
            self.activity=None
        else:
            self.activity=MessageActivity(activity_data)

        edited = data['edited_timestamp']
        if (edited is not None):
            edited = parse_time(edited)
        self.edited = edited
        
        self.pinned=data.get('pinned',False)
        self.everyone_mention=data.get('mention_everyone',False)
        self.tts=data.get('tts',False)
        self.type=MessageType.INSTANCES[data['type']]
        
        attachment_datas=data['attachments']
        if attachment_datas:
            attachments=[Attachment(attachment) for attachment in attachment_datas]
        else:
            attachments=None
        self.attachments=attachments
        
        embed_datas=data['embeds']
        if embed_datas:
            self.embeds=[EmbedCore.from_data(embed) for embed in embed_datas]
        else:
            self.embeds=None
        
        self.nonce=data.get('nonce',None)
        self.content=data['content']
        self.flags=MessageFlag(data.get('flags',0))
        
        user_mention_datas=data['mentions']
        if user_mention_datas:
            self.user_mentions=[User(user_mention_data,guild) for user_mention_data in user_mention_datas]
            self.user_mentions.sort()
        else:
            self.user_mentions=None
        
        if guild is None:
            self._channel_mentions=None
            self.role_mentions=None
            self.cross_mentions=None
            self.cross_reference=None
        else:
            self._channel_mentions=_spaceholder
    
            try:
                role_mention_ids=data['mention_roles']
            except KeyError:
                role_mentions=None
            else:
                if role_mention_ids:
                    roles=guild.all_role
                    role_mentions=[]
                    for role_id in role_mention_ids:
                        try:
                            role_mentions.append(roles[int(role_id)])
                        except KeyError:
                            continue
                    role_mentions.sort()
                else:
                    role_mentions=None
            
            self.role_mentions=role_mentions
        
        MESSAGES[self.id]=self
        
    @BaseMethodDescriptor
    def custom(cls, base, validate=True, **kwargs):
        """
        Creates a custom message. If called as a method of a message, then the attribues of the created custom message
        will default to that message's. Meanwhile if called as a classmethod, then the attributes of the created
        custom message will default to the overall defaults.
        
        Parameters
        ----------
        validate : `bool`
            Whether contradictory between the message's attributes should be checked. If there is any, `ValueError`
           is raised.
        **kwargs : keyword arguments
            Additional attributes of the created message.
        
        Other Parameters
        ----------------
        activity : `None` or ``MessageActivity``, Optional
            The `.activity` attribute the message.
            If called as classmethod defaults to `None`.
        application : `None` or ``MessageApplication``., Optional
            The `.application` attribute the message.
            If called as a classmethod defaults to `None`.
        attachments : `None` or (`list` of ``Attachment``), Optional
            The `.attachments` attribute of the message. If passed as an empty list, then will be as `None` instead.
            If called as a classmethod defaults to `None`.
        author : `None`, ``Client``, ``User``, ``Webhook`` or ``WebhookRepr``, Optional
            The `.author` attribute of the message. If passed as `None` then it will be set as `ZEROUSER` instead.
            If called as a classmethod, defaults to `ZEROUSER`.
        channel : `ChannelTextBase` instance, Optional if called as method
            The `.channel` attribute of the message.
            If called as a clasmethod this attribute must be passed, or `TypeError` is raised.
        content : `str`, Optional
            The `.content` attribute of the message. Can be between length `0` and `2000`.
            If called as a classmethod defaults to `''` (empty string).
        cross_mentions : `None` or (`list` of (``UnknownCrossMetntion`` or ``ChannelGUildBase`` instances)), Optional
            The `.cross_mentions` attribute of the message. If passed as an empty list, then will be set `None` instead.
            If called as a classmethod defaults to `None`.
        cross_reference : `None` or ``MessageReference``, Optional
            The `.cross_reference` attribute of the message.
            If called as a classmethod defaults to `None`.
        edited : `None` or `datetime`, Optional.
            The `.edited` attribute of the message.
            If called as a classmethod, defaults to `None`.
        embeds : `None` or (`list` of ( ``EmbedCore`` or any embed compatible)), Optional
            The `.embeds` attribute of the message. If passed as an empty list, then is set as `None` instead. If
            passed as list and it contains any embeds, which are not type ``EmbedCore``, then those will be converted
            to ``EmbedCore`` as well.
            If called as a classmethod defaults to `None`.
        everyone_mention : `bool` or `int` instance (`0` or `1`), Optional
            The `.everyone_mention` attribute of the message. Accepts other `int` instance as `bool` as well, but
            their value still cannot be other than `0` or `1`.
            If called as a classmethod, defaults to `False`.
        flags : ``MessageFlag`` or `int`, Optional
            The `.flags` attribute of the message. If passed as other `int` instances than ``MessageFlag``, then will
            be converted to ``MessageFlag``.
            If called as a classmethod defaults to `MesageFlag()`.
        id : `int` or `str`, Optional
            The `.id` attribute of the message. If passed as `str`, will be converted to `int`.
            If called as a classmethod defaults to `0`.
        id_ : `int` or `str`, Optional.
            Alias of `id`.
        message_id : `int` or `str`, Optional
            Alias of `id`.
        nonce : `None` or `str`, Optional.
            The `.nonce` attribute of the message. If passed as `str` can be between length `0` and `32`.
            If called as a classmethod defaults to `None`.
        pinned :  : `bool` or `int` instance (`0` or `1`), Optional
            The `.pinned` attribute of the message. Accepts other `int` instances as `bool` as well, but their value
            still cannot be other than `0` or `1`.
            If called as a classmethod, defaults to `False`.
        reactions : `None` or ``reaction_mapping``, Optional.
            The `.reactions` attribute of the message. If passed as `None` will be set as an empty
            ``reaction_mapping``.
            If called as a classmethod defaults to empty ``reaction_mapping``.
        role_mentions : `None` or (`list` of ``Role``), Optional
            The `.role_mentions` attribute of the message. If passed as an empty `list`, will be set as `None`
            instead.
            If called as a classmethod defaults to `None`.
        tts :  : `bool` or `int` instance (`0` or `1`), Optional
            The `.tts` attribute of the message. Accepts other `int` instances as `bool` as well, but their value
            still cannot be other than `0` or `1`.
            If called as a classmethod, defaults to `False`.
        type : ``MessageType`` or `int`, Optional
            The `.type` attribute of the message. If passed as `int`, it will be converted to it's wrapper side
            ``MessageType`` representation.
            If called as a classmethod defaults to ``Messagetype.default`
        type_ : ``MesageType`` or `int`, Optional
            Alias of ``type`.
        user_mentions : `None` or (`list` of (``User`` or ``Client``)), Optional
            The `.user_mentions` attribute of the message. If passed as an empty list will be set as `None` instead.
            If called as a classmethod defaults to `None`.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            If any of the argument's type is incorrect.
        ValueError
            - If a passed argument's type is correct, but it's value is not.
            - If `validate` is passed as `True` and there is a contradictory between the message's attributes.
        """
        if (base is not None) and (type(base) is not cls):
            raise TypeError(f'`base` should be either `None`, or type `{cls.__name__}`, got `{base!r}`')
        
        try:
            channel=kwargs.pop('channel')
        except KeyError:
            if base is None:
                raise TypeError('Expected to be called as method, but was called as a classmethod and `channel` was not passed.')
            channel=base.channel
        else:
            if not isinstance(channel,ChannelTextBase):
                raise TypeError(f'`channel` should be `{ChannelTextBase.__name__}` subclasse\'s instance, got `{channel!r}`')
        
        # `_channel_mentions` is internal, we wont check kwargs
        if isinstance(channel,ChannelGuildBase):
            _channel_mentions=None
        else:
            _channel_mentions=_spaceholder
        
        try:
            activity=kwargs.pop('activity')
        except KeyError:
            if base is None:
                activity=None
            else:
                activity=base.activity
        else:
            if (activity is not None) and (type(activity) is not MessageActivity):
                raise TypeError(f'`activity` should be `None` or type `{MessageActivity.__name__}`, got `{activity!r}`')
        
        try:
            application=kwargs.pop('application')
        except KeyError:
            if base is None:
                application=None
            else:
                application=base.application
        else:
            if (application is not None) and (type(application) is not MessageApplication):
                raise TypeError(f'`application` should be `None` or type `{MessageApplication.__name__}`, got `{application!r}`')
        
        try:
            attachments=kwargs.pop('attachments')
        except KeyError:
            if base is None:
                attachments=None
            else:
                attachments=base.attachments
                if (attachments is not None):
                    # Copy it, because it might change
                    attachments=attachments.copy()
        else:
            if (attachments is not None):
                if (type(attachments) is not list):
                    raise TypeError(f'`attachments` should be `None` or `list` of type `{Attachment.__name__}`, got `{attachments!r}`')
                
                attachment_ln=len(attachments)
                if validate:
                    if attachment_ln>10:
                        raise ValueError(f'`attachments` should have maximal length of `10`, got `{attachment_ln!r}`')
                
                if attachment_ln:
                    for attachment in attachments:
                        if (type(attachment) is not Attachment):
                            raise TypeError(f'`attachments` `list` contains at least 1 non `{Attachment.__name__}` object, `{attachment!r}`')
                else:
                    # We should not have empty attachment list, lets fix it
                    attachments=None
        
        try:
            author=kwargs.pop('author')
        except KeyError:
            if base is None:
                author=ZEROUSER
            else:
                author=base.author
        else:
            if author is None:
                # Author cannot be None, but accept it as `ZEROUSER`
                author=ZEROUSER
            elif (type(author) in (User, Client, Webhook, WebhookRepr)):
                # This should be the case
                pass
            else:
                raise TypeError(
                    f'`author` can be type `None`, `{User.__name__}`, `{Client.__name__}`, `{Webhook.__name__}` or '
                    f'`{WebhookRepr.__name__}`, got `{author!r}`')
        
        try:
            content=kwargs.pop('content')
        except KeyError:
            if base is None:
                content = ''
            else:
                content = base.content
        else:
            content = preconvert_str(content, 'content', 0, 2000)
        
        try:
            cross_reference=kwargs.pop('cross_reference')
        except KeyError:
            if base is None:
                cross_reference=None
            else:
                cross_reference=base.cross_reference
        else:
            if (cross_reference is not None) and (type(cross_reference) is not MessageReference):
                    raise TypeError(f'`cross_reference` should be `None` or type `{MessageReference.__call__}`, got `{cross_reference!r}`')
        
        if validate:
            if (cross_reference is not None) and (type(channel) is not ChannelText):
                raise ValueError(
                    f'Only `{ChannelText.__name__}` can have `cross_reference` set as not `None`, but `channel` is set '
                    f'as `{channel!r}`')
        
        try:
            cross_mentions=kwargs.pop('cross_mentions')
        except KeyError:
            if base is None:
                cross_mentions=None
            else:
                cross_mentions=base.cross_mentions
                if (cross_mentions is not None):
                    # Copy it, it might change
                    cross_mentions=cross_mentions.copy()
        else:
            if (cross_mentions is not None):
                if (type(cross_mentions) is not list):
                    raise TypeError(
                        f'`cross_mentions` should be `None` or `list` of `{ChannelGuildBase.__name__}` subclass instances, or '
                        f'`{UnknownCrossMention.__name__}` instances, got `{cross_mentions!r}`')
                
                for channel_ in cross_mentions:
                    if isinstance(channel_,ChannelGuildBase):
                        continue
                        
                    if type(channel_) is UnknownCrossMention:
                        continue
                        
                    raise TypeError(
                        f'`cross_mentions` `list` contains at least 1 non `{ChannelGuildBase.__name__}` subclass '
                        f'instance or `{UnknownCrossMention.__name__}` instance; `{channel_!r}`')
        
        if validate:
            if (cross_reference is None) and (cross_mentions is not None):
                raise ValueError('`cross_mentions` are supported, only if `cross_reference` is provided')
        
        for name in ('message_id', 'id', 'id_'):
            try:
                message_id = kwargs.pop('message_id')
            except KeyError:
                continue
            
            message_id_found = True
            break
        else:
            message_id_found = False
        
        if message_id_found:
            message_id = preconvert_snowflake(message_id, name)
        else:
            if base is None:
                message_id = 0
            else:
                message_id = base.id
        
        try:
            edited=kwargs.pop('edited')
        except KeyError:
            if base is None:
                edited=None
            else:
                edited=base.edited
        else:
            if (edited is not None) and (type(edited) is not datetime):
                raise TypeError(f'`edited` can be `None` or type `datetime`, got `{edited!r}`')
        
        if validate:
            if (edited is not None) and (time_to_id(edited)<message_id):
                raise ValueError('`edited` can not be lower, than `created_at`')
        
        try:
            embeds=kwargs.pop('embeds')
        except KeyError:
            if base is None:
                embeds=None
            else:
                embeds=base.embeds
        else:
            if (embeds is not None):
                if (type(embeds) is not list):
                    raise TypeError(f'`embeds` can be `None` or `list` of type `{EmbedCore.__name__}`, got `{embeds!r}`')
                
                # Do not check embed length, Discord might be able to send more?
                
                embed_ln=len(embeds)
                if validate:
                    if len(embeds)>10:
                        raise ValueError(f'`embeds` can have maximal length of `10`, got `{embed_ln!r}`')
                
                if embed_ln:
                    for index in range(embed_ln):
                        embed=embeds[index]
                        
                        if type(embed) is EmbedCore:
                            continue
                            
                        if hasattr(type(embed),'to_data'):
                            # Embed compatible, lets convert it
                            embed=EmbedCore.from_data(embed.to_data())
                            embeds[index]=embed
                            continue
                        
                        raise TypeError(f'`embeds` `list` contains at least 1 non `{EmbedCore.__name__}` object; `{embeds!r}`')
                else:
                    # embeds cannot be an empty list, lets fix it
                    embeds=None
        
        try:
            everyone_mention=kwargs.pop('everyone_mention')
        except KeyError:
            if base is None:
                everyone_mention=False
            else:
                everyone_mention=base.everyone_mention
        else:
            everyone_mention = preconvert_bool(everyone_mention, 'everyone_mention')
        
        try:
            flags=kwargs.pop('flags')
        except KeyError:
            if base is None:
                flags=MessageFlag(0)
            else:
                flags=base.flags
        else:
            if flags is None:
                # Accept None, and then convert it.
                flags=MessageFlag()
            else:
                flags = preconvert_flag(flags, 'flags', MessageFlag)
        
        if validate:
            if type(channel) is ChannelText:
                if flags.source_message_deleted and (not flags.is_crosspost):
                    raise ValueError(
                        '`flags.source_message_deleted` is set, but `flags.is_crosspost` is not -> Only crossposted '
                        'message\'s source can be deleted')
                
                if (cross_reference is not None) and (not flags.is_crosspost):
                    raise ValueError(
                        '`cross_reference` is set, but `flags.is_crosspost` is not -> Only crossposted messages can have `cross_reference`')
                
                # Other cases?
            else:
                if flags.crossposted:
                    raise ValueError(f'`flags.crossposted` is set, meanwhile `channel` is not type `{ChannelText.__name__}`; `{channel!r}`')
    
                if flags.is_crosspost:
                    raise ValueError(f'`flags.is_crosspost` is set, meanwhile `channel` is not type `{ChannelText.__name__}`; `{channel!r}`')
    
                if flags.source_message_deleted:
                    raise ValueError(f'`flags.source_message_deleted` is set, meanwhile `channel` is not type `{ChannelText.__name__}`; `{channel!r}`')
        
        try:
            nonce=kwargs.pop('nonce')
        except KeyError:
            if base is None:
                nonce=None
            else:
                nonce=base.nonce
        else:
            if (nonce is not None):
                if (type(nonce) is not str):
                    raise TypeError(f'`nonce` should be `None` or type `str` instance, got `{nonce!r}`.')
                if len(nonce) > 32:
                    raise TypeError(f'`nonce`\'s length can be be maximum 32, got: `{nonce!r}`.')
            
        try:
            pinned=kwargs.pop('pinned')
        except KeyError:
            if base is None:
                pinned = False
            else:
                pinned=base.pinned
        else:
            pinned = preconvert_bool(pinned, 'pinned')
        
        try:
            reactions=kwargs.pop('reactions')
        except KeyError:
            if base is None:
                reactions=reaction_mapping(None)
            else:
                # Copy it, because it might be modified
                reactions=base.reactions.copy()
        else:
            if reactions is None:
                # Lets accept `None` and create an empty one
                reactions=reaction_mapping(None)
            elif type(reactions) is reaction_mapping:
                # We expect this as default
                pass
            else:
                raise TypeError(f'`reactions`, should be type `{reaction_mapping.__name__}`, got `{reactions}`')
        
        try:
            role_mentions=kwargs.pop('role_mentions')
        except KeyError:
            if base is None:
                role_mentions=None
            else:
                role_mentions=base.role_mentions
                if (role_mentions is not None):
                    # Copy it, because it might change
                    role_mentions=role_mentions.copy()
        else:
            if (role_mentions is not None):
                if (type(role_mentions) is not list):
                    raise TypeError(f'`role_mentions` should be `None` or `list` of type `{Role.__name__}`, got `{role_mentions!r}`')
                
                if role_mentions:
                    for role in role_mentions:
                        if type(role) is Role:
                            continue
                        
                        raise TypeError(f'`role_mentions` contains at least 1 non `{Role.__name__}` object, `{role_mentions!r}`')
                else:
                    # There cannot be an empty mention list, so lets fix it.
                    role_mentions=None
        
        if validate:
            if (role_mentions is not None) and (not isinstance(channel,ChannelGuildBase)):
                raise ValueError(
                    f'`role_mentions` are set as not `None`, meanhile the `channel` is not `{ChannelGuildBase}` '
                    f'subclasse\'s instance; `{channel!r}`')
        
        try:
            tts=kwargs.pop('tts')
        except KeyError:
            if base is None:
                tts=False
            else:
                tts=base.tts
        else:
            tts = preconvert_bool(tts, 'tts')
        
        for name in ('type_', 'type'):
            try:
                type_=kwargs.pop('type')
            except KeyError:
                continue
            
            type_found = True
            break
        else:
            type_found = False
        
        if type_found:
            if type(type_) is MessageType:
                # This is as it should be
                pass
            elif (type(type_) is int) and (type_>=0) and (type_<len(MessageType.INSTANCES)):
                # For second attemt, lets check int and it's value as well
                type_=MessageType.INSTANCES[type_]
            else:
                raise TypeError(f'`{name}` should be type `{MessageType.__name__}`, got `{type_!r}`')
            
        else:
            if base is None:
                type_=MessageType.default
            else:
                type_=base.type
        
        try:
            user_mentions=kwargs.pop('user_mentions')
        except KeyError:
            if base is None:
                user_mentions=None
            else:
                user_mentions=base.user_mentions
                if (user_mentions is not None):
                    # Copy it, because it might change
                    user_mentions=user_mentions.copy()
        else:
            if (user_mentions is not None):
                if (type(user_mentions) is not list):
                    raise TypeError(f'`user_mentions` should be type `list` of `{Client.__name__}` / `{User.__name__}`, got `{user_mentions!r}`')
                
                if user_mentions:
                    for user in user_mentions:
                        if type(user) in (Client,User):
                            continue
                        
                        raise TypeError(f'`user_mentions` contains at least 1 non `{Client.__name__}` or `{User.__name__}` object; `{user!r}`')
                else:
                    user_mentions = None
        
        # Check kwargs and raise TypeError if not every in used up
        if kwargs:
            raise TypeError(f'Unused aruments: {", ".join(list(kwargs))}')
        
        message=object.__new__(cls)
        
        message._channel_mentions=_channel_mentions
        message.activity=activity
        message.application=application
        message.attachments=attachments
        message.author=author
        message.channel=channel
        message.content=content
        message.cross_mentions=cross_mentions
        message.cross_reference=cross_reference
        message.edited=edited
        message.embeds=embeds
        message.everyone_mention=everyone_mention
        message.flags=flags
        message.id=message_id
        message.nonce=nonce
        message.pinned=pinned
        message.reactions=reactions
        message.role_mentions=role_mentions
        message.tts=tts
        message.type=type_
        message.user_mentions=user_mentions
        
        return message
        
    def _parse_channel_mentions(self):
        """
        Looks up the ``.contents`` of the message and searches channel mentions in them. If non, then sets
        `.channel_mentions` as `None`, else it sets it as a `list` of ``ChannelBase`` (and ``UnknownCrossMention``)
        instances. Invalid channel mentions are ignored.
        """
        content=self.content
        channel_mentions=[]
        channels=self.channel.guild.all_channel
        cross_mentions=self.cross_mentions

        for channel_id in CHANNEL_MENTION_RP.findall(content):
            channel_id=int(channel_id)
            try:
                channel=channels[channel_id]
            except KeyError:
                if cross_mentions is None:
                    continue
                try:
                    channel=cross_mentions[channel_id]
                except KeyError:
                    continue
            if channel not in channel_mentions:
                channel_mentions.append(channel)
        channel_mentions.sort()

        if channel_mentions:
            self._channel_mentions=channel_mentions
            return channel_mentions
        self._channel_mentions=None
    
    url = property(URLS.message_jump_url)
    
    @property
    def channel_mentions(self):
        """
        The mentioned channels by the message. If there is non, returns `None`.
        
        Returns
        -------
        channel_mentions : `None` or (`list` of (``Channelbase`` or ``UnknownCrossMentions`` instances))
        """
        channel_mentions = self._channel_mentions
        if channel_mentions is _spaceholder:
            channel_mentions = self._parse_channel_mentions()
        return channel_mentions
    
    def __repr__(self):
        """Returns the represnetation of the message."""
        return f'<{self.__class__.__name__} id={self.id}, ln={len(self)}, author={self.author.full_name}>'
    
    __str__ = __repr__
    
    def __format__(self,code):
        """
        Formats the message in a format string.
        
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
        >>>> from hata import Message, ChannelText, now_as_id
        >>>> message = Message.custom(content='Fluffy nekos', channel=ChannelText.precreate(now_as_id()))
        >>>> message
        <Message id=0, ln=12, author=#0000>
        >>>> # No code stands for str(message), what is same as repr(message) for the time being.
        >>>> f'{message}'
        '<Message id=0, ln=12, author=#0000>'
        >>>> # 'c' stands for created at.
        >>>> f'{message:c}'
        '2015.01.01-00:00:00'
        >>>> # 'e' stands for edited.
        >>>> f'{message:e}'
        'never'
        >>>> from datetime import datetime
        >>>> message = message.custom(edited=datetime.now())
        >>>> message
        <Message id=0, ln=12, author=#0000>
        >>>> f'{message:e}'
        '2020.05.31-16:00:00'
        """
        if not code:
            return self.__str__()
        
        if code=='c':
            return self.created_at.__format__('%Y.%m.%d-%H:%M:%S')
        
        if code=='e':
            edited = self.edited
            if edited is None:
                edited = 'never'
            else:
                edited = f'{edited:%Y.%m.%d-%H:%M:%S}'
            return edited
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    def _update(self, data):
        """
        Updates the message and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.

        A special case is if a message is (un)pinned or (un)suppressed , because then the returned dict is not going to
        contain `'edited'`, only `'pinned'` or `'flags'`. If the embeds are (un)suppressed of the message, then the
        returned dict might contain also an `'embeds'` key.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-------------------+-----------------------------------------------------------------------+
        | Keys              | Values                                                                |
        +===================+=======================================================================+
        | activity          | `None` or ``MessageActivity``                                         |
        +-------------------+-----------------------------------------------------------------------+
        | application       | `None` or ``MessageApplication``                                      |
        +-------------------+-----------------------------------------------------------------------+
        | attachments       | `None` or (`list` of ``Attachment``)                                  |
        +-------------------+-----------------------------------------------------------------------+
        | content           | `str                                                                  |
        +-------------------+-----------------------------------------------------------------------+
        | cross_mentions    | `None` or (`list` of (``ChannelBase`` or ``UnknownCrossMention``))    |
        +-------------------+-----------------------------------------------------------------------+
        | edited            | `None`  or `datetime`                                                 |
        +-------------------+-----------------------------------------------------------------------+
        | embeds            | `None`  or `(list` of ``EmbedCore``)                                  |
        +-------------------+-----------------------------------------------------------------------+
        | flags             | `UserFlag`                                                            |
        +-------------------+-----------------------------------------------------------------------+
        | mention_everyone  | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | pinned            | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | user_mentions     | `None` or (`list` of (``User`` or ``Client``))                        |
        +-------------------+-----------------------------------------------------------------------+
        | role_mentions     | `None` or (`list` of ``Role``)                                        |
        +-------------------+-----------------------------------------------------------------------+
        """
        old_attributes = {}

        pinned=data['pinned']
        if self.pinned!=pinned:
            old_attributes['pinned']=self.pinned
            self.pinned=pinned

        flags=data.get('flags',0)
        flag_difference=self.flags^flags
        if flag_difference:
            old_attributes['flags'] = self.flags
            self.flags = MessageFlag(flags)
            
            if MessageFlag(flag_difference).embeds_suppressed:
                embed_datas=data['embeds']
                if embed_datas:
                    embeds=[EmbedCore.from_data(embed) for embed in embed_datas]
                else:
                    embeds=None
                
                if self.embeds is None:
                    if (embeds is not None):
                        old_attributes['embeds']=None
                        self.embeds=embeds
                else:
                    if embeds is None:
                        old_attributes['embeds']=self.embeds
                        self.embeds=None
                    elif self.embeds!=embeds:
                        old_attributes['embeds']=self.embeds
                        self.embeds=embeds
        
        #at the case of pin update edited is None
        edited_timestamp=data['edited_timestamp']
        if edited_timestamp is None:
            return old_attributes
        
        edited=parse_time(edited_timestamp)
        if self.edited==edited:
            return old_attributes
        
        old_attributes['edited']=self.edited
        self.edited=edited
        
        try:
            application=MessageApplication(data['application'])
        except KeyError:
            application=None
        
        if self.application!=application:
            old_attributes['application']=self.application
            self.application=self.application
        
        try:
            activity_data=data['activity']
        except KeyError:
            activity=None
        else:
            activity=MessageActivity(activity_data)
        
        if self.activity is None:
            if (activity is not None):
                old_attributes['activity']=None
                self.activity=activity
        else:
            if activity is None:
                old_attributes['activity']=self.activity
                self.activity=None
            elif self.activity!=activity:
                old_attributes['activity']=self.activity
                self.activity=activity
                    
        everyone_mention=data.get('mention_everyone',False)
        if self.everyone_mention!=everyone_mention:
            old_attributes['everyone_mention']=self.everyone_mention
            self.everyone_mention=everyone_mention

        #ignoring tts
        #ignoring type
        #ignoring nonce
        
        attachment_datas=data['attachments']
        if attachment_datas:
            attachments=[Attachment(attachment) for attachment in attachment_datas]
        else:
            attachments=None
        
        if self.attachments is None:
            if (attachments is not None):
                old_attributes['attachments']=None
                self.attachments=attachments
        else:
            if attachments is None:
                old_attributes['attachments']=self.attachments
                self.attachments=None
            elif self.attachments!=attachments:
                old_attributes['attachments']=self.attachments
                self.attachments=attachments
        
        embed_datas=data['embeds']
        if embed_datas:
            embeds=[EmbedCore.from_data(embed) for embed in embed_datas]
        else:
            embeds=None
        
        if self.embeds is None:
            if (embeds is not None):
                old_attributes['embeds']=None
                self.embeds=embeds
        else:
            if embeds is None:
                old_attributes['embeds']=self.embeds
                self.embeds=None
            elif self.embeds!=embeds:
                old_attributes['embeds']=self.embeds
                self.embeds=embeds
            
        content=data['content']
        if self.content!=content:
            old_attributes['content']=self.content
            self.content=content

        user_mention_datas=data['mentions']

        guild=self.channel.guild
        
        if user_mention_datas:
            user_mentions=[User(user_mention_data,guild) for user_mention_data in user_mention_datas]
            user_mentions.sort()
        else:
            user_mentions=None

        if self.user_mentions is None:
            if (user_mentions is not None):
                old_attributes['user_mentions']=None
                self.user_mentions=user_mentions
        else:
            if user_mentions is None:
                old_attributes['user_mentions']=self.user_mentions
                self.user_mentions=None
            elif self.user_mentions!=user_mentions:
                old_attributes['user_mentions']=self.user_mentions
                self.user_mentions=user_mentions
        
        if guild is None:
            return old_attributes

        self._channel_mentions=_spaceholder

        cross_mention_datas=data.get('mention_channels',None)
        if cross_mention_datas is None:
            cross_mentions=None
        else:
            cross_mentions=[UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas]
            cross_mentions.sort()

        if self.cross_mentions is None:
            if (cross_mentions is not None):
                old_attributes['cross_mentions']=None
                self.cross_mentions=cross_mentions
        else:
            if cross_mentions is None:
                old_attributes['cross_mentions']=self.cross_mentions
                self.cross_mentions=None
            else:
                if self.cross_mentions!=cross_mentions:
                    old_attributes['cross_mentions']=self.cross_mentions
                    self.cross_mentions=cross_mentions
        
        try:
            role_mention_ids=data['mention_roles']
        except KeyError:
            role_mentions=None
        else:
            if role_mention_ids:
                roles=guild.all_role
                role_mentions=[]
                for role_id in role_mention_ids:
                    try:
                        role_mentions.append(roles[int(role_id)])
                    except KeyError:
                        continue
                role_mentions.sort()
            else:
                role_mentions=None

        if self.role_mentions is None:
            if (role_mentions is not None):
                old_attributes['role_mentions']=None
                self.role_mentions=role_mentions
        else:
            if role_mentions is None:
                old_attributes['role_mentions']=self.role_mentions
                self.role_mentions=None
            else:
                if self.role_mentions!=role_mentions:
                    old_attributes['role_mentions']=self.role_mentions
                    self.role_mentions=role_mentions

        return old_attributes
    
    def _update_no_return(self, data):
        """
        Updates the message with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        """
        self.pinned=data['pinned']
        
        flags=data.get('flags',0)
        flag_difference=self.flags^flags
        if flag_difference:
            self.flags = MessageFlag(flags)
            
            if MessageFlag(flag_difference).embeds_suppressed:
                embed_datas=data['embeds']
                if embed_datas:
                    embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
                else:
                    embeds=None
                self.embeds=embeds
        
        edited_timestamp=data['edited_timestamp']
        if edited_timestamp is None:
            return
        
        edited=parse_time(edited_timestamp)
        if self.edited==edited:
            return
        self.edited=edited

        try:
            self.application=MessageApplication(data['application'])
        except KeyError:
            self.application=None

        try:
            activity_data=data['activity']
        except KeyError:
            self.activity=None
        else:
            self.activity=MessageActivity(activity_data)

        self.everyone_mention=data['mention_everyone']

        #ignoring tts
        #ignoring type
        #ignoring nonce
        
        attachment_datas=data['attachments']
        if attachment_datas:
            attachments=[Attachment(attachment) for attachment in attachment_datas]
        else:
            attachments=None
        self.attachments=attachments

        embed_datas=data['embeds']
        if embed_datas:
            embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
        else:
            embeds=None
        self.embeds=embeds
        
        self.content=data['content']

        user_mention_datas=data['mentions']

        guild=self.channel.guild
        
        if user_mention_datas:
            user_mentions=self.user_mentions
            if user_mentions is None:
                user_mentions=[User(user_mention_data,guild) for user_mention_data in user_mention_datas]
                self.user_mentions=user_mentions
            else:
                user_mentions.clear()
                user_mentions.extend(User(user_mention_data,guild) for user_mention_data in user_mention_datas)
            user_mentions.sort()
        else:
            self.user_mentions=None

        if guild is None:
            return

        self._channel_mentions=_spaceholder

        cross_mention_datas=data.get('mention_channels',None)
        if cross_mention_datas is None:
            self.cross_mentions=None
        else:
            cross_mentions=[UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas]
            cross_mentions.sort()
            self.cross_mentions=cross_mentions
        
        try:
            role_mention_ids=data['role_mentions']
        except KeyError:
            self.role_mentions=None
        else:
            if role_mention_ids:
                role_mentions=self.role_mentions
                if role_mentions is None:
                    role_mentions=[]
                    self.role_mentions=role_mentions
                else:
                    role_mentions.clear()
                
                roles=guild.all_role
                for role_id in role_mention_ids:
                    try:
                        role_mentions.append(roles[int(role_id)])
                    except KeyError:
                        continue
                role_mentions.sort()
            else:
                self.role_mentions=None
        
    def _update_embed(self, data):
        """
        After getting a message, it's embeds might be updated from links, or with image, video sizes. If it happens
        this method is called.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        
        Returns
        -------
        change_state: `int`
            Possible values:
            
            +---------------------------+-------+
            | Respective name           | Value |
            +===========================+=======+
            | EMBED_UPDATE_NONE         | 0     |
            +---------------------------+-------+
            | EMBED_UPDATE_SIZE_UPDATE  | 1     |
            +---------------------------+-------+
            | EMBED_UPDATE_EMBED_ADD    | 2     |
            +---------------------------+-------+
            | EMBED_UPDATE_EMBED_REMOVE | 3     |
            +---------------------------+-------+
        """
        # This function gets called if only the embeds of the message are updated. There can be 3 case:
        # 0 -> Nothing changed or the embeds are already suppressed.
        # 1 -> Only sizes are updated -> images showed up?
        # 2 -> New embeds appeard -> link.
        # 3 -> There are less embed -> bug?
        
        embeds=self.embeds
        if embeds is None:
            ln1=0
        else:
            ln1=len(embeds)
        
        embed_datas=data.get('embeds',None)
        if embed_datas is None:
            ln2=0
        else:
            ln2=len(embed_datas)
        
        if ln1==0:
            if ln2==0:
                # No change
                return EMBED_UPDATE_NONE
            
            # New embeds are added
            self.embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
            return EMBED_UPDATE_EMBED_ADD
        
        if ln2<ln1:
            # Embeds are removed, should not happen, except if the message was suppressed.
            if self.flags.embeds_suppressed:
                self.embeds=None
                # Embeds are suppressed, message_edit was already called. Return 0.
                return EMBED_UPDATE_NONE
            
            # We have less embeds as we had, should not happen. Return 3.
            if ln2==0:
                self.embeds=None
            else:
                self.embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
            return EMBED_UPDATE_EMBED_REMOVE
        
        if ln1==0:
            embeds=[]
            self.embeds=embeds
        else:
            change_state = EMBED_UPDATE_NONE
            for index in range(ln1):
                embed_data=embed_datas[index]
                if embeds[index]._update_sizes(embed_data):
                    change_state = EMBED_UPDATE_SIZE_UPDATE
            
            if ln1==ln2:
                return change_state
        
        for index in range(ln1,ln2):
            embeds.append(EmbedCore.from_data(embed_datas[index]))
        
        return EMBED_UPDATE_EMBED_ADD

    def _update_embed_no_return(self, data):
        """
        Updates the message's embeds.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        """
        embeds=self.embeds
        if embeds is None:
            ln1=0
        else:
            ln1=len(embeds)
        
        embed_datas=data.get('embeds',None)
        if embed_datas is None:
            ln2=0
        else:
            ln2=len(embed_datas)
        
        if ln1==0:
            if ln2==0:
                # No change
                return
            
            # New embeds are added
            self.embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
            return
        
        if ln2<ln1:
            # Embeds are removed, should not happen, except if the message was suppressed.
            if self.flags.embeds_suppressed:
                self.embeds=None
                # Embeds are suppressed, message_edit was already called.
                return
            
            # We have less embeds as we had, should not happen.
            if ln2==0:
                self.embeds=None
            else:
                self.embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
            return
        
        if ln1==0:
            embeds=[]
            self.embeds=embeds
        else:
            for index in range(ln1):
                embed_data=embed_datas[index]
                embeds[index]._update_sizes_no_return(embed_data)

            if ln1==ln2:
                return

        for index in range(ln1,ln2):
            embeds.append(EmbedCore.from_data(embed_datas[index]))
    
    @property
    def guild(self):
        """
        Returns the message's channel's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return self.channel.guild

    @property
    def clean_content(self):
        """
        Returns them message's clean content, what actually depends on the message's type. By default it is the
        message's content with transformed mentions, but for differnt message types it means different things.
        
        Returns
        -------
        clean_content : `str`
        
        Notes
        -----
        The converting can not display join messages, call mesages and private channel names correctly.
        """
        return self.type.convert(self)
    
    @property
    def contents(self):
        """
        A list of all of the contents sent in the message. It means the message's content if it has and the content of
        the message's embeds.
        
        Returns
        -------
        contents : `list` of `str`
        """
        contents = []
        content = self.content
        if content:
            contents.append(content)
        
        embeds = self.embeds
        if (embeds is not None):
            for embed in embeds:
                contents.extend(embed.contents)

        return contents

    @property
    def mentions(self):
        """
        Returns a list of all the mentions sent at the message.
        
        Returns
        -------
        mentions : `list` of (`str` (`'everyone'`), ``User``, ``Client``, ``Role``, ``ChannelBase`` or
                ``UnknownCrossMention``)
        """
        mentions = []
        if self.everyone_mention:
            mentions.append('everyone')
        
        user_mentions = self.user_mentions
        if (user_mentions is not None):
            mentions.extend(user_mentions)
        
        role_mentions = self.role_mentions
        if (role_mentions is not None):
            mentions.extend(role_mentions)
            
        channel_mentions = self.channel_mentions
        if channel_mentions is not None:
            mentions.extend(channel_mentions)

        return mentions
        
    def __len__(self):
        """
        Returns the length of the message, including of the non link typed embeds's.
        
        Returns
        -------
        length : `int`
        """
        if self.type is MessageType.default:
            result=len(self.content)
        else:
            result=len(self.clean_content)
        
        embeds = self.embeds
        if (embeds is not None):
            for embed in embeds:
                if embed.type in EXTRA_EMBED_TYPES:
                    break
                result+=len(embed)
        return result

    @property
    def clean_embeds(self):
        """
        Returns the message's not link typed embeds with converted content without mentions.
        
        Returns
        -------
        clean_emebds : `list` of ``EmbedCore``
        
        Notes
        -----
        Not changes the original embeds of the message.
        """
        clean_embeds = []
        embeds = self.embeds
        
        if (embeds is not None):
            for embed in embeds:
                if embed.type in EXTRA_EMBED_TYPES:
                    continue
                
                clean_embeds.append(embed._clean_copy(self))
        
        return clean_embeds

    def did_react(self, emoji, user):
        """
        Returns whether the given user reacted with the given emoji on the mesage.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reacted emoji.
        user : ``User`` or ``Client``
            The reacter.
        
        Returns
        -------
        did_react : `bool`
        """
        try:
            reacters=self.reactions[emoji]
        except KeyError:
            return False
        return (user in reacters)

class MessageType(object):
    """
    Represnets a ``Message``'s type.
    
    Attributes
    ----------
    convert : `function`
        The converter function of the message type, what tries to convert the message's content to it's Discord side
        representation.
    name : `str`
        The name of the message type.
    value : `int`
        The Discord side identificator value of the message type.
        
    Class Attributes
    ----------------
    INSTANCES : `list` of ``MessageType``
        Stores the predefined ``MessageType`` instances. These can be accessed with their `value` as index.
    
    Every predefind message type can be accessed as class attribute as well:
    
    +-------------------------------------------+---------------------------------------------------+-------+
    | Class attribute name & name               | convert                                           | value |
    +===========================================+===================================================+=======+
    | default                                   | convert_default                                   | 0     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | add_user                                  | convert_add_user                                  | 1     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | remove_user                               | convert_remove_user                               | 2     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | call                                      | convert_call                                      | 3     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | channel_name_change                       | convert_channel_name_change                       | 4     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | channel_icon_change                       | convert_channel_icon_change                       | 5     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_pin                                   | convert_new_pin                                   | 6     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | welcome                                   | convert_welcome                                   | 7     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub                             | convert_new_guild_sub                             | 8     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t1                          | convert_new_guild_sub_t1                          | 9     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t2                          | convert_new_guild_sub_t2                          | 10    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t3                          | convert_new_guild_sub_t3                          | 11    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_follower_channel                      | convert_new_follower_channel                      | 12    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | stream                                    | convert_stream                                    | 13    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_disqualified                    | convert_discovery_disqualified                    | 14    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_requalified                     | convert_discovery_requalified                     | 15    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_grace_period_initial_warning    | convert_discovery_grace_period_initial_warning    | 16    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_grace_period_final_warning      | convert_discovery_grace_period_final_warning      | 17    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | thread_created                            | convert_thread_created                            | 18    |
    +-------------------------------------------+---------------------------------------------------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 19
    
    # object related
    __slots__ = ('convert', 'name', 'value', )
    
    def __init__(self, value, name, convert):
        """
        Creates an ``InviteTargetType`` and stores it at the classe's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the message type.
        name : `str`
            The name of the message type.
        convert : `function`
            The converter function of the message type.
        """
        self.value  = value
        self.name   = name
        self.convert= convert
        
        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the message type's name."""
        return self.name
    
    def __int__(self):
        """Returns the message type's value."""
        return self.value
    
    def __repr__(self):
        """Returns the representation of the message type."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r}, covert={self.convert!r})'
    
    # predefined
    default = NotImplemented
    add_user = NotImplemented
    remove_user = NotImplemented
    call = NotImplemented
    channel_name_change = NotImplemented
    channel_icon_change = NotImplemented
    new_pin = NotImplemented
    welcome = NotImplemented
    new_guild_sub = NotImplemented
    new_guild_sub_t1 = NotImplemented
    new_guild_sub_t2 = NotImplemented
    new_guild_sub_t3 = NotImplemented
    new_follower_channel = NotImplemented
    stream = NotImplemented
    discovery_disqualified = NotImplemented
    discovery_requalified = NotImplemented
    discovery_grace_period_initial_warning = NotImplemented
    discovery_grace_period_final_warning = NotImplemented

def convert_default(self):
    escape=re.escape
    transformations = {
        '@everyone':'@\u200beveryone',
        '@here':'@\u200bhere'
            }
    
    guild=self.channel.guild
    if guild is None:
        if self.user_mentions is not None:
            for user in self.user_mentions:
                transformations[escape(f'<@{user.id}>')]=f'@{user.name}'
    else:
        if self.channel_mentions is not None:
            for channel in self.channel_mentions:
                transformations[escape(f'<#{channel.id}>')]=f'#{channel.name}'
        
        if self.user_mentions is not None:
            for user in self.user_mentions:
                profile=user.guild_profiles.get(guild,None)
                if (profile is None) or (profile.nick is None):
                    name=f'@{user.name}'
                else:
                    name=f'@{profile.nick}'
                    
                transformations[escape(f'<@!{user.id}>')]=name
                transformations[escape(f'<@{user.id}>')]=name
        
        if self.role_mentions is not None:
            for role in self.role_mentions:
                transformations[escape(f'<@&{role.id}>')]=f'@{role.name}'

    return re.compile("|".join(transformations)).sub(lambda mention:transformations[escape(mention.group(0))],self.content)

def convert_add_user(self):
    return f'{self.author.name} added {self.user_mentions[0].name} to the group.'

def convert_remove_user(self):
    return f'{self.author.name} removed {self.user_mentions[0].name} from the group.'

def convert_call(self):
    if any_to_any(self.channel.clients,self.call.users):
        return f'{self.author.name} started a call.'
    if self.call.ended_timestamp is None:
        return f'{self.author.name} started a call \N{EM DASH} Join the call.'
    return f'You missed a call from {self.author.name}'

def convert_channel_name_change(self):
    return f'{self.author.name} changed the channel name: {self.content}'

def convert_channel_icon_change(self):
    return f'{self.author.name} changed the channel icon.'

def convert_new_pin(self):
    return f'{self.author.name} pinned a message to this channel.'

#TODO: this system changed, just pulled out the new texts from the js client source, but the calculation is bad
def convert_welcome(self):
    #tuples with immutable elements are stored directly
    join_messages=(
        '{0} just joined the server - glhf!',
        '{0} just joined. Everyone, look busy!',
        '{0} just joined. Can I get a heal?',
        '{0} joined your party.',
        '{0} joined. You must construct additional pylons.',
        'Ermagherd. {0} is here.',
        'Welcome, {0}. Stay awhile and listen.',
        'Welcome, {0}. We were expecting you ( ͡° ͜ʖ ͡°)',
        'Welcome, {0}. We hope you brought pizza.',
        'Welcome {0}. Leave your weapons by the door.',
        'A wild {0} appeared.',
        'Swoooosh. {0} just landed.',
        'Brace yourselves. {0} just joined the server.',
        '{0} just joined... or did they?',
        '{0} just arrived. Seems OP - please nerf.',
        '{0} just slid into the server.',
        'A {0} has spawned in the server.',
        'Big {0} showed up!',
        'Where’s {0}? In the server!',
        '{0} hopped into the server. Kangaroo!!',
        '{0} just showed up. Hold my beer.',
        'Challenger approaching - {0} has appeared!',
        'It\'s a bird! It\'s a plane! Nevermind, it\'s just {0}.',
        'It\'s {0}! Praise the sun! [T]/',
        'Never gonna give {0} up. Never gonna let {0} down.',
        '{0} has joined the battle bus.',
        'Cheers, love! {0}\'s here!',
        'Hey! Listen! {0} has joined!',
        'We\'ve been expecting you {0}',
        'It\'s dangerous to go alone, take {0}!',
        '{0} has joined the server! It\'s super effective!',
        'Cheers, love! {0} is here!',
        '{0} is here, as the prophecy foretold.',
        '{0} has arrived. Party\'s over.',
        'Ready player {0}',
        '{0} is here to kick butt and chew bubblegum. And {0} is all out of gum.',
        'Hello. Is it {0} you\'re looking for?',
        '{0} has joined. Stay a while and listen!',
        'Roses are red, violets are blue, {0} joined this server with you',
            )

    return join_messages[int(self.created_at.timestamp())%len(join_messages)].format(self.author.name)

def convert_new_guild_sub(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
    return f'{self.author.name} boosted {guild_name} with Nitro!'

def convert_new_guild_sub_t1(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 1!'

def convert_new_guild_sub_t2(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
    
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 2!'

def convert_new_guild_sub_t3(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 3!'

def convert_new_follower_channel(self):
    channel=self.channel
    guild = channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name = guild.name
    
    user_name = self.author.name_at(guild)
    
    return (f'{user_name} has added {guild_name} #{channel.name} to this channel. Its most important updates '
        'will show up here.')

def convert_stream(self):
    user = self.author
    for activity in user.activities:
        if type(activity) is ActivityStream:
            activity_name = activity.name
            break
    else:
        activity_name = 'Unknown'
    
    user_name = user.name_at(self.guild)
    
    return f'{user_name} is live! Now streaming {activity_name}'

def convert_discovery_disqualified(self):
    return ('This server has been removed from Server Discovery because it no longer passes all the requirements. '
        'Check `Server Settings` for more details.')

def convert_discovery_requalified(self):
    return 'This server is eligible for Server Discovery again and has been automatically relisted!'

def convert_discovery_grace_period_initial_warning(self):
    return ('This server has failed Discovery activity requirements for 1 week. If this server fails for 4 weeks in '
        'a row, it will be automatically removed from Discovery.')

def convert_discovery_grace_period_final_warning(self):
    return ('This server has failed Discovery activity requirements for 3 weeks in a row. If this server fails for 1 '
        'more week, it will be removed from Discovery.')

def convert_thread_created(self):
    user_name = self.author.name_at(self.guild)
    return f'{user_name} started a thread'

MessageType.default = MessageType(0, 'default', convert_default)
MessageType.add_user = MessageType(1, 'add_user', convert_add_user)
MessageType.remove_user = MessageType(2, 'remove_user', convert_remove_user)
MessageType.call = MessageType(3, 'call', convert_call)
MessageType.channel_name_change = MessageType(4, 'channel_name_change', convert_channel_name_change)
MessageType.channel_icon_change = MessageType(5, 'channel_icon_change', convert_channel_icon_change)
MessageType.new_pin = MessageType(6, 'new_pin', convert_new_pin)
MessageType.welcome = MessageType(7, 'welcome', convert_welcome)
MessageType.new_guild_sub = MessageType(8, 'new_guild_sub', convert_new_guild_sub)
MessageType.new_guild_sub_t1 = MessageType(9, 'new_guild_sub_t1', convert_new_guild_sub_t1)
MessageType.new_guild_sub_t2 = MessageType(1, 'new_guild_sub_t2', convert_new_guild_sub_t2)
MessageType.new_guild_sub_t3 = MessageType(11, 'new_guild_sub_t3', convert_new_guild_sub_t3)
MessageType.new_follower_channel = MessageType(12, 'new_follower_channel', convert_new_follower_channel)
MessageType.stream = MessageType(13, 'stream', convert_stream)
MessageType.discovery_disqualified = MessageType(14, 'discovery_disqualified', convert_discovery_disqualified)
MessageType.discovery_requalified = MessageType(15, 'discovery_requalified', convert_discovery_requalified)
MessageType.discovery_grace_period_initial_warning = MessageType(16, 'discovery_grace_period_initial_warning',
    convert_discovery_grace_period_initial_warning)
MessageType.discovery_grace_period_final_warning = MessageType(17, 'discovery_grace_period_final_warning',
    convert_discovery_grace_period_final_warning)
MessageType.discovery_grace_period_final_warning = MessageType(18, 'thread_created', convert_thread_created)

del convert_default
del convert_add_user
del convert_remove_user
del convert_call
del convert_channel_name_change
del convert_channel_icon_change
del convert_new_pin
del convert_welcome
del convert_new_guild_sub
del convert_new_guild_sub_t1
del convert_new_guild_sub_t2
del convert_new_guild_sub_t3
del convert_new_follower_channel
del convert_stream
del convert_discovery_disqualified
del convert_discovery_requalified
del convert_thread_created

ratelimit.Message = Message

del URLS
del ratelimit
del DiscordEntity
del FlagBase
