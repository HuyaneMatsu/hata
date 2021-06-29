__all__ = ()

from ...backend.futures import is_coroutine_generator

from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.embed import EmbedBase

def is_only_embed(maybe_embeds):
    """
    Checks whether the given value is a `tuple` or `list` containing only `embed-like`-s.
    
    Parameters
    ----------
    maybe_embeds : (`tuple` or `list`) of `EmbedBase` or `Any`
        The value to check whether is a `tuple` or `list` containing only `embed-like`-s.
    
    Returns
    -------
    is_only_embed : `bool`
    """
    if not isinstance(maybe_embeds, (list, tuple)):
        return False
    
    for maybe_embed in maybe_embeds:
        if not isinstance(maybe_embed, EmbedBase):
            return False
    
    return True


async def send_response(command_context, response):
    """
    Sends to discord the given response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    command_context : ``CommandContext``
        The respective command context.
    response : `Any`
        Any object yielded or returned by the command coroutine.
    
    Returns
    -------
    message : `None` or ``Message``
        The sent message if any.
    """
    if (response is None):
        return
    
    if isinstance(response, str):
        return await command_context.client.message_create(command_context.channel, response)
        
    if isinstance(response, EmbedBase) or is_only_embed(response) and response:
        return await command_context.client.message_create(command_context.channel, embed=response)
    
    if is_coroutine_generator(response):
        return await process_command_coroutine_generator(command_context, response)
    
    response = str(response)
    if len(response) > 2000:
        response = response[:2000]
    
    if response:
        response = await command_context.client.message_create(command_context.channel, response)
        return await send_response(command_context, response)
    
    # No more cases
    return


async def process_command_coroutine_generator(command_context, coroutine_generator):
    """
    Processes a command coroutine generator.
    
    This function is a coroutine.
    
    Parameters
    ----------
    command_context : ``CommandContext``
        The respective command context.
    coroutine_generator : `CoroutineGenerator`
        A coroutine generator with will send command response.
    
    Returns
    -------
    response : `Any`
        Returned object by the coroutine generator.
    
    Raises
    ------
    BaseException
        Any exception raised by `coroutine_generator`.
    """
    response_message = None
    response_exception = None
    while True:
        if response_exception is None:
            step = coroutine_generator.asend(response_message)
        else:
            step = coroutine_generator.athrow(response_exception)
        
        try:
            response = await step
        except StopAsyncIteration as err:
            # catch `StopAsyncIteration` only if it is a new one.
            if (response_exception is not None) and (response_exception is not err):
                raise
            
            args = err.args
            if args:
                response = args[0]
            else:
                response = None
            break
        
        except BaseException as err:
            if (response_exception is None) or (response_exception is not err):
                raise
            
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # Message's channel deleted; Can we get this?
                        ERROR_CODES.missing_access, # Client removed.
                            ):
                    return
            
            raise
        
        else:
            try:
                response_message = await send_response(command_context, response)
            except BaseException as err:
                response_message = None
                response_exception = err
            else:
                response_exception = None
    
    return response


async def process_command_coroutine(command_context, coroutine):
    """
    Processes a command coroutine.
    
    If the coroutine returns or yields a string or an embed like then sends it to the respective channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    command_context : ``CommandContext``
        The respective command context.
    coroutine : `Coroutine`
        A coroutine with will send command response.
    
    Raises
    ------
    BaseException
        Any exception raised by `coro`.
    """
    if is_coroutine_generator(coroutine):
        response = await process_command_coroutine_generator(command_context, coroutine)
    else:
        response = await coroutine
    
    await send_response(command_context, response)
