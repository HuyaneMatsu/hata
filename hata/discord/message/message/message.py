__all__ = ('Message',)

from scarletio import export, include

from ...bases import DiscordEntity, id_sort_key
from ...core import CHANNELS, GUILDS, MESSAGES
from ...embed import EXTRA_EMBED_TYPES, Embed
from ...emoji import ReactionMapping
from ...http.urls import build_message_jump_url
from ...poll import Poll
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...role import create_partial_role_from_id
from ...user import ClientUserBase, UserBase, ZEROUSER
from ...utils import CHANNEL_MENTION_RP, DATETIME_FORMAT_CODE

from .constants import (
    EMBED_UPDATE_EMBED_ADD, EMBED_UPDATE_EMBED_REMOVE, EMBED_UPDATE_NONE, EMBED_UPDATE_SIZE_UPDATE,
    MESSAGE_STATE_MASK_CACHE_ALL, MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS, MESSAGE_STATE_MASK_DELETED,
    MESSAGE_STATE_MASK_PARTIAL_ALL, MESSAGE_STATE_MASK_SHOULD_UPDATE, MESSAGE_STATE_MASK_TEMPLATE
)
from .fields import (
    parse_activity, parse_application, parse_application_id, parse_attachments, parse_author, parse_call,
    parse_channel_id, parse_components, parse_content, parse_edited_at, parse_embeds, parse_flags, parse_guild_id,
    parse_id, parse_interaction, parse_mentioned_channels_cross_guild, parse_mentioned_everyone,
    parse_mentioned_role_ids, parse_mentioned_users, parse_message_id, parse_nonce, parse_pinned, parse_poll,
    parse_poll_and_change, parse_reactions, parse_referenced_message, parse_resolved, parse_role_subscription,
    parse_snapshots, parse_soundboard_sounds, parse_stickers, parse_thread, parse_tts, parse_type, put_activity,
    put_application_id, put_application, put_attachments, put_author, put_call,
    put_channel_id, put_components, put_content, put_edited_at, put_embeds, put_flags,
    put_guild_id, put_id, put_interaction, put_mentioned_channels_cross_guild,
    put_mentioned_everyone, put_mentioned_role_ids, put_mentioned_users, put_message_id,
    put_nonce, put_pinned, put_poll, put_reactions, put_referenced_message_into, put_resolved,
    put_role_subscription, put_snapshots, put_soundboard_sounds, put_stickers, put_thread,
    put_tts, put_type, validate_activity, validate_application, validate_application_id, validate_attachments,
    validate_author, validate_call, validate_channel_id, validate_components, validate_content, validate_edited_at,
    validate_embeds, validate_flags, validate_guild_id, validate_id, validate_interaction,
    validate_mentioned_channels_cross_guild, validate_mentioned_everyone, validate_mentioned_role_ids,
    validate_mentioned_users, validate_nonce, validate_pinned, validate_poll, validate_reactions,
    validate_referenced_message, validate_resolved, validate_role_subscription, validate_snapshots,
    validate_soundboard_sounds, validate_stickers, validate_thread, validate_tts, validate_type
)
from .flags import MessageFlag
from .preinstanced import MESSAGE_DEFAULT_CONVERTER, MessageType
from .utils import try_resolve_interaction_message


ChannelType = include('ChannelType')
create_partial_channel_from_id = include('create_partial_channel_from_id')


MESSAGE_TYPE_VALUES_WITH_CONTENT_FIELDS = frozenset((
    message_type.value
    for message_type in MessageType.INSTANCES.values()
    if message_type.converter is MESSAGE_DEFAULT_CONVERTER
))


PRECREATE_FIELDS = {
    'activity': ('activity', validate_activity),
    'application': ('application', validate_application),
    'application_id': ('application_id', validate_application_id),
    'attachments': ('attachments', validate_attachments),
    'author': ('author', validate_author),
    'call': ('call', validate_call),
    'channel': ('channel_id', validate_channel_id),
    'channel_id': ('channel_id', validate_channel_id),
    'components': ('components', validate_components),
    'content': ('content', validate_content),
    'edited_at': ('edited_at', validate_edited_at),
    'embeds': ('embeds', validate_embeds),
    'flags': ('flags', validate_flags),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'interaction': ('interaction', validate_interaction),
    'mentioned_channels_cross_guild': ('mentioned_channels_cross_guild', validate_mentioned_channels_cross_guild),
    'mentioned_everyone': ('mentioned_everyone', validate_mentioned_everyone),
    'mentioned_role_ids': ('mentioned_role_ids', validate_mentioned_role_ids),
    'mentioned_roles': ('mentioned_role_ids', validate_mentioned_role_ids),
    'mentioned_users': ('mentioned_users', validate_mentioned_users),
    'message_type': ('type', validate_type),
    'nonce': ('nonce', validate_nonce),
    'reactions': ('reactions', validate_reactions),
    'poll': ('poll', validate_poll),
    'referenced_message': ('referenced_message', validate_referenced_message),
    'resolved': ('resolved', validate_resolved),
    'role_subscription': ('role_subscription', validate_role_subscription),
    'snapshots': ('snapshots', validate_snapshots),
    'pinned': ('pinned', validate_pinned),
    'soundboard_sounds': ('soundboard_sounds', validate_soundboard_sounds),
    'stickers': ('stickers', validate_stickers),
    'thread': ('thread', validate_thread),
    'tts': ('tts', validate_tts),
}


