__all__ = ('InteractionEvent',)

from scarletio import Future, export, future_or_timeout, shield

from ...bases import DiscordEntity, EventBase
from ...core import (
    APPLICATION_ID_TO_CLIENT, CHANNELS, GUILDS, INTERACTION_EVENT_MESSAGE_WAITERS, INTERACTION_EVENT_RESPONSE_WAITERS,
    KOKORO
)
from ...guild import create_partial_guild_from_id
from ...message import Message
from ...oauth2.helpers import parse_guild_locale, parse_locale
from ...permission import Permission
from ...permission.permission import PERMISSION_PRIVATE
from ...user import ClientUserBase, User
from ...utils import now_as_id, seconds_to_id_difference

from ..interaction_response_context import (
    RESPONSE_FLAG_ACKNOWLEDGED, RESPONSE_FLAG_ACKNOWLEDGING, RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_DEFERRING,
    RESPONSE_FLAG_EPHEMERAL, RESPONSE_FLAG_NONE, RESPONSE_FLAG_RESPONDED, RESPONSE_FLAG_RESPONDING
)

from .application_command_autocomplete_interaction import ApplicationCommandAutocompleteInteraction
from .application_command_interaction import ApplicationCommandInteraction
from .component_interaction import ComponentInteraction
from .form_submit_interaction import FormSubmitInteraction
from .preinstanced import InteractionType


INTERACTION_TYPE_TABLE = {
    InteractionType.ping.value: None,
    InteractionType.application_command.value: ApplicationCommandInteraction,
    InteractionType.message_component.value: ComponentInteraction,
    InteractionType.application_command_autocomplete.value: ApplicationCommandAutocompleteInteraction,
    InteractionType.form_submit: FormSubmitInteraction,
}


INTERACTION_EVENT_EXPIRE_AFTER = 900 # 15 min
INTERACTION_EVENT_EXPIRE_AFTER_ID_DIFFERENCE = seconds_to_id_difference(INTERACTION_EVENT_EXPIRE_AFTER)

