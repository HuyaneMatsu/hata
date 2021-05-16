__all__ = ('ApplicationCommandInteraction', 'ApplicationCommandInteractionOption', 'ComponentInteraction',
    'INTERACTION_EVENT_RESPONSE_STATE_DEFERRED', 'INTERACTION_EVENT_RESPONSE_STATE_NONE',
    'INTERACTION_EVENT_RESPONSE_STATE_RESPONDED', 'InteractionEvent', )

import reprlib

from ...backend.futures import Future, shield, future_or_timeout

from ..bases import EventBase, DiscordEntity
from ..core import KOKORO, INTERACTION_EVENT_RESPONSE_WAITERS, INTERACTION_EVENT_MESSAGE_WAITERS
from ..channel import ChannelPrivate, ChannelText, create_partial_channel
from ..message import Message
from ..permission import Permission, PERMISSION_PRIVATE
from ..guild import Guild
from ..user import User, ClientUserBase
from ..role import Role

from .components import ComponentBase
from .preinstanced import ApplicationCommandOptionType, InteractionType, ComponentType

INTERACTION_EVENT_RESPONSE_STATE_NONE = 0
INTERACTION_EVENT_RESPONSE_STATE_DEFERRED = 1
INTERACTION_EVENT_RESPONSE_STATE_RESPONDED = 2

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command


