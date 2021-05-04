__all__ = ('EventBase', 'GuildUserChunkEvent', 'INTERACTION_EVENT_RESPONSE_STATE_DEFERRED',
    'INTERACTION_EVENT_RESPONSE_STATE_NONE', 'INTERACTION_EVENT_RESPONSE_STATE_RESPONDED', 'InteractionEvent',
    'ReactionAddEvent', 'ReactionDeleteEvent', )

from ...backend.futures import Future, Task, shield, future_or_timeout

from ...backend.export import export

from ..bases import DiscordEntity
from ..core import KOKORO, INTERACTION_EVENT_RESPONSE_WAITERS, INTERACTION_EVENT_MESSAGE_WAITERS
from ..user import User
from ..channel import ChannelPrivate, ChannelText
from ..guild import Guild
from ..exceptions import DiscordException, ERROR_CODES
from ..message import Message, MessageRepr
from ..interaction import INTERACTION_TYPE_TABLE
from ..permission import Permission, PERMISSION_PRIVATE
from ..preinstanced import InteractionType

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command

class EventBase:
    """
    Base class for events.
    """
    __slots__ = ()
    
    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f'Create {cls.__name__} with `object.__new__(cls)` and assign variables from outside.')
    
    def __repr__(self):
        """Returns the event's representation."""
        return f'<{self.__class__.__name__}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 0
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is a generator.
        """
        return
        yield # This is intentional. Python stuff... Do not ask, just accept.


class ReactionAddEvent(EventBase):
    """
    Represents a processed `MESSAGE_REACTION_ADD` dispatch event.
    
    Attributes
    ----------
    message : ``Message`` or ``MessageRepr``
        The message on what the reaction is added.
        
        If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, then message might be given as
        ``MessageRepr`` instance, if the respective event was received on an uncached message.
    emoji : ``Emoji``
        The emoji used as reaction.
    user : ``User`` or ``Client``
        The user who added the reaction.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message. Not applicable for
        ``ReactionAddEvent``.
    """
    __slots__ = ('message', 'emoji', 'user')
    def __new__(cls, message, emoji, user):
        """
        Creates a new ``ReactionAddEvent`` instance (or it's subclass's instance).
        
        Parameters
        ----------
        message : ``Message`` or ``MessageRepr``
            The respective message.
        emoji : ``Emoji``
            The emoji used.
        user : ``User`` or ``Client``
            The user who reacted.
        """
        self = object.__new__(cls)
        self.message = message
        self.emoji = emoji
        self.user = user
        return self
    
    def __repr__(self):
        """Returns the representation of the event."""
        return (f'<{self.__class__.__name__} message={self.message!r}, emoji={self.emoji!r}, '
            f'user={self.user.full_name!r}>')
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is a generator.
        """
        yield self.message
        yield self.emoji
        yield self.user
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identifier number of the action what will be executed.
            
            Can be one of the following:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DELETE_REACTION_OK    | 0     |
            +-----------------------+-------+
            | DELETE_REACTION_PERM  | 1     |
            +-----------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client).can_manage_messages:
            Task(_delete_reaction_with_task(self, client), KOKORO)
            result = self.DELETE_REACTION_OK
        else:
            result = self.DELETE_REACTION_PERM
        
        return result
    
    DELETE_REACTION_OK = 0
    DELETE_REACTION_PERM = 1
    DELETE_REACTION_NOT_ADDED = 2
    
async def _delete_reaction_with_task(reaction_add_event, client):
    try:
        await client.reaction_delete(reaction_add_event.message, reaction_add_event.emoji, reaction_add_event.user)
    except BaseException as err:
        
        if isinstance(err, ConnectionError):
            # no internet
            return
        
        if isinstance(err, DiscordException):
            if err.code in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ):
                return
        
        await client.events.error(client, f'_delete_reaction_with_task called from {reaction_add_event!r}', err)
        return


