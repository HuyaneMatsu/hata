__all__ = ()

import sys

from scarletio import Task, TaskGroup, write_exception_async

from ..core import KOKORO
from ..voice import VoiceClient


async def default_error_event_handler(client, name, err):
    """
    Defaults error event for client. Renders the given exception to `sys.stderr`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``client``
        The client who caught the error.
    name : `str`
        Identifier name of the place where the error occurred.
    err : `object`
        The caught exception. Can be given as non `BaseException` as well.
    """
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
    ]
    
    if isinstance(err, BaseException):
        await write_exception_async(err, extracted, loop = KOKORO)
        return
    
    if not isinstance(err, str):
        err = repr(err)
    
    extracted.append(err)
    extracted.append('\n')
    
    sys.stderr.write(''.join(extracted))


async def default_voice_server_update_event_handler(client, event):
    """
    Default voice server update event handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client, who received the event.
    event : ``VoiceServerUpdateEvent``
        The received event.
    """
    try:
        voice_client = client.voice_clients[event.guild_id]
    except KeyError:
        pass
    else:
        await voice_client._create_socket(event)


async def default_voice_client_ghost_event_handler(client, voice_state):
    """
    Defaults voice client ghost event handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The client's ghost voice state.
    """
    await VoiceClient._kill_ghost(client, voice_state)


async def default_voice_client_join_event_handler(client, voice_state):
    """
    Defaults voice client join event handler
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The created voice state.
    """
    try:
        voice_client = client.voice_clients[voice_state.guild_id]
    except KeyError:
        pass
    else:
        voice_client.channel_id = voice_state.channel_id


async def default_voice_client_move_event_handler(client, voice_state, old_channel_id):
    """
    Defaults voice client move event handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The client's voice state.
    old_channel_id : `int`
        The old channel's identifier, where the voice client was.
    """
    try:
        voice_client = client.voice_clients[voice_state.guild_id]
    except KeyError:
        pass
    else:
        voice_client.channel_id = voice_state.channel_id


async def default_voice_client_leave_event_handler(client, voice_state, old_channel_id):
    """
    Defaults voice client leave event handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The client's voice state.
    old_channel_id : `int`
        The old channel's identifier, where the voice client was.
    """
    try:
        voice_client = client.voice_clients[voice_state.guild_id]
    except KeyError:
        pass
    else:
        await voice_client._disconnect(force = True, terminate = False)


async def default_voice_client_update_event_handler(client, voice_state, old_attributes):
    """
    Defaults voice client update event handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    voice_state : ``VoiceState``
        The client's voice state.
    old_attributes : `dict` of `str`, `object`
        The modified attributes of the voice state.
        
        Every item in `old_attributes` is optional and they can be any of the following:
        
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None`, `datetime`    |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
        | speaker               | `bool`                |
        +-----------------------+-----------------------+
    """
    # We do nothing with it right now
    pass


async def default_voice_client_shutdown_event_handler(client):
    """
    Default voice client shutdown event handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who is disconnected.
    """
    voice_clients = client.voice_clients
    if voice_clients:
        await TaskGroup(
            KOKORO,
            (Task(KOKORO, voice_client._disconnect()) for voice_client in voice_clients.values())
        ).wait_all()
