__all__ = ()

from ...backend.futures import Task

from ..exceptions import DiscordException
from ..core import KOKORO

from .core import PARSERS

SYNC_REQUESTS = {}

async def sync_task(queue_id, coro, queue):
    """
    Syncer task ensured if a guild related dispatch event fails, when any expected entity mentioned by it was not
    found.
    
    This function is a coroutine.
    
    Parameters
    ----------
    queue_id : `int`
        The respective guild's id to identify queued up unhandled dispatch event when de-sync happened.
    coro : `coroutine`
        ``Client.guild_sync`` coroutine.
    queue : `list` of `tuple` (``Client``, `Any`, (`str` or `tuple` (`str`, `function`, `Any`)))
        A queue of events to call with the specified parameters.
        
        First element of the queue is always the respective client of the received dispatch event. The second is the
        payload of the dispatch event, meanwhile the third can be the name of it (parser name case), or a `tuple` of
        3 elements (checker case), where the first is the name of the parser, the second is a checker and the third is
        an additional value to check with.
        
        At the parser name case, the parser will be called at every case, meanwhile at the checker case, the checker
        will be called with the synced guild and with the passed value, and then the parser will be called only, if the
        the checker returned `True`.
    """
    try:
        guild = await coro
    except (DiscordException, ConnectionError):
        return
    else:
        # Fix infinite loops by do not dispatching again on error
        for index in range(len(queue)):
            client, data, parser_and_checker = queue[index]
            if type(parser_and_checker) is str:
                PARSERS[parser_and_checker](client, data)
                continue
            
            parser_name, checker, value = parser_and_checker
            if checker(guild, value):
                PARSERS[parser_name](client, data)
    finally:
        del SYNC_REQUESTS[queue_id]


def check_channel(guild, channel_id):
    """
    Checks whether the given guild has a channel with the specified id.
    
    This function is a checker used at guild syncing.
    
    Parameters
    ----------
    guild : ``Guild``
    channel_id : `int`
    """
    return (channel_id in guild.channels)


def guild_sync(client, data, parser_and_checker):
    """
    Syncer function what is called when any expected entity mentioned by a dispatch event's parser was not found.
    
    Looks up whether the given guild has already a syncer task, if it has not, then creates a new ``sync_task`` for it.
    If `parser_and_checker` is given as not `None`, then the respective failed parser will be called when the syncer
    finished.
    
    Parameters
    ----------
    client : ``Client``
        The respective client of the dispatch event.
    data : `Any`
        The payload of the dispatch event.
    parser_and_checker : `None` or `str` or `tuple` (`str`, `function`, `Any`)
        - Is passed as `None` if only the syncer task should run.
        - Is passed as `str`, if the respective parser should be called when syncing is done.
        - Is passed as `tuple` of 3 elements : `str`, `function`, `Any`; if the respective parser's calling is bound to
            a condition. The passed `function` should contain the condition and accept the respective guild and the
            third value (the type `Any` one) as parameters and return the condition's result.
    """
    try:
        guild_id = int(data['guild_id'])
    except KeyError:
        return
    
    try:
        queue = SYNC_REQUESTS[guild_id]
    except KeyError:
        queue = []
        Task(sync_task(guild_id, client.guild_sync(guild_id), queue), KOKORO)
        SYNC_REQUESTS[guild_id] = queue
    
    if parser_and_checker is None:
        return
    queue.append((client, data, parser_and_checker),)
