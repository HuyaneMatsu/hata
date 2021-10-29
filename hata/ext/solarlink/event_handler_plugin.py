__all__ = ()

from ...discord import EventHandlerPlugin, Event
from . import track_end_reasons as TRACK_END_REASONS

async def default_track_exception_event_handler(client, event):
    """
    Handles track exception by starting to play the next one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    event : ``TrackExceptionEvent``
        The exception event received.
    """
    await event.player.skip(0)


async def default_track_stuck_event_handler(client, event):
    """
    Handles track stuck by starting to play the next one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective event.
    event : ``TrackStuckEvent``
        The track stuck event.
    """
    await event.player.skip(0)


async def default_track_end_event_handler(client, event):
    """
    Handles track end by starting to play the next one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective event.
    event : ``TrackEndEvent``
        The track end event.
    """
    if event.reason == TRACK_END_REASONS.finished:
        await event.player.skip(0)


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
    track_end = Event(2, default_handler=default_track_end_event_handler)
    track_exception = Event(2, default_handler=default_track_exception_event_handler)
    track_start = Event(2)
    track_stuck = Event(2, default_handler=default_track_stuck_event_handler)
    player_websocket_closed = Event(2)
    
    def __repr__(self):
        """Returns the plugin's representation."""
        return f'<{self.__class__.__name__}>'
