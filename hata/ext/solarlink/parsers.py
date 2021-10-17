__all__ = ()

from ...backend.futures import Task
from ...discord.core import KOKORO

from .constants import LAVALINK_KEY_EVENT_TRACK_END, LAVALINK_KEY_EVENT_TRACK_EXCEPTION, LAVALINK_KEY_GUILD_ID, \
    LAVALINK_KEY_EVENT_TRACK_START, LAVALINK_KEY_EVENT_TRACK_STUCK, LAVALINK_KEY_EVENT_PLAYER_WEBSOCKET_CLOSED, \
    LAVALINK_KEY_END_REASON, LAVALINK_KEY_EXCEPTION_REASON, LAVALINK_KEY_THRESHOLD_MS, LAVALINK_KEY_TRACK, \
    LAVALINK_KEY_WEBSOCKET_CLOSE_CODE, LAVALINK_KEY_WEBSOCKET_CLOSE_REASON, LAVALINK_KEY_WEBSOCKET_CLOSE_BY_REMOTE
from .event_types import TrackEndEvent, TrackExceptionEvent, TrackStartEvent, TrackStuckEvent, \
    PlayerWebsocketClosedEvent
from .track import Track

def parse_track_end(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    track = player._current_track
    reason = data[LAVALINK_KEY_END_REASON]
    
    event = TrackEndEvent(player, track, reason)
    
    Task(client.solarlink._events.track_end(client, event), KOKORO)
    

def parse_track_exception(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    track = player._current_track
    reason = data[LAVALINK_KEY_EXCEPTION_REASON]
    
    event = TrackExceptionEvent(player, track, reason)
    
    Task(client.solarlink._events.track_exception(client, event), KOKORO)


def parse_track_start(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    track = Track.from_base64(data[LAVALINK_KEY_TRACK])
    event = TrackStartEvent(player, track)
    Task(client.solarlink._events.track_start(client, event), KOKORO)



def parse_track_stuck(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    track = player._current_track
    threshold = data[LAVALINK_KEY_THRESHOLD_MS]*1000.0
    
    event = TrackStuckEvent(player, track, threshold)
    Task(client.solarlink._events.track_stuck(client, event), KOKORO)


def parse_player_websocket_closed(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    close_code = data[LAVALINK_KEY_WEBSOCKET_CLOSE_CODE]
    close_reason = data[LAVALINK_KEY_WEBSOCKET_CLOSE_REASON]
    close_by_remote = data[LAVALINK_KEY_WEBSOCKET_CLOSE_BY_REMOTE]
    
    event = PlayerWebsocketClosedEvent(player, close_code, close_reason, close_by_remote)
    Task(client.solarlink._events.player_websocket_closed(client, event), KOKORO)


PARSERS = {
    LAVALINK_KEY_EVENT_TRACK_END: parse_track_end,
    LAVALINK_KEY_EVENT_TRACK_EXCEPTION: parse_track_exception,
    LAVALINK_KEY_EVENT_TRACK_START: parse_track_start,
    LAVALINK_KEY_EVENT_TRACK_STUCK: parse_track_stuck,
    LAVALINK_KEY_EVENT_PLAYER_WEBSOCKET_CLOSED: parse_player_websocket_closed,
}

del parse_track_end
del parse_track_exception
del parse_track_start
del parse_track_stuck
del parse_player_websocket_closed
