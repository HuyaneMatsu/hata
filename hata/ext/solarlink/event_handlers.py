__all__ = ()

from scarletio import Task, WaitTillAll

from ...discord.core import KOKORO

from .constants import LAVALINK_KEY_SESSION_ID, LAVALINK_KEY_VOICE_SERVER_UPDATE_EVENT


async def handle_voice_client_join(client, voice_state):
    """
    Called when the client joins a voice channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    voice_state : ``VoiceState``
        The client's voice state.
    """
    guild_id = voice_state.guild_id
    
    try:
        solar_player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    solar_player.channel_id = voice_state.channel_id
    
    forward_data = solar_player._forward_data
    if forward_data is None:
        forward_data = {}
        solar_player._forward_data = forward_data
    
    forward_data[LAVALINK_KEY_SESSION_ID] = voice_state.session_id
    
    await solar_player._voice_update()


async def handle_voice_client_move(client, voice_state, old_channel_id):
    """
    Called when the client moves between voice channels.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    voice_state : ``VoiceState``
        The client's voice state.
    old_channel_id : `int`
        The channel's identifier from where there client moved.
    """
    guild_id = voice_state.guild_id
    
    try:
        solar_player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    solar_player.channel_id = voice_state.channel_id


async def handle_voice_client_update(client, voice_state, old_attributes):
    """
    Called when the client's voice state is edited.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    voice_state : ``VoiceState``
        The client's voice state.
    old_attributes : `dict` of (`str`, `Any`) items
        The voice state's old, changed attributes in `attribute-name` - `old-value` relation.
    """
    guild_id = voice_state.guild_id
    
    try:
        solar_player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    if 'session_id' not in old_attributes:
        return
    
    forward_data = solar_player._forward_data
    if forward_data is None:
        forward_data = {}
        solar_player._forward_data = forward_data
        forward = False
    else:
        forward = True
        
    forward_data[LAVALINK_KEY_SESSION_ID] = voice_state.session_id
    
    if not forward:
        return
    
    await solar_player._voice_update()


async def handle_voice_client_leave(client, voice_state, old_channel_id):
    """
    Called when the client leaves from a voice channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    voice_state : ``VoiceState``
        The client's voice state.
    old_channel_id : `int`
        The channel's identifier from where there client left.
    """
    guild_id = voice_state.guild_id
    
    try:
        solar_player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    solar_player.channel_id = 0
    await solar_player.disconnect()


async def handle_voice_server_update(client, event):
    """
    Called when a guild's voice server, or when the client joins a voice channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    event : ``VoiceServerUpdateEvent``
        The event.
    """
    guild_id = event.guild_id
    
    try:
        solar_player = client.solarlink.players[guild_id]
    except KeyError:
        return
    
    forward_data = solar_player._forward_data
    if forward_data is None:
        forward_data = {}
        solar_player._forward_data = forward_data
    
    forward_data[LAVALINK_KEY_VOICE_SERVER_UPDATE_EVENT] = {
        'guild_id': str(event.guild_id),
        'endpoint': event.endpoint,
        'token': event.token,
    }
    
    await solar_player._voice_update()


async def handle_voice_client_ghost(client, voice_state):
    """
    Called when a ghost voice client is present, when logging into discord.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    voice_state : ``VoiceState``
        The client's voice state.
    """
    player = await client.solarlink.join_voice((voice_state.guild_id, voice_state.channel_id))
    await player.disconnect()


async def handle_voice_client_shutdown(client):
    """
    Called when the client logs out.
    
    This function is a coroutine.
    """
    tasks = []
    for player in client.solarlink.players.values():
        task = Task(player.disconnect(), KOKORO)
        tasks.append(task)
    
    task = None
    await WaitTillAll(tasks, KOKORO)
    
    tasks = []
    for node in client.solarlink.nodes:
        task = Task(node.close(), KOKORO)
        tasks.append(task)
    
    task = None
    await WaitTillAll(tasks, KOKORO)
