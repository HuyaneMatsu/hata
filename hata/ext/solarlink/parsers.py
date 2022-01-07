__all__ = ()

from scarletio import Task

from ...discord.core import KOKORO

from .constants import (
    LAVALINK_KEY_EVENT_PLAYER_WEBSOCKET_CLOSED, LAVALINK_KEY_EVENT_TRACK_END, LAVALINK_KEY_EVENT_TRACK_EXCEPTION,
    LAVALINK_KEY_EVENT_TRACK_START, LAVALINK_KEY_EVENT_TRACK_STUCK, LAVALINK_KEY_GUILD_ID
)
from .event_types import (
    PlayerWebsocketClosedEvent, TrackEndEvent, TrackExceptionEvent, TrackStartEvent, TrackStuckEvent
)


def parse_track_end(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    event = TrackEndEvent(player, data)
    
    Task(client.solarlink._events.track_end(client, event), KOKORO)
    

def parse_track_exception(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    event = TrackExceptionEvent(player, data)
    
    Task(client.solarlink._events.track_exception(client, event), KOKORO)


def parse_track_start(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    event = TrackStartEvent(player, data)
    Task(client.solarlink._events.track_start(client, event), KOKORO)



def parse_track_stuck(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    event = TrackStuckEvent(player, data)
    Task(client.solarlink._events.track_stuck(client, event), KOKORO)


def parse_player_websocket_closed(client, data):
    guild_id = int(data[LAVALINK_KEY_GUILD_ID])
    
    try:
        player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    event = PlayerWebsocketClosedEvent(player, data)
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
