__all__ = ()

import sys

from ..core import KOKORO


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
    err : `Any`
        The caught exception. Can be given as non `BaseException` instance as well.
    """
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
    ]
    
    if isinstance(err, BaseException):
        await KOKORO.render_exc_async(err, extracted)
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
