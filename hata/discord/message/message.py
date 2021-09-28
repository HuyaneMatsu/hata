__all__ = ('EMBED_UPDATE_EMBED_ADD', 'EMBED_UPDATE_EMBED_REMOVE', 'EMBED_UPDATE_NONE', 'EMBED_UPDATE_SIZE_UPDATE',
    'Message',)

import warnings
from datetime import datetime

from ...backend.utils import BaseMethodDescriptor
from ...backend.export import export, include

from ..bases import DiscordEntity, id_sort_key
from ..utils import timestamp_to_datetime, CHANNEL_MENTION_RP, time_to_id, DATETIME_FORMAT_CODE
from ..core import MESSAGES, CHANNELS, GUILDS
from ..user import ZEROUSER, User, ClientUserBase, UserBase
from ..emoji import reaction_mapping
from ..embed import EmbedCore, EXTRA_EMBED_TYPES, EmbedBase
from ..webhook import WebhookRepr, create_partial_webhook_from_id, WebhookType, Webhook
from ..role import Role, create_partial_role_from_id
from ..preconverters import preconvert_flag, preconvert_bool, preconvert_snowflake, preconvert_str, \
    preconvert_preinstanced_type, get_type_names, preconvert_snowflake_array
from ..sticker import Sticker

from ..http import urls as module_urls

from .utils import try_resolve_interaction_message
from .cross_mention import UnknownCrossMention
from .message_activity import MessageActivity
from .attachment import Attachment
from .message_application import MessageApplication
from .message_interaction import MessageInteraction
from .message_reference import MessageReference
from .flags import MessageFlag
from .preinstanced import MessageType, GENERIC_MESSAGE_TYPES


ChannelTextBase = include('ChannelTextBase')
ChannelGuildBase = include('ChannelGuildBase')
ChannelText = include('ChannelText')
ChannelPrivate = include('ChannelPrivate')
ChannelGroup = include('ChannelGroup')
create_component = include('create_component')
ChannelGuildUndefined = include('ChannelGuildUndefined')
CHANNEL_TYPE_MAP = include('CHANNEL_TYPE_MAP')
InteractionType = include('InteractionType')
ComponentBase = include('ComponentBase')
ChannelThread = include('ChannelThread')

EMBED_UPDATE_NONE = 0
EMBED_UPDATE_SIZE_UPDATE = 1
EMBED_UPDATE_EMBED_ADD = 2
EMBED_UPDATE_EMBED_REMOVE = 3

MESSAGE_FLAGS_EMPTY = MessageFlag()
MESSAGE_TYPE_DEFAULT = MessageType.default
MESSAGE_TYPE_DEFAULT_VALUE = MESSAGE_TYPE_DEFAULT.value

MESSAGE_FIELD_KEY_ACTIVITY = 1
MESSAGE_FIELD_KEY_APPLICATION = 2
MESSAGE_FIELD_KEY_APPLICATION_ID = 3
MESSAGE_FIELD_KEY_ATTACHMENTS = 4
MESSAGE_FIELD_KEY_CHANNEL_MENTIONS = 5
MESSAGE_FIELD_KEY_COMPONENTS = 6
MESSAGE_FIELD_KEY_CONTENT = 7
MESSAGE_FIELD_KEY_CROSS_MENTIONS = 8
MESSAGE_FIELD_KEY_REFERENCED_MESSAGE = 9
MESSAGE_FIELD_KEY_DELETED = 10
MESSAGE_FIELD_KEY_EDITED_AT = 11
MESSAGE_FIELD_KEY_EMBEDS = 12
MESSAGE_FIELD_KEY_EVERYONE_MENTION = 13
MESSAGE_FIELD_KEY_FLAGS = 14
MESSAGE_FIELD_KEY_INTERACTION = 15
MESSAGE_FIELD_KEY_PARTIAL = 16
MESSAGE_FIELD_KEY_NONCE = 17
MESSAGE_FIELD_KEY_PINNED = 18
MESSAGE_FIELD_KEY_REACTIONS = 19
MESSAGE_FIELD_KEY_ROLE_MENTION_IDS = 20
MESSAGE_FIELD_KEY_ROLE_MENTIONS = 21
MESSAGE_FIELD_KEY_STICKERS = 22
MESSAGE_FIELD_KEY_THREAD = 23
MESSAGE_FIELD_KEY_TTS = 24
MESSAGE_FIELD_KEY_TYPE = 25
MESSAGE_FIELD_KEY_USER_MENTIONS = 26

MESSAGE_CACHE_FIELD_KEYS = (
    MESSAGE_FIELD_KEY_CHANNEL_MENTIONS,
    MESSAGE_FIELD_KEY_ROLE_MENTIONS,
)

def _set_message_field(message, field_key, value):
    """
    Stores the given value in the message's fields.
    
    Parameters
    ----------
    message : ``Message``
        The message to store the value in it's fields.
    field_key : `int`
        Message field key.
    value : `Any``
        The value to store.
    """
    fields = message._fields
    if fields is None:
        message._fields = fields = {}
    
    fields[field_key] = value


def _remove_message_field(message, field_key):
    """
    Tries to remove the given from a message's fields.
    
    Parameters
    ----------
    message : ``Message``
        The message to remove the value from.
    field_key : `int`
        Message field key.
    """
    fields = message._fields
    if (fields is not None):
        try:
            del fields[field_key]
        except KeyError:
            pass
        else:
            if not fields:
                message._fields = None


def _get_message_field(message, field_key):
    """
    Tries to get the given field of the message.
    
    Parameters
    ----------
    message : ``Message``
        The message to get the field from.
    field_key : `int`
        Message field key to get.
    
    Returns
    -------
    value : `None` or `Any`
    """
    fields = message._fields
    if (fields is not None):
        return fields.get(field_key, None)


def _get_first_message_field(message, field_key):
    """
    Tries to get the first element given field of the message.
    
    Parameters
    ----------
    message : ``Message``
        The message to get the field from.
    field_key : `int`
        Message field key to get.
    
    Returns
    -------
    value : `None` or `Any`
    """
    fields = message._fields
    if (fields is not None):
        try:
            field_value = fields[field_key]
        except KeyError:
            pass
        else:
            return field_value[0]


def _has_message_field(message, field_key):
    """
    Returns whether the message has the given field.
    
    
    Parameters
    ----------
    message : ``Message``
        The message to check whether it has the field.
    field_key : `int`
        Message field key to check.
    
    Returns
    -------
    has_field : `bool`
    """
    fields = message._fields
    if (fields is None):
        has_field = False
    else:
        has_field = (field_key in fields)
    
    return has_field


