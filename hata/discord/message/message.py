__all__ = (
    'EMBED_UPDATE_EMBED_ADD', 'EMBED_UPDATE_EMBED_REMOVE', 'EMBED_UPDATE_NONE', 'EMBED_UPDATE_SIZE_UPDATE', 'Message'
)

import warnings
from datetime import datetime

from scarletio import BaseMethodDescriptor, export, include

from ..bases import DiscordEntity, id_sort_key
from ..core import CHANNELS, GUILDS, MESSAGES
from ..component import Component
from ..embed import EXTRA_EMBED_TYPES, EmbedBase, EmbedCore
from ..emoji import ReactionMapping, merge_update_reaction_mapping
from ..http import urls as module_urls
from ..preconverters import (
    get_type_names, preconvert_bool, preconvert_flag, preconvert_preinstanced_type, preconvert_snowflake,
    preconvert_snowflake_array, preconvert_str
)
from ..role import Role, create_partial_role_from_id
from ..sticker import Sticker
from ..user import ClientUserBase, User, UserBase, ZEROUSER
from ..utils import (
    CHANNEL_MENTION_RP, DATETIME_FORMAT_CODE, datetime_to_id, datetime_to_timestamp, id_to_datetime,
    timestamp_to_datetime
)
from ..webhook import Webhook, WebhookRepr, WebhookType, create_partial_webhook_from_id

from .attachment import Attachment
from .cross_mention import UnknownCrossMention
from .flags import MessageFlag
from .message_activity import MessageActivity
from .message_application import MessageApplication
from .message_interaction import MessageInteraction
from .preinstanced import GENERIC_MESSAGE_TYPES, MESSAGE_DEFAULT_CONVERTER, MessageType
from .utils import try_resolve_interaction_message


Channel = include('Channel')
ChannelType = include('ChannelType')
InteractionType = include('InteractionType')
create_partial_channel_from_id = include('create_partial_channel_from_id')


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


MESSAGE_TYPE_VALUES_WITH_CONTENT_FIELDS = frozenset((
    message_type.value
    for message_type in MessageType.INSTANCES.values()
    if message_type.converter is MESSAGE_DEFAULT_CONVERTER
))

