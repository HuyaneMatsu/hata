__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from ...discord import Event, EventDeprecation, EventHandlerPlugin

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
    await event.player.remove(0)


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


async def default_player_web_socket_closed_event_handler(client, event):
    """
    Handles web socket close event.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    event : ``PlayerWebSocketClosedEvent``
        The received web socket closed event.
    """
    player = event.player
    if event.should_reconnect():
        if player.is_playing():
            current = player.get_current()
            if (current is not None):
                current = current.copy()
                current.start_time = player.position
                await player._play(current)
    
    else:
        player.disconnect()


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
    
    player_web_socket_closed(client: ``Client``, event: ``PlayerWebSocketClosedEvent``)
        Called when a player's web socket is disconnected from a guild.
    """
    track_end = Event(2, default_handler = default_track_end_event_handler)
    track_exception = Event(2, default_handler = default_track_exception_event_handler)
    track_start = Event(2)
    track_stuck = Event(2, default_handler = default_track_stuck_event_handler)
    player_web_socket_closed = Event(2, default_handler = default_player_web_socket_closed_event_handler)
    
    # Deprecations
    player_websocket_closed = Event(
        2,
        deprecation = EventDeprecation('player_web_socket_closed', DateTime(2025, 11, 1, tzinfo = TimeZone.utc)),
    )
    
    
    def __repr__(self):
        """Returns the plugin's representation."""
        return f'<{type(self).__name__}>'
