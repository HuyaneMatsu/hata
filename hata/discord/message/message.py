__all__ = ('EMBED_UPDATE_EMBED_ADD', 'EMBED_UPDATE_EMBED_REMOVE', 'EMBED_UPDATE_NONE', 'EMBED_UPDATE_SIZE_UPDATE',
    'Message',)

from datetime import datetime

from ...backend.utils import BaseMethodDescriptor
from ...backend.export import export, include

from ..bases import DiscordEntity, id_sort_key
from ..utils import parse_time, CHANNEL_MENTION_RP, time_to_id, DATETIME_FORMAT_CODE
from ..core import MESSAGES
from ..user import ZEROUSER, User, ClientUserBase, UserBase
from ..emoji import reaction_mapping
from ..embed import EmbedCore, EXTRA_EMBED_TYPES, EmbedBase
from ..webhook import WebhookRepr, create_partial_webhook_from_id, WebhookType, Webhook
from ..role import Role
from ..preconverters import preconvert_flag, preconvert_bool, preconvert_snowflake, preconvert_str, \
    preconvert_preinstanced_type

from .. import urls as module_urls

from .utils import try_resolve_interaction_message
from .cross_mention import UnknownCrossMention
from .message_activity import MessageActivity
from .attachment import Attachment
from .message_application import MessageApplication
from .message_interaction import MessageInteraction
from .message_reference import MessageReference
from .sticker import Sticker
from .flags import MessageFlag
from .preinstanced import MessageType


ChannelTextBase = include('ChannelTextBase')
ChannelGuildBase = include('ChannelGuildBase')
ChannelText = include('ChannelText')
ChannelPrivate = include('ChannelPrivate')
ChannelGroup = include('ChannelGroup')
create_component = include('create_component')
ChannelGuildUndefined = include('ChannelGuildUndefined')
CHANNEL_TYPES = include('CHANNEL_TYPES')
InteractionType = include('InteractionType')
ComponentBase = include('ComponentBase')
ChannelThread = include('ChannelThread')

EMBED_UPDATE_NONE = 0
EMBED_UPDATE_SIZE_UPDATE = 1
EMBED_UPDATE_EMBED_ADD = 2
EMBED_UPDATE_EMBED_REMOVE = 3