class ReactionDeleteEvent(ReactionAddEvent):
    """
    Represents a processed `MESSAGE_REACTION_REMOVE` dispatch event.
    
    Attributes
    ----------
    message : ``Message`` or ``MessageRepr``
        The message from what the reaction was removed.
        
        If `HATA_ALLOW_DEAD_EVENTS` environmental variable is given as `True`, then message might be given as
        ``MessageRepr`` instance, if the respective event was received on an uncached message.
    emoji : ``Emoji``
        The removed emoji.
    user : ``User`` or ``Client``
        The user who's reaction was removed.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove. Not
        applicable on ``ReactionDeleteEvent``.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message.
    """
    __slots__ = ReactionAddEvent.__slots__
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction. Because the event is ``ReactionDeleteEvent``, it will not remove any reaction, but
        only check the permissions.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identifier number of the action what will be executed.
            
            Can be one of the following:
            +---------------------------+-------+
            | Respective name           | Value |
            +===========================+=======+
            | DELETE_REACTION_PERM      | 1     |
            +---------------------------+-------+
            | DELETE_REACTION_NOT_ADDED | 2     |
            +---------------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client).can_manage_messages:
            result = self.DELETE_REACTION_NOT_ADDED
        else:
            result = self.DELETE_REACTION_PERM
        
        return result


class GuildUserChunkEvent(EventBase):
    """
    Represents a processed `GUILD_MEMBERS_CHUNK` dispatch event.
    
    Attributes
    ----------
    guild : ``Guild``
        The guild what received the user chunk.
    users : `list` of (``User`` or ``Client``)
        The received users.
    nonce : `None` or `str`
        A nonce to identify guild user chunk response.
    index : `int`
        The index of the received chunk response (0 <= index < count).
    count : `int`
        The total number of chunk responses what Discord sends for the respective gateway.
    """
    __slots__ = ('guild', 'users', 'nonce', 'index', 'count')
    
    def __repr__(self):
        """Returns the representation of the guild user chunk event."""
        return f'<{self.__class__.__name__} guild={self.guild}, users={len(self.users)}, nonce={self.nonce!r}, index={self.index}, count={self.count}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 5
    
    def __iter__(self):
        """
        Unpacks the guild user chunk event.
        
        This method is a generator.
        """
        yield self.guild
        yield self.users
        yield self.nonce
        yield self.index
        yield self.count


INTERACTION_EVENT_RESPONSE_STATE_NONE = 0
INTERACTION_EVENT_RESPONSE_STATE_DEFERRED = 1
INTERACTION_EVENT_RESPONSE_STATE_RESPONDED = 2

