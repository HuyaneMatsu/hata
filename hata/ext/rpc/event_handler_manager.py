__all__ = ()

from functools import partial as partial_func

from ...discord.events.core import DEFAULT_EVENT_HANDLER
from ...discord.events.handling_helpers import asynclist, check_name, check_parameter_count_and_convert


DEFAULT_PARAMETER_COUNTS = {
    'activity_join': 2,
    'activity_join_request': 2,
    'activity_spectate': 2,
    'channel_create': 2,
    'guild_create': 2,
    'guild_status_update': 2,
    'message_create': 2,
    'message_delete': 2,
    'message_edit': 3,
    'notification_create': 2,
    'ready': 1,
    'speaking_start': 2,
    'speaking_stop': 2,
    'voice_channel_select': 2,
    'voice_connection_status': 2,
    'voice_settings_update': 2,
    'voice_state_create': 2,
    'voice_state_delete': 2,
    'voice_state_update': 2,
    
}

class RPCEventHandlerManager:
    """
    When an ``RPCClient`` receives a dispatch event, am event handler registered to ``RPCEventHandlerManager`` is
    ensured.
    
    Additional Event Attributes
    ---------------------------
    activity_join(rpc_client: ``RPCClient``, secret: `str`)
        Called when the user locks a rich presence join invite in chat to join a game.
    
    activity_join_request(rpc_client: ``RPCClient``, user: ``ClientUserBase``)
        Called when the user received a rich presence ask to join.
    
    activity_spectate(rpc_client: ``RPCClient``, secret: `str`)
        Called when the user locks a rich presence join invite in chat to spectate a game.
    
    channel_create(rpc_client: ``RPCClient``, event: ``ChannelCreateEvent``)
        Called when the client joins or creates a channel.
    
    guild_create(rpc_client: ``RPCClient``, event: ``GuildCreateEvent``)
        Called when the client joins or creates a guild.
    
    guild_status_update(rpc_client: ``RPCClient``, guild: ``Guild``)
        Called when a subscribed guild's status changed.
    
    message_create(rpc_client: ``RPCClient``, message: ``Message``)
        Called when a message is created in a subscribed text channel.
    
    message_delete(rpc_client: ``RPCClient``, message: ``Message``)
        Called when a message is deleted in a subscribed text channel.
    
    message_edit(rpc_client: ``RPCClient``, message: ``Message``, old_attributes : {`dict`, `None`})
        Called when a message is edited in a subscribed text channel.
    
    notification_create(rpc_client: ``RPCClient``, event: ``NotificationCreateEvent``)
        Called when the client receives a notification (mention and such).
    
    ready(rpc_client: ``RPCClient``)
        Called immediately after connecting.
    
    speaking_start(rpc_client: ``RPCClient``, user_id: `int`)
        Sent when a user starts speaking at a subscribed voice channel.
    
    speaking_stop(rpc_client: ``RPCClient``, user_id: `int`)
        Sent when a user stops speaking at a subscribed voice channel.
    
    voice_channel_select(rpc_client: ``RPCClient``, event: ``ChannelVoiceSelectEvent``)
        Called when the client joins a voice channel.
    
    voice_connection_status(rpc_client: ``RPCClient``, voice_connection_status: ``VoiceConnectionStatus``)
        Called when the client's voice connection status changes.
    
    voice_settings_update(rpc_client: ``RPCClient``, voice_settings: ``VoiceSettings``)
        Called when the client's voice settings are updated.
    
    voice_state_create(rpc_client: ``RPCClient``, voice_state: ``RichVoiceState``)
        Called when a user joins a subscribed voice channel.
    
    voice_state_delete(rpc_client: ``RPCClient``, voice_state: ``RichVoiceState``)
        Called when a user leaves or is disconnected from a subscribed voice channel.
    
    voice_state_update(rpc_client: ``RPCClient``, voice_state: ``RichVoiceState``)
         Called when a user's voice state changes inside of a subscribed channel.
    """
    __slots__ = (
        'activity_join', 'activity_join_request', 'activity_spectate', 'channel_create', 'guild_create',
        'guild_status_update', 'message_create', 'message_delete', 'message_edit', 'notification_create', 'ready',
        'speaking_start', 'speaking_stop', 'voice_channel_select', 'voice_connection_status', 'voice_settings_update',
        'voice_state_create', 'voice_state_delete', 'voice_state_update'
    )

    def __init__(self):
        """
        Creates a new rpc event handler manager with every event handler set as the default one.
        """
        for event_name in DEFAULT_PARAMETER_COUNTS.keys():
            setattr(self, event_name, DEFAULT_EVENT_HANDLER)
    
    
    def __repr__(self):
        """Returns the rpc event handler manager's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __call__(self, func=None, name=None, overwrite=False):
        """
        Adds the given `func` as an event handler.
        
        Parameters
        ----------
        func : `None`, `callable` = `None`, Optional
            The async callable to add as an event handler.
        name : `None`, `str` = `None`, Optional
            A name to be used instead of the passed `func`'s when adding it.
        overwrite : `bool` = `False`, Optional
            Whether the passed `func` should overwrite the already added ones with the same name or extend them.
        
        Returns
        -------
        func : `callable`
            The added callable or `functools.partial` if `func` was not given.
        
        Raises
        ------
        LookupError
            Invalid event name.
        TypeError
            - If `func` was not given as callable.
            - If `func` is not as async and neither cannot be converted to an async one.
            - If `func` expects less or more non reserved positional parameters as `expected` is.
            - If `name` was not passed as `None` or type `str`.
        """
        if func is None:
            return partial_func(self, name=name, overwrite=overwrite)
        
        name = check_name(func, name)
        
        try:
            parameter_count = DEFAULT_PARAMETER_COUNTS[name]
        except KeyError:
            raise LookupError(f'Invalid event name: {name!r}.') from None
        
        func = check_parameter_count_and_convert(func, parameter_count, name=name)
        
        actual = getattr(self, name)
        
        if func is DEFAULT_EVENT_HANDLER:
            if actual is DEFAULT_EVENT_HANDLER:
                pass
            
            else:
                if overwrite:
                    object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
                
                else:
                    pass
        
        else:
            if actual is DEFAULT_EVENT_HANDLER:
                object.__setattr__(self, name, func)
            
            else:
                if overwrite:
                    object.__setattr__(self, name, func)
                
                else:
                    if type(actual) is asynclist:
                        list.append(actual, func)
                    else:
                        new = asynclist()
                        list.append(new, actual)
                        list.append(new, func)
                        object.__setattr__(self, name, new)
        
        return func
    
    
    def __delattr__(self, name):
        """
        Removes the event handler with switching it to it's default value.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        
        Raises
        ------
        AttributeError
            The ``RPCEventHandlerManager`` has no attribute named as the given `name`.
        """
        
        if name not in DEFAULT_PARAMETER_COUNTS:
            raise AttributeError(f'Unknown attribute: `{name!r}`.')
        
        object.__setattr__(self, name, DEFAULT_EVENT_HANDLER)
    
    
    def clear(self):
        """
        Clears the ``RPCEventHandlerManager`` to it's initial state.
        """
        for event_name in DEFAULT_PARAMETER_COUNTS.keys():
            setattr(self, event_name, DEFAULT_EVENT_HANDLER)