MESSAGE_CONTENT_FIELDS = (
    MESSAGE_FIELD_KEY_CONTENT,
    MESSAGE_FIELD_KEY_EMBEDS,
    MESSAGE_FIELD_KEY_ATTACHMENTS,
    MESSAGE_FIELD_KEY_COMPONENTS,
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
    value : `None`, `Any`
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
    value : `None`, `Any`
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


def _iter_message_field(message, field_key):
    """
    Iterates over a field of the message.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    message : ``Message``
        The message to get the field from.
    field_key : `int`
        Message field key to get.
    
    Yields
    ------
    value : `Any`
    """
    fields = message._fields
    if (fields is not None):
        try:
            field_value = fields[field_key]
        except KeyError:
            pass
        else:
            yield from field_value


@export
class Message(DiscordEntity, immortal = True):
    """
    Represents a message from Discord.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the message.
    _fields : `bool`
        Optional fields of the message.
    author : ``UserBase``
        The author of the message. Can be any user type and if not found, then set as `ZEROUSER`.
    channel_id : `int`
        The channel's identifier where the message is sent.
    guild_id : `int`
        The channel's guild's identifier.
    
    Notes
    -----
    Message instances are weakreferable.
    
    The `content`, `embeds`, `attachments` and the `components` fields are restricted for the message content intent.
    
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
        `.__new__` will be repurposed. Please use `.from_data` instead.
        """
        warnings.warn(
            f'`{cls.__name__}.__new__` will be repurposed. Please use `.from_data` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return cls.from_data(data)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message object form the given message payload. If the message already exists, picks it up.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        
        Returns
        -------
        self : ``Message``
        """
        message_id = int(data['id'])
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = message_id
            MESSAGES[message_id] = self
        
        else:
            if not self.partial:
                if self.flags.loading:
                    self._set_attributes(data)
                
                elif not self.has_any_content_field():
                    self._update_content_fields(data)
                
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
            MESSAGES[message_id] = self
        
        else:
            if not self.partial:
                if self.flags.loading:
                    self._set_attributes(data)
                
                elif not self.has_any_content_field():
                    self._update_content_fields(data)
                
                return True, self
        
        self._fields = None
        self._set_attributes(data)
        return False, self
    
    
    @classmethod
    def _create_from_partial_data(cls, data):
        """
        Creates a message from message reference data.
        
        If the message is loaded already, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message reference data.
        
        Returns
        -------
        self : ``Message``
        """
        while True:
            try:
                message_id = data['message_id']
            except KeyError:
                pass
            else:
                message_id = int(message_id)
                break
            
            try:
                message_id = data['id']
            except KeyError:
                pass
            else:
                message_id = int(message_id)
                break
            
            message_id = 0
            break
        
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = message_id
            
            if message_id:
                MESSAGES[message_id] = self
        else:
            if not self.partial:
                return self
        
        # `._fields`
        self._fields = None
        
        # `.author`
        self.author = ZEROUSER
        
        # `.channel_id`
        channel_id = data.get('channel_id', None)
        if channel_id is None:
            channel_id = 0
        else:
            channel_id = int(channel_id)
        self.channel_id = channel_id
        
        # `.guild_id`
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        self.guild_id = guild_id
        return self
    
    
    @classmethod
    def _create_from_partial_fields(cls, message_id, channel_id, guild_id):
        """
        Creates a new message from the given fields describing it.
        
        Parameters
        ----------
        message_id : `int`
            The unique identifier number of the represented message.
        channel_id : `int`
            The respective message's channel's identifier.
        guild_id : `int`
            The respective message's guild's identifier.
        
        Returns
        -------
        self : ``Message``
        """
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
        self.author = ZEROUSER
        self.channel_id = channel_id
        self.guild_id = guild_id
        
        return self
    
    
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
        
        try:
            guild_id = data['guild_id']
        except KeyError:
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                guild_id = 0
            else:
                guild_id = channel.guild_id
        else:
            if guild_id is None:
                guild_id = 0
            else:
                guild_id = int(guild_id)
        
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
                author = User.from_data(author_data, data.get('member', None), guild_id)
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
                merge_update_reaction_mapping(
                    _get_message_field(
                        self,
                        MESSAGE_FIELD_KEY_REACTIONS,
                    ),
                    ReactionMapping.from_data(reactions_data),
                )
            )
        
        referenced_message_data = data.get('referenced_message', None)
        if referenced_message_data is None:
            referenced_message_data = data.get('message_reference', None)
            if referenced_message_data is None:
                referenced_message = None
            else:
                referenced_message = self._create_from_partial_data(referenced_message_data)
        else:
            referenced_message = type(self).from_data(referenced_message_data)
        
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
                tuple(Attachment.from_data(attachment) for attachment in attachment_datas),
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
            interaction = MessageInteraction(interaction_data, guild_id)
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
                tuple(Component.from_data(component_data) for component_data in component_datas),
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
                    (
                        User.from_data(user_mention_data, user_mention_data.get('member', None), guild_id)
                        for user_mention_data in user_mention_datas
                    ),
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
                Channel.from_data(thread_data, None, guild_id),
            )
    
    
    def _late_init(self, data):
        """
        Some message fields might be missing after receiving a payload. This method is called to check and set those
        if multiple payload is received.
        
        The fields are:
        
        - `content`
        - `components`
        - `embeds`
        - `interaction`
        
        Since we update the content fields anyways, in this method we only update the `interaction` field.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data.
        """
        if self.flags.loading:
            self._set_attributes(data)
            return
        
        fields = self._fields
        if (fields is None):
            update_interaction = True
        else:
            update_interaction = (MESSAGE_FIELD_KEY_INTERACTION not in fields)
        
        if update_interaction:
            interaction_data = data.get('interaction', None)
            if (interaction_data is not None):
                interaction = MessageInteraction(interaction_data, self.guild_id)
                try_resolve_interaction_message(self, interaction)
                
                _set_message_field(
                    self,
                    MESSAGE_FIELD_KEY_INTERACTION,
                    interaction,
                )
    
    
    @BaseMethodDescriptor
    def custom(cls, base, validate=True, **kwargs):
        """
        Creates a custom message. If called as a method of a message, then the attributes of the created custom message
        will default to that message's. Meanwhile if called as a classmethod, then the attributes of the created
        custom message will default to the overall defaults.
        
        Parameters
        ----------
        validate : `bool` = `True`, Optional
            Whether contradictory between the message's attributes can be checked. If there is any, `ValueError`
            is raised.
        **kwargs : keyword parameters
            Additional attributes of the created message.
        
        Other Parameters
        ----------------
        activity : `None`, ``MessageActivity``, Optional (Keyword only)
            The ``.activity`` attribute the message.
            
            If called as classmethod defaults to `None`.
        
        application : `None`, ``MessageApplication``., Optional (Keyword only)
            The ``.application`` attribute the message.
            
            If called as a classmethod defaults to `None`.
        
        application_id : `int`, Optional (Keyword Only)
            The ``.application_id`` attribute of the message.
            
            If called as a classmethod defaults to `0`.
        
        attachments : `None`, ((`list`, `tuple`) of ``Attachment``), Optional (Keyword only)
            The ``.attachments`` attribute of the message. If passed as an empty list, then will be as `None` instead.
            
            If called as a classmethod defaults to `None`.
        
        author : `None`, ``ClientUserBase``, ``Webhook``, ``WebhookRepr``, Optional (Keyword only)
            The ``.author`` attribute of the message. If passed as `None` then it will be set as `ZEROUSER` instead.
            
            If called as a classmethod, defaults to `ZEROUSER`.
        
        channel_id : ``Channel``, `int`, Optional if called as method (Keyword only)
            The ``.channel_id`` attribute of the message.
            
            If called as a classmethod this attribute must be passed, or `TypeError` is raised.
        
        components : `None`, (`list`, `tuple`) of ``Component``, Optional (Keyword only)
            The ``.components`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        
        content : `None`, `str`, Optional (Keyword only)
            The ``.content`` attribute of the message. Can be between length `0` and `4000`.
            
            If called as a classmethod defaults to `''` (empty string).
        
        cross_mentions : `None`, (`tuple`, `list`) of (``UnknownCrossMention``, ``Channel``)
                , Optional (Keyword only)
            The `.cross_mentions` attribute of the message. If passed as an empty list, then will be set `None` instead.
            
            If called as a classmethod defaults to `None`.
        
        referenced_message : `None`, ``Message``, Optional (Keyword only)
            The ``.referenced_message`` attribute of the message.
            
            If called as a classmethod defaults to `None`.
        
        deleted : `bool`, Optional (Keyword only)
            The ``.deleted`` attribute of the message. If called as a class method, defaults to `True`.
        
        edited_at : `None`, `datetime`, Optional (Keyword only)
            The ``.edited_at`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        
        embeds : `None`, (`list`, `tuple`) of ``EmbedBase``, Optional (Keyword only)
            The ``.embeds`` attribute of the message. If passed as an empty list, then is set as `None` instead. If
            passed as list and it contains any embeds, which are not type ``EmbedCore``, then those will be converted
            to ``EmbedCore`` as well.
            
            If called as a classmethod defaults to `None`.
        
        everyone_mention : `bool`, `int` (`0`, `1`), Optional (Keyword only)
            The ``.everyone_mention`` attribute of the message. Accepts other `int` as `bool` as well, but
            their value still cannot be other than `0`, `1`.
            
            If called as a classmethod, defaults to `False`.
        
        flags : ``MessageFlag``, `int`, Optional (Keyword only)
            The ``.flags`` attribute of the message. If passed as other `int` than ``MessageFlag``, then will
            be converted to ``MessageFlag``.
            
            If called as a classmethod defaults to `MessageFlag(0)`.
        
        interaction : `None`, ``MessageInteraction``, Optional (Keyword only)
           The `.interaction` attribute of the message.
        
            If called as a classmethod defaults to `None`.
        
        id : `int`, `str`, Optional (Keyword only)
            The ``.id`` attribute of the message. If passed as `str`, will be converted to `int`.
            
            If called as a classmethod defaults to `0`.
        
        id_ : `int`, `str`, Optional (Keyword only)
            Alias of `id`.
        
        message_id : `int`, `str`, Optional (Keyword only)
            Alias of `id`.
        
        nonce : `None`, `str`, Optional (Keyword only)
            The ``.nonce`` attribute of the message. If passed as `str` can be between length `0` and `32`.
            
            If called as a classmethod defaults to `None`.
        
        pinned : `bool`, `int` (`0`, `1`), Optional (Keyword only)
            The ``.pinned`` attribute of the message. Accepts other `int` as `bool` as well, but their value
            still cannot be other than `0`, `1`.
            
            If called as a classmethod, defaults to `False`.
        
        reactions : `None`, ``ReactionMapping``, Optional (Keyword only)
            The ``.reactions`` attribute of the message.
            
            If called as a classmethod defaults to `None`.
        
        role_mentions : `None`, (`list`, `tuple`) of ``Role``, Optional (Keyword only)
            The ``.role_mentions`` attribute of the message. If passed as an empty `list`, will be set as `None`
            instead.
            
            If called as a classmethod defaults to `None`.
        
        stickers : `None`, (`list`, `tuple`) of ``Sticker``, Optional (Keyword only)
            The ``.stickers`` attribute of the message.
            
            If called as a classmethod, defaults to `None`.
        
        thread : `None`, ``Channel``
            The ``.thread`` attribute of the message.
            
            If called as a classmethod defaults to `None`.
        
        tts : `bool`, `int` (`0`, `1`), Optional (Keyword only)
            The ``.tts`` attribute of the message. Accepts other `int` as `bool` as well, but their value
            still cannot be other than `0`, `1`.
            
            If called as a classmethod, defaults to `False`.
        
        type : ``MessageType``, `int`, Optional (Keyword only)
            The ``.type`` attribute of the message. If passed as `int`, it will be converted to it's wrapper side
            ``MessageType`` representation.
            
            If called as a classmethod defaults to `MessageType.default`
        
        type_ : ``MessageType``, `int`, Optional (Keyword only)
            Alias of ``type`.
        
        user_mentions : `None`, `list`, `tuple`  of ``UserBase``, Optional (Keyword only)
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
            raise TypeError(f'`base` can be `None`, or type `{cls.__name__}`, got `{base!r}`')
        
        try:
            channel = kwargs.pop('channel')
        except KeyError:
            
            try:
                channel_id = kwargs.pop('channel_id')
            except KeyError:
                if base is None:
                    raise TypeError(
                        '`channel_id` is a required parameter if called as a classmethod.'
                    )
                
                channel_id = base.channel_id
                channel = None
            else:
                if isinstance(channel_id, int):
                    channel = None
                elif isinstance(channel_id, Channel):
                    channel = channel_id
                    channel_id = channel_id.id
                else:
                    raise TypeError(
                        f'`channel_id` can be `int`, `{Channel.__name__}`, got `{channel_id!r}`.'
                    )
            
            if (channel is None):
                channel = CHANNELS.get(channel_id, None)
        
            if channel is None:
                guild_id = 0
            else:
                guild_id = channel.guild_id
        
        else:
            warnings.warn(
                (
                    f'`{cls.__name__}.custom`\'s `channel` parameter is deprecated, and will be removed in 2022 '
                    f'January. Please use `channel_id` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            if not isinstance(channel, Channel):
                raise TypeError(
                    f'`channel` can be `{Channel.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                )
                
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
                raise TypeError(
                    f'`activity` can be `None` or type `{MessageActivity.__name__}`, got '
                    f'{activity.__class__.__name__}; {activity!r}.'
                )
        
        try:
            application = kwargs.pop('application')
        except KeyError:
            if base is None:
                application = None
            else:
                application = base.application
        else:
            if (application is not None) and (type(application) is not MessageApplication):
                raise TypeError(
                    f'`application` can be `None`, `{MessageApplication.__name__}`, got '
                    f'{application.__class__.__name__}; {application!r}.'
                )
        
        
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
                    raise TypeError(
                        f'`attachments` can be `None`, `tuple`, `list` of `{Attachment.__name__}`, got '
                        f'{attachments.__class__.__name__}; {attachments!r}'
                    )
                
                attachments = tuple(attachments)
                
                if attachments:
                    for attachment in attachments:
                        if not isinstance(attachment, Attachment):
                            raise TypeError(
                                f'`attachments` can contain `{Attachment.__name__}` elements, got '
                                f'{attachment.__class__.__name__}, {attachment!r}; attachments={attachment!r}.'
                            )
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
                # This can be the case
                pass
            else:
                raise TypeError(
                    f'`author` can be `None`, `{ClientUserBase.__name__}`, `{Webhook.__name__}`, '
                    f'`{WebhookRepr.__name__}`, got {author.__class__.__name__}; {author!r}.'
                )
        
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
            if (referenced_message is not None) and not isinstance(referenced_message, Message):
                raise TypeError(
                    f'`referenced_message` can be `None`, `{Message.__name__}`, got '
                    f'{referenced_message.__class__.__name__}; {referenced_message!r}.'
                )
        
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
                    raise TypeError(
                        f'`cross_mentions` can be `None`, `tuple`, `list` of `{Channel.__name__}` or '
                        f'`{UnknownCrossMention.__name__}`, got '
                        f'{cross_mentions.__class__.__name__}; {cross_mentions!r}.'
                    )
                
                cross_mentions_processed = []
                
                for channel_ in cross_mentions:
                    if not isinstance(channel_, (Channel, UnknownCrossMention)):
                        raise TypeError(
                            f'`cross_mentions` can contain `{Channel.__name__}`, '
                            f'`{UnknownCrossMention.__name__}` elements, got {channel_.__class__.__name__};'
                            f'{channel_!r}; cross_mentions={cross_mentions!r}.'
                        )
                    
                    cross_mentions_processed.append(channel_)
                
                if cross_mentions_processed:
                    cross_mentions_processed.sort(key = id_sort_key)
                    cross_mentions = tuple(cross_mentions_processed)
                else:
                    cross_mentions = None
        
        if validate:
            if (referenced_message is None) and (cross_mentions is not None):
                raise ValueError(
                    '`cross_mentions` are supported, only if `referenced_message` is provided'
                )
        
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
                raise TypeError(
                    f'`edited_at` can be `None`, `datetime`, got {edited_at.__class__.__name__}; {edited_at!r}.'
                )
        
        if validate:
            if (edited_at is not None) and (datetime_to_id(edited_at)<message_id):
                raise ValueError(
                    f'`edited_at` can not be lower, than `created_at`, got edited_at={edited_at!r}, '
                    f'created_at={id_to_datetime(message_id)}.'
                )
        
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
                    raise TypeError(
                        f'`embeds` can be `None`, `tuple`, `list` of `{EmbedBase.__name__}`, got '
                        f'{embeds.__class__.__name__}; {embeds!r}.'
                    )
                
                embeds = list(embeds)
                
                embeds_length = len(embeds)
                if validate:
                    if len(embeds) > 10:
                        raise ValueError(
                            f'A message can have up to `10` embeds, got {embeds_length!r}; {embeds!r}.'
                        )
                
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
                        
                        raise TypeError(
                            f'`embeds` can contain `{EmbedBase.__name__}` elements, got {embeds.__class__.__name__}; '
                            f'{embeds!r}; embeds={embeds!r}.'
                        )
                    
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
            if isinstance(channel, Channel):
                if flags.source_message_deleted and (not flags.is_crosspost):
                    raise ValueError(
                        '`flags.source_message_deleted` is set, but `flags.is_crosspost` is not -> Only crossposted '
                        'message\'s source can be deleted.'
                    )
                
                # Other cases?
            else:
                if flags.crossposted:
                    raise ValueError(
                        '`flags.crossposted` is set, meanwhile `channel` is not type '
                        f'`{Channel.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                    )
    
                if flags.is_crosspost:
                    raise ValueError(
                        '`flags.is_crosspost` is set, meanwhile `channel` is not type '
                        f'`{Channel.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                    )
    
                if flags.source_message_deleted:
                    raise ValueError(
                        '`flags.source_message_deleted` is set, meanwhile `channel` is not type '
                        f'`{Channel.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                    )
        
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
                    raise TypeError(
                        f'`nonce` can be `None`, `str`, got {nonce.__class__.__name__}; {nonce!r}.'
                    )
                
                nonce_length = len(nonce)
                if nonce_length > 32:
                    raise TypeError(
                        f'`nonce`\'s length can be be in range [1:32], got: {nonce_length!r}; {nonce!r}.'
                    )
                
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
                reactions = ReactionMapping()
            else:
                reactions = base.reactions
                if (reactions is not None):
                    # Copy it, because it might be modified
                    reactions = reactions.copy()
        else:
            if reactions is None:
                # Lets accept `None` and create an empty one
                reactions = ReactionMapping()
            elif type(reactions) is ReactionMapping:
                # We expect this as default
                pass
            else:
                raise TypeError(
                    f'`reactions`, can be `None`, `{ReactionMapping.__name__}`, got '
                    f'{reactions.__class__.__name__}; {reactions}.'
                )
        
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
                    raise TypeError(
                        f'`role_mentions` can be `None`, `list`, `tuple` of `{Role.__name__}`, got '
                        f'{role_mentions.__class__.__name__}; {role_mentions!r}.'
                    )
                
                if role_mentions:
                    for role in role_mentions:
                        if not isinstance(role, Role):
                            raise TypeError(
                                f'`role_mentions` can contain `{Role.__name__}` elements, got '
                                f'{role.__class__.__name__}; {role!r}; role_mentions={role_mentions!r}.'
                            )
                    
                else:
                    # There cannot be an empty mention list, so lets fix it.
                    role_mentions = None
        
        if validate:
            if (role_mentions is not None) and (not isinstance(channel, Channel)):
                raise ValueError(
                    f'`role_mentions` are only applicable for guild channels, got {channel.__class__.__name__}; '
                    f'{channel!r}; role_mentions={role_mentions!r}.'
                )
        
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
                raise TypeError(
                    f'`stickers` can be `None`, ` tuple`, `list` of `{Sticker.__name__}`, got '
                    f'{stickers.__class__.__name__}; {stickers!r}.'
                )
            
            stickers = tuple(stickers)
            
            stickers_length = len(stickers)
            if stickers_length:
                for sticker in stickers:
                    if not isinstance(sticker, Sticker):
                        raise TypeError(
                            f'`stickers` can contain `{Sticker.__name__}`, got'
                            f'{sticker.__class__.__name__}; {sticker!r}; stickers={stickers!r}.'
                        )
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
                    raise TypeError(
                        f'`user_mentions` can be `None`, `tuple`, `list` of `{UserBase.__name__}`, got '
                        f'{user_mentions.__class__.__name__}; {user_mentions!r}.'
                    )
                
                if user_mentions:
                    for user in user_mentions:
                        if not isinstance(user, UserBase):
                            raise TypeError(
                                f'`user_mentions`can contain `{UserBase.__name__}` elements, got '
                                f'{user.__class__.__name__}; {user!r}.'
                            )
                    
                    user_mentions = tuple(sorted(user_mentions, key = id_sort_key))
                    
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
                raise TypeError(
                    f'`interaction` can be `None`, `{MessageInteraction.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
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
                    raise TypeError(
                        f'`components` can be `None`, `tuple`, `list` of `{Component.__name__}` , got '
                        f'{components.__class__.__name__}; {components!r}.'
                    )
                
                components = tuple(components)
                
                if components:
                    for component in components:
                        if not isinstance(component, Component):
                            raise TypeError(
                                f'`components` can contain `{Component.__name__}` elements, got '
                                f'{component.__class__.__name__}; {component!r}.'
                            )
                    
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
            if (thread is not None) and (not isinstance(thread, Channel)):
                raise TypeError(
                    f'`thread` can be `None`, `{Channel.__name__}` , got '
                    f'{thread.__class__.__name__}; {thread!r}.'
                )
        
        # Check kwargs and raise TypeError if not every in used up
        if kwargs:
            raise TypeError(f'Unused parameters: {kwargs!r}.')
        
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
        >>>> from hata import Message, Channel, now_as_id
        >>>> message = Message.custom(content = 'Fluffy nekos', channel = Channel.precreate(now_as_id()))
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
        >>>> message = message.custom(edited_at=datetime.utcnow())
        >>>> message
        <Message id=0, ln=12, author=#0000>
        >>>> f'{message:e}'
        '2020.05.31-16:00:00'
        ```
        """
        if not code:
            return self.__repr__()
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        if code == 'e':
            edited_at = self.edited_at
            if edited_at is None:
                edited_at = 'never'
            else:
                edited_at = format(edited_at, DATETIME_FORMAT_CODE)
            return edited_at
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"e"!r}.'
        )
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the message and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.

        A special case is if a message is (un)pinned or (un)suppressed , because then the returned dict is not going to
        contain `'edited_at'`, only `'pinned'`, `'flags'`. If the embeds are (un)suppressed of the message, then the
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
        | attachments       | `None`, (`tuple` of ``Attachment``)                                   |
        +-------------------+-----------------------------------------------------------------------+
        | components        | `None`, (`tuple` of ``Component``)                                |
        +-------------------+-----------------------------------------------------------------------+
        | content           | `None`, `str`                                                         |
        +-------------------+-----------------------------------------------------------------------+
        | cross_mentions    | `None`, (`tuple` of (``Channel``, ``UnknownCrossMention``))           |
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
        | user_mentions     | `None`, (`tuple` of ``ClientUserBase``)                               |
        +-------------------+-----------------------------------------------------------------------+
        | role_mention_ids  | `None`, (`tuple` of `int`)                                            |
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
                attachments = tuple(Attachment.from_data(attachment) for attachment in attachment_datas)
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
                    (
                        User.from_data(user_mention_data, user_mention_data.get('member', None), self.guild_id)
                        for user_mention_data in user_mention_datas
                    ),
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
                components = tuple(Component.from_data(component_data) for component_data in component_datas)
            
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
        flag_difference = self.flags ^ flags
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
            user_mention_datas = data['mentions']
        except KeyError:
            pass
        else:
            if user_mention_datas:
                user_mentions = tuple(sorted(
                    (
                        User.from_data(user_mention_data, user_mention_data.get('member', None), self.guild_id)
                        for user_mention_data in user_mention_datas
                    ),
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
        
        
        self._update_content_fields(data)
    
    
    def _update_content_fields(self, data):
        """
        Updates the message's content attributes with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        """
        try:
            attachment_datas = data['attachments']
        except KeyError:
            pass
        else:
            if attachment_datas:
                attachments = tuple(Attachment.from_data(attachment) for attachment in attachment_datas)
            else:
                attachments = None
            self.attachments = attachments
        

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
                components = tuple(Component.from_data(component_data) for component_data in component_datas)
            self.components = components
        
        
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
        guild : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the message's channel's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
        
        if self.flags.invoking_user_only:
            try:
                channel = CHANNELS[self.channel_id]
            except KeyError:
                pass
            else:
                return channel.guild
    
    
    @property
    def clean_content(self):
        """
        Returns the message's clean content, what actually depends on the message's type. By default it is the
        message's content with transformed mentions, but for different message types it means different things.
        
        Returns
        -------
        clean_content : `None`, `str`
        
        Notes
        -----
        The converting can not display join messages, call messages and private channel names correctly.
        """
        return self.type.converter(self)
    
    
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
        mentions : `list` of (`str` (`'everyone'`), ``ClientUserBase``, ``Role``, ``Channel``,
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
        Returns the length of the message, including of the non link typed embeds'.
        
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
            
            try:
                message_type = fields[MESSAGE_FIELD_KEY_TYPE]
            except KeyError:
                pass
            else:
                is_deletable = message_type.deletable
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
            reactions = ReactionMapping(None)
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
        line : `None`, ``ReactionMappingLine``
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
        activity : `None`, ``MessageActivity``, Optional (Keyword only)
            The ``.activity`` attribute the message.
        
        application : `None`, ``MessageApplication``., Optional (Keyword only)
            The ``.application`` attribute the message.
        
        application_id : `int`, Optional (Keyword Only)
            The ``.application_id`` attribute of the message.
        
        attachments : `None`, ((`list`, `tuple`) of ``Attachment``), Optional (Keyword only)
            The ``.attachments`` attribute of the message. If passed as an empty list, then will be as `None` instead.
        
        author : `None`, ``ClientUserBase``, ``Webhook``, ``WebhookRepr``, Optional (Keyword only)
            The ``.author`` attribute of the message. If passed as `None` then it will be set as `ZEROUSER` instead.
        
        channel_id : ``Channel``, `int`, Optional if called as method (Keyword only)
            The ``.channel_id`` attribute of the message.
        
        components : `None`, (`list`, `tuple`) of ``Component``, Optional (Keyword only)
            The ``.components`` attribute of the message.
        
        content : `None`, `str`, Optional (Keyword only)
            The ``.content`` attribute of the message. Can be between length `0` and `4000`.
        
        cross_mentions : `None`, (`tuple`, `list`) of (``UnknownCrossMention``, ``Channel``)
                , Optional (Keyword only)
            The `.cross_mentions` attribute of the message. If passed as an empty list, then will be set `None` instead.
        
        referenced_message : `None`, ``Message``, Optional (Keyword only)
            The ``.referenced_message`` attribute of the message.
        
        deleted : `bool`, Optional (Keyword only)
            The ``.deleted`` attribute of the message. If called as a class method, defaults to `True`.
        
        edited_at : `None`, `datetime`, Optional (Keyword only)
            The ``.edited_at`` attribute of the message.
        
        embeds : `None`, (`list`, `tuple`) of ``EmbedBase``, Optional (Keyword only)
            The ``.embeds`` attribute of the message. If passed as an empty list, then is set as `None` instead. If
            passed as list and it contains any embeds, which are not type ``EmbedCore``, then those will be converted
            to ``EmbedCore`` as well.
        
        everyone_mention : `bool`, `int` (`0`, `1`), Optional (Keyword only)
            The ``.everyone_mention`` attribute of the message. Accepts other `int` as `bool` as well, but
            their value still cannot be other than `0`, `1`.
        
        flags : ``MessageFlag``, `int`, Optional (Keyword only)
            The ``.flags`` attribute of the message. If passed as other `int` than ``MessageFlag``, then will
            be converted to ``MessageFlag``.
        
        guild_id : ``Guild``, `int`, Optional if called as method (Keyword only)
            The ``.guild_id`` attribute of the message.
        
        interaction : `None`, ``MessageInteraction``, Optional (Keyword only)
           The `.interaction` attribute of the message.
        
        nonce : `None`, `str`, Optional (Keyword only)
            The ``.nonce`` attribute of the message. If passed as `str` can be between length `0` and `32`.
            
            If called as a classmethod defaults to `None`.
        pinned : `bool`, `int` (`0`, `1`), Optional (Keyword only)
            The ``.pinned`` attribute of the message. Accepts other `int` as `bool` as well, but their value
            still cannot be other than `0`, `1`.
        
        reactions : `None`, ``ReactionMapping``, Optional (Keyword only)
            The ``.reactions`` attribute of the message.
        
        role_mentions : `None`, (`list`, `tuple`) of ``Role``, Optional (Keyword only)
            The ``.role_mentions`` attribute of the message. If passed as an empty `list`, will be set as `None`
            instead.
            
        stickers : `None`, (`list`, `tuple`) of ``Sticker``, Optional (Keyword only)
            The ``.stickers`` attribute of the message.
            
        thread : `None`, ``Channel``
            The ``.thread`` attribute of the message.
        
        tts : `bool`, `int` (`0`, `1`), Optional (Keyword only)
            The ``.tts`` attribute of the message. Accepts other `int` as `bool` as well, but their value
            still cannot be other than `0`, `1`.
        
        type : ``MessageType``, `int`, Optional (Keyword only)
            The ``.type`` attribute of the message. If passed as `int`, it will be converted to it's wrapper side
            ``MessageType`` representation.
        
        user_mentions : `None`, `list`, `tuple`  of ``UserBase``, Optional (Keyword only)
            The ``.user_mentions`` attribute of the message. If passed as an empty list will be set as `None` instead.
        
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
                    raise TypeError(f'`author` can be `{UserBase.__name__}`, got '
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
                (MESSAGE_FIELD_KEY_REFERENCED_MESSAGE, Message, 'referenced_message'),
                (MESSAGE_FIELD_KEY_EDITED_AT, datetime, 'edited_at'),
                (MESSAGE_FIELD_KEY_INTERACTION, MessageInteraction, 'interaction'),
                (MESSAGE_FIELD_KEY_REACTIONS, ReactionMapping, 'reactions'),
                (MESSAGE_FIELD_KEY_THREAD, Channel, 'thread'),
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
                (MESSAGE_FIELD_KEY_COMPONENTS, Component, 'components', False),
                (MESSAGE_FIELD_KEY_STICKERS, Sticker, 'stickers', False),
                (MESSAGE_FIELD_KEY_CROSS_MENTIONS, (Channel, UnknownCrossMention), 'cross_mentions', True),
                (MESSAGE_FIELD_KEY_USER_MENTIONS, ClientUserBase, 'user_mentions', True),
            ):
                try:
                    variable_value = kwargs.pop(variable_name)
                except KeyError:
                    pass
                else:
                    if (variable_value is not None):
                        if not isinstance(variable_value, (list, tuple, set)):
                            raise TypeError(
                                f'`{variable_name}` can be `None`, `tuple`, `list`, `set` of '
                                f'{get_type_names(variable_element_type)}, got '
                                f'{variable_value.__class__.__name__}; {variable_value!r}.'
                            )
                        
                        variable_values_processed = []
                        
                        for variable_element_value in variable_value:
                            if not isinstance(variable_element_value, variable_element_type):
                                raise TypeError(
                                    f'`{variable_name}` can contain '
                                    f'{get_type_names(variable_element_type)} elements, got '
                                    f'{variable_element_value.__class__.__name__}; {variable_element_value!r};'
                                    f'{variable_name}={variable_value!r}.'
                                )
                            
                            variable_values_processed.append(variable_element_value)
                        
                        if variable_values_processed:
                            if is_sorted:
                                variable_values_processed.sort(key = id_sort_key)
                            
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
                            raise TypeError(
                                f'`{variable_name}` can be `None`, `str`, got '
                                f'{variable_type.__name__}; {variable_value!r}.'
                            )
                        
                        if variable_value:
                            processable_by_field.append((variable_field_key, variable_value))
            
            
            try:
                embeds = kwargs.pop('embeds')
            except KeyError:
                pass
            else:
                if (embeds is not None):
                    if not isinstance(embeds, (list, tuple)):
                        raise TypeError(
                            f'`embeds` can be `None`, `tuple`, `list` of `{EmbedBase.__name__}`, got '
                            f'{embeds.__class__.__name__}; {embeds!r}.'
                        )
                    
                    embeds_processed = []
                    
                    for embed in embeds:
                        if isinstance(embed, EmbedCore):
                            pass
                        
                        elif isinstance(embed, EmbedBase):
                            # Embed compatible, lets convert it
                            embed = EmbedCore.from_data(embed.to_data())
                        
                        else:
                            raise TypeError(
                                f'`embeds` can contain `{EmbedBase.__name__}` elements, got '
                                f'{embeds.__class__.__name__}; {embeds!r}; embeds={embeds!r}.'
                            )
                    
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
                        raise TypeError(
                            f'`{variable_name}` can be `bool`, got '
                            f'{variable_value.__class__.__name__}; {variable_value!r}.'
                        )
                    
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
                raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
            
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
    
    
    def to_data(self, *, defaults = False, include_internals = False, recursive = True):
        """
        Tries to convert the message back to json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        recursive : `bool` = `True`, Optional (Keyword only)
            Whether referenced messages can be converted as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        data = {}
        
        # id
        data['id'] = str(self.id)
        
        # channel_id
        data['channel_id'] = str(self.channel_id)
        
        # guild_id
        guild_id = self.guild_id
        if not guild_id:
            guild_id = None
        data['guild_id'] = guild_id
        
        # author
        author = self.author
        if (author is not ZEROUSER):
            data['author'] = author.to_data()
        
        # activity
        activity = self.activity
        if (activity is not None):
            data['activity'] = activity.to_data()
        
        # application
        application = self.application
        if (application is not None):
            data['application'] = application.to_data()
        
        # application_id
        application_id = self.application_id
        if application_id:
            data['application_id'] = self.application_id
        
        # attachments
        attachments = self.attachments
        if attachments is None:
            attachment_datas = []
        else:
            attachment_datas = [
                attachment.to_data(defaults = True, include_internals = True) for attachment in attachments
            ]
        data['attachments'] = attachment_datas
        
        # components
        components = self.components
        if (components is None):
            component_datas = []
        else:
            component_datas = [component.to_data() for component in components]
        data['components'] = component_datas
        
        # content
        content = self.content
        if (content is None):
            content = ''
        data['content'] = content
        
        # cross_mentions
        cross_mentions = self.cross_mentions
        if (cross_mentions is not None):
            data['cross_mentions'] = [
                {
                    'id': str(channel.id),
                    'name': channel.name,
                    'guild_id': str(channel.guild_id),
                    'type': channel.type,
                }
                for channel in cross_mentions
            ]
        
        # edited_at
        edited_at = self.edited_at
        if (edited_at is None):
            edited_timestamp = None
        else:
            edited_timestamp = datetime_to_timestamp(edited_at)
        data['edited_timestamp'] = edited_timestamp
        
        # embeds
        embeds = self.embeds
        if embeds is None:
            embed_datas = []
        else:
            embed_datas = [embed.to_data() for embed in embeds]
        data['embeds'] = embed_datas
        
        # everyone_mention
        data['mention_everyone'] = self.everyone_mention
        
        # flags
        data['flags'] = int(self.flags)
        
        # interaction
        interaction = self.interaction
        if (interaction is not None):
            data['interaction'] = interaction.to_data()
        
        # nonce
        data['nonce'] = self.nonce
        
        # pinned
        data['pinned'] = self.pinned
        
        # reactions
        reactions = self.reactions
        if reactions is None:
            reaction_datas = []
        else:
            reaction_datas = reactions.to_data()
        data['reactions'] = reaction_datas
        
        # referenced_message
        referenced_message = self.referenced_message
        if (referenced_message is not None):
            data['message_reference'] = referenced_message.to_message_reference_data()
        
        # referenced_message # 2
        if recursive and self.type in (MessageType.inline_reply, MessageType.thread_started):
            if (referenced_message is None):
                # Bug ?
                referenced_message_data = None
            elif isinstance(referenced_message, Message):
                if referenced_message.deleted:
                    referenced_message_data = None
                else:
                    referenced_message_data = referenced_message.to_data(recursive=False)
            else:
                # Bug ?
                referenced_message_data = None
            
            data['referenced_message'] = referenced_message_data
        
        # role_mention_ids
        role_mention_ids = self.role_mention_ids
        if role_mention_ids is None:
            role_mention_ids = []
        else:
            role_mention_ids = [str(role_id) for role_id in role_mention_ids]
        data['mention_roles'] = role_mention_ids
        
        # stickers
        stickers = self.stickers
        if stickers is None:
            sticker_datas = []
        else:
            sticker_datas = [sticker.to_partial_data() for sticker in stickers]
        data['sticker_items'] = sticker_datas
        
        # thread
        thread = self.thread
        if (thread is not None):
            data['thread'] = thread.to_data()
        
        # tts
        data['tts'] = self.tts
        
        # type
        data['type'] = self.type.value
        
        user_mentions = self.user_mentions
        if (user_mentions is None):
            user_mention_datas = []
        else:
            user_mention_datas = [user_mention.to_data() for user_mention in user_mentions]
        data['mentions'] = user_mention_datas
        
        return data
    
    
    def to_message_reference_data(self):
        """
        Tries to convert the message to json serializable dictionary representing a message reference.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        data = {
            'message_id': str(self.id)
        }
        
        channel_id = self.channel_id
        if channel_id:
            channel_id = str(channel_id)
        else:
            channel_id = None
        
        data['channel_id'] = channel_id
        
        guild_id = self.guild_id
        if guild_id:
            guild_id = str(guild_id)
        else:
            guild_id = None
        
        data['guild_id'] = guild_id
        
        return data
    
    
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
        activity : `None`, ``MessageActivity``
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
        application : `None`, ``MessageApplication``
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
        attachments : `None`, `tuple` of ``Attachment``
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
        attachment : `None`, ``Attachment``
        """
        return _get_first_message_field(
            self,
            MESSAGE_FIELD_KEY_ATTACHMENTS,
        )
    
    
    def iter_attachments(self):
        """
        Iterates over the attachments of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        attachment : ``Attachment``
        """
        yield from _iter_message_field(
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
        channel_mentions : `None`, `tuple` of (``Channel``, ``UnknownCrossMention``) instances.
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
                channel_mentions.sort(key = id_sort_key)
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
        channel_mentions : `None`, (`tuple` of (``Channel``, ``UnknownCrossMentions``))
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
        components : `None`, `tuple` of ``Component``
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
    
    
    def iter_components(self):
        """
        Iterates over the components of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``Component``
        """
        yield from _iter_message_field(
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
        content : `None`, `str`
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
        cross_mentions : `None`, `tuple` of (``UnknownCrossMention``, ``Channel``)
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
        The referenced message. Set as ``Message``. The message can be partial.
        
        Set when the message is a reply, a crosspost or when is a pin message.
        
        Defaults to `None`.
        
        Returns
        -------
        referenced_message : `None`, ``Message``
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
        edited_at : `None`, `datetime`
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
        embeds : `None`, `tuple` of ``EmbedCore``
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
        embed : `None`, ``EmbedCore``
        """
        return _get_first_message_field(
            self,
            MESSAGE_FIELD_KEY_EMBEDS,
        )
    
    
    def iter_embeds(self):
        """
        Iterates over the embeds of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        embed : ``EmbedCore``
        """
        yield from _iter_message_field(
            self,
            MESSAGE_FIELD_KEY_EMBEDS,
        )
    
    # Message.everyone_mention
    
    @property
    def everyone_mention(self):
        """
        Whether the message contains `@everyone`, `@here`.
        
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
        interaction : `None`, ``MessageInteraction``
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
        
        if self.author is ZEROUSER:
            return True
        
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
        nonce : `None`, `str`
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
        reactions : `None`, ``ReactionMapping``
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
        The mentioned roles' identifier by the message if any.
        
        Defaults to `None`.
        
        Returns
        -------
        role_mention_ids : `None`, `tuple` of `int`
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
        role_mentions : `None`, `tuple` of ``Role``
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
        role_mentions : `None`, `tuple` of ``Role``
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
        stickers : `None`, `tuple` of ``Sticker``
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
        sticker : `None`, ``Sticker``
        """
        return _get_first_message_field(
            self,
            MESSAGE_FIELD_KEY_STICKERS,
        )
    
    
    def iter_stickers(self):
        """
        Iterates over the stickers of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        sticker : ``Sticker``
        """
        yield from _iter_message_field(
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
        thread : `None`, ``Channel``
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
        user_mentions : `None`, `tuple` of ``UserBase``
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
    
        
    def has_any_content_field(self):
        """
        Returns whether the message has any content field. Can be used to check whether the bot receiving / requesting
        the message has the message content intent.
        
        Returns
        -------
        has_any_content_field : `bool`
        """
        fields = self._fields
        if fields is None:
            return False
        
        try:
            message_type = fields[MESSAGE_FIELD_KEY_TYPE]
        except KeyError:
            pass
        else:
            if message_type not in MESSAGE_TYPE_VALUES_WITH_CONTENT_FIELDS:
                return True
        
        for field_key in MESSAGE_CONTENT_FIELDS:
            if field_key in fields:
                return True
        
        return False