@export
class Message(DiscordEntity, immortal = True):
    """
    Represents a message from Discord.
    
    Attributes
    ----------
    _cache_mentioned_channels : ``None | tuple<Channel>``
        Mentioned channels by the message. Parsed from ``.content``. Defaults to `None`.
        
        Cache field used by ``.mentioned_channels``.
    
    _state : `int`
        Bitwise mask used to track the message's state.
    
    activity : `None`, ``MessageActivity``
        Sent with rich presence related embeds. Defaults to `None`.
    
    application : `None`, ``MessageApplication``
        Sent with rich presence related embeds. Defaults to `None`.
    
    application_id : `int`
        The application's identifier who sent the message. Defaults to `0`.
    
    attachments : `None`, `tuple` of ``Attachment``
        Attachments sent with the message. Defaults to `None`.
    
    author : ``UserBase``
        The author of the message. Can be any user type and if not found, then set as `ZEROUSER`.
    
    call : `None`, ``MessageCall``
        Call information of the message. Applicable if the message's type is `.call`. Defaults to `None`.
    
    channel_id : `int`
        The channel's identifier where the message is sent. Defaults to `0`
    
    components : ``None | tuple<Component>``
        Components attached to the message. Defaults to `None`.
    
    content : `None | str`
        The message's content. Defaults to `None`.
    
    edited_at : `None | DateTime`
        The time when the message was edited, or `None` if it was not.
        
        Pinning or (un)suppressing a message will not change it's edited value.
        
        Defaults to `None`.
    
    embeds : `None`, `tuple` of ``Embed``
        Embeds included with the message.
        
        If a message contains links then those links' embeds might not be included with the initial payload, but only
        with a followup one.
        
        Defaults to `None`.
    
    flags : ``MessageFlag``
        The message's flags. Defaults to `MessageFlag(0)`.
    
    guild_id : `int`
        The channel's guild's identifier. Defaults to `0˙.
    
    id : `int`
        The unique identifier number of the message. Defaults to `0`.
    
    interaction : `None`, ``MessageInteraction``
        Present if the message is a response to an ``InteractionEvent``. Defaults to `None`.
    
    mentioned_channels_cross_guild : ``None | tuple<Channel>``
        Cross guild channel mentions of a crosspost message if applicable. Defaults to `None`.
    
    mentioned_everyone : `bool`
        Whether the message contains `@everyone`, `@here`. Defaults to `False`.
    
    mentioned_role_ids : `None | tuple<int>`
        The mentioned roles' identifiers. Defaults to `None`.
    
    mentioned_users : `None`, `tuple` of ``ClientUserBase``
        The mentioned users by the message. Defaults to `None`.
    
    nonce : `None | str`
        A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
        be shown up at the message's received payload as well. Defaults to `None`.
    
    pinned : `bool`
        Whether the message is pinned. Defaults to `False`.
    
    poll : `None`, ``Poll``
        The poll of the message. Defaults to `None`.
    
    reactions : `None`, ``ReactionMapping``
        A dictionary like object that contains the reactions on the message. Defaults to `None`.
        
        > If all reactions are removed from a message, `.reactions` will not default back to `None`.
    
    referenced_message : `None`, ``Message``
        The referenced message. The message can be partial.
        
        Set when the message is a reply, a crosspost or when is a pin message.
        
        Defaults to `None`.
    
    resolved : ``None | Resolved``
        Resolved entities of selected options.
        
        Defaults to `None`.
    
    role_subscription : ``None | MessageRoleSubscription``
        Additional role subscription information attached to the message. Defaults to `None`.
    
    snapshots : ``None | tuple<MessageSnapshot>``
        Forwarded snapshots of other messages.
    
    soundboard_sounds : ``None | tuple<SoundboardSound>``
        The soundboard sounds attached to the message. 
    
    stickers : `None`, `tuple` of ``Sticker``
        The stickers sent with the message. Defaults to `None`.
    
    thread : ``None | Channel``
        The thread that was started from this message. Defaults to `None`.
    
    tts : `bool`
        Whether the message is "text to speech". Defaults to `False`.
    
    type : ``MessageType``
        The type of the message. Defaults to `MessageType.default`.
    
    Notes
    -----
    Message instances are weakreferable.
    
    The `content`, `embeds`, `attachments` and the `components` fields are restricted for the message content intent.
    """
    __slots__ = (
        '_cache_mentioned_channels', '_state', 'activity', 'application', 'application_id', 'attachments', 'author',
        'call', 'channel_id', 'components', 'content', 'edited_at', 'embeds', 'flags', 'guild_id', 'interaction',
        'mentioned_channels_cross_guild', 'mentioned_everyone', 'mentioned_role_ids', 'mentioned_users', 'nonce',
        'pinned', 'poll', 'reactions', 'referenced_message', 'resolved', 'role_subscription', 'snapshots',
        'soundboard_sounds', 'stickers', 'thread', 'tts', 'type'
    )
    
    
    def __new__(
        cls,
        *,
        activity = ...,
        application = ...,
        application_id = ...,
        attachments = ...,
        author = ...,
        call = ...,
        components = ...,
        content = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
        interaction = ...,
        mentioned_channels_cross_guild = ...,
        mentioned_everyone = ...,
        mentioned_role_ids = ...,
        mentioned_users = ...,
        message_type = ...,
        nonce = ...,
        pinned = ...,
        poll = ...,
        reactions = ...,
        referenced_message = ...,
        resolved = ...,
        role_subscription = ...,
        snapshots = ...,
        soundboard_sounds = ...,
        stickers = ...,
        thread = ...,
        tts = ...,
    ):
        """
        Creates a new partial message with the given fields.
        
        Parameters
        ----------
        activity : `None`, ``MessageActivity``, Optional (Keyword only)
            Message's activity information, sent with rich presence related embeds.
            
        application : `None`, ``MessageApplication``, Optional (Keyword only)
            Message's application information, sent with rich presence related embeds.
        
        application_id : ``None | int | Application``, Optional (Keyword only)
            The application or its identifier who sent the message.
        
        attachments : `None`, `iterable` of ``Attachment``, Optional (Keyword only)
            Attachments sent with the message.
        
        author : ``UserBase``, Optional (Keyword only)
            The author of the message.
        
        call : `None`, ``MessageCall``, Optional (Keyword only)
            Call information of the message.
        
        components : ``None | iterable<Component>``, Optional (Keyword only)
            Components attached to the message.
        
        content : `None | str`, Optional (Keyword only)
            The message's content.
        
        edited_at : `None | DateTime`
            The time when the message was edited.
        
        embeds : `None`, `iterable` of ``Embed``, Optional (Keyword only)
            Embeds included with the message.
        
        flags : ``MessageFlag``, `int`, Optional (Keyword only)
            The message's flags.
        
        interaction : `None`, ``MessageInteraction``, Optional (Keyword only)
            Present if the message is a response to an ``InteractionEvent``.
        
        mentioned_channels_cross_guild : `None`, `iterable` of ``Channel``, Optional (Keyword only)
            Cross guild channel mentions of a crosspost message if applicable.
        
        mentioned_everyone : `bool`, Optional (Keyword only)
            Whether the message contains `@everyone`, `@here`.
        
        mentioned_role_ids : `None`, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            The mentioned roles' identifiers.
        
        mentioned_users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The mentioned users by the message.
        
        message_type : ``MessageType``, `int`, Optional (Keyword only)
            The type of the message.
        
        nonce : `None | str`, Optional (Keyword only)
            A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
            be shown up at the message's received payload as well.
        
        pinned : `bool`, Optional (Keyword only)
            Whether the message is pinned.
        
        poll : `None`, ``Poll``, Optional (Keyword only)
            The poll of the message.
        
        reactions : `None`, ``ReactionMapping`` (or compatible), Optional (Keyword only)
            A dictionary like object that contains the reactions on the message
        
        referenced_message : `None`, ``Message``, Optional (Keyword only)
            The referenced message.
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Resolved entities of selected options.
        
        role_subscription : ``None | MessageRoleSubscription``, Optional (Keyword only)
            Additional role subscription information attached to the message.
        
        snapshots : `None`, `iterable` of ``MessageSnapshot`, Optional (Keyword only)
            Forwarded snapshots of other messages.
        
        soundboard_sounds : `None | iterable<SoundboardSound>`, Optional (Keyword only)
            Soundboard sounds attached to the message.
        
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers sent with the message.
        
        thread : ``None | Channel``, Optional (Keyword only)
            The thread that was started from this message.
        
        tts : `bool`, Optional (Keyword only)
            Whether the message is "text to speech".
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # activity
        if activity is ...:
            activity = None
        else:
            activity = validate_activity(activity)
        
        # application
        if application is ...:
            application = None
        else:
            application = validate_application(application)
        
        # application_id
        if application_id is ...:
            application_id = 0
        else:
            application_id = validate_application_id(application_id)
        
        # attachments
        if attachments is ...:
            attachments = None
        else:
            attachments = validate_attachments(attachments)
        
        # author
        if author is ...:
            author = ZEROUSER
        else:
            author = validate_author(author)
        
        # call
        if call is ...:
            call = None
        else:
            call = validate_call(call)
        
        # components
        if components is ...:
            components = None
        else:
            components = validate_components(components)
        
        # content
        if content is ...:
            content = None
        else:
            content = validate_content(content)
        
        # edited_at
        if edited_at is ...:
            edited_at = None
        else:
            edited_at = validate_edited_at(edited_at)
        
        # embeds
        if embeds is ...:
            embeds = None
        else:
            embeds = validate_embeds(embeds)
        
        # flags
        if flags is ...:
            flags = MessageFlag()
        else:
            flags = validate_flags(flags)
        
        # interaction
        if interaction is ...:
            interaction = None
        else:
            interaction = validate_interaction(interaction)
        
        # mentioned_channels_cross_guild
        if mentioned_channels_cross_guild is ...:
            mentioned_channels_cross_guild = None
        else:
            mentioned_channels_cross_guild = validate_mentioned_channels_cross_guild(mentioned_channels_cross_guild)
        
        # mentioned_everyone
        if mentioned_everyone is ...:
            mentioned_everyone = False
        else:
            mentioned_everyone = validate_mentioned_everyone(mentioned_everyone)
        
        # mentioned_role_ids
        if mentioned_role_ids is ...:
            mentioned_role_ids = None
        else:
            mentioned_role_ids = validate_mentioned_role_ids(mentioned_role_ids)
        
        # mentioned_users
        if mentioned_users is ...:
            mentioned_users = None
        else:
            mentioned_users = validate_mentioned_users(mentioned_users)
        
        # nonce
        if nonce is ...:
            nonce = None
        else:
            nonce = validate_nonce(nonce)
        
        # pinned
        if pinned is ...:
            pinned = False
        else:
            pinned = validate_pinned(pinned)
        
        # poll
        if poll is ...:
            poll = None
        else:
            poll = validate_poll(poll)
        
        # reactions
        if reactions is ...:
            reactions = None
        else:
            reactions = validate_reactions(reactions)
        
        # referenced_message
        if referenced_message is ...:
            referenced_message = None
        else:
            referenced_message = validate_referenced_message(referenced_message)
        
        # resolved
        if resolved is ...:
            resolved = None
        else:
            resolved = validate_resolved(resolved)
        
        # role_subscription
        if role_subscription is ...:
            role_subscription = None
        else:
            role_subscription = validate_role_subscription(role_subscription)
        
        # snapshots
        if snapshots is ...:
            snapshots = None
        else:
            snapshots = validate_snapshots(snapshots)
        
        # soundboard_sounds
        if soundboard_sounds is ...:
            soundboard_sounds = None
        else:
            soundboard_sounds = validate_soundboard_sounds(soundboard_sounds)
        
        # stickers
        if stickers is ...:
            stickers = None
        else:
            stickers = validate_stickers(stickers)
        
        # thread
        if thread is ...:
            thread = None
        else:
            thread = validate_thread(thread)
        
        # tts
        if tts is ...:
            tts = False
        else:
            tts = validate_tts(tts)
        
        # type
        if message_type is ...:
            message_type = MessageType.default
        else:
            message_type = validate_type(message_type)
        
        # Construct
        
        self = object.__new__(cls)
        self._cache_mentioned_channels = None
        self._state = MESSAGE_STATE_MASK_TEMPLATE
        self.activity = activity
        self.application = application
        self.application_id = application_id
        self.attachments = attachments
        self.author = author
        self.call = call
        self.channel_id = 0
        self.components = components
        self.content = content
        self.edited_at = edited_at
        self.embeds = embeds
        self.flags = flags
        self.guild_id = 0
        self.id = 0
        self.interaction = interaction
        self.mentioned_channels_cross_guild = mentioned_channels_cross_guild
        self.mentioned_everyone = mentioned_everyone
        self.mentioned_role_ids = mentioned_role_ids
        self.mentioned_users = mentioned_users
        self.nonce = nonce
        self.pinned = pinned
        self.poll = poll
        self.reactions = reactions
        self.referenced_message = referenced_message
        self.resolved = resolved
        self.role_subscription = role_subscription
        self.snapshots = snapshots
        self.soundboard_sounds = soundboard_sounds
        self.stickers = stickers
        self.thread = thread
        self.tts = tts
        self.type = message_type
        
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message object form the given message payload. If the message already exists, picks it up.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        message_id = parse_id(data)
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            pass
        else:
            while True:
                # if the message is partial or loading update the whole
                if (self._state & MESSAGE_STATE_MASK_PARTIAL_ALL) or self.flags.loading:
                    self._set_attributes(data, False)
                    break
                
                # If no client can see the message update the whole.
                # This can happen when we use user installed interactions and request back a message.
                channel = self.channel
                if not any(channel.cached_permissions_for(client).view_channel for client in channel.clients):
                    self._set_attributes(data, False)
                    break
                
                # If the message has no content fields we update them.
                if not self.has_any_content_field():
                    self._update_content_fields(data)
                    self.referenced_message = parse_referenced_message(data)
                    break
                
                # No other cases for now
                break
            
            return self
        
        self = object.__new__(cls)
        self.id = message_id
        MESSAGES[message_id] = self
        self._set_attributes(data, True)
        
        return self
    
    
    @classmethod
    def _create_message_was_up_to_date(cls, data):
        """
        Creates a new message object form the given message payload. If the message already exists, picks it up.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message data.
        
        Returns
        -------
        self : `instance<cls>`
            The created or found message instance.
        was_up_to_date : `bool`
            Whether the message was found in the cache.
        """
        message_id = parse_id(data)
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            pass
        else:
            if (self._state & MESSAGE_STATE_MASK_PARTIAL_ALL):
                self._set_attributes(data, False)
                
                return self, False
            
            if self.flags.loading:
                self._set_attributes(data, False)
            
            elif not self.has_any_content_field():
                self._update_content_fields(data)
                self.referenced_message = parse_referenced_message(data)
            
            return self, True
        
        self = object.__new__(cls)
        self.id = message_id
        MESSAGES[message_id] = self
        self._set_attributes(data, True)
        
        return self, False
    
    
    @classmethod
    def _create_from_partial_data(cls, data):
        """
        Creates a message from message reference data.
        
        If the message is loaded already, returns that instead.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message reference data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # allow both `message_id` and `id` keys.
        message_id = parse_message_id(data)
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = cls._create_empty(message_id, parse_channel_id(data),  parse_guild_id(data))
            
            if message_id:
                MESSAGES[message_id] = self
            
            return self
        
        if not (self._state & MESSAGE_STATE_MASK_PARTIAL_ALL):
            return self
        
        self._state |= MESSAGE_STATE_MASK_SHOULD_UPDATE
        self.channel_id = parse_channel_id(data)
        self.guild_id = parse_guild_id(data)
        
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
        self : `instance<cls>`
        """
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = cls._create_empty(message_id, channel_id,  guild_id)
            MESSAGES[message_id] = self
            return self
        
        if not self._state & MESSAGE_STATE_MASK_PARTIAL_ALL:
            return self
        
        self._state |= MESSAGE_STATE_MASK_SHOULD_UPDATE
        self.channel_id = channel_id
        self.guild_id = guild_id
        
        return self
    
    
    def _set_attributes(self, data, creation = True):
        """
        Finishes the message's initialization process by setting it's attributes.
         
        > This method required `.id` and `.reactions` to be set already.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message data.
        creation : `bool` = `True`, Optional
            Whether the entity was just created.
        """
        # Clear cache with other states
        if creation:
            self._state = 0
            self._cache_mentioned_channels = None
        else:
            self._clear_cache()
            self._state &= ~ MESSAGE_STATE_MASK_SHOULD_UPDATE
        
        # Parse default fields
        channel_id = parse_channel_id(data)
        
        guild_id = parse_guild_id(data)
        if not guild_id:
            # At some cases the message has no guild id set, as an example at invoker user only messages.
            # At these cases we get the channel's `.guild_id`
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                pass
            else:
                guild_id = channel.guild_id
        
        # Set default fields
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.type = parse_type(data)
        self.author = parse_author(data, guild_id, channel_id)
        
        # Parse and set extra fields
        self.activity = parse_activity(data)
        self.application = parse_application(data)
        self.application_id = parse_application_id(data)
        self.attachments = parse_attachments(data)
        self.call = parse_call(data)
        self.components = parse_components(data)
        self.content = parse_content(data)
        self.edited_at = parse_edited_at(data)
        self.embeds = parse_embeds(data)
        self.flags = parse_flags(data)
        self.interaction = interaction = parse_interaction(data)
        self.mentioned_channels_cross_guild = parse_mentioned_channels_cross_guild(data)
        self.mentioned_everyone = parse_mentioned_everyone(data)
        self.mentioned_role_ids = parse_mentioned_role_ids(data)
        self.mentioned_users = parse_mentioned_users(data, guild_id)
        self.nonce = parse_nonce(data)
        self.pinned = parse_pinned(data)
        self.poll = parse_poll(data, (None if creation else self.poll))
        self.reactions = parse_reactions(data, (None if creation else self.reactions))
        self.referenced_message = parse_referenced_message(data)
        self.resolved = parse_resolved(data, guild_id = guild_id)
        self.role_subscription = parse_role_subscription(data)
        self.snapshots = parse_snapshots(data, guild_id)
        self.soundboard_sounds = parse_soundboard_sounds(data)
        self.stickers = parse_stickers(data)
        self.thread = parse_thread(data, guild_id)
        self.tts = parse_tts(data)
        
        # Postprocess
        if (interaction is not None):
            try_resolve_interaction_message(self, interaction)
    
    
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
        data : `dict<str, object>`
            Message data.
        """
        if self.flags.loading:
            self._set_attributes(data, False)
            return
        
        if self.interaction is None:
            interaction = parse_interaction(data)
            if (interaction is not None):
                self.interaction = interaction
                try_resolve_interaction_message(self, interaction)
    
    
    def __repr__(self):
        """Returns the representation of the message."""
        repr_parts = ['<', type(self).__name__,]
        
        if self.deleted:
            repr_parts.append(' (deleted)')
        
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append(', length = ')
        repr_parts.append(repr(len(self)))
        
        repr_parts.append(', author = ')
        repr_parts.append(repr(self.author))
        
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
        >>>> from hata import Message
        >>>> message = Message.precreate(103589856105356645, content = 'Fluffy nekos')
        >>>> message
        <Message id = 103589856105356645, length = 12, author = <User name = '#0000'>>
        >>>> # No code stands for str(message), what is same as repr(message) for the time being.
        >>>> f'{message}'
        '<Message id = 103589856105356645, length = 12, author = <User name = '#0000'>>'
        >>>> # 'c' stands for created at.
        >>>> f'{message:c}'
        '2015-10-13 20:29:06'
        >>>> # 'e' stands for edited.
        >>>> f'{message:e}'
        'never'
        >>>> from datetime import datetime as DateTime, timezone as TimeZone
        >>>> message = Message(edited_at = DateTime.now(TimeZone.utc))
        >>>> message
        <Message id = 0, length = 0, <User name = '#0000'>>
        >>>> f'{message:e}'
        '2015-10-13 20:29:06'
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
            f'Unknown format code {code!r} for {type(self).__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"e"!r}.'
        )
    
    
    def __len__(self):
        """Returns the message's total length."""
        return sum(len(content) for content in self.iter_contents())
    
    
    def __eq__(self, other):
        """Returns whether the two messages are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two messages are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        if self is other:
            return True
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return (self_id == other_id)
        
        # activity
        if self.activity != other.activity:
            return False
        
        # application
        if self.application != other.application:
            return False
        
        # application_id
        if self.application_id != other.application_id:
            return False
        
        # attachments
        if self.attachments != other.attachments:
            return False
        
        # author
        if self.author != other.author:
            return False
        
        # call
        if self.call != other.call:
            return False
        
        # channel_id -> skip
        
        # components
        if self.components != other.components:
            return False
        
        # content
        if self.content != other.content:
            return False
        
        # edited_at
        if self.edited_at != other.edited_at:
            return False
        
        # embeds
        if self.embeds != other.embeds:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # guild_id -> skip
        
        # interaction
        if self.interaction != other.interaction:
            return False
        
        # mentioned_channels_cross_guild
        if self.mentioned_channels_cross_guild != other.mentioned_channels_cross_guild:
            return False
        
        # mentioned_everyone
        if self.mentioned_everyone != other.mentioned_everyone:
            return False
        
        # mentioned_role_ids
        if self.mentioned_role_ids != other.mentioned_role_ids:
            return False
        
        # mentioned_users
        if self.mentioned_users != other.mentioned_users:
            return False
        
        # nonce
        if self.nonce != other.nonce:
            return False
        
        # pinned
        if self.pinned != other.pinned:
            return False
        
        # poll
        if self.poll != other.poll:
            return False
        
        # reactions
        if self.reactions != other.reactions:
            return False
        
        # referenced_message
        if self.referenced_message != other.referenced_message:
            return False
        
        # resolved
        if self.resolved != other.resolved:
            return False
        
        # role_subscription
        if self.role_subscription != other.role_subscription:
            return False
        
        # snapshots
        if self.snapshots != other.snapshots:
            return False
        
        # soundboard_sounds
        if self.soundboard_sounds != other.soundboard_sounds:
            return False
        
        # stickers
        if self.stickers != other.stickers:
            return False
        
        # thread
        if self.thread != other.thread:
            return False
        
        # tts
        if self.tts != other.tts:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the message's hash."""
        message_id = self.id
        if message_id:
            return message_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial message's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # activity
        activity = self.activity
        if (activity is not None):
            hash_value ^= hash(activity)
        
        # application
        application = self.application
        if (application is not None):
            hash_value ^= hash(application)
        
        # application_id
        hash_value ^= self.application_id
        
        # attachments
        attachments = self.attachments
        if (attachments is not None):
            hash_value ^= len(attachments)
            
            for attachment in attachments:
                hash_value ^= hash(attachment)
        
        # author
        hash_value ^= hash(self.author)
        
        # call
        call = self.call
        if (call is not None):
            hash_value ^= hash(call)
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components) << 4
            
            for component in components:
                hash_value ^= hash(component)
        
        # content
        content = self.content
        if (content is not None):
            hash_value ^= hash(content)
        
        # edited_at
        edited_at = self.edited_at
        if (edited_at is not None):
            hash_value ^= hash(edited_at)
        
        # embeds
        embeds = self.embeds
        if (embeds is not None):
            hash_value ^= len(embeds) << 8
            
            for embed in embeds:
                hash_value ^= hash(embed)
        
        # flags
        hash_value ^= self.flags << 12
        
        # interaction
        interaction = self.interaction
        if (interaction is not None):
            hash_value ^= hash(interaction)
        
        # mentioned_channels_cross_guild
        mentioned_channels_cross_guild = self.mentioned_channels_cross_guild
        if (mentioned_channels_cross_guild is not None):
            hash_value ^= len(mentioned_channels_cross_guild) << 16
            
            for channel in mentioned_channels_cross_guild:
                hash_value ^= hash(channel)
        
        # mentioned_everyone
        hash_value ^= self.mentioned_everyone << 20
        
        # mentioned_role_ids
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            hash_value ^= len(mentioned_role_ids) << 21
            
            for role_id in mentioned_role_ids:
                hash_value ^= role_id
        
        # mentioned_users
        mentioned_users = self.mentioned_users
        if (mentioned_users is not None):
            hash_value ^= len(mentioned_users) << 25
            
            for user in mentioned_users:
                hash_value ^= hash(user)
        
        # nonce
        nonce = self.nonce
        if (nonce is not None):
            hash_value ^= hash(nonce)
        
        # pinned
        hash_value ^= self.pinned << 29
        
        # poll
        poll = self.poll
        if (poll is not None):
            hash_value ^= hash(poll)
        
        # reactions
        reactions = self.reactions
        if (reactions is not None):
            hash_value ^= hash(reactions)
        
        # referenced_message
        referenced_message = self.referenced_message
        if (referenced_message is not None):
            hash_value ^= hash(referenced_message)
        
        # resolved
        resolved = self.resolved
        if (resolved is not None):
            hash_value ^= hash(resolved)
        
        # role_subscription
        role_subscription = self.role_subscription
        if (role_subscription is not None):
            hash_value ^= hash(role_subscription)
        
        # snapshots
        snapshots = self.snapshots
        if (snapshots is not None):
            hash_value ^= len(snapshots) << 35
            for snapshot in snapshots:
                hash_value ^= hash(snapshot)
        
        # soundboard_sounds
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            hash_value ^= len(soundboard_sounds) << 36
            
            for soundboard_sound in soundboard_sounds:
                hash_value ^= hash(soundboard_sound)
        
        # stickers
        stickers = self.stickers
        if (stickers is not None):
            hash_value ^= len(stickers) << 1
            
            for sticker in stickers:
                hash_value ^= hash(sticker)
        
        # thread
        thread = self.thread
        if (thread is not None):
            hash_value ^= hash(thread)
        
        # tts
        hash_value ^= self.tts << 5
        
        # type
        hash_value ^= hash(self.type) << 6
        
        return hash_value
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the message and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.

        A special case is if a message is (un)pinned or (un)suppressed , because then the returned dict is not going to
        contain `'edited_at'`, only `'pinned'`, `'flags'`. If the embeds are (un)suppressed of the message, then the
        returned dict might contain also an `'embeds'` key.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message data received from Discord.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-----------------------------------+-----------------------------------------------------------------------+
        | Keys                              | Values                                                                |
        +===================================+=======================================================================+
        | attachments                       | `None`, `tuple` of ``Attachment``                                     |
        +-----------------------------------+-----------------------------------------------------------------------+
        | call                              | `None`, ``MessageCall``                                               |
        +-----------------------------------+-----------------------------------------------------------------------+
        | components                        | ``None | tuple<Component>``                                           |
        +-----------------------------------+-----------------------------------------------------------------------+
        | content                           | `None | str`                                                          |
        +-----------------------------------+-----------------------------------------------------------------------+
        | edited_at                         | `None | DateTime`                                                     |
        +-----------------------------------+-----------------------------------------------------------------------+
        | embeds                            | `None`, `tuple` of ``Embed``                                          |
        +-----------------------------------+-----------------------------------------------------------------------+
        | flags                             | ``MessageFlag``                                                       |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_channels_cross_guild    | ``None | tuple<Channel>``                                             |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_everyone                | `bool`                                                                |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_role_ids                | `None | tuple<int>`                                                   |
        +-----------------------------------+-----------------------------------------------------------------------+
        | mentioned_users                   | `None`, `tuple` of ``ClientUserBase``                                 |
        +-----------------------------------+-----------------------------------------------------------------------+
        | pinned                            | `bool`                                                                |
        +-----------------------------------+-----------------------------------------------------------------------+
        | poll                              | ``PollChange``                                                        |
        +-----------------------------------+-----------------------------------------------------------------------+
        | resolved                          | ``None | Resolved``                                                   |
        +-----------------------------------+-----------------------------------------------------------------------+
        """
        self._clear_cache()
        
        old_attributes = {}
        
        attachments = parse_attachments(data)
        if self.attachments != attachments:
            old_attributes['attachments'] = self.attachments
            self.attachments = attachments
        
        call = parse_call(data)
        if self.call != call:
            old_attributes['call'] = self.call
            self.call = call
        
        components = parse_components(data)
        if self.components != components:
            old_attributes['components'] = self.components
            self.components = components
        
        content = parse_content(data)
        if self.content != content:
            old_attributes['content'] = self.content
            self.content = content
        
        edited_at = parse_edited_at(data)
        if self.edited_at != edited_at:
            old_attributes['edited_at'] = self.edited_at
            self.edited_at = edited_at
        
        embeds = parse_embeds(data)
        if self.embeds != embeds:
            old_attributes['embeds'] = self.embeds
            self.embeds = embeds
        
        flags = parse_flags(data)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        mentioned_channels_cross_guild = parse_mentioned_channels_cross_guild(data)
        if self.mentioned_channels_cross_guild != mentioned_channels_cross_guild:
            old_attributes['mentioned_channels_cross_guild'] = self.mentioned_channels_cross_guild
            self.mentioned_channels_cross_guild = mentioned_channels_cross_guild
    
        mentioned_everyone = parse_mentioned_everyone(data)
        if self.mentioned_everyone != mentioned_everyone:
            old_attributes['mentioned_everyone'] = self.mentioned_everyone
            self.mentioned_everyone = mentioned_everyone
        
        mentioned_role_ids = parse_mentioned_role_ids(data)
        if self.mentioned_role_ids != mentioned_role_ids:
            old_attributes['mentioned_role_ids'] = self.mentioned_role_ids
            self.mentioned_role_ids = mentioned_role_ids
        
        mentioned_users = parse_mentioned_users(data)
        if self.mentioned_users != mentioned_users:
            old_attributes['mentioned_users'] = self.mentioned_users
            self.mentioned_users = mentioned_users
        
        pinned = parse_pinned(data)
        if self.pinned != pinned:
            old_attributes['pinned'] = self.pinned
            self.pinned = pinned
        
        poll, change = parse_poll_and_change(data, self.poll)
        if (change is not None):
            old_attributes['poll'] = change
            self.poll = poll
        
        resolved = parse_resolved(data)
        if self.resolved != resolved:
            old_attributes['resolved'] = self.resolved
            self.resolved = resolved    
        
        return old_attributes
    
    
    def _update_attributes(self, data):
        """
        Updates the message with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message data received from Discord.
        """
        self.edited_at = parse_edited_at(data)
        self.call = parse_call(data)
        self.flags = parse_flags(data)
        self.mentioned_channels_cross_guild = parse_mentioned_channels_cross_guild(data)
        self.mentioned_everyone = parse_mentioned_everyone(data)
        self.mentioned_role_ids = parse_mentioned_role_ids(data)
        self.mentioned_users = parse_mentioned_users(data)
        self.pinned = parse_pinned(data)
        self.resolved = parse_resolved(data, guild_id = self.guild_id)
        
        self._update_content_fields(data)
    
    
    def _update_content_fields(self, data):
        """
        Updates the message's content attributes with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Message data received from Discord.
        """
        self._clear_cache()
        
        self.attachments = parse_attachments(data)
        self.components = parse_components(data)
        self.content = parse_content(data)
        self.embeds = parse_embeds(data)
        self.poll = parse_poll(data, self.poll)
    
    
    def _clear_cache(self):
        """
        Clears the message's cache fields.
        """
        self._state &= ~ MESSAGE_STATE_MASK_CACHE_ALL
        self._cache_mentioned_channels = None
    
    
    def _update_embed(self, data):
        """
        After getting a message, it's embeds might be updated from links, or with image, video sizes. If it happens
        this method is called.
        
        Parameters
        ----------
        data : `dict<str, object>`
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
            self.embeds = tuple(Embed.from_data(embed_data) for embed_data in embed_datas)
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
                embeds = tuple(Embed.from_data(embed_data) for embed_data in embed_datas)
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
            embeds = tuple(Embed.from_data(embed_data) for embed_data in embed_datas)
        else:
            embeds = (
                *embeds,
                *(Embed.from_data(embed_datas[index]) for index in range(embeds_length_actual, embeds_length_new)),
            )
        
        self.embeds = embeds
        
        return EMBED_UPDATE_EMBED_ADD
    
    
    def _update_embed_no_return(self, data):
        """
        Updates the message's embeds.
        
        Parameters
        ----------
        data : `dict<str, object>`
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
            self.embeds = tuple(Embed.from_data(embed_data) for embed_data in embed_datas)
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
                embeds = tuple(Embed.from_data(embed_data) for embed_data in embed_datas)
            self.embeds = embeds
            return
        
        if embeds_length_actual != 0:
            for index in range(embeds_length_actual):
                embed_data = embed_datas[index]
                embeds[index]._set_sizes(embed_data)

            if embeds_length_actual == embeds_length_new:
                return
        
        if embeds is None:
            embeds = tuple(Embed.from_data(embed_data) for embed_data in embed_datas)
        else:
            embeds = (
                *embeds,
                *(Embed.from_data(embed_datas[index]) for index in range(embeds_length_actual, embeds_length_new)),
            )
        
        self.embeds = embeds
    
    
    def _add_poll_vote(self, answer_id, user):
        """
        Adds a poll vote to the message.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        user : ``ClientUserBase``
            The user who voted.
        
        Returns
        -------
        success : `bool`
        """
        poll = self.poll
        if poll is None:
            poll = Poll._create_empty()
            self.poll = poll
        
        return poll._add_vote(answer_id, user)
    
    
    def _remove_poll_vote(self, answer_id, user):
        """
        Removes a poll vote from the message.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        user : ``ClientUserBase``
            The user who removed their vote.
        
        Returns
        -------
        success : `bool`
        """
        poll = self.poll
        if poll is None:
            return False
            
        return poll._remove_vote(answer_id, user)
    
    
    def _add_reaction(self, reaction, user):
        """
        Adds a reaction to the message.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction.
        user : ``ClientUserBase``
            The reactor user.
        
        Returns
        -------
        success : `bool`
        """
        reactions = self.reactions
        if reactions is None:
            reactions = ReactionMapping()
            self.reactions = reactions
        
        return reactions._add_reaction(reaction, user)
    
    
    def _remove_reaction(self, reaction, user):
        """
        Removes a reaction to the message.
        
        Parameters
        ----------
        reaction : ``Reaction``
            The reaction.
        user : ``ClientUserBase``
            The user who removed their reaction.
        
        Returns
        -------
        success : `bool`
        """
        reactions = self.reactions
        if reactions is None:
            return False
            
        return reactions._remove_reaction(reaction, user)
    
    
    def _remove_reaction_emoji(self, emoji):
        """
        Removes all reactions of an emoji from the message.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to remove it's reactions.
        
        Returns
        -------
        removed_reactions : `None`, `dict` of (``Reaction``, ``ReactionMappingLine``) items
        """
        reactions = self.reactions
        if (reactions is not None):
            return reactions._remove_reaction_emoji(emoji)
    
    
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
            Whether the referenced message's data should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        if include_internals:
            put_author(self.author, data, defaults, guild_id = self.guild_id)
            put_channel_id(self.channel_id, data, defaults)
            put_guild_id(self.guild_id, data, defaults)
            put_id(self.id, data, defaults)
            put_type(self.type, data, defaults)
            
            put_activity(self.activity, data, defaults)
            put_application(self.application, data, defaults)
            put_application_id(self.application_id, data, defaults)
            put_call(self.call, data, defaults)
            put_edited_at(self.edited_at, data, defaults)
            put_interaction(self.interaction, data, defaults)
            put_mentioned_channels_cross_guild(self.mentioned_channels_cross_guild, data, defaults)
            put_mentioned_everyone(self.mentioned_everyone, data, defaults)
            put_mentioned_role_ids(self.mentioned_role_ids, data, defaults)
            put_mentioned_users(self.mentioned_users, data, defaults, guild_id = self.guild_id)
            put_pinned(self.pinned, data, defaults)
            put_reactions(self.reactions, data, defaults)
            put_referenced_message_into(
                self.referenced_message, data, defaults, recursive = recursive, message_type = self.type
            )
            put_resolved(self.resolved, data, defaults, guild_id = self.guild_id)
            put_role_subscription(self.role_subscription, data, defaults)
            put_snapshots(self.snapshots, data, defaults, guild_id = self.guild_id)
            put_soundboard_sounds(self.soundboard_sounds, data, defaults)
            put_stickers(self.stickers, data, defaults)
            put_thread(self.thread, data, defaults)
        
        put_attachments(self.attachments, data, defaults, include_internals = include_internals)
        put_components(self.components, data, defaults, include_internals = include_internals)
        put_content(self.content, data, defaults)
        put_embeds(self.embeds, data, defaults, include_internals = include_internals)
        put_flags(self.flags, data, defaults)
        put_nonce(self.nonce, data, defaults)
        put_poll(self.poll, data, defaults, include_internals = include_internals)
        put_tts(self.tts, data, defaults)
        
        return data
    
    
    def to_message_reference_data(self):
        """
        Tries to convert the message to json serializable dictionary representing a message reference.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_message_id(self.id, data, True)
        put_channel_id(self.channel_id, data, True)
        put_guild_id(self.guild_id, data, True)
        return data
    
    
    @classmethod
    def _create_empty(cls, message_id, channel_id = 0, guild_id = 0):
        """
        Creates a message with default parameters set.
        
        Parameters
        ----------
        message_id : `int`
            The message's identifier.
        channel_id : `int` = `0`, Optional
            The channel's identifier where the message was created at.
        guild_id : `int` = `0`, Optional
            The guild's identifier where the message was created at.
        
        Returns
        -------
        self : ``Message``
        """
        self = object.__new__(cls)
        self._cache_mentioned_channels = None
        self._state = MESSAGE_STATE_MASK_SHOULD_UPDATE
        self.activity = None
        self.application = None
        self.application_id = 0
        self.attachments = None
        self.author = ZEROUSER
        self.call = None
        self.channel_id = channel_id
        self.components = None
        self.content = None
        self.edited_at = None
        self.embeds = None
        self.flags = MessageFlag()
        self.guild_id = guild_id
        self.id = message_id
        self.interaction = None
        self.mentioned_channels_cross_guild = None
        self.mentioned_everyone = False
        self.mentioned_role_ids = None
        self.mentioned_users = None
        self.nonce = None
        self.pinned = False
        self.poll = None
        self.reactions = None
        self.referenced_message = None
        self.resolved = None
        self.role_subscription = None
        self.snapshots = None
        self.soundboard_sounds = None
        self.stickers = None
        self.thread = None
        self.tts = False
        self.type = MessageType.default
        return self
    
    # Utility
    
    @classmethod
    def precreate(cls, message_id, **keyword_parameters):
        """
        Precreates the message with the given parameters. Precreated messages are picked up when the message's data is
        received with the same id.
        
        First tries to find whether a message exists with the given id. If it does and it is partial, updates it with
        the given parameters, else it creates a new one.
        
        Parameters
        ----------
        message_id : `int`
            The message's id.
        
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the message.
        
        Other Parameters
        ----------------
        activity : `None`, ``MessageActivity``, Optional (Keyword only)
            Message's activity information, sent with rich presence related embeds.
            
        application : `None`, ``MessageApplication``, Optional (Keyword only)
            Message's application information, sent with rich presence related embeds.
        
        application_id : ``None | int | Application``, Optional (Keyword only)
            The application or its identifier who sent the message.
        
        attachments : `None`, `iterable` of ``Attachment``, Optional (Keyword only)
            Attachments sent with the message.
        
        author : ``UserBase``, Optional (Keyword only)
            The author of the message.
        
        call : `None`, ``MessageCall``, Optional (Keyword only)
            Call information of the message.
        
        channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `channel_id`.
        
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's identifier where the message was created at.
        
        components : ``None | iterable<Component>``, Optional (Keyword only)
            Components attached to the message.
        
        content : `None | str`, Optional (Keyword only)
            The message's content.
        
        edited_at : `None | DateTime`
            The time when the message was edited.
        
        embeds : `None`, `iterable` of ``Embed``, Optional (Keyword only)
            Embeds included with the message.
        
        flags : ``MessageFlag``, `int`, Optional (Keyword only)
            The message's flags.
        
        guild : `int`, ``Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier where the message was created at.
        
        interaction : `None`, ``MessageInteraction``, Optional (Keyword only)
            Present if the message is a response to an ``InteractionEvent``.
        
        mentioned_channels_cross_guild : `None`, `iterable` of ``Channel``, Optional (Keyword only)
            Cross guild channel mentions of a crosspost message if applicable.
        
        mentioned_everyone : `bool`, Optional (Keyword only)
            Whether the message contains `@everyone`, `@here`.
        
        mentioned_role_ids : `None`, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            The mentioned roles' identifiers.
        
        mentioned_roles : `None`, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            Alternative for `mentioned_role_ids`.
        
        mentioned_users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The mentioned users by the message.
        
        message_type : ``MessageType``, `int`, Optional (Keyword only)
            The type of the message.
        
        nonce : `None | str`, Optional (Keyword only)
            A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
            be shown up at the message's received payload as well.
        
        pinned : `bool`, Optional (Keyword only)
            Whether the message is pinned.
        
        poll : `None`, ``Poll``, Optional (Keyword only)
            The poll of the message.
        
        reactions : `None`, ``ReactionMapping`` (or compatible), Optional (Keyword only)
            A dictionary like object that contains the reactions on the message
        
        referenced_message : `None`, ``Message``, Optional (Keyword only)
            The referenced message.
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Resolved entities of selected options.
        
        role_subscription : ``None | MessageRoleSubscription``, Optional (Keyword only)
            Additional role subscription information attached to the message.
        
        snapshots : `None`, `iterable` of ``MessageSnapshot`, Optional (Keyword only)
            Forwarded snapshots of other messages.
        
        soundboard_sounds : `None | iterable<SoundboardSound>`, Optional (Keyword only)
            Soundboard sounds attached to the message.
        
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers sent with the message.
        
        thread : ``None | Channel``, Optional (Keyword only)
            The thread that was started from this message.
        
        tts : `bool`, Optional (Keyword only)
            Whether the message is "text to speech".
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            If a parameter's type is invalid.
        ValueError
            If a parameter's value is invalid.
        """
        message_id = validate_id(message_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
            
        else:
            processed = None
        
        try:
            self = MESSAGES[message_id]
        except KeyError:
            self = cls._create_empty(message_id)
            MESSAGES[message_id] = self
        else:
            if not self._state & MESSAGE_STATE_MASK_PARTIAL_ALL:
                return self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the message returning a new partial one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._cache_mentioned_channels = None
        new._state = MESSAGE_STATE_MASK_TEMPLATE
        
        activity = self.activity
        if (activity is not None):
            activity = activity.copy()
        new.activity = activity
        
        application = self.application
        if (application is not None):
            application = application.copy()
        new.application = application
        
        new.application_id = self.application_id
        
        attachments = self.attachments
        if (attachments is not None):
            attachments = (*attachments,)
        new.attachments = attachments
        
        new.author = self.author
        
        call = self.call
        if (call is not None):
            call = call.copy()
        new.call = call
        
        new.channel_id = 0
        
        components = self.components
        if (components is not None):
            components = (*(component.copy() for component in components),)
        new.components = components
        
        new.content = self.content
        new.edited_at = self.edited_at
        
        embeds = self.embeds
        if (embeds is not None):
            embeds = (*(embed.copy() for embed in embeds),)
        new.embeds = embeds
        
        new.flags = self.flags
        new.guild_id = 0
        new.id = 0
        
        interaction = self.interaction
        if (interaction is not None):
            interaction = interaction.copy()
        new.interaction = interaction
        
        mentioned_channels_cross_guild = self.mentioned_channels_cross_guild
        if (mentioned_channels_cross_guild is not None):
            mentioned_channels_cross_guild = (*mentioned_channels_cross_guild,)
        new.mentioned_channels_cross_guild = mentioned_channels_cross_guild
        
        new.mentioned_everyone = self.mentioned_everyone
        
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            mentioned_role_ids = (*mentioned_role_ids,)
        new.mentioned_role_ids = mentioned_role_ids
        
        mentioned_users = self.mentioned_users
        if (mentioned_users is not None):
            mentioned_users = (*mentioned_users,)
        new.mentioned_users = mentioned_users
        
        new.nonce = self.nonce
        new.pinned = self.pinned
        
        poll = self.poll
        if (poll is not None):
            poll = poll.copy()
        new.poll = poll
        
        reactions = self.reactions
        if (reactions is not None):
            reactions = reactions.copy()
        new.reactions = reactions
        
        new.referenced_message = self.referenced_message
        
        resolved = self.resolved
        if (resolved is not None):
            resolved = resolved.copy()
        new.resolved = resolved
        
        role_subscription = self.role_subscription
        if (role_subscription is not None):
            role_subscription = role_subscription.copy()
        new.role_subscription = role_subscription
        
        snapshots = self.snapshots
        if (snapshots is not None):
            snapshots = (*(snapshot.copy() for snapshot in snapshots),)
        new.snapshots = snapshots
        
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            soundboard_sounds = (*soundboard_sounds,)
        new.soundboard_sounds = soundboard_sounds
        
        stickers = self.stickers
        if (stickers is not None):
            stickers = (*stickers,)
        new.stickers = stickers
        
        new.thread = self.thread
        new.tts = self.tts
        new.type = self.type
        
        return new
    
    
    def copy_with(
        self,
        *,
        activity = ...,
        application = ...,
        application_id = ...,
        attachments = ...,
        author = ...,
        call = ...,
        components = ...,
        content = ...,
        edited_at = ...,
        embeds = ...,
        flags = ...,
        interaction = ...,
        mentioned_channels_cross_guild = ...,
        mentioned_everyone = ...,
        mentioned_role_ids = ...,
        mentioned_users = ...,
        message_type = ...,
        nonce = ...,
        pinned = ...,
        poll = ...,
        reactions = ...,
        referenced_message = ...,
        resolved = ...,
        role_subscription = ...,
        snapshots = ...,
        soundboard_sounds = ...,
        stickers = ...,
        thread = ...,
        tts = ...,
    ):
        """
        Copies the message with the given fields.
        
        Parameters
        ----------
        activity : `None`, ``MessageActivity``, Optional (Keyword only)
            Message's activity information, sent with rich presence related embeds.
            
        application : `None`, ``MessageApplication``, Optional (Keyword only)
            Message's application information, sent with rich presence related embeds.
        
        application_id : ``None | int | Application``, Optional (Keyword only)
            The application or its identifier who sent the message.
        
        attachments : `None`, `iterable` of ``Attachment``, Optional (Keyword only)
            Attachments sent with the message.
        
        author : ``UserBase``, Optional (Keyword only)
            The author of the message.
        
        call : `None`, ``MessageCall``, Optional (Keyword only)
            Call information of the message.
        
        components : ``None | iterable<Component>``, Optional (Keyword only)
            Components attached to the message.
        
        content : `None | str`, Optional (Keyword only)
            The message's content.
        
        edited_at : `None | DateTime`
            The time when the message was edited.
        
        embeds : `None`, `iterable` of ``Embed``, Optional (Keyword only)
            Embeds included with the message.
        
        flags : ``MessageFlag``, `int`, Optional (Keyword only)
            The message's flags.
        
        interaction : `None`, ``MessageInteraction``, Optional (Keyword only)
            Present if the message is a response to an ``InteractionEvent``.
        
        mentioned_channels_cross_guild : `None`, `iterable` of ``Channel``, Optional (Keyword only)
            Cross guild channel mentions of a crosspost message if applicable.
        
        mentioned_everyone : `bool`, Optional (Keyword only)
            Whether the message contains `@everyone`, `@here`.
        
        mentioned_role_ids : `None`, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            The mentioned roles' identifiers.
        
        mentioned_users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The mentioned users by the message.
        
        message_type : ``MessageType``, `int`, Optional (Keyword only)
            The type of the message.
        
        nonce : `None | str`, Optional (Keyword only)
            A nonce that is used for optimistic message sending. If a message is created with a nonce, then it should
            be shown up at the message's received payload as well.
        
        pinned : `bool`, Optional (Keyword only)
            Whether the message is pinned.
        
        poll : `None`, ``Poll``, Optional (Keyword only)
            The poll of the message.
        
        reactions : `None`, ``ReactionMapping`` (or compatible), Optional (Keyword only)
            A dictionary like object that contains the reactions on the message
        
        referenced_message : `None`, ``Message``, Optional (Keyword only)
            The referenced message.
        
        resolved : ``None | Resolved``, Optional (Keyword only)
            Resolved entities of selected options.
        
        role_subscription : ``None | MessageRoleSubscription``, Optional (Keyword only)
            Additional role subscription information attached to the message.
        
        snapshots : `None`, `iterable` of ``MessageSnapshot`, Optional (Keyword only)
            Forwarded snapshots of other messages.
        
        soundboard_sounds : `None | iterable<SoundboardSound>`, Optional (Keyword only)
            Soundboard sounds attached to the message.
        
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers sent with the message.
        
        thread : ``None | Channel``, Optional (Keyword only)
            The thread that was started from this message.
        
        tts : `bool`, Optional (Keyword only)
            Whether the message is "text to speech".
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # activity
        if activity is ...:
            activity = self.activity
            if (activity is not None):
                activity = activity.copy()
        else:
            activity = validate_activity(activity)
        
        # application
        if application is ...:
            application = self.application
            if (application is not None):
                application = application.copy()
        else:
            application = validate_application(application)
        
        # application_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
        # attachments
        if attachments is ...:
            attachments = self.attachments
            if (attachments is not None):
                attachments = (*attachments,)
        else:
            attachments = validate_attachments(attachments)
        
        # author
        if author is ...:
            author = self.author
        else:
            author = validate_author(author)
        
        # call
        if call is ...:
            call = self.call
            if (call is not None):
                call = call.copy()
        else:
            call = validate_call(call)
        
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*(component.copy() for component in components),)
        else:
            components = validate_components(components)
        
        # content
        if content is ...:
            content = self.content
        else:
            content = validate_content(content)
        
        # edited_at
        if edited_at is ...:
            edited_at = self.edited_at
        else:
            edited_at = validate_edited_at(edited_at)
        
        # embeds
        if embeds is ...:
            embeds = self.embeds
            if (embeds is not None):
                embeds = (*(embed.copy() for embed in embeds),)
        else:
            embeds = validate_embeds(embeds)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # interaction
        if interaction is ...:
            interaction = self.interaction
            if (interaction is not None):
                interaction = interaction.copy()
        else:
            interaction = validate_interaction(interaction)
        
        # mentioned_channels_cross_guild
        if mentioned_channels_cross_guild is ...:
            mentioned_channels_cross_guild = self.mentioned_channels_cross_guild
            if (mentioned_channels_cross_guild is not None):
                mentioned_channels_cross_guild = (*mentioned_channels_cross_guild,)
        else:
            mentioned_channels_cross_guild = validate_mentioned_channels_cross_guild(mentioned_channels_cross_guild)
        
        # mentioned_everyone
        if mentioned_everyone is ...:
            mentioned_everyone = self.mentioned_everyone
        else:
            mentioned_everyone = validate_mentioned_everyone(mentioned_everyone)
        
        # mentioned_role_ids
        if mentioned_role_ids is ...:
            mentioned_role_ids = self.mentioned_role_ids
            if (mentioned_role_ids is not None):
                mentioned_role_ids = (*mentioned_role_ids,)
        else:
            mentioned_role_ids = validate_mentioned_role_ids(mentioned_role_ids)
        
        # mentioned_users
        if mentioned_users is ...:
            mentioned_users = self.mentioned_users
            if (mentioned_users is not None):
                mentioned_users = (*mentioned_users,)
        else:
            mentioned_users = validate_mentioned_users(mentioned_users)
        
        # nonce
        if nonce is ...:
            nonce = self.nonce
        else:
            nonce = validate_nonce(nonce)
        
        # pinned
        if pinned is ...:
            pinned = self.pinned
        else:
            pinned = validate_pinned(pinned)
        
        # poll
        if poll is ...:
            poll = self.poll
            if (poll is not None):
                poll = poll.copy()
        else:
            poll = validate_poll(poll)
        
        # reactions
        if reactions is ...:
            reactions = self.reactions
            if (reactions is not None):
                reactions = reactions.copy()
        else:
            reactions = validate_reactions(reactions)
        
        # referenced_message
        if referenced_message is ...:
            referenced_message = self.referenced_message
        else:
            referenced_message = validate_referenced_message(referenced_message)
        
        # resolved
        if resolved is ...:
            resolved = self.resolved
            if (resolved is not None):
                resolved = resolved.copy()
        else:
            resolved = validate_resolved(resolved)
        
        # role_subscription
        if role_subscription is ...:
            role_subscription = self.role_subscription
            if (role_subscription is not None):
                role_subscription = role_subscription.copy()
        else:
            role_subscription = validate_role_subscription(role_subscription)
        
        # snapshots
        if snapshots is ...:
            snapshots = self.snapshots
            if (snapshots is not None):
                snapshots = (*(snapshot.copy() for snapshot in snapshots),)
        else:
            snapshots = validate_snapshots(snapshots)
        
        # soundboard_sounds
        if soundboard_sounds is ...:
            soundboard_sounds = self.soundboard_sounds
            if (soundboard_sounds is not None):
                soundboard_sounds = (*soundboard_sounds,)
        else:
            soundboard_sounds = validate_soundboard_sounds(soundboard_sounds)
        
        # stickers
        if stickers is ...:
            stickers = self.stickers
            if (stickers is not None):
                stickers = (*stickers,)
        else:
            stickers = validate_stickers(stickers)
        
        # thread
        if thread is ...:
            thread = self.thread
        else:
            thread = validate_thread(thread)
        
        # tts
        if tts is ...:
            tts = self.tts
        else:
            tts = validate_tts(tts)
        
        # type
        if message_type is ...:
            message_type = self.type
        else:
            message_type = validate_type(message_type)
    
        # Construct
        
        new = object.__new__(type(self))
        new._cache_mentioned_channels = None
        new._state = MESSAGE_STATE_MASK_TEMPLATE
        new.activity = activity
        new.application = application
        new.application_id = application_id
        new.attachments = attachments
        new.author = author
        new.call = call
        new.channel_id = 0
        new.components = components
        new.content = content
        new.edited_at = edited_at
        new.embeds = embeds
        new.flags = flags
        new.guild_id = 0
        new.id = 0
        new.interaction = interaction
        new.mentioned_channels_cross_guild = mentioned_channels_cross_guild
        new.mentioned_everyone = mentioned_everyone
        new.mentioned_role_ids = mentioned_role_ids
        new.mentioned_users = mentioned_users
        new.nonce = nonce
        new.pinned = pinned
        new.poll = poll
        new.reactions = reactions
        new.referenced_message = referenced_message
        new.resolved = resolved
        new.role_subscription = role_subscription
        new.snapshots = snapshots
        new.soundboard_sounds = soundboard_sounds
        new.stickers = stickers
        new.thread = thread
        new.tts = tts
        new.type = message_type
        
        return new

    # Questions (without has)
    
    def is_deletable(self):
        """
        Returns whether the message can be deleted.
        
        Returns
        -------
        is_deletable : `bool`
        """
        if not self.type.deletable:
            return False
        
        if self.deleted:
            return False
    
        if self.flags.invoking_user_only:
            return False
        
        return True
    
    
    def did_vote(self, answer, user):
        """
        Returns whether the given user voted with the given answer on the message.
        
        Parameters
        ----------
        answer : ``VoteAnswer``
            The answer.
        user : ``ClientUserBase``
            The voter.
        
        Returns
        -------
        did_vote : `bool`
        
        Raises
        ------
        TypeError
        """
        poll = self.poll
        if (poll is None):
            return False
        
        result = poll[answer]
        if result is None:
            return False
        
        return user in result
    
    
    def did_react(self, reaction, user):
        """
        Returns whether the given user reacted with the given emoji on the message.
        
        Parameters
        ----------
        reaction : ``Reaction``, ``Emoji``
            The reaction.
        user : ``ClientUserBase``
            The reactor.
        
        Returns
        -------
        did_react : `bool`
        """
        reactions = self.reactions
        if (reactions is None):
            return False
        
        reactors = reactions[reaction]
        if reactors is None:
            return False
        
        return (user in reactors)
    
    # Properties
    
    @property
    def url(self):
        """
        Returns a jump url to the message.
        
        Returns
        -------
        url : `str`
        """
        return build_message_jump_url(self.guild_id, self.channel_id, self.id)
    
    
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
        guild : ``None | Guild``
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
        clean_content : `None | str`
        
        Notes
        -----
        The converting can not display join messages, call messages and private channel names correctly.
        """
        return self.type.converter(self)
    
    
    @property
    def mentions(self):
        """
        Returns a list of all the mentions sent at the message.
        
        Returns
        -------
        mentions : `list` of (`str` (`'everyone'`), ``ClientUserBase``, ``Role``, ``Channel``)
        """
        mentions = []
        if self.mentioned_everyone:
            mentions.append('everyone')
        
        mentions.extend(self.iter_mentioned_channels())
        mentions.extend(self.iter_mentioned_roles())
        mentions.extend(self.iter_mentioned_users())
        
        return mentions
    
    
    @property
    def contents(self):
        """
        A list of all of the contents sent in the message. It means the message's content if it has and the content of
        the message's embeds.
        
        Returns
        -------
        contents : `list<str>`
        """
        return [*self.iter_contents()]
    
    
    @property
    def clean_embeds(self):
        """
        Returns the message's not link typed embeds with converted content without mentions.
        
        Returns
        -------
        clean_embeds : ``list<Embed>``
        
        Notes
        -----
        Not changes the original embeds of the message.
        """
        clean_embeds = []
        
        embeds = self.embeds
        if (embeds is not None):
            guild = self.guild
            
            for embed in embeds:
                if embed.type in EXTRA_EMBED_TYPES:
                    continue
                
                clean_embeds.append(embed.clean_copy(guild))
        
        return clean_embeds
    
    
    @property
    def clean_components(self):
        """
        Returns the message's not link typed components with converted content without mentions.
        
        Returns
        -------
        clean_components : ``list<Component>``
        
        Notes
        -----
        Not changes the original components of the message.
        """
        clean_components = []
        
        components = self.components
        if (components is not None):
            guild = self.guild
            
            for component in components:
                clean_components.append(component.clean_copy(guild))
        
        return clean_components
    
    
    def _get_mentioned_channels(self):
        """
        Looks up the ``.contents`` of the message and searches channel mentions in them.
        
        Invalid channel mentions are ignored.
        
        Returns
        -------
        channel_mentions : ``None | tuple<Channel>``
            The parsed channel mentions.
        """
        mentioned_channels = None
        
        content = self.content
        if content is None:
            return mentioned_channels
        
        for channel_id in CHANNEL_MENTION_RP.findall(content):
            channel_id = int(channel_id)
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                continue
            
            if mentioned_channels is None:
                mentioned_channels = set()
            
            mentioned_channels.add(channel)
        
        if mentioned_channels is not None:
            mentioned_channels = tuple(sorted(mentioned_channels, key = id_sort_key))
        
        return mentioned_channels
    
    
    @property
    def mentioned_channels(self):
        """
        The mentioned channels by the message. If there is non returns `None`.
        
        Returns
        -------
        mentioned_channels : ``None | tuple<Channel>``
        """
        state = self._state
        if state & MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS:
            mentioned_channels = self._cache_mentioned_channels
        else:
            mentioned_channels = self._get_mentioned_channels()
            self._cache_mentioned_channels = mentioned_channels
            self._state = state | MESSAGE_STATE_MASK_CACHE_MENTIONED_CHANNELS
        
        return mentioned_channels
    
    
    @property
    def mentioned_roles(self):
        """
        The mentioned roles by the message. If there is non, returns `None`.
        
        Returns
        -------
        role_mentions : ``None | tuple<Role>``
        """
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            return tuple(create_partial_role_from_id(role_id) for role_id in mentioned_role_ids)
    
    
    @property
    def deleted(self):
        """
        Returns whether the message is deleted.
        
        Defaults to `False`.
        
        Returns
        -------
        deleted : `bool`
        """
        return True if self._state & MESSAGE_STATE_MASK_DELETED else False
    
    
    @deleted.setter
    def deleted(self, value):
        state = self._state
        if value:
            state |= MESSAGE_STATE_MASK_DELETED
        else:
            state &= ~MESSAGE_STATE_MASK_DELETED
        self._state = state
    
    
    @property
    def partial(self):
        """
        Returns whether the message is partial.
        
        Returns
        -------
        partial : `bool`
        """
        # Might not be the most accurate check, lol
        return True if self._state & MESSAGE_STATE_MASK_PARTIAL_ALL else False
    
    # Get one
    
    @property
    def attachment(self):
        """
        Returns the first attachment in the message.

        Returns
        -------
        attachment : `None`, ``Attachment``
        """
        attachments = self.attachments
        if attachments is not None:
            return attachments[0]
    
    
    @property
    def embed(self):
        """
        Returns the first embed in the message.

        Returns
        -------
        embed : `None`, ``Embed``
        """
        embeds = self.embeds
        if embeds is not None:
            return embeds[0]
    
    @property
    def snapshot(self):
        """
        Returns the first snapshot in the message.

        Returns
        -------
        snapshot : ``None | MessageSnapshot``
        """
        snapshots = self.snapshots
        if snapshots is not None:
            return snapshots[0]
    
    @property
    def soundboard_sound(self):
        """
        Returns the message's first soundboard sound.
        
        Returns
        -------
        soundboard_sound : ``None | SoundboardSound``
        """
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            return soundboard_sounds[0]
    
    
    @property
    def sticker(self):
        """
        Returns the first sticker in the message.

        Returns
        -------
        sticker : `None`, ``Sticker``
        """
        stickers = self.stickers
        if stickers is not None:
            return stickers[0]
    
    # Iter
    
    def iter_attachments(self):
        """
        Iterates over the attachments of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        attachment : ``Attachment``
        """
        attachments = self.attachments
        if attachments is not None:
            yield from attachments
    
    
    def iter_components(self):
        """
        Iterates over the components of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``Component``
        """
        components = self.components
        if components is not None:
            yield from components
    
    
    def iter_contents(self):
        """
        Iterates over the contents of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        content : `str`
        """
        content = self.content
        if (content is not None):
            yield content
        
        for embed in self.iter_embeds():
            yield from embed.iter_contents()
        
        poll = self.poll
        if (poll is not None):
            yield from poll.iter_contents()
        
        for component in self.iter_components():
            yield from component.iter_contents()
    
    
    def iter_embeds(self):
        """
        Iterates over the embeds of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        embed : ``Embed``
        """
        embeds = self.embeds
        if embeds is not None:
            yield from embeds
    
    
    def iter_mentioned_channels(self):
        """
        Iterates over the mentioned channels in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_channel : ``Channel``
        """
        mentioned_channels = self.mentioned_channels
        if (mentioned_channels is not None):
            yield from mentioned_channels
    
    
    def iter_mentioned_channels_cross_guild(self):
        """
        Iterates over the mentioned channels from an other guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_channel : ``Channel``
        """
        mentioned_channels_cross_guild = self.mentioned_channels_cross_guild
        if (mentioned_channels_cross_guild is not None):
            yield from mentioned_channels_cross_guild
    
    
    def iter_mentioned_role_ids(self):
        """
        Iterates over the mentioned roles' identifiers in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_role_id : `int`
        """
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            yield from mentioned_role_ids
    
    
    def iter_mentioned_roles(self):
        """
        Iterates over the mentioned roles in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_role : ``Role``
        """
        mentioned_role_ids = self.mentioned_role_ids
        if (mentioned_role_ids is not None):
            for role_id in mentioned_role_ids:
                yield create_partial_role_from_id(role_id)
    
    
    def iter_mentioned_users(self):
        """
        Iterates over the mentioned users in the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        mentioned_user : ``ClientUserBase``
        """
        mentioned_users = self.mentioned_users
        if (mentioned_users is not None):
            yield from mentioned_users
    
    
    def iter_snapshots(self):
        """
        Iterates over the snapshots of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        snapshot : ``Snapshot``
        """
        snapshots = self.snapshots
        if snapshots is not None:
            yield from snapshots
    
    
    def iter_soundboard_sounds(self):
        """
        Iterates over the soundboard sounds of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        soundboard_sounds : ``SoundboardSound``
        """
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            yield from soundboard_sounds
    
    
    def iter_stickers(self):
        """
        Iterates over the stickers of the message.
        
        This method is an iterable generator.
        
        Yields
        ------
        sticker : ``Sticker``
        """
        stickers = self.stickers
        if stickers is not None:
            yield from stickers
    
    # Has
    
    def has_activity(self):
        """
        Returns whether the message has ``.activity`` set as its non-default value.
        
        Returns
        -------
        has_activity : `bool`
        """
        return self.activity is not None
    
    
    def has_application(self):
        """
        Returns whether the message has ``.application`` set as its non-default value.
        
        Returns
        -------
        has_application : `bool`
        """
        return self.application is not None
    
    
    def has_application_id(self):
        """
        Returns whether the message has ``.application_id`` set as its non-default value.
        
        Returns
        -------
        has_application_id : `bool`
        """
        return True if self.application_id else False
    
    
    def has_attachments(self):
        """
        Returns whether the message has ``.attachments`` set as its non-default value.
        
        Returns
        -------
        has_attachments : `bool`
        """
        return self.attachments is not None
    
    
    def has_components(self):
        """
        Returns whether the message has ``.components`` set as its non-default value.
        
        Returns
        -------
        has_components : `bool`
        """
        return self.components is not None
    
    
    def has_content(self):
        """
        Returns whether the message has ``.content`` set as its non-default value.
        
        Returns
        -------
        has_content : `bool`
        """
        return self.content is not None
    
    
    def has_edited_at(self):
        """
        Returns whether the message has ``.edited_at`` set as its non-default value.
        
        Returns
        -------
        has_edited_at : `bool`
        """
        return self.edited_at is not None
    
    
    def has_embeds(self):
        """
        Returns whether the message has ``.embeds`` set as its non-default value.
        
        Returns
        -------
        has_embeds : `bool`
        """
        return self.embeds is not None
    
    
    def has_flags(self):
        """
        Returns whether the message has ``.flags`` set as its non-default value.
        
        Returns
        -------
        has_flags : `bool`
        """
        return True if self.flags else False
    
    
    def has_interaction(self):
        """
        Returns whether the message has ``.interaction`` set.
        
        Returns
        -------
        has_interaction : `bool`
        """
        return self.interaction is not None
    
    
    def has_mentioned_channels(self):
        """
        Returns whether the message has ``.mentioned_channels`` set as its non-default value.
        
        Returns
        -------
        has_channel_mentions : `bool`
        """
        return (self.mentioned_channels is not None)
    
    
    def has_mentioned_channels_cross_guild(self):
        """
        Returns whether the message has ``.mentioned_channels_cross_guild`` set as its non-default value.
        
        Returns
        -------
        has_mentioned_channels_cross_guild : `bool`
        """
        return self.mentioned_channels_cross_guild is not None
    
    
    def has_mentioned_everyone(self):
        """
        Returns whether the message has ``.mentioned_everyone`` set as its non-default value.
        
        Returns
        -------
        has_mentioned_everyone : `bool`
        """
        return self.mentioned_everyone
    
    
    def has_mentioned_role_ids(self):
        """
        Returns whether the message has ``.mentioned_role_ids`` set as its non-default value.
        
        Returns
        -------
        has_role_mention_ids : `bool`
        """
        return self.mentioned_role_ids is not None
    
    
    def has_mentioned_roles(self):
        """
        Returns whether the message has ``.has_mentioned_roles`` set as its non-default value.
        
        Returns
        -------
        has_mentioned_roles : `bool`
        """
        return self.mentioned_role_ids is not None
    
    
    def has_mentioned_users(self):
        """
        Returns whether the message has ``.mentioned_users``.
        
        Returns
        -------
        has_mentioned_users : `bool`
        """
        return self.mentioned_users is not None
    
    
    def has_nonce(self):
        """
        Returns whether the message has ``.nonce`` set as its non-default value.
        
        Returns
        -------
        has_nonce : `bool`
        """
        return self.nonce is not None
    
    
    def has_pinned(self):
        """
        Returns whether the message has ``.pinned`` set as its non-default value.
        
        Returns
        -------
        has_pinned : `bool`
        """
        return self.pinned
    
    
    def has_poll(self):
        """
        Returns whether the message has ``.poll`` set as its non-default value.
        
        Returns
        -------
        has_poll : `bool`
        """
        return self.poll is not None
    
    
    def has_reactions(self):
        """
        Returns whether the message has any reactions.
        
        > A message can have no reactions even if its ``.reactions`` is not set as its default value.
        > This can happen if reactions were removed from the message.
        
        Returns
        -------
        has_reactions : `bool`
        """
        reactions = self.reactions
        if reactions is None:
            has_reactions = False
        else:
            if reactions:
                has_reactions = True
            else:
                has_reactions = False
        
        return has_reactions
    
    
    def has_referenced_message(self):
        """
        Returns whether the message has ``.referenced_message`` set as its non-default value.
        
        Returns
        -------
        has_referenced_message : `bool`
        """
        return self.referenced_message is not None
    
    
    def hash_resolved(self):
        """
        Returns whether the message has ``.resolved`` set as its non-default value.
        
        Returns
        -------
        has_resolved : `bool`
        """
        return self.resolved is not None
    
    
    def has_role_subscription(self):
        """
        Returns whether the message has ``.role_subscription`` set as its non-default value.
        
        Returns
        -------
        has_role_subscription : `bool`
        """
        return self.role_subscription is not None
    
    
    def has_snapshots(self):
        """
        Returns whether the message has ``.snapshots`` set as its non default value.
        
        Returns
        -------
        has_snapshots : `bool`
        """
        return self.snapshots is not None
    
    
    def has_soundboard_sounds(self):
        """
        Returns whether the message has ``.soundboard_sounds`` set as its non-default value.
        
        Returns
        -------
        has_soundboard_sounds : `bool`
        """
        return (self.soundboard_sounds is not None)
    
    
    def has_stickers(self):
        """
        Returns whether the message has ``.stickers`` set as its non-default value.
        
        Returns
        -------
        has_stickers : `bool`
        """
        return self.stickers is not None
    
    
    def has_thread(self):
        """
        Returns whether the message has ``.thread`` set as its non-default value.
        
        Returns
        -------
        has_thread : `bool`
        """
        return self.thread is not None
    
    
    def has_tts(self):
        """
        Returns whether the message has ``.tts`` set as its non-default value.
        
        Returns
        -------
        has_tts : `bool`
        """
        return self.tts
    
    
    def has_type(self):
        """
        Returns whether the message has ``.type`` set as its non-default value.
        
        Returns
        -------
        has_type : `bool`
        """
        return self.type is not MessageType.default
    
    # Has | Others
        
    def has_any_content_field(self):
        """
        Returns whether the message has any content field. Can be used to check whether the bot receiving / requesting
        the message has the message content intent.
        
        Returns
        -------
        has_any_content_field : `bool`
        """
        if self.type not in MESSAGE_TYPE_VALUES_WITH_CONTENT_FIELDS:
            return True
        
        if self.content is not None:
            return True
        
        if self.embeds is not None:
            return True
            
        if self.attachments is not None:
            return True
        
        if self.components is not None:
            return True
        
        if self.poll is not None:
            return True
        
        return False