@export
class Message(DiscordEntity, immortal=True):
    """
    Represents a message from Discord.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the message.
    _channel_mentions : `None` or `list` of (``UnknownCrossMention`` or ``ChannelBase`` instances)
        Cache used by the ``.channel_mentions` property.
    activity : `None` or ``MessageActivity``
        Sent with rich presence related embeds.
    application : `None` or ``MessageApplication``
        Sent with rich presence related embeds.
    application_id : `int`
        The application's identifier who sent the message. Defaults to `0`.
    attachments : `None` or `tuple` of ``Attachment``
        Attachments sent with the message.
    author : ``UserBase`` instance
        The author of the message. Can be any user type and if not found, then set as `ZEROUSER`.
    channel : ``ChannelTextBase`` instance
        The channel where the message is sent.
    components : `None` or `tuple` of ``ComponentBase``
        Message components.
    content : `str`
        The message's content.
    cross_mentions : `None` or `tuple` of (``UnknownCrossMention`` or ``ChannelBase`` instances)
        Cross guild channel mentions of a crosspost message if applicable. If a channel is not loaded by the wrapper,
        then it will be represented with a ``UnknownCrossMention`` instead.
    referenced_message : `None`, ``Message`` or ``MessageReference``
        the referenced message. Set as ``Message`` instance if the message is cached, else as ``MessageReference``.
        
        Set when the message is a reply, a crosspost or when is a pin message.
    deleted : `bool`
        Whether the message is deleted.
    edited_at : `None` or `datetime`
        The time when the message was edited, or `None` if it was not.
        
        Pinning or (un)suppressing a message will not change it's edited value.
    embeds : `None` or `tuple` of ``EmbedCore``
        List of embeds included with the message if any.
        
        If a message contains links, then those embeds' might not be included with the source payload and those
        will be added only later.
    everyone_mention : `bool`
        Whether the message contains `@everyone` or `@here`.
    flags : ``MessageFlag``
        The message's flags.
    interaction : `None` or ``MessageInteraction``
        Present if the message is a response to an ``InteractionEvent``.
    nonce : `str` or `None`
        A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
        be shown up at the message's received payload as well.
    pinned : `bool`
        Whether the message is pinned.
    reactions : ``reaction_mapping``
        A dictionary like object, which contains the reactions on the message.
    role_mentions : `None` or `tuple` of ``Role``
        The mentioned roles by the message if any.
    stickers : `None` or `tuple` of ``Sticker``
        The stickers sent with the message.
        
        Bots currently can only receive messages with stickers, not send.
    thread : `None` or ``ChannelThread``
        The thread which was started from this message. Defaults to `None`.
    tts : `bool`
        Whether the message is "text to speech".
    type : ``MessageType``
        The type of the message.
    user_mentions : `None` or `tuple` of ``UserBase``
        The mentioned users by the message if any.
    """
    __slots__ = ('_channel_mentions', 'activity', 'application', 'application_id', 'attachments', 'author', 'channel',
        'components', 'content', 'cross_mentions', 'deleted', 'edited_at', 'embeds', 'everyone_mention', 'flags',
        'interaction', 'nonce', 'pinned', 'reactions', 'referenced_message', 'role_mentions', 'stickers', 'thread',
        'tts', 'type', 'user_mentions',)
    
    def __new__(cls, data, channel):
        """
        A message should not be created with `.__new__` method, but should be created through a channel method, or
        by ``Message.custom``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        channel : ``ChannelTextBase`` instance
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
            The message's unique identifier number.
        data : `dict` of (`str`, `Any`) items
            Message data.
        channel : ``ChannelTextBase`` instance
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
        channel : ``ChannelTextBase`` instance
            Source channel.
        """
        self.deleted = False
        self.channel = channel
        guild = channel.guild
        webhook_id = data.get('webhook_id', None)
        author_data = data.get('author', None)
        
        if webhook_id is None:
            cross_mentions = None
            if author_data is None:
                author = ZEROUSER
            else:
                try:
                     author_data['member'] = data['member']
                except KeyError:
                    pass
                author = User(author_data, guild)
        else:
            webhook_id = int(webhook_id)
            if (data.get('message_reference', None) is not None):
                cross_mention_datas = data.get('mention_channels', None)
                if (cross_mention_datas is None) or (not cross_mention_datas):
                    cross_mentions = None
                else:
                    cross_mentions = tuple(sorted(
                        (UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas),
                        key=id_sort_key,
                    ))
                
                webhook_type = WebhookType.server
            else:
                cross_mentions = None
                webhook_type = WebhookType.bot
            
            if author_data is None:
                author = create_partial_webhook_from_id(webhook_id, '', type_=webhook_type)
            else:
                author = WebhookRepr(author_data, webhook_id, type_=webhook_type, channel=channel)
        
        self.author = author
        self.cross_mentions = cross_mentions
        
        self.reactions = reaction_mapping(data.get('reactions', None))
        
        # Most common case is reply
        # First always check the `referenced_message` payload, and then second the `message_reference` one.
        #
        # Note, that `referenced_message` wont contain an another `referenced_message`, but only `message_reference`
        # one.
        
        referenced_message_data = data.get('referenced_message', None)
        if referenced_message_data is None:
            referenced_message_data = data.get('message_reference', None)
            if referenced_message_data is None:
                referenced_message = None
            else:
                referenced_message = MessageReference(referenced_message_data)
        else:
            referenced_message = channel._create_unknown_message(referenced_message_data)
        
        self.referenced_message = referenced_message
        
        
        try:
            application_data = data['application']
        except KeyError:
            application = None
        else:
            application = MessageApplication(application_data)
        self.application = application
        
        try:
            activity_data = data['activity']
        except KeyError:
            activity = None
        else:
            activity = MessageActivity(activity_data)
        self.activity = activity
        
        edited_timestamp = data.get('edited_timestamp', None)
        if (edited_timestamp is None):
            edited_at = None
        else:
            edited_at = parse_time(edited_timestamp)
        self.edited_at = edited_at
        
        self.pinned = data.get('pinned', False)
        self.everyone_mention = data.get('mention_everyone', False)
        self.tts = data.get('tts', False)
        self.flags = flags = MessageFlag(data.get('flags', 0))
        
        try:
            message_type_value = data['type']
        except KeyError:
            if flags.invoking_user_only:
                message_type = MessageType.application_command
            else:
                message_type = MessageType.default
        else:
            message_type = MessageType.get(message_type_value)
        
        self.type = message_type
        
        attachment_datas = data.get('attachments', None)
        if (attachment_datas is not None) and attachment_datas:
            attachments = tuple(Attachment(attachment) for attachment in attachment_datas)
        else:
            attachments = None
        self.attachments = attachments
        
        embed_datas = data.get('embeds', None)
        if (embed_datas is not None) and embed_datas:
            embeds = tuple(EmbedCore.from_data(embed) for embed in embed_datas)
        else:
            embeds = None
        self.embeds = embeds
        
        self.nonce = data.get('nonce', None)
        self.content = data.get('content', '')
        
        interaction_data = data.get('interaction', None)
        if interaction_data is None:
            interaction = None
        else:
            interaction = MessageInteraction(interaction_data)
            try_resolve_interaction_message(self, interaction)
        
        self.interaction = interaction
        
        component_datas = data.get('components', None)
        if (component_datas is None) or (not component_datas):
            components = None
        else:
            components = tuple(create_component(component_data) for component_data in component_datas)
        self.components = components
        
        sticker_datas = data.get('stickers', None)
        if sticker_datas is None:
            stickers = None
        else:
            stickers = tuple(Sticker(sticker_data) for sticker_data in sticker_datas)
        self.stickers = stickers
        
        user_mention_datas = data.get('mentions', None)
        if (user_mention_datas is not None) and user_mention_datas:
            user_mentions = tuple(sorted(
                (User(user_mention_data, guild) for user_mention_data in user_mention_datas),
                key=id_sort_key,
            ))
        else:
            user_mentions = None
        self.user_mentions = user_mentions
        
        if guild is None:
            channel_mentions = None
        else:
            channel_mentions = ...
        
        self._channel_mentions = channel_mentions
        
        if guild is None:
            role_mentions = None
        else:
            role_mention_ids = data.get('mention_roles', None)
            if (role_mention_ids is None) or (not role_mention_ids):
                role_mentions = None
            else:
                roles = guild.roles
                role_mentions = []
                
                for role_id in role_mention_ids:
                    role_id = int(role_id)
                    try:
                        role = roles[role_id]
                    except KeyError:
                        continue
                    
                    role_mentions.append(role)
                
                role_mentions.sort(key=id_sort_key)
                role_mentions = tuple(role_mentions)
        
        self.role_mentions = role_mentions
        
        
        try:
            application_id = data['application_id']
        except KeyError:
            application_id = 0
        else:
            application_id = int(application_id)
        
        self.application_id = application_id
        
        try:
            thread_data = data['thread']
        except KeyError:
            thread = None
        else:
            thread = CHANNEL_TYPES.get(thread_data['type'], ChannelGuildUndefined)(thread_data, None, guild)
        self.thread = thread
        
        MESSAGES[self.id] = self
    
    
    def _late_init(self, data):
        """
        Some message fields might be missing after receiving a payload. This method is called to check and set those
        if multiple payload is received.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        """
        if not self.content:
            try:
                content = data['content']
            except KeyError:
                pass
            else:
                self.content = content
        
        if (self.interaction is None):
            interaction_data = data.get('interaction', None)
            if (interaction_data is not None):
                interaction = MessageInteraction(interaction_data)
                try_resolve_interaction_message(self, interaction)
                self.interaction = interaction
        
        if (self.components is None):
            component_datas = data.get('components', None)
            if (component_datas is not None) and component_datas:
                self.components = tuple(create_component(component_data) for component_data in component_datas)
        
        if (self.embeds is None):
            embed_datas = data.get('embeds', None)
            if (embed_datas is not None) and embed_datas:
                self.embeds = tuple(EmbedCore.from_data(embed) for embed in embed_datas)
    
    
    @BaseMethodDescriptor
    def custom(cls, base, validate=True, **kwargs):
        """
        Creates a custom message. If called as a method of a message, then the attributes of the created custom message
        will default to that message's. Meanwhile if called as a classmethod, then the attributes of the created
        custom message will default to the overall defaults.
        
        Parameters
        ----------
        validate : `bool`, Optional
            Whether contradictory between the message's attributes should be checked. If there is any, `ValueError`
            is raised. Defaults to `True`.
        **kwargs : keyword arguments
            Additional attributes of the created message.
        
        Other Parameters
        ----------------
        activity : `None` or ``MessageActivity``, Optional (Keyword only)
            The ``.activity`` attribute the message.
            
            If called as classmethod defaults to `None`.
        application : `None` or ``MessageApplication``., Optional (Keyword only)
            The ``.application`` attribute the message.
            
            If called as a classmethod defaults to `None`.
        application_id : `int`, Optional (Keyword Only)
            The ``.application_id`` attribute of the message.
            
            If called as a classmethod defaults to `0`.
        attachments : `None` or ((`list`, `tuple`) of ``Attachment``), Optional (Keyword only)
            The ``.attachments`` attribute of the message. If passed as an empty list, then will be as `None` instead.
            
            If called as a classmethod defaults to `None`.
        author : `None`, ``ClientUserBase``, ``Webhook`` or ``WebhookRepr``, Optional (Keyword only)
            The ``.author`` attribute of the message. If passed as `None` then it will be set as `ZEROUSER` instead.
            
            If called as a classmethod, defaults to `ZEROUSER`.
        channel : `ChannelTextBase` instance, Optional if called as method (Keyword only)
            The ``.channel`` attribute of the message.
            
            If called as a classmethod this attribute must be passed, or `TypeError` is raised.
        
        components : `None` or (`list` or `tuple`) of ``ComponentBase``, Optional (Keyword only)
            The ``.components`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        
        content : `str`, Optional (Keyword only)
            The ``.content`` attribute of the message. Can be between length `0` and `4000`.
            
            If called as a classmethod defaults to `''` (empty string).
        
        cross_mentions : `None` or (`tuple`, `list`) of (``UnknownCrossMention`` or ``ChannelGuildBase`` instances)
                , Optional (Keyword only)
            The `.cross_mentions` attribute of the message. If passed as an empty list, then will be set `None` instead.
            
            If called as a classmethod defaults to `None`.
        referenced_message : `None`, ``Message`` ``MessageReference``, Optional (Keyword only)
            The ``.referenced_message`` attribute of the message.
            
            If called as a classmethod defaults to `None`.
        deleted : `bool`, Optional (Keyword only)
            The ``.deleted`` attribute of the message. If called as a class method, defaults to `True`.
        
        edited_at : `None` or `datetime`, Optional (Keyword only)
            The ``.edited_at`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        embeds : `None` or (`list` or `tuple`) of ``EmbedBase``, Optional (Keyword only)
            The ``.embeds`` attribute of the message. If passed as an empty list, then is set as `None` instead. If
            passed as list and it contains any embeds, which are not type ``EmbedCore``, then those will be converted
            to ``EmbedCore`` as well.
            
            If called as a classmethod defaults to `None`.
        everyone_mention : `bool` or `int` instance (`0` or `1`), Optional (Keyword only)
            The ``.everyone_mention`` attribute of the message. Accepts other `int` instance as `bool` as well, but
            their value still cannot be other than `0` or `1`.
            
            If called as a classmethod, defaults to `False`.
        flags : ``MessageFlag`` or `int`, Optional (Keyword only)
            The ``.flags`` attribute of the message. If passed as other `int` instances than ``MessageFlag``, then will
            be converted to ``MessageFlag``.
            
            If called as a classmethod defaults to `MessageFlag(0)`.
        
        interaction : `None` or ``MessageInteraction``, Optional (Keyword only)
           The `.interaction` attribute of the message.
        
            If called as a classmethod defaults to `None`.
        
        id : `int` or `str`, Optional (Keyword only)
            The ``.id`` attribute of the message. If passed as `str`, will be converted to `int`.
            
            If called as a classmethod defaults to `0`.
        id_ : `int` or `str`, Optional (Keyword only)
            Alias of `id`.
        message_id : `int` or `str`, Optional (Keyword only)
            Alias of `id`.
        nonce : `None` or `str`, Optional (Keyword only)
            The ``.nonce`` attribute of the message. If passed as `str` can be between length `0` and `32`.
            
            If called as a classmethod defaults to `None`.
        pinned : `bool` or `int` instance (`0` or `1`), Optional (Keyword only)
            The ``.pinned`` attribute of the message. Accepts other `int` instances as `bool` as well, but their value
            still cannot be other than `0` or `1`.
            
            If called as a classmethod, defaults to `False`.
        reactions : `None` or ``reaction_mapping``, Optional (Keyword only)
            The ``.reactions`` attribute of the message. If passed as `None` will be set as an empty
            ``reaction_mapping``.
            
            If called as a classmethod defaults to empty ``reaction_mapping``.
        role_mentions : `None` or (`list` or `tuple`) of ``Role``, Optional (Keyword only)
            The ``.role_mentions`` attribute of the message. If passed as an empty `list`, will be set as `None`
            instead.
            
            If called as a classmethod defaults to `None`.
        stickers : `None` or (`list`, `tuple`) of ``Sticker``, Optional (Keyword only)
            The ``.stickers`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        
        thread : `None` or ``ChannelThread``
            The ``.thread`` attribute of the message.
            
            If called as a classmethod defaults to `None`.
        
        tts : `bool` or `int` instance (`0` or `1`), Optional (Keyword only)
            The ``.tts`` attribute of the message. Accepts other `int` instances as `bool` as well, but their value
            still cannot be other than `0` or `1`.
            
            If called as a classmethod, defaults to `False`.
        type : ``MessageType`` or `int`, Optional (Keyword only)
            The ``.type`` attribute of the message. If passed as `int`, it will be converted to it's wrapper side
            ``MessageType`` representation.
            
            If called as a classmethod defaults to ``MessageType.default`
        type_ : ``MessageType`` or `int`, Optional (Keyword only)
            Alias of ``type`.
        user_mentions : `None` or `list`, `tuple`  of ``UserBase``, Optional (Keyword only)
            The ``.user_mentions`` attribute of the message. If passed as an empty list will be set as `None` instead.
            
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
            channel = kwargs.pop('channel')
        except KeyError:
            if base is None:
                raise TypeError('Expected to be called as method, but was called as a classmethod and `channel` was '
                    f'not passed.')
            channel = base.channel
        else:
            if not isinstance(channel, ChannelTextBase):
                raise TypeError(f'`channel` should be `{ChannelTextBase.__name__}` subclass\'s instance, got '
                    f'`{channel!r}`')
        
        # `_channel_mentions` is internal, we wont check kwargs
        if isinstance(channel, ChannelGuildBase):
            _channel_mentions = None
        else:
            _channel_mentions = ...
        
        try:
            activity = kwargs.pop('activity')
        except KeyError:
            if base is None:
                activity = None
            else:
                activity = base.activity
        else:
            if (activity is not None) and (type(activity) is not MessageActivity):
                raise TypeError(f'`activity` should be `None` or type `{MessageActivity.__name__}`, got `{activity!r}`')
        
        try:
            application = kwargs.pop('application')
        except KeyError:
            if base is None:
                application = None
            else:
                application = base.application
        else:
            if (application is not None) and (type(application) is not MessageApplication):
                raise TypeError(f'`application` should be `None` or type `{MessageApplication.__name__}`, got '
                    f'`{application!r}`')
        
        
        try:
            application_id = kwargs.pop('application_id')
        except KeyError:
            if base is None:
                application_id = 0
            else:
                application_id = base.application_id
        else:
            application_id = preconvert_snowflake(application_id, 'application_id')
        
        
        try:
            attachments = kwargs.pop('attachments')
        except KeyError:
            if base is None:
                attachments = None
            else:
                attachments = base.attachments
                if (attachments is not None):
                    # Copy it, because it might change
                    attachments = attachments
        else:
            if (attachments is not None):
                if not isinstance(attachments, (list, tuple)):
                    raise TypeError(f'`attachments` should be `None` or `tuple`, `list` of `{Attachment.__name__}` '
                        f'instances, got `{attachments!r}`')
                
                attachments = tuple(attachments)
                
                attachments_length = len(attachments)
                
                if validate:
                    if attachments_length > 10:
                        raise ValueError(f'`attachments` should have maximal length of `10`, got `{attachments_length!r}`')
                
                if attachments_length:
                    for attachment in attachments:
                        if not isinstance(attachment, Attachment):
                            raise TypeError(f'`attachments` `list` contains a non `{Attachment.__name__}` '
                                f'instance, `{attachment!r}`')
                else:
                    # We should not have empty attachment list, lets fix it
                    attachments = None
        
        try:
            author = kwargs.pop('author')
        except KeyError:
            if base is None:
                author = ZEROUSER
            else:
                author = base.author
        else:
            if author is None:
                # Author cannot be None, but accept it as `ZEROUSER`
                author = ZEROUSER
            elif isinstance(author, (ClientUserBase, Webhook, WebhookRepr)):
                # This should be the case
                pass
            else:
                raise TypeError(
                    f'`author` can be type `None`, `{ClientUserBase.__name__}`, `{Webhook.__name__}` or '
                    f'`{WebhookRepr.__name__}`, got `{author!r}`')
        
        try:
            content = kwargs.pop('content')
        except KeyError:
            if base is None:
                content = ''
            else:
                content = base.content
        else:
            content = preconvert_str(content, 'content', 0, 4000)
        
        try:
            referenced_message = kwargs.pop('referenced_message')
        except KeyError:
            if base is None:
                referenced_message = None
            else:
                referenced_message = base.referenced_message
        else:
            if (referenced_message is not None) and (type(referenced_message) not in (Message, MessageReference)):
                    raise TypeError(f'`referenced_message` should be `None` or type `{Message.__name__}`, '
                        f'`{MessageReference.__call__}`, got `{referenced_message!r}`')
        
        try:
            cross_mentions = kwargs.pop('cross_mentions')
        except KeyError:
            if base is None:
                cross_mentions = None
            else:
                cross_mentions = base.cross_mentions
                if (cross_mentions is not None):
                    # Copy it, it might change
                    cross_mentions = tuple(cross_mentions)
        else:
            if (cross_mentions is not None):
                if not isinstance(cross_mentions, (tuple, list)):
                    raise TypeError(f'`cross_mentions` should be `None` or `tuple`, `list` of '
                        f'`{ChannelGuildBase.__name__}` or `{UnknownCrossMention.__name__}` instances, got '
                        f'`{cross_mentions.__class__.__name__}`.')
                
                for channel_ in cross_mentions:
                    if not isinstance(channel_, (ChannelGuildBase, UnknownCrossMention)):
                        raise TypeError(f'`cross_mentions` contains a non `{ChannelGuildBase.__name__}` or '
                            f'`{UnknownCrossMention.__name__}` instance: `{channel_.__class__.__name__}`.')
                
                cross_mentions = tuple(sorted(cross_mentions, key=id_sort_key))
        
        if validate:
            if (referenced_message is None) and (cross_mentions is not None):
                raise ValueError('`cross_mentions` are supported, only if `referenced_message` is provided')
        
        try:
            deleted = kwargs.pop('deleted')
        except KeyError:
            if base is None:
                deleted = True
            else:
                deleted = base.deleted
        else:
            deleted = preconvert_bool(deleted, 'deleted')
        
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
            edited_at = kwargs.pop('edited_at')
        except KeyError:
            if base is None:
                edited_at = None
            else:
                edited_at = base.edited_at
        else:
            if (edited_at is not None) and (type(edited_at) is not datetime):
                raise TypeError(f'`edited_at` can be `None` or `datetime`, got `{edited_at.__class__.__name__}`.')
        
        if validate:
            if (edited_at is not None) and (time_to_id(edited_at)<message_id):
                raise ValueError('`edited_at` can not be lower, than `created_at`')
        
        try:
            embeds = kwargs.pop('embeds')
        except KeyError:
            if base is None:
                embeds = None
            else:
                embeds = base.embeds
        else:
            if (embeds is not None):
                if not isinstance(embeds, (list, tuple)):
                    raise TypeError(f'`embeds` can be `None` or `list` of type `{EmbedCore.__name__}`, got '
                        f'`{embeds.__class__.__name__}`.')
                
                embeds = list(embeds)
                
                embeds_length = len(embeds)
                if validate:
                    if len(embeds) > 10:
                        raise ValueError(f'`embeds` can have maximal length of `10`, got `{embeds_length!r}`.')
                
                if embeds_length:
                    for index in range(embeds_length):
                        embed = embeds[index]
                        
                        if isinstance(embed, EmbedCore):
                            continue
                            
                        if isinstance(embed, EmbedBase):
                            # Embed compatible, lets convert it
                            embed = EmbedCore.from_data(embed.to_data())
                            embeds[index] = embed
                            continue
                        
                        raise TypeError(f'`embeds` `list` contains a non `{EmbedBase.__name__}` instance: '
                            f'`{embeds.__class__.__name__}`.')
                    
                    embeds = tuple(embeds)
                else:
                    # embeds cannot be an empty list, lets fix it
                    embeds = None
        
        try:
            everyone_mention = kwargs.pop('everyone_mention')
        except KeyError:
            if base is None:
                everyone_mention = False
            else:
                everyone_mention = base.everyone_mention
        else:
            everyone_mention = preconvert_bool(everyone_mention, 'everyone_mention')
        
        try:
            flags = kwargs.pop('flags')
        except KeyError:
            if base is None:
                flags = MessageFlag(0)
            else:
                flags = base.flags
        else:
            if flags is None:
                # Accept None, and then convert it.
                flags = MessageFlag()
            else:
                flags = preconvert_flag(flags, 'flags', MessageFlag)
        
        if validate:
            if isinstance(channel, ChannelText):
                if flags.source_message_deleted and (not flags.is_crosspost):
                    raise ValueError(
                        '`flags.source_message_deleted` is set, but `flags.is_crosspost` is not -> Only crossposted '
                        'message\'s source can be deleted')
                
                # Other cases?
            else:
                if flags.crossposted:
                    raise ValueError('`flags.crossposted` is set, meanwhile `channel` is not type '
                        f'`{ChannelText.__name__}`; `{channel!r}`')
    
                if flags.is_crosspost:
                    raise ValueError('`flags.is_crosspost` is set, meanwhile `channel` is not type '
                        f'`{ChannelText.__name__}`; `{channel!r}`')
    
                if flags.source_message_deleted:
                    raise ValueError('`flags.source_message_deleted` is set, meanwhile `channel` is not type '
                        f'`{ChannelText.__name__}`; `{channel!r}`')
        
        try:
            nonce = kwargs.pop('nonce')
        except KeyError:
            if base is None:
                nonce = None
            else:
                nonce = base.nonce
        else:
            if (nonce is not None):
                if type(nonce) is str:
                    pass
                elif isinstance(nonce, str):
                    nonce = str(nonce)
                else:
                    raise TypeError(f'`nonce` should be `None` or type `str` instance, got `{nonce!r}`.')
                
                nonce_length = len(nonce)
                if nonce_length > 32:
                    raise TypeError(f'`nonce`\'s length can be be in range [1:32], got: `{nonce_length!r}`; '
                        f'`{nonce!r}`.')
                elif nonce_length == 0:
                    nonce = None
        
        try:
            pinned = kwargs.pop('pinned')
        except KeyError:
            if base is None:
                pinned = False
            else:
                pinned = base.pinned
        else:
            pinned = preconvert_bool(pinned, 'pinned')
        
        try:
            reactions = kwargs.pop('reactions')
        except KeyError:
            if base is None:
                reactions = reaction_mapping(None)
            else:
                # Copy it, because it might be modified
                reactions = base.reactions.copy()
        else:
            if reactions is None:
                # Lets accept `None` and create an empty one
                reactions = reaction_mapping(None)
            elif type(reactions) is reaction_mapping:
                # We expect this as default
                pass
            else:
                raise TypeError(f'`reactions`, should be type `{reaction_mapping.__name__}`, got `{reactions}`')
        
        try:
            role_mentions = kwargs.pop('role_mentions')
        except KeyError:
            if base is None:
                role_mentions = None
            else:
                role_mentions = base.role_mentions
                if (role_mentions is not None):
                    # Copy it, because it might change
                    role_mentions = tuple(role_mentions)
        else:
            if (role_mentions is not None):
                if not isinstance(role_mentions, (tuple, list)):
                    raise TypeError(f'`role_mentions` should be `None` or `list`, `tuple` of `{Role.__name__}` '
                        f'instances, got `{role_mentions.__class__.__name__}`.')
                
                if role_mentions:
                    for role in role_mentions:
                        if not isinstance(role, Role):
                            raise TypeError(f'`role_mentions` contains a non `{Role.__name__}` instance, '
                                f'`{role.__class__.__name__}`.')
                    
                    role_mentions = tuple(sorted(role_mentions, key=id_sort_key))
                else:
                    # There cannot be an empty mention list, so lets fix it.
                    role_mentions = None
        
        if validate:
            if (role_mentions is not None) and (not isinstance(channel,ChannelGuildBase)):
                raise ValueError('`role_mentions` are set as not `None`, meanwhile the `channel` is not '
                    f'`{ChannelGuildBase}` subclass\'s instance; `{channel!r}`')
        
        try:
            stickers = kwargs.pop('stickers')
        except KeyError:
            if base is None:
                stickers = None
            else:
                stickers = base.stickers
                if (stickers is not None):
                    stickers = tuple(stickers)
        else:
            if not isinstance(stickers, (list, tuple)):
                raise TypeError(f'`stickers` should be `None` or ` tuple`, `list` of `{Sticker.__name__}` instances, '
                    f'got `{stickers!r}`')
            
            stickers = tuple(stickers)
            
            stickers_length = len(stickers)
            if stickers_length:
                for sticker in stickers:
                    if not isinstance(sticker, Sticker):
                        raise TypeError(f'`stickers` contains a non `{Sticker.__name__}` instance, '
                            f'`{sticker!r}`')
            else:
                # We should not have empty attachment list, lets fix it
                stickers = None
        
        try:
            tts = kwargs.pop('tts')
        except KeyError:
            if base is None:
                tts = False
            else:
                tts = base.tts
        else:
            tts = preconvert_bool(tts, 'tts')
        
        for name in ('type_', 'type'):
            try:
                type_ = kwargs.pop(name)
            except KeyError:
                continue
            
            type_found = True
            break
        else:
            type_found = False
        
        if type_found:
            type_ = preconvert_preinstanced_type(type_, 'type_', MessageType)
        else:
            if base is None:
                type_ = MessageType.default
            else:
                type_ = base.type
        
        try:
            user_mentions = kwargs.pop('user_mentions')
        except KeyError:
            if base is None:
                user_mentions = None
            else:
                user_mentions = base.user_mentions
                if (user_mentions is not None):
                    # Copy it, because it might change
                    user_mentions = tuple(user_mentions)
        else:
            if (user_mentions is not None):
                if not isinstance(user_mentions, (tuple, list)):
                    raise TypeError(f'`user_mentions` should be `None` or `tuple`, `list` of `{UserBase.__name__}` '
                        f'instances, got `{user_mentions.__class__.__name__}`.')
                
                if user_mentions:
                    for user in user_mentions:
                        if not isinstance(user, UserBase):
                            raise TypeError(f'`user_mentions` contains at least 1 non `{UserBase.__name__}` '
                                f'instance; `{user.__class__.__name__}`.')
                    
                    user_mentions = tuple(sorted(user_mentions, key=id_sort_key))
                    
                else:
                    user_mentions = None
        
        try:
            interaction = kwargs.pop('interaction')
        except KeyError:
            if base is None:
                interaction = None
            else:
                interaction = base.interaction
        else:
            if (interaction is not None) and (not isinstance(interaction, MessageInteraction)):
                raise TypeError(f'`interaction` can be given as `None` or as `{MessageInteraction.__name__}` '
                    f'instance, got {interaction.__class__.__name__}.')
        
        try:
            components = kwargs.pop('components')
        except KeyError:
            if base is None:
                components = None
            else:
                components = base.components
                if (components is not None):
                    components = tuple(components)
        else:
            if (components is not None):
                if not isinstance(components, (list, tuple)):
                    raise TypeError(f'`components` should be `None` or `tuple`, `list` of `{ComponentBase.__name__}` '
                        f'instances, got `{components.__class__.__name__}`.')
                
                if components:
                    for component in components:
                        if not isinstance(component, ComponentBase):
                            raise TypeError(f'`components` contains at least 1 non `{ComponentBase.__name__}` '
                                f'instance; `{component.__class__.__name__}`.')
                    
                    components = tuple(components)
                else:
                    components = None
        
        try:
            thread = kwargs.pop('thread')
        except KeyError:
            if base is None:
                thread = None
            else:
                thread = base.thread
        else:
            if (thread is not None) and (not isinstance(thread, ChannelThread)):
                raise TypeError(f'`thread` can be given as `None` or as `{ChannelThread.__name__}` '
                    f'instance, got {thread.__class__.__name__}.')
        
        # Check kwargs and raise TypeError if not every in used up
        if kwargs:
            raise TypeError(f'Unused parameters: {", ".join(list(kwargs))}')
        
        self = object.__new__(cls)
        
        self._channel_mentions = _channel_mentions
        self.activity = activity
        self.application = application
        self.application_id = application_id
        self.attachments = attachments
        self.author = author
        self.channel = channel
        self.content = content
        self.cross_mentions = cross_mentions
        self.referenced_message = referenced_message
        self.deleted = deleted
        self.edited_at = edited_at
        self.embeds = embeds
        self.everyone_mention = everyone_mention
        self.flags = flags
        self.id = message_id
        self.nonce = nonce
        self.pinned = pinned
        self.reactions = reactions
        self.role_mentions = role_mentions
        self.stickers = stickers
        self.tts = tts
        self.type = type_
        self.user_mentions = user_mentions
        self.interaction = interaction
        self.components = components
        self.thread = thread
        
        return self
    
    def _parse_channel_mentions(self):
        """
        Looks up the ``.contents`` of the message and searches channel mentions in them. If non, then sets
        ``.channel_mentions`` as `None`, else as a `list` of ``ChannelBase`` (and ``UnknownCrossMention``) instances.
        
        Invalid channel mentions are ignored.
        
        Returns
        -------
        channel_mentions : `None` or `tuple` of (``GuildChannelBase``, ``UnknownCrossMention``) instances.
            The parsed channel mentions.
        """
        content = self.content
        channel_mentions = []
        channels = self.channel.guild.channels
        cross_mentions = self.cross_mentions

        for channel_id in CHANNEL_MENTION_RP.findall(content):
            channel_id = int(channel_id)
            try:
                channel = channels[channel_id]
            except KeyError:
                if cross_mentions is None:
                    continue
                try:
                    channel = cross_mentions[channel_id]
                except KeyError:
                    continue
            
            if channel not in channel_mentions:
                channel_mentions.append(channel)
        
        if channel_mentions:
            channel_mentions.sort(key=id_sort_key)
            channel_mentions = tuple(channel_mentions)
        else:
            channel_mentions = None
        
        self._channel_mentions = channel_mentions
        return channel_mentions
    
    url = property(module_urls.message_jump_url)
    
    @property
    def channel_mentions(self):
        """
        The mentioned channels by the message. If there is non, returns `None`.
        
        Returns
        -------
        channel_mentions : `None` or (`list` of (``ChannelBase`` or ``UnknownCrossMentions`` instances))
        """
        channel_mentions = self._channel_mentions
        if channel_mentions is ...:
            channel_mentions = self._parse_channel_mentions()
        
        return channel_mentions
    
    def __repr__(self):
        """Returns the representation of the message."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        if self.deleted:
            repr_parts.append(' deleted')
        
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        repr_parts.append(', length=')
        repr_parts.append(repr(len(self)))
        repr_parts.append(', author=')
        repr_parts.append(repr(self.author.full_name))
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    __str__ = __repr__
    
    def __format__(self, code):
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
        ```py
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
        >>>> message = message.custom(edited_at=datetime.now())
        >>>> message
        <Message id=0, ln=12, author=#0000>
        >>>> f'{message:e}'
        '2020.05.31-16:00:00'
        ```
        """
        if not code:
            return self.__str__()
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        if code == 'e':
            edited_at = self.edited_at
            if edited_at is None:
                edited_at = 'never'
            else:
                edited_at = self.edited_at.__format__(DATETIME_FORMAT_CODE)
            return edited_at
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    def _update(self, data):
        """
        Updates the message and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.

        A special case is if a message is (un)pinned or (un)suppressed , because then the returned dict is not going to
        contain `'edited_at'`, only `'pinned'` or `'flags'`. If the embeds are (un)suppressed of the message, then the
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
        | attachments       | `None` or (`tuple` of ``Attachment``)                                 |
        +-------------------+-----------------------------------------------------------------------+
        | components        | `None` or (`tuple` of ``ComponentBase``)                              |
        +-------------------+-----------------------------------------------------------------------+
        | content           | `str                                                                  |
        +-------------------+-----------------------------------------------------------------------+
        | cross_mentions    | `None` or (`tuple` of (``ChannelBase`` or ``UnknownCrossMention``))   |
        +-------------------+-----------------------------------------------------------------------+
        | edited_at         | `None`  or `datetime`                                                 |
        +-------------------+-----------------------------------------------------------------------+
        | embeds            | `None`  or `(tuple` of ``EmbedCore``)                                 |
        +-------------------+-----------------------------------------------------------------------+
        | flags             | `UserFlag`                                                            |
        +-------------------+-----------------------------------------------------------------------+
        | mention_everyone  | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | pinned            | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | user_mentions     | `None` or (`tuple` of ``ClientUserBase``)                             |
        +-------------------+-----------------------------------------------------------------------+
        | role_mentions     | `None` or (`tuple` of ``Role``)                                       |
        +-------------------+-----------------------------------------------------------------------+
        """
        old_attributes = {}
        
        try:
            pinned = data['pinned']
        except KeyError:
            pass
        else:
            if self.pinned != pinned:
                old_attributes['pinned'] = self.pinned
                self.pinned = pinned
        
        flags = data.get('flags', 0)
        flag_difference = self.flags^flags
        if flag_difference:
            old_attributes['flags'] = self.flags
            self.flags = MessageFlag(flags)
            
            if MessageFlag(flag_difference).embeds_suppressed:
                try:
                    embed_datas = data['embeds']
                except KeyError:
                    pass
                else:
                    if embed_datas:
                        embeds = tuple(EmbedCore.from_data(embed) for embed in embed_datas)
                    else:
                        embeds = None
                    
                    if self.embeds != embeds:
                        old_attributes['embeds'] = self.embeds
                        self.embeds = embeds
        
        # at the case of pin update edited is None
        try:
            edited_timestamp = data['edited_timestamp']
        except KeyError:
            pass
        else:
            if edited_timestamp is None:
                return old_attributes
            
            edited_at = parse_time(edited_timestamp)
        
            if self.edited_at == edited_at:
                return old_attributes
            
            old_attributes['edited_at'] = self.edited_at
            self.edited_at = edited_at
        
        try:
            application_data = data['application']
        except KeyError:
            application = None
        else:
            application = MessageApplication(application_data)
        
        if self.application != application:
            old_attributes['application'] = self.application
            self.application = self.application
        
        try:
            activity_data = data['activity']
        except KeyError:
            activity = None
        else:
            activity = MessageActivity(activity_data)
        
        if self.activity != activity:
            old_attributes['activity'] = self.activity
            self.activity = activity
        
        everyone_mention = data.get('mention_everyone', False)
        if self.everyone_mention != everyone_mention:
            old_attributes['everyone_mention'] = self.everyone_mention
            self.everyone_mention = everyone_mention
        
        # ignoring tts
        # ignoring type
        # ignoring nonce
        
        try:
            attachment_datas = data['attachments']
        except KeyError:
            pass
        else:
            if attachment_datas:
                attachments = tuple(Attachment(attachment) for attachment in attachment_datas)
            else:
                attachments = None
            
            if self.attachments != attachments:
                old_attributes['attachments'] = self.attachments
                self.attachments = attachments
        
        try:
            embed_datas = data['embeds']
        except KeyError:
            pass
        else:
            if embed_datas:
                embeds = tuple(EmbedCore.from_data(embed) for embed in embed_datas)
            else:
                embeds = None
            
            if self.embeds != embeds:
                old_attributes['embeds'] = self.embeds
                self.embeds = embeds
        
        try:
            content = data['content']
        except KeyError:
            pass
        else:
            if self.content != content:
                old_attributes['content'] = self.content
                self.content = content
        
        try:
            user_mention_datas = data['mentions']
        except KeyError:
            pass
        else:
            guild = self.channel.guild
            
            if (user_mention_datas is None) or (not user_mention_datas):
                user_mentions = None
            else:
                user_mentions = tuple(sorted(
                    (User(user_mention_data, guild) for user_mention_data in user_mention_datas),
                    key=id_sort_key,
                ))
            
            if self.user_mentions != user_mentions:
                old_attributes['user_mentions'] = self.user_mentions
                self.user_mentions = user_mentions
        
        try:
            component_datas = data['components']
        except KeyError:
            pass
        else:
            if (component_datas is None) or (not component_datas):
                components = None
            else:
                components = tuple(create_component(component_data) for component_data in component_datas)
            
            if self.components != components:
                old_attributes['components'] = self.components
                self.components = components
        
        
        if guild is None:
            return old_attributes
        
        self._channel_mentions = ...
        
        try:
            cross_mention_datas = data['mention_channels']
        except KeyError:
            pass
        else:
            if (cross_mention_datas is None) or (not cross_mention_datas):
                cross_mentions = None
            else:
                cross_mentions = tuple(sorted(
                    (UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas),
                    key=id_sort_key,
                ))
            
            if self.cross_mentions != cross_mentions:
                old_attributes['cross_mentions'] = self.cross_mentions
                self.cross_mentions = cross_mentions
        
        try:
            role_mention_ids = data['mention_roles']
        except KeyError:
            pass
        else:
            if (role_mention_ids is None) or (not role_mention_ids):
                role_mentions = None
            else:
                roles = guild.roles
                role_mentions = []
                
                for role_id in role_mention_ids:
                    role_id = int(role_id)
                    try:
                        role = roles[role_id]
                    except KeyError:
                        continue
                    
                    role_mentions.append(role)
                
                role_mentions.sort(key=id_sort_key)
                role_mentions = tuple(role_mentions)
            
            if self.role_mentions != role_mentions:
                old_attributes['role_mentions'] = self.role_mentions
                self.role_mentions = role_mentions
        
        return old_attributes
    
    def _update_no_return(self, data):
        """
        Updates the message with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        """
        try:
            pinned = data['pinned']
        except KeyError:
            pass
        else:
            self.pinned = pinned
        
        flags = data.get('flags', 0)
        flag_difference = self.flags^flags
        if flag_difference:
            self.flags = MessageFlag(flags)
            
            if MessageFlag(flag_difference).embeds_suppressed:
                try:
                    embed_datas = data['embeds']
                except KeyError:
                    pass
                else:
                    if embed_datas:
                        embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
                    else:
                        embeds = None
                    self.embeds = embeds
        
        try:
            edited_timestamp = data['edited_timestamp']
        except KeyError:
            pass
        else:
            if edited_timestamp is None:
                return
            
            edited_at = parse_time(edited_timestamp)
            if self.edited_at == edited_at:
                return
            
            self.edited_at = edited_at

        try:
            application_data = data['application']
        except KeyError:
            application = None
        else:
            application = MessageApplication(application_data)
        self.application = application
        
        try:
            activity_data = data['activity']
        except KeyError:
            activity = None
        else:
            activity = MessageActivity(activity_data)
        self.activity = activity
        
        self.everyone_mention = data['mention_everyone']

        #ignoring tts
        #ignoring type
        #ignoring nonce
        
        try:
            attachment_datas = data['attachments']
        except KeyError:
            pass
        else:
            if attachment_datas:
                attachments = tuple(Attachment(attachment) for attachment in attachment_datas)
            else:
                attachments = None
            self.attachments = attachments
        
        try:
            embed_datas = data['embeds']
        except KeyError:
            pass
        else:
            if embed_datas:
                embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
            else:
                embeds = None
            self.embeds = embeds
        
        try:
            content = data['content']
        except KeyError:
            pass
        else:
            self.content = content
        
        try:
            component_datas = data['components']
        except KeyError:
            pass
        else:
            if (component_datas is None) or (not component_datas):
                components = None
            else:
                components = tuple(create_component(component_data) for component_data in component_datas)
            self.components = components
        
        guild = self.channel.guild
        
        try:
            user_mention_datas = data['mentions']
        except KeyError:
            pass
        else:
            if user_mention_datas:
                user_mentions = tuple(sorted(
                    (User(user_mention_data, guild) for user_mention_data in user_mention_datas),
                    key=id_sort_key,
                ))
            else:
                user_mentions = None
            
            self.user_mentions = user_mentions
        
        if guild is None:
            return
        
        self._channel_mentions = ...
        
        try:
            cross_mention_datas = data['mention_channels']
        except KeyError:
            pass
        else:
            if (cross_mention_datas is None) or (not cross_mention_datas):
                cross_mentions = None
            else:
                cross_mentions = tuple(sorted(
                    (UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas),
                    key=id_sort_key,
                ))
            
            self.cross_mentions = cross_mentions
        
        try:
            role_mention_ids = data['mention_roles']
        except KeyError:
            pass
        else:
            if (role_mention_ids is None) or (not role_mention_ids):
                role_mentions = None
            else:
                roles = guild.roles
                role_mentions = []
                
                for role_id in role_mention_ids:
                    role_id = int(role_id)
                    try:
                        role = roles[role_id]
                    except KeyError:
                        continue
                    
                    role_mentions.append(role)
                
                role_mentions.sort(key=id_sort_key)
                role_mentions = tuple(role_mentions)
            
            self.role_mentions = role_mentions
    
    
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
        # 2 -> New embeds appeared -> link.
        # 3 -> There are less embed -> bug?
        
        embeds = self.embeds
        if embeds is None:
            embeds_length_actual = 0
        else:
            embeds_length_actual = len(embeds)
        
        embed_datas = data.get('embeds', None)
        if embed_datas is None:
            embeds_length_new = 0
        else:
            embeds_length_new = len(embed_datas)
        
        if embeds_length_actual == 0:
            if embeds_length_new == 0:
                # No change
                return EMBED_UPDATE_NONE
            
            # New embeds are added
            self.embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
            return EMBED_UPDATE_EMBED_ADD
        
        if embeds_length_new < embeds_length_actual:
            # Embeds are removed, should not happen, except if the message was suppressed.
            if self.flags.embeds_suppressed:
                self.embeds = None
                # Embeds are suppressed, message_edit was already called. Return 0.
                return EMBED_UPDATE_NONE
            
            # We have less embeds as we had, should not happen. Return 3.
            if embeds_length_new == 0:
                embeds = None
            else:
                embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
            self.embeds = embeds
            return EMBED_UPDATE_EMBED_REMOVE
        
        if embeds_length_actual != 0:
            change_state = EMBED_UPDATE_NONE
            for index in range(embeds_length_actual):
                embed_data = embed_datas[index]
                if embeds[index]._update_sizes(embed_data):
                    change_state = EMBED_UPDATE_SIZE_UPDATE
            
            if embeds_length_actual == embeds_length_new:
                return change_state
        
        if embeds is None:
            embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
        else:
            embeds = (
                *embeds,
                *(EmbedCore.from_data(embed_datas[index]) for index in range(embeds_length_actual, embeds_length_new)),
            )
        
        self.embeds = embeds
        
        return EMBED_UPDATE_EMBED_ADD


    def _update_embed_no_return(self, data):
        """
        Updates the message's embeds.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        """
        embeds = self.embeds
        if embeds is None:
            embeds_length_actual = 0
        else:
            embeds_length_actual = len(embeds)
        
        embed_datas = data.get('embeds', None)
        if embed_datas is None:
            embeds_length_new = 0
        else:
            embeds_length_new = len(embed_datas)
        
        if embeds_length_actual == 0:
            if embeds_length_new == 0:
                # No change
                return
            
            # New embeds are added
            self.embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
            return
        
        if embeds_length_new < embeds_length_actual:
            # Embeds are removed, should not happen, except if the message was suppressed.
            if self.flags.embeds_suppressed:
                self.embeds = None
                # Embeds are suppressed, message_edit was already called.
                return
            
            # We have less embeds as we had, should not happen.
            if embeds_length_new == 0:
                embeds = None
            else:
                embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
            self.embeds = embeds
            return
        
        if embeds_length_actual != 0:
            for index in range(embeds_length_actual):
                embed_data = embed_datas[index]
                embeds[index]._update_sizes_no_return(embed_data)

            if embeds_length_actual == embeds_length_new:
                return
        
        if embeds is None:
            embeds = tuple(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
        else:
            embeds = (
                *embeds,
                *(EmbedCore.from_data(embed_datas[index]) for index in range(embeds_length_actual, embeds_length_new)),
            )
        
        self.embeds = embeds
    
    @property
    def embed(self):
        """
        Returns the first embed in the message.

        Returns
        -------
        embed : `None` or ``EmbedCore``
        """
        embeds = self.embeds
        if (embeds is not None):
            return embeds[0]
    
    @property
    def attachment(self):
        """
        Returns the first attachment in the message.

        Returns
        -------
        attachment : `None` or ``Attachment``
        """
        attachments = self.attachments
        if (attachments is not None):
            return attachments[0]
    
    @property
    def sticker(self):
        """
        Returns the first sticker in the message.

        Returns
        -------
        sticker : `None` or ``Sticker``
        """
        stickers = self.stickers
        if (stickers is not None):
            return stickers[0]
    
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
        Returns the message's clean content, what actually depends on the message's type. By default it is the
        message's content with transformed mentions, but for different message types it means different things.
        
        Returns
        -------
        clean_content : `str`
        
        Notes
        -----
        The converting can not display join messages, call messages and private channel names correctly.
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
        mentions : `list` of (`str` (`'everyone'`), ``ClientUserBase``, ``Role``, ``ChannelBase`` or
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
            result = len(self.content)
        else:
            result = len(self.clean_content)
        
        embeds = self.embeds
        if (embeds is not None):
            for embed in embeds:
                if embed.type in EXTRA_EMBED_TYPES:
                    break
                result += len(embed)
        
        return result
    
    @property
    def clean_embeds(self):
        """
        Returns the message's not link typed embeds with converted content without mentions.
        
        Returns
        -------
        clean_embeds : `list` of ``EmbedCore``
        
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
        Returns whether the given user reacted with the given emoji on the message.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reacted emoji.
        user : ``ClientUserBase``
            The reactor.
        
        Returns
        -------
        did_react : `bool`
        """
        try:
            reactors = self.reactions[emoji]
        except KeyError:
            return False
        return (user in reactors)