@export
class InteractionEvent(DiscordEntity, EventBase, immortal=True):
    """
    Represents a processed `INTERACTION_CREATE` dispatch event.
    
    Attributes
    ----------
    id : `int`
        The interaction's id.
    _cached_users : `None` or `list` of (``User`` or ``Client``)
        A list of users, which are temporary cached.
    _response_state : `bool`
        The response order state of ``InteractionEvent``
        
        +--------------------------------------------+----------+---------------------------------------------------+
        | Respective name                            | Value    | Description                                       |
        +============================================+==========+===================================================+
        | INTERACTION_EVENT_RESPONSE_STATE_NONE      | 0        | No response was yet sent.                         |
        +--------------------------------------------+----------+---------------------------------------------------+
        | INTERACTION_EVENT_RESPONSE_STATE_DEFERRED  | 1        | The event was acknowledged and response will be   |
        |                                            |          | sent later. Shows loading screen for the user.    |
        +--------------------------------------------+----------+---------------------------------------------------+
        | INTERACTION_EVENT_RESPONSE_STATE_RESPONDED | 2        | Response was sent on the interaction.             |
        +--------------------------------------------+----------+---------------------------------------------------+
        
        Can be used by extensions and is used by the the ``Client`` instances to ensure correct flow order.
    application_id : `int`
        The interaction's application's identifier.
    channel : ``ChannelText`` or ``ChannelPrivate``
        The channel from where the interaction was called. Might be a partial channel if not cached.
    guild : `None` or ``Guild`
        The from where the interaction was called from. Might be `None` if the interaction was called from a private
        channel.
    interaction : `None` or ``ApplicationCommandInteraction`` or ``ComponentInteraction``
        The called interaction by it's route by the user.
    message : `None` or ``Message``
        The message from where the interaction was received. Applicable for message components.
    token : `str`
        Interaction's token used when responding on it.
    type : ``InteractionType``
        The interaction's type.
    user : ``Client`` or ``User``
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
    __slots__ = ('_cached_users', '_response_state', 'application_id', 'channel', 'guild', 'interaction', 'message',
        'token', 'type', 'user', 'user_permissions')
    
    _USER_GUILD_CACHE = {}
    
    def __new__(cls, data):
        """
        Creates a new ``InteractionEvent`` instance with the given parameters.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            `INTERACTION_CREATE` dispatch event data.
        """
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        if guild_id:
            guild = Guild.precreate(guild_id)
        else:
            guild = None
        
        if (guild is not None) and (not guild.partial):
            cached_users = []
        else:
            cached_users = None
        
        channel_id = int(data['channel_id'])
        if guild_id:
            channel = ChannelText.precreate(channel_id)
        else:
            channel = ChannelPrivate._create_dataless(channel_id)
        
        try:
            user_data = data['member']
        except KeyError:
            user_data = data['user']
        
        invoker_user = User(user_data, guild)
        if (cached_users is not None):
            cached_users.append(invoker_user)
        
        try:
            user_permissions = user_data['permissions']
        except KeyError:
            user_permissions = PERMISSION_PRIVATE
        else:
            user_permissions = Permission(user_permissions)
        
        try:
            message_data = data['message']
        except KeyError:
            message = None
        else:
            message = channel._create_unknown_message(message_data)
        
        
        type_value = data['type']
        interaction_type = INTERACTION_TYPE_TABLE.get(type_value, None)
        if interaction_type is None:
            interaction = None
        else:
            interaction, cached_users = interaction_type(data['data'], guild, cached_users)
        
        application_id = int(data['application_id'])
        
        self = object.__new__(cls)
        self.id = int(data['id'])
        self.application_id = application_id
        self.type = InteractionType.get(type_value)
        self.channel = channel
        self.guild = guild
        self.interaction = interaction
        self.token = data['token']
        # We ignore `type` field, since we always get only `InteractionType.application_command`.
        self.user = invoker_user
        self.user_permissions = user_permissions
        self._response_state = INTERACTION_EVENT_RESPONSE_STATE_NONE
        self._cached_users = cached_users
        self.message = message
        
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
        
        if self.type is INTERACTION_TYPE_APPLICATION_COMMAND:
            INTERACTION_EVENT_RESPONSE_WAITERS[self.id] = self
        
        return self
    
    
    async def wait_for_response_message(self, *, timeout=None):
        """
        Waits for response message. Applicable for application command interactions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        timeout : `None` or `float`, Optional (Keyword only)
            The maximal time to wait for message before `TimeoutError` is raised.
        
        Returns
        -------
        message : ``Message``
            The received message.
        
        Raises
        ------
        TimeoutError
            Message was not received before timeout.
        """
        message = self.message
        if (message is not None):
            return message
        
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
                    del user.guild_profiles[guild]
                except KeyError:
                    pass
    
    def __repr__(self):
        """Returns the representation of the event."""
        result = ['<', self.__class__.__name__]
        
        response_state = self._response_state
        if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
            response_state_name = None
        elif response_state == INTERACTION_EVENT_RESPONSE_STATE_DEFERRED:
            response_state_name = 'deferred'
        elif response_state == INTERACTION_EVENT_RESPONSE_STATE_RESPONDED:
            response_state_name = 'responded'
        else:
            response_state_name = None
        
        if (response_state_name is not None):
            result.append(' (')
            result.append(response_state_name)
            result.append('),')
        
        result.append(' type=')
        interaction_type = self.type
        result.append(interaction_type.name)
        result.append(' (')
        result.append(repr(interaction_type.value))
        result.append(')')
        
        result.append(' channel=')
        result.append(repr(self.channel))
        result.append(', user=')
        result.append(repr(self.user))
        result.append(', interaction=')
        result.append(repr(self.interaction))
        result.append('>')
        
        return ''.join(result)
    
    def _maybe_set_message(self, message):
        """
        Called when a message is received which is maybe linked to the interaction.
        
        """
    
    def is_acknowledged(self):
        """
        Returns whether the event is acknowledged.
        
        Returns
        -------
        is_acknowledged : `bool`
        """
        return (self._response_state != INTERACTION_EVENT_RESPONSE_STATE_NONE)
    
    def is_responded(self):
        """
        Returns whether was responded.
        
        Returns
        -------
        is_responded : `bool`
        """
        return (self._response_state == INTERACTION_EVENT_RESPONSE_STATE_RESPONDED)
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is a generator.
        """
        yield self.channel
        yield self.user
        yield self.interaction
