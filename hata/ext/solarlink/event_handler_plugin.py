__all__ = ()

from ...discord import EventHandlerPlugin, Event

class SolarLinkEventManager(EventHandlerPlugin):
    """
    Plugin to extend `client.events` auto registered when setting up the extension to a client.
    
    Event Attributes
    ----------------
    track_end(client: ``Client``, event: ``TrackEndEvent``)
        Called when a track ended.
    
    track_exception(client: ``Client``, event: ``TrackExceptionEvent``)
        Called when a track finished with exception.
    
    track_start(client: ``Client``, event: ``TrackStartEvent``)
        Called when a track started.
    
    track_stuck(client: ``Client``, event: ``TrackStuckEvent``)
        Called when the currently playing track is stuck.
    
    player_websocket_closed(client: ``Client``, event: ``PlayerWebsocketClosedEvent``)
        Called when a player's websocket is disconnected from a guild.
    """
    track_end = Event(2)
    track_exception = Event(2)
    track_start = Event(2)
    track_stuck = Event(2)
    player_websocket_closed = Event(2)
    
    def __repr__(self):
        """Returns the plugin's representation."""
        return f'<{self.__class__.__name__}>'