class ApplicationCommandInteraction(DiscordEntity):
    """
    Represents an ``ApplicationCommand`` invoked by a user.
    
    Attributes
    ----------
    id : `int`
        The represented application command's identifier number.
    name : `str`
        The name of the command. It's length can be in range [1:32].
    options : `None` or `list` of ApplicationCommandInteractionOption
        The parameters and values from the user if any. Defaults to `None` if non is received.
    resolved_channels : `None` or `dict` of (`int`, ``ChannelBase``) items
        Resolved received channels stored by their identifier as keys if any.
    resolved_roles : `None` or `dict` of (`int`, ``Role``) items
        Resolved received roles stored by their identifier as keys if any.
    resolved_users : `None` or `dict` of (`int`, ``ClientUserBase``) items
        Resolved received users stored by their identifier as keys if any.
    """
    __slots__ = ('name', 'options', 'resolved_channels', 'resolved_roles', 'resolved_users')
    def __new__(cls, data, guild, cached_users):
        """
        Creates a new ``ApplicationCommandInteraction`` from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction data.
        guild : `None` or ``Guild``
            The respective guild.
        cached_users : `None` or `list` of ``ClientUserBase``
            Users, which might need temporary caching.
        
        Returns
        -------
        self : ``ApplicationCommandInteraction``
            The created object.
        cached_users : `None` or `list` of ``ClientUserBase``
            Users, which might need temporary caching.
        """
        try:
            resolved_data = data['resolved']
        except KeyError:
            resolved_users = None
            resolved_channels = None
            resolved_roles = None
        else:
            try:
                resolved_user_datas = resolved_data['users']
            except KeyError:
                resolved_users = None
            else:
                if resolved_user_datas:
                    try:
                        resolved_guild_profile_datas = resolved_data['members']
                    except KeyError:
                        resolved_guild_profile_datas = None
                    
                    resolved_users = {}
                    
                    for user_id, user_data in resolved_user_datas.items():
                        if resolved_guild_profile_datas is None:
                            guild_profile_data = None
                        else:
                            guild_profile_data = resolved_guild_profile_datas.get(user_id, None)
                        
                        if (guild_profile_data is not None):
                            user_data['member'] = guild_profile_data
                        
                        user = User(user_data, guild)
                        resolved_users[user.id] = user
                        
                        if (guild_profile_data is not None) and (cached_users is not None) and \
                                (user not in cached_users):
                            cached_users.append(user)
                    
                else:
                    resolved_users = None
            
            try:
                resolved_channel_datas = resolved_data['channels']
            except KeyError:
                resolved_channels = None
            else:
                if resolved_channel_datas:
                    resolved_channels = {}
                    
                    for channel_data in resolved_channel_datas.values():
                        channel = create_partial_channel(channel_data, guild)
                        if (channel is not None):
                            resolved_channels[channel.id] = channel
                    
                    if not resolved_channels:
                        resolved_channels = None
                else:
                    resolved_channels = None
            
            try:
                resolved_role_datas = resolved_data['roles']
            except KeyError:
                resolved_roles = None
            else:
                if resolved_role_datas:
                    resolved_roles = {}
                    for role_data in resolved_role_datas.values():
                        role = Role(role_data, guild)
                        resolved_roles[role.id] = role
                else:
                    resolved_roles = None
        
        id_ = int(data['id'])
        name = data['name']
        
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandInteractionOption(option_data) for option_data in option_datas]
        
        self = object.__new__(cls)
        self.id = id_
        self.name = name
        self.options = options
        self.resolved_users = resolved_users
        self.resolved_channels = resolved_channels
        self.resolved_roles = resolved_roles
        
        return self, cached_users
    
    def __repr__(self):
        """Returns the application command interaction's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
            ', name=', repr(self.name),
        ]
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class ApplicationCommandInteractionOption:
    """
    Represents an option of a ``ApplicationCommandInteraction``.
    
    Attributes
    ----------
    name : `str`
        The option's name.
    options : `None` or `list` of ``ApplicationCommandInteractionOption``
        The parameters and values from the user. Present if a sub-command was used. Defaults to `None` if non is
        received.
        
        Mutually exclusive with the `value` attribute.
    type : ``ApplicationCommandOptionType``
        The option's type.
    value : `None`, `str`
        The given value by the user. Should be always converted to the expected type.
    """
    __slots__ = ('name', 'options', 'type', 'value')
    def __new__(cls, data):
        """
        Creates a new ``ApplicationCommandInteractionOption`` instance from the data received from Discord.
        
        Attributes
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction option data.
        """
        name = data['name']
        
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = [ApplicationCommandInteractionOption(option_data) for option_data in option_datas]
        
        self = object.__new__(cls)
        self.name = name
        self.options = options
        self.type = ApplicationCommandOptionType.get(data.get('type', 0))
        
        value = data.get('value', None)
        if value is not None:
            value = str(value)
        
        self.value = value
        
        return self
    
    def __repr__(self):
        """Returns the application command interaction option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ', name=', repr(self.name),
        ]
        
        type_ = self.type
        if type_ is not ApplicationCommandOptionType.none:
            repr_parts.append('type=')
            repr_parts.append(type_.name)
            repr_parts.append(' (')
            repr_parts.append(repr(type_.value))
            repr_parts.append(')')
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        value = self.value
        if (value is not None):
            repr_parts.append(', value=')
            repr_parts.append(repr(value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)



class ComponentInteraction:
    """
    A component interaction of an ``InteractionEvent``.
    
    Attributes
    ----------
    component_type : ``ComponentType``
        The component's type.
    custom_id : `str` or `None`
        The component's custom identifier.
    options : `None` or `tuple` of `str`
        Option values selected of the respective interaction.
    """
    __slots__ = ('component_type', 'custom_id', 'components', 'options')
    
    def __new__(cls, data, guild, cached_users):
        """
        Creates a new component interaction with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received application command interaction data.
        guild : `None` or ``Guild``
            The respective guild.
        cached_users : `None` or `list` of ``ClientUserBase``
            Users, which might need temporary caching.
        
        Returns
        -------
        self : ``ComponentInteraction``
            The created object.
        cached_users : `None` or `list` of ``ClientUserBase``
            Users, which might need temporary caching.
        """
        self = object.__new__(cls)
        
        self.custom_id = data.get('custom_id', None)
        self.component_type = ComponentType.get(data['component_type'])
        
        option_datas = data.get('options', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(option_datas)
        
        self.options = options
        
        return self, cached_users
    
    
    def __repr__(self):
        """Returns the component interaction's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' custom_id=', repr(self.custom_id),
            ', component_type=',
        ]
        component_type = self.component_type
        repr_parts.append(component_type.name)
        repr_parts.append(' (')
        repr_parts.append(repr(component_type.value))
        repr_parts.append(')')
        
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            index = 0
            limit = len(options)
            while True:
                option = options[index]
                repr_parts.append(repr(option))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Compares the two component or component interaction."""
        other_type = type(other)
        if other_type is type(self):
            if self.component_type is not other.component_type:
                return False
            
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        if issubclass(other_type, ComponentBase):
            if self.component_type is not other.type:
                return False
            
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        
        return NotImplemented
    
    
    def __hash__(self):
        """Returns the component interaction's hash value."""
        hash_value = self.component_type.value^hash(self.custom_id)
        
        options = self.options
        if (options is not None):
            hash_value ^ len(options)<<24
            for option in options:
                hash_value ^ hash(option)
        
        return hash_value


INTERACTION_TYPE_TABLE = {
    InteractionType.ping.value: None,
    InteractionType.application_command.value: ApplicationCommandInteraction,
    InteractionType.message_component.value: ComponentInteraction,
}


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