@export
class InteractionEvent(DiscordEntity, EventBase, immortal=True):
    """
    Represents a processed `INTERACTION_CREATE` dispatch event.
    
    Attributes
    ----------
    id : `int`
        The interaction's id.
    _async_task : `None`, ``Task``
        Task set if interaction event is acknowledged asynchronously.
    _cached_users : `None`, `list` of ``ClientUserBase``
        A list of users, which are temporary cached.
    _response_flag : `bool`
        The response order state of ``InteractionEvent``
        
        +-------------------------------+-------+---------------------------------------------------+
        | Respective name               | Shift | Description                                       |
        +===============================+=======+===================================================+
        | RESPONSE_FLAG_DEFERRING       | 0     | The vent is being acknowledged.                   |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_DEFERRED        | 1     | The event was acknowledged and response will be   |
        |                               |       | sent later. Shows loading screen for the user.    |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_RESPONDING      | 2     | Responding to the interaction.                    |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_RESPONDED       | 3     | Response was sent on the interaction.             |
        +-------------------------------+-------+---------------------------------------------------+
        | RESPONSE_FLAG_EPHEMERAL       | 4     | Whether the main response is an ephemeral,        |
        |                               |       | showing for the invoking user only.               |
        +-------------------------------+-------+---------------------------------------------------+
        
        Can be used by extensions and is used by the the ``Client``-s to ensure correct flow order.
    application_id : `int`
        The interaction's application's identifier.
    channel_id : `int`
        The channel's identifier from where the interaction was called.
    guild_id : `int`
        The guild's identifier from where the interaction was called from. Might be `0` if the interaction was called
        from a private channel.
    guild_locale : `str`
        The guild's preferred locale if invoked from guild.
    interaction : `None`, ``ApplicationCommandInteraction``, ``ComponentInteraction``, \
            ``ApplicationCommandAutocompleteInteraction``
        
        The called interaction by it's route by the user.
    locale : `str`
        The selected language of the invoking user.
    message : `None`, ``Message``
        The message from where the interaction was received. Applicable for message components.
    token : `str`
        Interaction's token used when responding on it.
    type : ``InteractionType``
        The interaction's type.
    user : ``ClientUserBase``
        The user who called the interaction.
    user_permissions : ``Permission``
        The user's permissions in the respective channel.
    
    Class Attributes
    ----------------
    _USER_GUILD_CACHE : `dict` of (`tuple` (``ClientUserBase``, ``Guild``), `int`)
        A cache which stores `user-guild` pairs as keys and their reference count as values to remember
        ``InteractionEvent``'s ``.user``-s' guild profiles of the respective ``.guild`` even if the ``Guild`` is
        uncached.
    
        Note, that private channel interaction, neither interactions of cached guilds are not added, what means if
        all the clients are kicked from a guild the guild profile can be lost in unexpected time.
    
    Notes
    -----
    The interaction token can be used for 15 minutes, tho if it is not used within the first 3 seconds, it is
    invalidated immediately.
    
    ˙˙InteractionEvent˙˙ instances are weakreferable.
    """
    __slots__ = (
        '_async_task', '_cached_users', '_response_flag', 'application_id', 'channel_id', 'guild_id', 'guild_locale',
        'interaction', 'locale', 'message', 'token', 'type', 'user', 'user_permissions'
    )
    
    _USER_GUILD_CACHE = {}
    
    def __new__(cls, data):
        """
        Creates a new ``InteractionEvent`` with the given parameters.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            `INTERACTION_CREATE` dispatch event data.
        """
        # id_
        id_ = int(data['id'])
        
        # application_id
        application_id = int(data['application_id'])
        
        # channel_id
        channel_id = int(data['channel_id'])
        
        # guild_id
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        if guild_id:
            guild = create_partial_guild_from_id(guild_id)
        else:
            guild = None
        
        # guild_locale
        guild_locale = parse_guild_locale(data)
        
        # interaction
        # We set interaction at the end when the object is fully initialized
        
        # locale
        locale = parse_locale(data)
        
        # message
        try:
            message_data = data['message']
        except KeyError:
            message = None
        else:
            message = Message(message_data)
        
        # token
        token = data['token']
        
        # type
        type_value = data['type']
        type_ = InteractionType.get(type_value)
        
        # user
        try:
            user_data = data['member']
        except KeyError:
            user_data = data['user']
        
        user = User(user_data, guild)
        
        # user_permissions
        try:
            user_permissions = user_data['permissions']
        except KeyError:
            user_permissions = PERMISSION_PRIVATE
        else:
            user_permissions = Permission(user_permissions)
        
        
        self = object.__new__(cls)
        self._async_task = None
        self._cached_users = None
        self._response_flag = RESPONSE_FLAG_NONE
        self.id = id_
        self.application_id = application_id
        self.type = type_
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.guild_locale = guild_locale
        self.interaction = None
        self.locale = locale
        self.token = token
        self.user = user
        self.user_permissions = user_permissions
        self.message = message
        
        # Cache our user if called from guild. This is required to kill references to the user in the guild.
        if (guild is not None):
            self._add_cached_user(user)
        
        # All field is set -> we can now create our own child
        interaction_type = INTERACTION_TYPE_TABLE.get(type_value, None)
        if (interaction_type is not None):
            self.interaction = interaction_type(data['data'], self)
        
        # Bind cached users to the guild for un-caching on object unallocation.
        cached_users = self._cached_users
        if (cached_users is not None):
            for user in cached_users:
                key = (user, guild)
                USER_GUILD_CACHE = cls._USER_GUILD_CACHE
                try:
                    reference_count = USER_GUILD_CACHE[key]
                except KeyError:
                    reference_count = 1
                else:
                    reference_count += 1
                
                USER_GUILD_CACHE[key] = reference_count
        
        return self
    
    
    async def wait_for_response_message(self, *, timeout=None):
        """
        Waits for response message. Applicable for application command interactions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        timeout : `None`, `float` = `None`, Optional (Keyword only)
            The maximal time to wait for message before `TimeoutError` is raised.
        
        Returns
        -------
        message : ``Message``
            The received message.
        
        Raises
        ------
        RuntimeError
            The interaction was acknowledged with `show_for_invoking_user_only=True` (as ephemeral). Response
            `message` cannot be detected.
        TimeoutError
            Message was not received before timeout.
        """
        message = self.message
        if (message is not None):
            return message
        
        if self._response_flag & RESPONSE_FLAG_EPHEMERAL:
            raise RuntimeError(
                f'The interaction was acknowledged with `show_for_invoking_user_only=True` '
                f'(as ephemeral). Response `message` cannot be detected.'
            )
        
        try:
            waiter = INTERACTION_EVENT_MESSAGE_WAITERS[self]
        except KeyError:
            waiter = Future(KOKORO)
            INTERACTION_EVENT_MESSAGE_WAITERS[self] = waiter
        
        waiter = shield(waiter, KOKORO)
        
        if (timeout is not None):
            future_or_timeout(waiter, timeout)
        
        await waiter
        return self.message
    
    
    def __del__(self):
        """
        Unregisters the user-guild pair from the interaction cache.
        """
        cached_users = self._cached_users
        if cached_users is None:
            return
        
        guild = self.guild
        if (guild is None):
            return
        
        for user in cached_users:
            key = (user, guild)
            USER_GUILD_CACHE = self._USER_GUILD_CACHE
            
            # A client meanwhile joined the guild?
            if not guild.partial:
                try:
                    del USER_GUILD_CACHE[key]
                except KeyError:
                    pass
                return
            
            try:
                reference_count = USER_GUILD_CACHE[key]
            except KeyError:
                reference_count = 0
            else:
                if reference_count == 1:
                    del USER_GUILD_CACHE[key]
                    reference_count = 0
                else:
                    reference_count -= 1
            
            if reference_count == 0:
                try:
                    del user.guild_profiles[guild.id]
                except KeyError:
                    pass
    
    
    def __repr__(self):
        """Returns the representation of the event."""
        repr_parts = ['<', self.__class__.__name__]
        
        response_state_names = None
        response_state = self._response_flag
        
        if response_state == RESPONSE_FLAG_NONE:
            pass
        
        if response_state & RESPONSE_FLAG_DEFERRING:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('deferring')
        
        if response_state & RESPONSE_FLAG_DEFERRED:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('deferred')
        
        if response_state & RESPONSE_FLAG_RESPONDING:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('responding')
        
        if response_state & RESPONSE_FLAG_RESPONDED:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('responded')
        
        if response_state & RESPONSE_FLAG_EPHEMERAL:
            if response_state_names is None:
                response_state_names = []
            response_state_names.append('ephemeral')
        
        if (response_state_names is not None):
            repr_parts.append(' (')
            index = 0
            limit = len(response_state_names)
            while True:
                response_state_name = response_state_names[index]
                repr_parts.append(response_state_name)
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append('),')
        
        repr_parts.append(' type=')
        interaction_type = self.type
        repr_parts.append(interaction_type.name)
        repr_parts.append(' (')
        repr_parts.append(repr(interaction_type.value))
        repr_parts.append(')')
        
        
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(', guild_id=')
            repr_parts.append(repr(guild_id))
        
        
        repr_parts.append(', channel_id=')
        repr_parts.append(repr(self.channel_id))
        
        
        message = self.message
        if (message is not None):
            repr_parts.append(', message=')
            repr_parts.append(repr(message))
        
        
        repr_parts.append(', user=')
        repr_parts.append(repr(self.user))
        
        repr_parts.append(', guild_locale=')
        repr_parts.append(repr(self.guild_locale))
        
        if guild_id:
            repr_parts.append(', locale=')
            repr_parts.append(repr(self.locale))
        
        repr_parts.append(', interaction=')
        repr_parts.append(repr(self.interaction))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def is_unanswered(self):
        """
        Returns whether the event was not acknowledged and not acknowledging either.
        
        Returns
        -------
        is_unanswered : `bool`
        """
        return True if (self._response_flag == RESPONSE_FLAG_NONE) else False
    
    
    def is_acknowledging(self):
        """
        Returns whether the event is being acknowledged.
        
        Returns
        -------
        is_acknowledging : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_ACKNOWLEDGING) else False
    
    
    def is_acknowledged(self):
        """
        Returns whether the event is acknowledged.
        
        Returns
        -------
        is_acknowledged : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_ACKNOWLEDGED) else False
    
    
    def is_deferred(self):
        """
        Returns whether the event is deferred.
        
        Returns
        -------
        is_deferred : `bool`
        """
        response_state = self._response_flag
        if response_state & RESPONSE_FLAG_RESPONDED:
            return False
        
        if response_state & RESPONSE_FLAG_DEFERRED:
            return True
        
        return False
    
    
    def is_responding(self):
        """
        Returns whether the event it being responded.
        
        Returns
        -------
        is_responding : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_RESPONDING) else False
    
    
    def is_responded(self):
        """
        Returns whether was responded.
        
        Returns
        -------
        is_responded : `bool`
        """
        return True if (self._response_flag & RESPONSE_FLAG_RESPONDED) else False
    
    
    def is_expired(self):
        """
        Returns whether the event is already expired.
        
        Returns
        -------
        is_expired : `bool`
        """
        return now_as_id() > (self.id + INTERACTION_EVENT_EXPIRE_AFTER_ID_DIFFERENCE)
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is a generator.
        """
        yield self.type
        yield self.user
        yield self.interaction
    
    
    @property
    def channel(self):
        """
        Returns the interaction's event.
        
        Returns
        -------
        channel : ``ChannelTextBase``, `None`
        """
        return CHANNELS.get(self.channel_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the interaction's guild.
        
        Returns
        -------
        guild : ``Guild``, `None`
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def client(self):
        """
        Returns the interaction's client.
        
        Returns
        -------
        client : `Client`
        
        Raises
        ------
        RuntimeError
            Client could not be identified.
        """
        try:
            return APPLICATION_ID_TO_CLIENT[self.application_id]
        except KeyError:
            raise RuntimeError(
                f'Client of {self!r} could not be identified.'
            ) from None
    
    
    @property
    def voice_client(self):
        """
        Returns the voice client of the interaction's client in it's guild.
        
        Returns
        -------
        voice_client : `None`, ``VoiceClient``
        """
        try:
            client = APPLICATION_ID_TO_CLIENT[self.application_id]
        except KeyError:
            voice_client = None
        else:
            guild_id = self.message.guild_id
            if guild_id:
                voice_client = client.voice_clients.get(guild_id, None)
            else:
                voice_client = None
        
        return voice_client
    
    
    def _add_cached_user(self, user):
        """
        Adds a user to the cached ones by the interaction.
        
        This function might be called inside of ``InteractionEvent.__new__`` when initializing it's interaction.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user to add to cache.
        """
        cached_users = self._cached_users
        if cached_users is None:
            self._cached_users = [user]
        else:
            if (user not in cached_users):
                cached_users.append(user)
    
    
    def _add_response_waiter(self):
        """
        Adds the interaction event to response waiters.
        
        Called when the interaction is application command one, to resolve it's ``.message`` attribute when created.
        """
        INTERACTION_EVENT_RESPONSE_WAITERS[self.id] = self
    
    
    async def _wait_for_async_task_completion(self):
        """
        Waits for async task's completion.
        
        This method is a coroutine.
        """
        async_task = self._async_task
        if (async_task is not None) and (async_task is not KOKORO.current_task):
            try:
                await async_task
            finally:
                self._async_task = None