@export
class Message(DiscordEntity, immortal=True):
    """
    Represents a message from Discord.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the message.
    _fields : `bool`
        Optional fields of the message.
    author : ``UserBase`` instance
        The author of the message. Can be any user type and if not found, then set as `ZEROUSER`.
    channel_id : `int`
        The channel's identifier where the message is sent.
    guild_id : `int`
        The channel's guild's identifier.
    
    Notes
    -----
    Message instances are weakreferable.
    
    Structure
    ---------
    Not like other Discord entities, message attributes can be accessed mainly through properties, which are the
    following:
    
    - ``.activity``
    - ``.channel_mentions`` (cache field)
    - ``.application``
    - ``.application_id``
    - ``.attachments``
    - ``.components``
    - ``.content``
    - ``.cross_mentions``
    - ``.deleted`` (internal field)
    - ``.edited_at``
    - ``.embeds``
    - ``.everyone_mention``
    - ``.flags``
    - ``.interaction``
    - ``.nonce``
    - ``.partial`` (internal field)
    - ``.pinned``
    - ``.reactions``
    - ``.referenced_message``
    - ``.role_mentions`` (cache field)
    - ``.role_mention_ids``
    - ``.stickers``
    - ``.thread``
    - ``.tts``
    - ``.type``
    - ``.user_mentions``
    
    In average only 1.5 field of a message is used, which makes keeping up over 20 allocated field questionable.
    The message type have high field increase tendency, making the dynamic attribute allocation more and more worth it.
    At the current moment a message usually has 1-6 extra fields used, but in the close future in 2022 with message
    content intent, it will decrease to 0-6, making the system save a lot of memory.
    """
    __slots__ = ('_fields', 'author', 'channel_id', 'guild_id')
    
    def __new__(cls, data):
        """
        Creates a new message object form the given message payload. If the message already exists, picks it up.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        """
        message_id = int(data['id'])
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = message_id
            MESSAGES[self.id] = self
        else:
            if not self.partial:
                return self
        
        self._fields = None
        self._set_attributes(data)
        return self
    
    
    @classmethod
    def _create_message_is_in_cache(cls, data):
        """
        Creates a new message object form the given message payload. If the message already exists, picks it up.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        
        Returns
        -------
        self : ``Message``
            The created or found message instance.
        from_cache : `bool`
            Whether the message was found in the cache.
        """
        message_id = int(data['id'])
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = message_id
            MESSAGES[self.id] = self
        else:
            if not self.partial:
                return True, self
        
        self._fields = None
        self._set_attributes(data)
        return False, self
    
    
    def _set_attributes(self, data):
        """
        Finishes the message's initialization process by setting it's attributes (except `.id`).
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        """
        channel_id = int(data['channel_id'])
        self.channel_id = channel_id
        
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
            guild = None
        else:
            guild_id = int(guild_id)
            guild = GUILDS.get(guild_id, None)
        
        self.guild_id = guild_id
        
        author_data = data.get('author', None)
        webhook_id = data.get('webhook_id', None)
        if webhook_id is None:
            webhook_id = 0
        else:
            webhook_id = int(webhook_id)
        
        application_id = data.get('application_id', None)
        
        if (application_id is None):
            application_id = 0
        else:
            application_id = int(application_id)
            
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_APPLICATION_ID,
                application_id,
            )
        
        if (not webhook_id) or (application_id and ((webhook_id == application_id) or (not webhook_id))):
            if author_data is None:
                author = ZEROUSER
            else:
                try:
                     author_data['member'] = data['member']
                except KeyError:
                    pass
                
                author = User(author_data, guild)
        else:
            if (data.get('message_reference', None) is not None):
                cross_mention_datas = data.get('mention_channels', None)
                if (cross_mention_datas is not None) and cross_mention_datas:
                    _set_message_field(
                        self,
                        MESSAGE_FIELD_KEY_CROSS_MENTIONS,
                        tuple(sorted(
                            (UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas),
                            key = id_sort_key,
                        )),
                    )
                
                webhook_type = WebhookType.server
            else:
                webhook_type = WebhookType.bot
            
            if author_data is None:
                author = create_partial_webhook_from_id(webhook_id, '', type_=webhook_type)
            else:
                author = WebhookRepr(author_data, webhook_id, type_=webhook_type, channel_id=channel_id)
        
        self.author = author
        
        # At this point every static field is set, now we switch to dynamic ones.
        
        reactions_data = data.get('reactions', None)
        if (reactions_data is not None) and reactions_data:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_REACTIONS,
                reaction_mapping(reactions_data),
            )
        
        referenced_message_data = data.get('referenced_message', None)
        if referenced_message_data is None:
            referenced_message_data = data.get('message_reference', None)
            if referenced_message_data is None:
                referenced_message = None
            else:
                referenced_message = MessageReference(referenced_message_data)
        else:
            # Discord do not sends `guild_id` for nested message instances.
            referenced_message_data['guild_id'] = data.get('guild_id', None)
            
            referenced_message = Message(referenced_message_data)
        
        if (referenced_message is not None):
            _set_message_field(self, MESSAGE_FIELD_KEY_REFERENCED_MESSAGE, referenced_message)
        
        
        application_data = data.get('application', None)
        if (application_data is not None):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_APPLICATION,
                MessageApplication(application_data),
            )
        
        
        activity_data = data.get('activity', None)
        if (activity_data is not None):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_ACTIVITY,
                MessageActivity(activity_data),
            )
        
        
        edited_timestamp = data.get('edited_timestamp', None)
        if (edited_timestamp is not None):
            edited_at = timestamp_to_datetime(edited_timestamp)
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_EDITED_AT,
                edited_at,
            )
        
        
        if data.get('pinned', False):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_PINNED,
                None,
            )
        
        
        if data.get('mention_everyone', False):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_EVERYONE_MENTION,
                None,
            )
        
        
        if data.get('tts', False):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_TTS,
                None,
            )
        
        
        flags = data.get('flags', 0)
        if flags:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_FLAGS,
                MessageFlag(flags),
            )
        
        
        message_type_value = data.get('type', MESSAGE_TYPE_DEFAULT_VALUE)
        if message_type_value != MESSAGE_TYPE_DEFAULT_VALUE:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_TYPE,
                MessageType.get(message_type_value),
            )
        
        
        attachment_datas = data.get('attachments', None)
        if (attachment_datas is not None) and attachment_datas:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_ATTACHMENTS,
                tuple(Attachment(attachment) for attachment in attachment_datas),
            )
        
        
        embed_datas = data.get('embeds', None)
        if (embed_datas is not None) and embed_datas:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_EMBEDS,
                tuple(EmbedCore.from_data(embed) for embed in embed_datas),
            )
        
        
        nonce = data.get('nonce', None)
        if (nonce is not None):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_NONCE,
                nonce,
            )
        
        
        content = data.get('content', None)
        if (content is not None) and content:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_CONTENT,
                content,
            )
        
        
        interaction_data = data.get('interaction', None)
        if (interaction_data is not None):
            interaction = MessageInteraction(interaction_data)
            try_resolve_interaction_message(self, interaction)
            
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_INTERACTION,
                interaction,
            )
        
        
        component_datas = data.get('components', None)
        if (component_datas is not None) and component_datas:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_COMPONENTS,
                tuple(create_component(component_data) for component_data in component_datas),
            )
        
        
        sticker_datas = data.get('sticker_items', None)
        if (sticker_datas is not None) and sticker_datas:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_STICKERS,
                tuple(Sticker._create_partial(sticker_data) for sticker_data in sticker_datas),
            )
        
        
        user_mention_datas = data.get('mentions', None)
        if (user_mention_datas is not None) and user_mention_datas:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_USER_MENTIONS,
                tuple(sorted(
                    (User(user_mention_data, guild) for user_mention_data in user_mention_datas),
                    key = id_sort_key,
                )),
            )
        
        
        role_mention_ids = data.get('mention_roles', None)
        if (role_mention_ids is not None) and role_mention_ids:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
                tuple(sorted(int(role_id) for role_id in role_mention_ids)),
            )
        
        
        thread_data = data.get('thread', None)
        if (thread_data is not None):
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_THREAD,
                CHANNEL_TYPE_MAP.get(thread_data['type'], ChannelGuildUndefined)(thread_data, None, guild_id),
            )
    
    
    def _late_init(self, data):
        """
        Some message fields might be missing after receiving a payload. This method is called to check and set those
        if multiple payload is received.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        """
        fields = self._fields
        if (fields is None):
            update_content = True
            update_interaction = True
            update_components = True
            update_embeds = True
        else:
            update_content = (MESSAGE_FIELD_KEY_CONTENT not in fields)
            update_interaction = (MESSAGE_FIELD_KEY_INTERACTION not in fields)
            update_components = (MESSAGE_FIELD_KEY_COMPONENTS not in fields)
            update_embeds = (MESSAGE_FIELD_KEY_EMBEDS not in fields)
        
        if update_content:
            content = data.get('content', None)
            if (content is not None) and content:
                _set_message_field(
                    self,
                    MESSAGE_FIELD_KEY_CONTENT,
                    content,
                )
        
        if update_interaction:
            interaction_data = data.get('interaction', None)
            if (interaction_data is not None):
                interaction = MessageInteraction(interaction_data)
                try_resolve_interaction_message(self, interaction)
                
                _set_message_field(
                    self,
                    MESSAGE_FIELD_KEY_INTERACTION,
                    interaction,
                )
        
        if update_components:
            component_datas = data.get('components', None)
            if (component_datas is not None) and component_datas:
                _set_message_field(
                    self,
                    MESSAGE_FIELD_KEY_COMPONENTS,
                    tuple(create_component(component_data) for component_data in component_datas),
                )
            
        if update_embeds:
            embed_datas = data.get('embeds', None)
            if (embed_datas is not None) and embed_datas:
                _set_message_field(
                    self,
                    MESSAGE_FIELD_KEY_EMBEDS,
                    tuple(EmbedCore.from_data(embed) for embed in embed_datas),
                )
    
    
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
        **kwargs : keyword parameters
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
        channel_id : ``ChannelTextBase`` or `int` instance, Optional if called as method (Keyword only)
            The ``.channel_id`` attribute of the message.
            
            If called as a classmethod this attribute must be passed, or `TypeError` is raised.
        
        components : `None` or (`list` or `tuple`) of ``ComponentBase``, Optional (Keyword only)
            The ``.components`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        
        content : `None` or `str`, Optional (Keyword only)
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
            If any of the parameter's type is incorrect.
        ValueError
            - If a passed parameter's type is correct, but it's value is not.
            - If `validate` is passed as `True` and there is a contradictory between the message's attributes.
        """
        if (base is not None) and (type(base) is not cls):
            raise TypeError(f'`base` should be either `None`, or type `{cls.__name__}`, got `{base!r}`')
        
        try:
            channel = kwargs.pop('channel')
        except KeyError:
            
            try:
                channel_id = kwargs.pop('channel_id')
            except KeyError:
                if base is None:
                    raise TypeError('Expected to be called as method, but was called as a classmethod and `channel_id`'
                        'was not passed.')
                
                channel_id = base.channel_id
                channel = None
            else:
                if isinstance(channel_id, int):
                    channel = None
                elif isinstance(channel_id, ChannelTextBase):
                    channel = channel_id
                    channel_id = channel_id.id
                else:
                    raise TypeError(f'`channel_id` should be `int` or `{ChannelTextBase.__name__}` subclass\'s'
                        f'instance, got `{channel_id!r}`.')
            
            if (channel is None):
                channel = CHANNELS.get('channel_id', None)
        
            if channel is None:
                guild_id = 0
            else:
                guild_id = channel.guild_id
        
        else:
            warnings.warn(
                f'`{cls.__name__}.custom`\'s `channel` parameter is deprecated, and will be removed in 2022 January.'
                f'Please use `channel_id` instead.',
                FutureWarning)
            
            if not isinstance(channel, ChannelTextBase):
                raise TypeError(f'`channel` should be or `{ChannelTextBase.__name__}` subclass\'s'
                    f'instance, got `{channel!r}`.')
                
            channel_id = channel.id
            guild_id = channel.guild_id
        
        
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
                
                if attachments:
                    for attachment in attachments:
                        if not isinstance(attachment, Attachment):
                            raise TypeError(f'`attachments` contains a non `{Attachment.__name__}` '
                                f'instance, `{attachment.__class__.__name__}`.')
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
                    f'`{WebhookRepr.__name__}`, got `{author!r}`.')
        
        try:
            content = kwargs.pop('content')
        except KeyError:
            if base is None:
                content = None
            else:
                content = base.content
        else:
            if (content is not None):
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
                    raise TypeError(f'`cross_mentions` can be `None` or `tuple`, `list` of '
                        f'`{ChannelGuildBase.__name__}` or `{UnknownCrossMention.__name__}` instances, got '
                        f'`{cross_mentions.__class__.__name__}`.')
                
                cross_mentions_processed = []
                
                for channel_ in cross_mentions:
                    if not isinstance(channel_, (ChannelGuildBase, UnknownCrossMention)):
                        raise TypeError(f'`cross_mentions` contains a non `{ChannelGuildBase.__name__}` or '
                            f'`{UnknownCrossMention.__name__}` instance: `{channel_.__class__.__name__}`.')
                    
                    cross_mentions_processed.append(channel_)
                
                if cross_mentions_processed:
                    cross_mentions_processed.sort(key=id_sort_key)
                    cross_mentions = tuple(cross_mentions_processed)
                else:
                    cross_mentions = None
        
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
                    raise TypeError(f'`embeds` can be `None`, `tuple` or`list` of `{EmbedBase.__name__}` instances, '
                        f'got `{embeds.__class__.__name__}`.')
                
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
                        
                        raise TypeError(f'`embeds` contains a non `{EmbedBase.__name__}` instance: '
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
                reactions = base.reactions
                if (reactions is not None):
                    # Copy it, because it might be modified
                    reactions = reactions.copy()
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
                    
                else:
                    # There cannot be an empty mention list, so lets fix it.
                    role_mentions = None
        
        if validate:
            if (role_mentions is not None) and (not isinstance(channel,ChannelGuildBase)):
                raise ValueError('`role_mentions` are set as not `None`, meanwhile the `channel` is not '
                    f'`{ChannelGuildBase}` subclass\'s instance; `{channel!r}`')
        
        if (role_mentions is None):
            role_mention_ids = None
        else:
            role_mention_ids = tuple(sorted(role.id for role in role_mentions))
        
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
                type_ = MESSAGE_TYPE_DEFAULT
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
                
                components = tuple(components)
                
                if components:
                    for component in components:
                        if not isinstance(component, ComponentBase):
                            raise TypeError(f'`components` contains at least 1 non `{ComponentBase.__name__}` '
                                f'instance; `{component.__class__.__name__}`.')
                    
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
        self._fields = None
        self.author = author
        self.channel_id = channel_id
        self.guild_id = guild_id
        
        self.activity = activity
        self.application = application
        self.application_id = application_id
        self.attachments = attachments
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
        self.role_mention_ids = role_mention_ids
        self.stickers = stickers
        self.tts = tts
        self.type = type_
        self.user_mentions = user_mentions
        self.interaction = interaction
        self.components = components
        self.thread = thread
        
        self.partial = True
        
        return self
    
    
    url = property(module_urls.message_jump_url)
    
    
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
    
    
    def __format__(self, code):
        """
        Formats the message in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        message : `str`
        
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
            return self.__repr__()
        
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
    
    
    def _difference_update_attributes(self, data):
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
        | attachments       | `None` or (`tuple` of ``Attachment``)                                 |
        +-------------------+-----------------------------------------------------------------------+
        | components        | `None` or (`tuple` of ``ComponentBase``)                              |
        +-------------------+-----------------------------------------------------------------------+
        | content           | `None` or `str`                                                       |
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
        | role_mention_ids  | `None` or (`tuple` of `int`)                                          |
        +-------------------+-----------------------------------------------------------------------+
        """
        self._clear_cache()
        old_attributes = {}
        
        try:
            pinned = data['pinned']
        except KeyError:
            pass
        else:
            self_pinned = self.pinned
            if self_pinned != pinned:
                old_attributes['pinned'] = self_pinned
                self.pinned = pinned
        
        flags = data.get('flags', 0)
        self_flags = self.flags
        flag_difference = self_flags^flags
        if flag_difference:
            old_attributes['flags'] = self_flags
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
                    
                    self_embeds = self.embeds
                    if self_embeds != embeds:
                        old_attributes['embeds'] = self_embeds
                        self.embeds = embeds
        
        # at the case of pin update edited is None
        try:
            edited_timestamp = data['edited_timestamp']
        except KeyError:
            pass
        else:
            if edited_timestamp is None:
                return old_attributes
            
            edited_at = timestamp_to_datetime(edited_timestamp)
            
            self_edited_at = self.edited_at
            if self_edited_at == edited_at:
                return old_attributes
            
            old_attributes['edited_at'] = self_edited_at
            self.edited_at = edited_at
        
        try:
            everyone_mention = data['mention_everyone']
        except KeyError:
            pass
        else:
            self_everyone_mention = self.everyone_mention
            if self_everyone_mention != everyone_mention:
                old_attributes['everyone_mention'] = self_everyone_mention
                self.everyone_mention = everyone_mention
        
        # ignoring tts
        # ignoring type
        # ignoring nonce
        
        try:
            attachment_datas = data['attachments']
        except KeyError:
            pass
        else:
            if (attachment_datas is not None) and attachment_datas:
                attachments = tuple(Attachment(attachment) for attachment in attachment_datas)
            else:
                attachments = None
            
            self_attachments = self.attachments
            if self_attachments != attachments:
                old_attributes['attachments'] = self_attachments
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
            
            self_embeds = self.embeds
            if self_embeds != embeds:
                old_attributes['embeds'] = self_embeds
                self.embeds = embeds
        
        try:
            content = data['content']
        except KeyError:
            pass
        else:
            if (content is not None) and (not content):
                content = None
            
            self_content = self.content
            if self_content != content:
                old_attributes['content'] = self_content
                self.content = content
        
        try:
            user_mention_datas = data['mentions']
        except KeyError:
            pass
        else:
            guild = self.guild
            
            if (user_mention_datas is None) or (not user_mention_datas):
                user_mentions = None
            else:
                user_mentions = tuple(sorted(
                    (User(user_mention_data, guild) for user_mention_data in user_mention_datas),
                    key = id_sort_key,
                ))
            
            self_user_mentions = self.user_mentions
            if self_user_mentions != user_mentions:
                old_attributes['user_mentions'] = self_user_mentions
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
            
            self_components = self.components
            if self_components != components:
                old_attributes['components'] = self_components
                self.components = components
        
        
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
                    key = id_sort_key,
                ))
            
            self_cross_mentions = self.cross_mentions
            if self_cross_mentions != cross_mentions:
                old_attributes['cross_mentions'] = self_cross_mentions
                self.cross_mentions = cross_mentions
        
        try:
            role_mention_ids = data['mention_roles']
        except KeyError:
            pass
        else:
            if (role_mention_ids is None) or (not role_mention_ids):
                role_mention_ids = None
            else:
                role_mention_ids = tuple(sorted(int(role_id) for role_id in role_mention_ids))
            
            self_role_mention_ids = self.role_mention_ids
            if self_role_mention_ids != role_mention_ids:
                old_attributes['role_mention_ids'] = self_role_mention_ids
                self.role_mention_ids = role_mention_ids
        
        return old_attributes
    
    
    def _update_attributes(self, data):
        """
        Updates the message with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        """
        self._clear_cache()
        
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
            
            edited_at = timestamp_to_datetime(edited_timestamp)
            if self.edited_at == edited_at:
                return
            
            self.edited_at = edited_at
        
        
        try:
            everyone_mention = data['mention_everyone']
        except KeyError:
            pass
        else:
            self.everyone_mention = everyone_mention
        
        
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
            if (content is not None) and (not content):
                content = None
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
        
        guild = self.guild
        
        try:
            user_mention_datas = data['mentions']
        except KeyError:
            pass
        else:
            if user_mention_datas:
                user_mentions = tuple(sorted(
                    (User(user_mention_data, guild) for user_mention_data in user_mention_datas),
                    key = id_sort_key,
                ))
            else:
                user_mentions = None
            
            self.user_mentions = user_mentions
        
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
                    key = id_sort_key,
                ))
            
            self.cross_mentions = cross_mentions
        
        try:
            role_mention_ids = data['mention_roles']
        except KeyError:
            pass
        else:
            if (role_mention_ids is None) or (not role_mention_ids):
                role_mention_ids = None
            else:
                role_mention_ids = tuple(sorted(int(role_id) for role_id in role_mention_ids))
            
            self.role_mention_ids = role_mention_ids
    
    
    def _clear_cache(self):
        """
        Clears the message's cache fields.
        """
        fields = self._fields
        if (fields is not None):
            for field_key in MESSAGE_CACHE_FIELD_KEYS:
                try:
                    del fields[field_key]
                except KeyError:
                    pass
                else:
                    if not fields:
                        self._fields = None
                        break
    
    
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
                embeds[index]._set_sizes(embed_data)

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
    def channel(self):
        """
        Returns the message's channel's guild.
        
        Returns
        -------
        guild : `None` or ``ChannelTextBase``
        """
        channel_id = self.channel_id
        if channel_id:
            return CHANNELS.get(channel_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the message's channel's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def clean_content(self):
        """
        Returns the message's clean content, what actually depends on the message's type. By default it is the
        message's content with transformed mentions, but for different message types it means different things.
        
        Returns
        -------
        clean_content : `None` or `str`
        
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
        if (content is not None):
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
        if (channel_mentions is not None):
            mentions.extend(channel_mentions)
        
        return mentions
    
    
    def __len__(self):
        """
        Returns the length of the message, including of the non link typed embeds's.
        
        Returns
        -------
        length : `int`
        """
        if self.type in GENERIC_MESSAGE_TYPES:
            content = self.content
            if (content is None):
                length = 0
            else:
                length = len(content)
        else:
            length = len(self.clean_content)
        
        embeds = self.embeds
        if (embeds is not None):
            for embed in embeds:
                embed_type = embed.type
                if (embed_type is not None) and (embed_type in EXTRA_EMBED_TYPES):
                    break
                
                length += len(embed)
        
        return length
    
    
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
    
    def is_deletable(self):
        """
        Returns whether the message can be deleted.
        
        Returns
        -------
        is_deletable : `bool`
        """
        # Use goto
        while True:
            fields = self._fields
            if fields is None:
                is_deletable = True
                break
            
            if MESSAGE_FIELD_KEY_DELETED in fields:
                is_deletable = False
                break
            
            try:
                flags = fields[MESSAGE_FIELD_KEY_FLAGS]
            except KeyError:
                pass
            else:
                if flags.invoking_user_only:
                    is_deletable = False
                    break
            
            is_deletable = True
            break
        
        return is_deletable
    
    
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
    
    
    def _add_reaction(self, emoji, user):
        """
        Adds a reaction to the message.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The reacted emoji.
        user : ``ClientUserBase``
            The reactor user.
        """
        reactions = self.reactions
        if reactions is None:
            reactions = reaction_mapping(None)
            self.reactions = reactions
        
        return reactions.add(emoji, user)
    
    
    def _remove_reaction(self, emoji, user):
        """
        Removes a reaction to the message.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The removed emoji.
        user : ``ClientUserBase``
            The user who removed their reaction.
        """
        reactions = self.reactions
        if (reactions is not None):
            return reactions.remove(emoji, user)
    
    
    def _remove_reaction_emoji(self, emoji):
        """
        Removes all reactions of an emoji from the message.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to remove it's reactions.
        
        Returns
        -------
        line : `None` or ``reaction_mapping_line``
        """
        reactions = self.reactions
        if (reactions is not None):
            return reactions.remove_emoji(emoji)
    
    
    @classmethod
    def precreate(cls, message_id, **kwargs):
        """
        Precreates the message with the given parameters. Precreated messages are picked up when the message's data is
        received with the same id.
        
        First tries to find whether a message exists with the given id. If it does and it is partial, updates it with
        the given parameters, else it creates a new one.
        
        > Note, that message partial check is not working same as other entity's and may cause misbehaviour.
        >
        > This classmethod is for future usage, when the partial check will be resolved.
        
        Parameters
        ----------
        guild_id : `snowflake`
            The message's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the message.
        
        Other Parameters
        ----------------
        activity : `None` or ``MessageActivity``
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        message_id = preconvert_snowflake(message_id, 'message_id')
        
        if kwargs:
            processable = []
            
            try:
                author = kwargs.pop('author')
            except KeyError:
                pass
            else:
                if not isinstance(author, UserBase):
                    raise TypeError(f'`author` can be `{UserBase.__name__}` instance, got '
                        f'`{author.__class__.__name__}`.')
                
                processable.append(('author', author))
            
            for variable_name in ('channel_id', 'guild_id'):
                try:
                    variable_value = kwargs.pop(variable_name)
                except KeyError:
                    pass
                else:
                    variable_value = preconvert_snowflake(variable_value, variable_name)
                    processable.append((variable_name, variable_value))
            
            
            processable_by_field = []
            
            for variable_field_key, variable_type, variable_name in (
                (MESSAGE_FIELD_KEY_ACTIVITY, MessageActivity, 'activity'),
                (MESSAGE_FIELD_KEY_APPLICATION, MessageApplication, 'application'),
                (MESSAGE_FIELD_KEY_REFERENCED_MESSAGE, (Message, MessageReference), 'referenced_message'),
                (MESSAGE_FIELD_KEY_EDITED_AT, datetime, 'edited_at'),
                (MESSAGE_FIELD_KEY_INTERACTION, MessageInteraction, 'interaction'),
                (MESSAGE_FIELD_KEY_REACTIONS, reaction_mapping, 'reactions'),
                (MESSAGE_FIELD_KEY_THREAD, ChannelThread, 'thread'),
            ):
                try:
                    variable_value = kwargs.pop(variable_name)
                except KeyError:
                    pass
                else:
                    if (variable_value is not None):
                        if not isinstance(variable_value, variable_type):
                            raise TypeError(f'`{variable_name}` can be either {get_type_names(variable_type)} or '
                                f'`None`, got {variable_value.__class__.__name__}.')
                        
                        processable_by_field.append((variable_field_key, variable_value))
            
            
            try:
                application_id = kwargs.pop('application_id')
            except KeyError:
                pass
            else:
                application_id = preconvert_snowflake(application_id, 'application_id')
                if application_id:
                    processable_by_field.append((MESSAGE_FIELD_KEY_APPLICATION_ID, application_id))
            
            
            for variable_field_key, variable_element_type, variable_name, is_sorted in (
                (MESSAGE_FIELD_KEY_ATTACHMENTS, Attachment, 'attachments', False),
                (MESSAGE_FIELD_KEY_COMPONENTS, ComponentBase, 'components', False),
                (MESSAGE_FIELD_KEY_STICKERS, Sticker, 'stickers', False),
                (MESSAGE_FIELD_KEY_CROSS_MENTIONS, (ChannelGuildBase, UnknownCrossMention), 'cross_mentions', True),
                (MESSAGE_FIELD_KEY_USER_MENTIONS, ClientUserBase, 'user_mentions', True),
            ):
                try:
                    variable_value = kwargs.pop(variable_name)
                except KeyError:
                    pass
                else:
                    if (variable_value is not None):
                        if not isinstance(variable_value, (list, tuple, set)):
                            raise TypeError(f'`{variable_name}` should be `None` or `tuple`, `list` or `set` of '
                                f'{get_type_names(variable_element_type)} instances, got '
                                f'`{variable_value.__class__.__name__}`.')
                        
                        variable_values_processed = []
                        
                        for variable_element_value in variable_value:
                            if not isinstance(variable_element_value, variable_element_type):
                                raise TypeError(f'`{variable_name}` contains a non '
                                    f'{get_type_names(variable_element_type)} instance, got '
                                    f'`{variable_element_value.__class__.__name__}`.')
                            
                            variable_values_processed.append(variable_element_value)
                        
                        if variable_values_processed:
                            if is_sorted:
                                variable_values_processed.sort(key=id_sort_key)
                            
                            variable_values_processed = tuple(variable_values_processed)
                            processable_by_field.append((variable_field_key, variable_values_processed))
            
            
            for variable_field_key, variable_name in (
                (MESSAGE_FIELD_KEY_CONTENT, 'content'),
                (MESSAGE_FIELD_KEY_NONCE, 'nonce'),
            ):
                try:
                    variable_value = kwargs.pop(variable_name)
                except KeyError:
                    pass
                else:
                    if (variable_value is not None):
                        variable_type = type(variable_value)
                        if variable_type is str:
                            pass
                        elif issubclass(variable_type, str):
                            variable_value = str(variable_value)
                        else:
                            raise TypeError(f'`{variable_name}` can be either as `None` or `str` instance, got '
                                f'{variable_type.__name__}.')
                        
                        if variable_value:
                            processable_by_field.append((variable_field_key, variable_value))
            
            
            try:
                embeds = kwargs.pop('embeds')
            except KeyError:
                pass
            else:
                if (embeds is not None):
                    if not isinstance(embeds, (list, tuple)):
                        raise TypeError(f'`embeds` can be `None`, `tuple` or `list` of `{EmbedBase.__name__}` '
                            f'instances, got `{embeds.__class__.__name__}`.')
                    
                    embeds_processed = []
                    
                    for embed in embeds:
                        if isinstance(embed, EmbedCore):
                            pass
                        
                        elif isinstance(embed, EmbedBase):
                            # Embed compatible, lets convert it
                            embed = EmbedCore.from_data(embed.to_data())
                        
                        else:
                            raise TypeError(f'`embeds` contains a non `{EmbedBase.__name__}` instance: '
                                f'`{embeds.__class__.__name__}`.')
                    
                        embeds_processed.append(embed)
                    
                    if embeds_processed:
                        embeds_processed = tuple(embeds_processed)
                        
                        processable_by_field.append((MESSAGE_FIELD_KEY_EMBEDS, embeds_processed))
            
            for variable_field_key, variable_name in (
                (MESSAGE_FIELD_KEY_EVERYONE_MENTION, 'everyone_mention'),
                (MESSAGE_FIELD_KEY_PINNED, 'pinned'),
                (MESSAGE_FIELD_KEY_TTS, 'tss'),
            ):
                try:
                    variable_value = kwargs.pop(variable_name)
                except KeyError:
                    pass
                else:
                    if not isinstance(variable_value, bool):
                        raise TypeError(f'`{variable_name}` can be `bool` instance, got '
                            f'`{variable_value.__class__.__name__}`.')
                    
                    if variable_value:
                        processable_by_field.append((variable_field_key, variable_value))
            
            
            try:
                flags = kwargs.pop('flags')
            except KeyError:
                pass
            else:
                flags = preconvert_flag(flags, 'flags', MessageFlag)
                processable_by_field.append((MESSAGE_FIELD_KEY_FLAGS, flags))
            
            
            try:
                role_mention_ids = kwargs.pop('role_mention_ids')
            except KeyError:
                pass
            else:
                if (role_mention_ids is not None):
                    role_mention_ids = preconvert_snowflake_array(role_mention_ids, 'role_mention_ids')
                    processable_by_field.append((MESSAGE_FIELD_KEY_ROLE_MENTION_IDS, role_mention_ids))
            
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_preinstanced_type(type_, 'type_', MessageType)
                if type_ is not MESSAGE_TYPE_DEFAULT:
                    processable_by_field.append((MESSAGE_FIELD_KEY_TYPE, type_))
            
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
            
        else:
            processable = None
            processable_by_field = None
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = cls._create_empty(message_id)
            MESSAGES[message_id] = self
        else:
            if self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        if (processable_by_field is not None):
            for item in processable_by_field:
                _set_message_field(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, message_id):
        """
        Creates a message with default parameters set.
        
        Parameters
        ----------
        message_id : `int`
            The message's identifier.
        
        Returns
        -------
        self : ``Message``
        """
        self = object.__new__(cls)
        self.id = message_id
        self.channel_id = 0
        self.guild_id = 0
        self.author = ZEROUSER
        self._fields = {MESSAGE_FIELD_KEY_PARTIAL: None}
        return self
    
    # Message.activity
    
    @property
    def activity(self):
        """
        Sent with rich presence related embeds.
        
        Defaults to `None`.
        
        Returns
        -------
        activity : `None` or ``MessageActivity``
        """
        fields = self._fields
        if (fields is not None):
            return fields.get(MESSAGE_FIELD_KEY_ACTIVITY, None)
    
    @activity.setter
    def activity(self, activity):
        fields = self._fields
        
        if (fields is None):
            if (activity is None):
                return
            
            self._fields = fields = {}
        else:
            if (activity is None):
                try:
                    del fields[MESSAGE_FIELD_KEY_ACTIVITY]
                except KeyError:
                    pass
                else:
                    if not fields:
                        self._fields = None
            return
        
        fields[MESSAGE_FIELD_KEY_ACTIVITY] = activity
    
    @activity.deleter
    def activity(self):
        fields = self._fields
        if (fields is not None):
            try:
                del fields[MESSAGE_FIELD_KEY_ACTIVITY]
            except KeyError:
                pass
            else:
                if not fields:
                    self._fields = None
    
    
    def has_activity(self):
        """
        Returns whether the message has ``.activity`` set.
        
        Returns
        -------
        has_activity : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_ACTIVITY,
        )
    
    # Message.application
    
    @property
    def application(self):
        """
        Sent with rich presence related embeds.
        
        Defaults to `None`.
        
        Returns
        -------
        application : `None` or ``MessageApplication``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_APPLICATION,
        )
    
    @application.setter
    def application(self, application):
        if application is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_APPLICATION,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_APPLICATION,
                application,
            )
    
    @application.deleter
    def application(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_APPLICATION,
        )
    
    
    def has_application(self):
        """
        Returns whether the message has ``.application`` set.
        
        Returns
        -------
        has_application : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_APPLICATION,
        )
    
    # Message.application_id
    
    @property
    def application_id(self):
        """
        The application's identifier who sent the message.
        
        Defaults to `0`.
        
        Returns
        -------
        application_id : `int`
        """
        fields = self._fields
        if (fields is not None):
            return fields.get(MESSAGE_FIELD_KEY_APPLICATION_ID, 0)
    
    @application_id.setter
    def application_id(self, application_id):
        if application_id:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_APPLICATION_ID,
                application_id,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_APPLICATION_ID,
            )
    
    @application_id.deleter
    def application_id(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_APPLICATION_ID,
        )
    
    
    def has_application_id(self):
        """
        Returns whether the message has ``.application_id`` set.
        
        Returns
        -------
        has_application_id : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_APPLICATION_ID,
        )
    
    # Message.attachments
    
    @property
    def attachments(self):
        """
        Attachments sent with the message.
        
        Defaults to `None`.
        
        Returns
        -------
        attachments : `None` or `tuple` of ``Attachment``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_ATTACHMENTS,
        )
    
    @attachments.setter
    def attachments(self, attachments):
        if attachments is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_ATTACHMENTS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_ATTACHMENTS,
                attachments,
            )
    
    @attachments.deleter
    def attachments(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_ATTACHMENTS,
        )
    
    
    def has_attachments(self):
        """
        Returns whether the message has ``.attachments`` set.
        
        Returns
        -------
        has_attachments : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_ATTACHMENTS,
        )
    
    
    @property
    def attachment(self):
        """
        Returns the first attachment in the message.

        Returns
        -------
        attachment : `None` or ``Attachment``
        """
        return _get_first_message_field(
            self,
            MESSAGE_FIELD_KEY_ATTACHMENTS,
        )
    
    # Message.channel_mentions
    
    def _get_channel_mentions(self):
        """
        Looks up the ``.contents`` of the message and searches channel mentions in them.
        
        Invalid channel mentions are ignored.
        
        Returns
        -------
        channel_mentions : `None` or `tuple` of (``GuildChannelBase``, ``UnknownCrossMention``) instances.
            The parsed channel mentions.
        """
        content = self.content
        if content is None:
            channel_mentions = None
        else:
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
        
        return channel_mentions
    
    
    @property
    def channel_mentions(self):
        """
        The mentioned channels by the message. If there is non, returns `None`.
        
        Returns
        -------
        channel_mentions : `None` or (`tuple` of (``ChannelBase`` or ``UnknownCrossMentions`` instances))
        """
        fields = self._fields
        if fields is None:
            self._fields = fields = {}
        else:
            try:
                return fields[MESSAGE_FIELD_KEY_CHANNEL_MENTIONS]
            except KeyError:
                pass
        
        channel_mentions = self._get_channel_mentions()
        fields[MESSAGE_FIELD_KEY_CHANNEL_MENTIONS] = channel_mentions
        return channel_mentions
    
    @channel_mentions.deleter
    def channel_mentions(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_CHANNEL_MENTIONS,
        )
    
    
    def has_channel_mentions(self):
        """
        Returns whether the message has ``.channel_mentions`` set.
        
        Returns
        -------
        has_channel_mentions : `bool`
        """
        return (self.channel_mentions is not None)
    
    # Message.components
    
    @property
    def components(self):
        """
        Message components.
        
        Defaults to `None`.
        
        Returns
        -------
        components : `None` or `tuple` of ``ComponentBase``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_COMPONENTS,
        )
    
    @components.setter
    def components(self, components):
        if components is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_COMPONENTS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_COMPONENTS,
                components,
            )
    
    @components.deleter
    def components(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_COMPONENTS,
        )
    
    
    def has_components(self):
        """
        Returns whether the message has ``.components`` set.
        
        Returns
        -------
        has_components : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_COMPONENTS,
        )
    
    # Message.content
    
    @property
    def content(self):
        """
        The message's content.
        
        Defaults to `None`.
        
        Returns
        -------
        content : `None` or `str`
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_CONTENT,
        )
    
    @content.setter
    def content(self, content):
        if content is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_CONTENT,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_CONTENT,
                content,
            )
    
    @content.deleter
    def content(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_CONTENT,
        )
    
    
    def has_content(self):
        """
        Returns whether the message has ``.content`` set.
        
        Returns
        -------
        has_content : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_CONTENT,
        )
    
    # cross mentions
    
    @property
    def cross_mentions(self):
        """
        Cross guild channel mentions of a crosspost message if applicable. If a channel is not loaded by the wrapper,
        then it will be represented with a ``UnknownCrossMention`` instead.
        
        Defaults to `None`.
        
        Returns
        -------
        cross_mentions : `None` or `tuple` of (``UnknownCrossMention`` or ``ChannelBase`` instances)
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_CROSS_MENTIONS,
        )
    
    @cross_mentions.setter
    def cross_mentions(self, cross_mentions):
        if cross_mentions is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_CROSS_MENTIONS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_CROSS_MENTIONS,
                cross_mentions,
            )
    
    @cross_mentions.deleter
    def cross_mentions(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_CROSS_MENTIONS,
        )
    
    
    def has_cross_mentions(self):
        """
        Returns whether the message has ``.cross_mentions`` set.
        
        Returns
        -------
        has_cross_mentions : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_CROSS_MENTIONS,
        )
    
    # Message.referenced_message
    
    @property
    def referenced_message(self):
        """
        The referenced message. Set as ``Message`` instance if the message is cached, else as ``MessageReference``.
        
        Set when the message is a reply, a crosspost or when is a pin message.
        
        Defaults to `None`.
        
        Returns
        -------
        referenced_message : `None`, ``Message`` or ``MessageReference``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_REFERENCED_MESSAGE,
        )
    
    @referenced_message.setter
    def referenced_message(self, referenced_message):
        if referenced_message is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_REFERENCED_MESSAGE,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_REFERENCED_MESSAGE,
                referenced_message,
            )
    
    @referenced_message.deleter
    def referenced_message(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_REFERENCED_MESSAGE,
        )
    
    
    def has_referenced_message(self):
        """
        Returns whether the message has ``.referenced_message`` set.
        
        Returns
        -------
        has_referenced_message : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_REFERENCED_MESSAGE,
        )
    
    # Message.deleted
    
    @property
    def deleted(self):
        """
        Returns whether the message is deleted.
        
        Defaults to `False`.
        
        Returns
        -------
        deleted : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_DELETED,
        )
    
    @deleted.setter
    def deleted(self, deleted):
        if deleted:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_DELETED,
                None,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_DELETED,
            )
    
    @deleted.deleter
    def deleted(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_DELETED,
        )
    
    
    def has_deleted(self):
        """
        Returns whether the message has ``.deleted`` set.
        
        Returns
        -------
        has_deleted : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_DELETED,
        )
    
    # Message.exited_at
    
    @property
    def edited_at(self):
        """
        The time when the message was edited, or `None` if it was not.
        
        Pinning or (un)suppressing a message will not change it's edited value.
        
        Defaults to `None`.
        
        Returns
        -------
        edited_at : `None` or `datetime`
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_EDITED_AT,
        )
    
    @edited_at.setter
    def edited_at(self, edited_at):
        if edited_at is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_EDITED_AT,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_EDITED_AT,
                edited_at,
            )
    
    @edited_at.deleter
    def edited_at(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_EDITED_AT,
        )
    
    
    def has_edited_at(self):
        """
        Returns whether the message has ``.edited_at`` set.
        
        Returns
        -------
        has_edited_at : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_EDITED_AT,
        )
    
    # Message.embeds
    
    @property
    def embeds(self):
        """
        A tuple of embeds included with the message if any.
        
        If a message contains links, then those embeds' might not be included with the source payload and those
        will be added only later.
        
        Defaults to `None`.
        
        Returns
        -------
        embeds : `None` or `tuple` of ``EmbedCore``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_EMBEDS,
        )
    
    @embeds.setter
    def embeds(self, embeds):
        if embeds is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_EMBEDS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_EMBEDS,
                embeds,
            )
    
    @embeds.deleter
    def embeds(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_EMBEDS,
        )
    
    
    def has_embeds(self):
        """
        Returns whether the message has ``.embeds`` set.
        
        Returns
        -------
        has_embeds : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_EMBEDS,
        )
    
    
    @property
    def embed(self):
        """
        Returns the first embed in the message.

        Returns
        -------
        embed : `None` or ``EmbedCore``
        """
        return _get_first_message_field(
            self,
            MESSAGE_FIELD_KEY_EMBEDS,
        )
    
    # Message.everyone_mention
    
    @property
    def everyone_mention(self):
        """
        Whether the message contains `@everyone` or `@here`.
        
        Defaults to `False`.
        
        Returns
        -------
        everyone_mention : `bool`
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_EVERYONE_MENTION,
        )
    
    @everyone_mention.setter
    def everyone_mention(self, everyone_mention):
        if everyone_mention:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_EVERYONE_MENTION,
                None,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_EVERYONE_MENTION,
            )
    
    @everyone_mention.deleter
    def everyone_mention(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_EVERYONE_MENTION,
        )
    
    
    def has_everyone_mention(self):
        """
        Returns whether the message has ``.everyone_mention`` set.
        
        Returns
        -------
        has_everyone_mention : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_EVERYONE_MENTION,
        )
    
    # Message.flags
    
    @property
    def flags(self):
        """
        The message's flags.
        
        Defaults to `MessageFlag(0)`.
        
        Returns
        -------
        flags : ``MessageFlag``
        """
        fields = self._fields
        if fields is None:
            flags = MESSAGE_FLAGS_EMPTY
        else:
            flags = fields.get(MESSAGE_FIELD_KEY_FLAGS, MESSAGE_FLAGS_EMPTY)
        
        return flags
    
    @flags.setter
    def flags(self, flags):
        if flags:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_FLAGS,
                flags,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_FLAGS,
            )
    
    @flags.deleter
    def flags(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_FLAGS,
        )
    
    
    def has_flags(self):
        """
        Returns whether the message has ``.flags`` set.
        
        Returns
        -------
        has_flags : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_FLAGS,
        )
    
    # Message.interaction
    
    @property
    def interaction(self):
        """
        Present if the message is a response to an ``InteractionEvent``.
        
        Defaults to `None`.
        
        Returns
        -------
        interaction : `None` or ``MessageInteraction``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_INTERACTION,
        )
    
    @interaction.setter
    def interaction(self, interaction):
        if interaction is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_INTERACTION,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_INTERACTION,
                interaction,
            )
    
    @interaction.deleter
    def interaction(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_INTERACTION,
        )
    
    
    def has_interaction(self):
        """
        Returns whether the message has ``.interaction`` set.
        
        Returns
        -------
        has_interaction : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_INTERACTION,
        )
    
    # Message.partial
    
    @property
    def partial(self):
        """
        Returns whether the message is partial.
        
        Defaults to `False`.
        
        Returns
        -------
        partial : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_PARTIAL,
        )
    
    @partial.setter
    def partial(self, partial):
        if partial:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_PARTIAL,
                None,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_PARTIAL,
            )
    
    @partial.deleter
    def partial(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_PARTIAL,
        )
    
    
    def has_partial(self):
        """
        Returns whether the message has ``.partial`` set.
        
        Returns
        -------
        has_partial : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_PARTIAL,
        )
    
    # Message.nonce
    
    @property
    def nonce(self):
        """
        A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
        be shown up at the message's received payload as well.
        
        Defaults to `None`.
        
        Returns
        -------
        nonce : `None` or `str`
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_NONCE,
        )
    
    @nonce.setter
    def nonce(self, nonce):
        if nonce is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_NONCE,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_NONCE,
                nonce,
            )
    
    @nonce.deleter
    def nonce(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_NONCE,
        )
    
    
    def has_nonce(self):
        """
        Returns whether the message has ``.nonce`` set.
        
        Returns
        -------
        has_nonce : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_NONCE,
        )
    
    # Message.pinned
    
    @property
    def pinned(self):
        """
        Whether the message is pinned.
        
        Defaults to `False`.
        
        Returns
        -------
        pinned : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_PINNED,
        )
    
    @pinned.setter
    def pinned(self, pinned):
        if pinned:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_PINNED,
                None,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_PINNED,
            )
    
    @pinned.deleter
    def pinned(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_PINNED,
        )
    
    
    def has_pinned(self):
        """
        Returns whether the message has ``.pinned`` set.
        
        Returns
        -------
        has_pinned : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_PINNED,
        )
    
    # Message.reactions
    
    @property
    def reactions(self):
        """
        A dictionary like object, which contains the reactions on the message.
        
        Defaults to `None`.
        
        Returns
        -------
        reactions : `None` or ``reaction_mapping``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_REACTIONS,
        )
    
    @reactions.setter
    def reactions(self, reactions):
        if reactions is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_REACTIONS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_REACTIONS,
                reactions,
            )
    
    @reactions.deleter
    def reactions(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_REACTIONS,
        )
    
    
    def has_reactions(self):
        """
        Returns whether the message has ``.reactions`` set.
        
        Returns
        -------
        has_reactions : `bool`
        """
        fields = self._fields
        if (fields is None):
            has_reactions = False
        else:
            try:
                reactions = fields[MESSAGE_FIELD_KEY_REACTIONS]
            except KeyError:
                has_reactions = False
            else:
                if reactions:
                    has_reactions = True
                else:
                    has_reactions = False
        
        return has_reactions
    

    # Message.role_mention_ids
    
    @property
    def role_mention_ids(self):
        """
        The mentioned roles's identifier by the message if any.
        
        Defaults to `None`.
        
        Returns
        -------
        role_mention_ids : `None` or `tuple` of `int`
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
        )
    
    @role_mention_ids.setter
    def role_mention_ids(self, role_mention_ids):
        if role_mention_ids is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
                role_mention_ids,
            )
    
    @role_mention_ids.deleter
    def role_mention_ids(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
        )
    
    
    def has_role_mention_ids(self):
        """
        Returns whether the message has ``.role_mention_ids`` set.
        
        Returns
        -------
        has_role_mention_ids : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
        )
    
    # Message.role_mentions
    
    def _get_role_mentions(self):
        """
        Creates role instances from the the mentioned role id-s. If a mentioned role is not found, creates a new
        partial one.
        
        Returns
        -------
        role_mentions : `None` or `tuple` of ``Role``
        """
        fields = self._fields
        if (fields is None):
            role_mentions = None
        else:
            try:
                role_mention_ids = fields[MESSAGE_FIELD_KEY_ROLE_MENTION_IDS]
            except KeyError:
                role_mentions = None
            else:
                role_mentions = tuple(create_partial_role_from_id(role_id) for role_id in role_mention_ids)
        
        return role_mentions
    
    
    @property
    def role_mentions(self):
        """
        The mentioned roles by the message. If there is non, returns `None`.
        
        Returns
        -------
        role_mentions : `None` or `tuple` of ``Role``
        """
        fields = self._fields
        if fields is None:
            self._fields = fields = {}
        else:
            try:
                return fields[MESSAGE_FIELD_KEY_ROLE_MENTIONS]
            except KeyError:
                pass
        
        role_mentions = self._get_role_mentions()
        fields[MESSAGE_FIELD_KEY_ROLE_MENTIONS] = role_mentions
        return role_mentions
    
    @role_mentions.deleter
    def role_mentions(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_ROLE_MENTIONS,
        )
    
    
    def has_role_mentions(self):
        """
        Returns whether the message has ``.role_mentions`` set.
        
        Returns
        -------
        has_role_mentions : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_ROLE_MENTION_IDS,
        )
    
    # Message.stickers
    
    @property
    def stickers(self):
        """
        The stickers sent with the message.
        
        Defaults to `None`.
        
        Returns
        -------
        stickers : `None` or `tuple` of ``Sticker``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_STICKERS,
        )
    
    @stickers.setter
    def stickers(self, stickers):
        if stickers is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_STICKERS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_STICKERS,
                stickers,
            )
    
    @stickers.deleter
    def stickers(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_STICKERS,
        )
    
    
    def has_stickers(self):
        """
        Returns whether the message has ``.stickers`` set.
        
        Returns
        -------
        has_stickers : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_STICKERS,
        )
    
    
    @property
    def sticker(self):
        """
        Returns the first sticker in the message.

        Returns
        -------
        sticker : `None` or ``Sticker``
        """
        return _get_first_message_field(
            self,
            MESSAGE_FIELD_KEY_STICKERS,
        )
    
    # Message.thread
    
    @property
    def thread(self):
        """
        The thread which was started from this message.
        
        Defaults to `None`.
        
        Returns
        -------
        thread : `None` or ``ChannelThread``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_THREAD,
        )
    
    @thread.setter
    def thread(self, thread):
        if thread is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_THREAD,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_THREAD,
                thread,
            )
    
    @thread.deleter
    def thread(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_THREAD,
        )
    
    
    def has_thread(self):
        """
        Returns whether the message has ``.thread`` set.
        
        Returns
        -------
        has_thread : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_THREAD,
        )
    
    # Message.tts
    
    @property
    def tts(self):
        """
        Whether the message is "text to speech".
        
        Defaults to `False`.
        
        Returns
        -------
        tts : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_TTS,
        )
    
    @tts.setter
    def tts(self, tts):
        if tts:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_TTS,
                None,
            )
        else:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_TTS,
            )
    
    @tts.deleter
    def tts(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_TTS,
        )
    
    
    def has_tts(self):
        """
        Returns whether the message has ``.tts`` set.
        
        Returns
        -------
        has_tts : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_TTS,
        )
    
    # Message.type
    
    @property
    def type(self):
        """
        The type of the message.
        
        Defaults to `None`.
        
        Returns
        -------
        type : ``MessageType``
        """
        fields = self._fields
        if (fields is None):
            type_ = MESSAGE_TYPE_DEFAULT
        else:
            type_ = fields.get(MESSAGE_FIELD_KEY_TYPE, MESSAGE_TYPE_DEFAULT)
        
        return type_
    
    @type.setter
    def type(self, type_):
        fields = self._fields
        
        if (fields is None):
            if (type_ is MESSAGE_TYPE_DEFAULT):
                return
            
            self._fields = fields = {}
        else:
            if (type_ is MESSAGE_TYPE_DEFAULT):
                try:
                    del fields[MESSAGE_FIELD_KEY_TYPE]
                except KeyError:
                    pass
                else:
                    if not fields:
                        self._fields = None
            return
        
        fields[MESSAGE_FIELD_KEY_TYPE] = type_
    
    @type.deleter
    def type(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_TYPE,
        )
    
    
    def has_type(self):
        """
        Returns whether the message has ``.type`` set.
        
        Returns
        -------
        has_type : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_TYPE,
        )
    
    # Message.user_mentions
    
    @property
    def user_mentions(self):
        """
        The mentioned users by the message if any.
        
        Defaults to `None`.
        
        Returns
        -------
        user_mentions : `None` or `tuple` of ``UserBase``
        """
        return _get_message_field(
            self,
            MESSAGE_FIELD_KEY_USER_MENTIONS,
        )
    
    @user_mentions.setter
    def user_mentions(self, user_mentions):
        if user_mentions is None:
            _remove_message_field(
                self,
                MESSAGE_FIELD_KEY_USER_MENTIONS,
            )
        else:
            _set_message_field(
                self,
                MESSAGE_FIELD_KEY_USER_MENTIONS,
                user_mentions,
            )
    
    @user_mentions.deleter
    def user_mentions(self):
        _remove_message_field(
            self,
            MESSAGE_FIELD_KEY_USER_MENTIONS,
        )
    
    
    def has_user_mentions(self):
        """
        Returns whether the message has ``.user_mentions`` set.
        
        Returns
        -------
        has_user_mentions : `bool`
        """
        return _has_message_field(
            self,
            MESSAGE_FIELD_KEY_USER_MENTIONS,
        )
