__all__ = ('abort', 'InteractionResponse',)

import warnings

from ...backend.futures import is_coroutine_generator

from ...discord.embed import EmbedBase
from ...discord.client import Client
from ...discord.interaction import InteractionType

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component


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


async def get_request_coroutines(client, interaction_event, show_for_invoking_user_only, response, is_return):
    """
    Gets request coroutine after an output from a command coroutine. Might return `None` if there is nothing to send.
    
    This function is a coroutine generator, which should be ued inside of an async for loop.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    show_for_invoking_user_only : `bool`
        Whether the response message should only be shown for the invoking user.
    response : `Any`
        Any object yielded or returned by the command coroutine.
    is_return : `bool`
        Whether the response is used in a return and we do not require response message.
    
    Yields
    -------
    request_coro : `None` or `coroutine`
    """
    interaction_event_type = interaction_event.type
    
    if (response is None):
        if interaction_event.is_unanswered():
            
            if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
                yield client.interaction_application_command_acknowledge(
                    interaction_event,
                    show_for_invoking_user_only = show_for_invoking_user_only,
                )
            
            elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
                yield client.interaction_component_acknowledge(interaction_event)
        
        return
    
    if isinstance(response, (str, EmbedBase)) or is_only_embed(response):
        if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
            if interaction_event.is_unanswered():
                yield client.interaction_response_message_create(
                    interaction_event,
                    response,
                    show_for_invoking_user_only = show_for_invoking_user_only,
                )
            
            elif interaction_event.is_deferred():
                yield client.interaction_followup_message_create(interaction_event, response)
            elif interaction_event.is_responded():
                yield client.interaction_followup_message_create(
                    interaction_event,
                    response,
                    show_for_invoking_user_only = show_for_invoking_user_only,
                )
        
        elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
            yield client.interaction_component_message_edit(interaction_event, response)
        
        # No more cases
        return
    
    if is_coroutine_generator(response):
        response = await process_command_coroutine_generator(
            client,
            interaction_event,
            show_for_invoking_user_only,
            response,
        )
        
        async for request_coro in get_request_coroutines(
            client,
            interaction_event,
            show_for_invoking_user_only,
            response,
            is_return,
        ):
            yield request_coro
        
        return
    
    if isinstance(response, InteractionResponse):
        for request_coro in response.get_request_coroutines(
            client,
            interaction_event,
            show_for_invoking_user_only,
            is_return,
        ):
            yield request_coro
        
        return
    
    response = str(response)
    if len(response) > 2000:
        response = response[:2000]
    
    if response:
        
        if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
            if interaction_event.is_unanswered():
                yield client.interaction_response_message_create(
                    interaction_event,
                    response,
                    show_for_invoking_user_only = show_for_invoking_user_only,
                )
            elif interaction_event.is_deferred():
                yield client.interaction_response_message_edit(interaction_event, response)
            elif interaction_event.is_responded():
                yield client.interaction_followup_message_create(
                    interaction_event,
                    response,
                    show_for_invoking_user_only = show_for_invoking_user_only,
                )
        elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
            yield client.interaction_component_message_edit(interaction_event, response)
        
        # No more cases
        return
    else:
        if interaction_event.is_unanswered():
            
            if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
                yield client.interaction_response_message_create(
                    interaction_event,
                    show_for_invoking_user_only = show_for_invoking_user_only
                )
            elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
                yield client.interaction_component_acknowledge(interaction_event)
            
            return
    
    # No more cases
    return


async def process_command_coroutine_generator(
    client,
    interaction_event,
    show_for_invoking_user_only,
    coroutine_generator,
):
    """
    Processes a slash command coroutine generator.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    show_for_invoking_user_only : `bool`
        Whether the response message should only be shown for the invoking user.
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
        
        except InteractionAbortedError as err:
            response = err.response
            break
        
        except BaseException as err:
            if (response_exception is None) or (response_exception is not err):
                raise
            
            if isinstance(err, ConnectionError):
                return
            
            raise
        
        else:
            # We set it first, since if `get_request_coroutines` yields nothing, we would be meowed up.
            response_message = None
            response_exception = None
            
            async for request_coro in get_request_coroutines(
                client,
                interaction_event,
                show_for_invoking_user_only,
                response,
                False,
            ):
                try:
                    response_message = await request_coro
                except BaseException as err:
                    # `response_message` may have be set before with an iteration, so reset it.
                    response_message = None
                    response_exception = err
                    break
    
    
    return response


async def process_command_coroutine(client, interaction_event, show_for_invoking_user_only, coroutine):
    """
    Processes a slasher application command coroutine.
    
    If the coroutine returns or yields a string or an embed like then sends it to the respective channel.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    show_for_invoking_user_only : `bool`
        Whether the response message should only be shown for the invoking user.
    coroutine : `Coroutine`
        A coroutine which will produce command response.
    
    Raises
    ------
    BaseException
        Any exception raised by `coroutine`.
    """
    if is_coroutine_generator(coroutine):
        response = await process_command_coroutine_generator(
            client,
            interaction_event,
            show_for_invoking_user_only,
            coroutine,
        )
    else:
        try:
            response = await coroutine
        except InteractionAbortedError as err:
            response = err.response
    
    async for request_coro in get_request_coroutines(
        client,
        interaction_event,
        show_for_invoking_user_only,
        response,
        True,
    ):
        try:
            await request_coro
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            raise


class InteractionResponse:
    """
    Rich interaction response message usable with `return` or with `yield` statements.
    
    May pass it's parameters to any oft he following method depending on control flow.
    
    - ``Client.interaction_response_message_create``
    - ``Client.interaction_response_message_edit``
    - ``Client.interaction_followup_message_create``
    - ``Client.interaction_component_acknowledge``
    - ``Client.interaction_component_message_edit``
    
    Attributes
    ----------
    _event : `None` or ``InteractionEvent``
        The interaction event to use instead of the default one.
    _is_abort : `bool`
        Whether the slash response is derived from an ``abort`` call.
    _message : `Ellipsis`, `None` or ``Message`` instance.
        Whether a message should be edited instead of creating a new one.
    _parameters : `dict` of (`str`, `Any`) items
        Parameters to pass to the respective ``Client`` functions.
        
        Can have the following keys:
        
        - `'allowed_mentions'`
        - `'content'`
        - `'components'`
        - `'embed'`
        - `'file'`
        - `'show_for_invoking_user_only'`
        - `'tts'`
    """
    __slots__ = ('_event', '_is_abort', '_message', '_parameters',)
    
    def __init__(self, content=..., *, embed=..., file=..., allowed_mentions=..., components=..., tts=...,
            show_for_invoking_user_only=..., message=..., event=None):
        """
        Creates a new ``InteractionResponse`` instance with the given parameters.
        
        Parameters
        ----------
        content : `str`, ``EmbedBase``, `Any`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str` or ``EmbedBase`` instance is given, then will be casted to string.
            
            If given as ``EmbedBase`` instance, then is sent as the message's embed.
            
        embed : ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `TypeError` is raised.
        file : `Any`, Optional (Keyword only)
            A file to send. Check ``Client._create_file_form`` for details.
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``Client._parse_allowed_mentions`` for details.
        components : `None`, ``ComponentBase``, (`set`, `list`) of ``ComponentBase``, Optional (Keyword only)
            Components attached to the message.
        tts : `bool`, Optional (Keyword only)
            Whether the message is text-to-speech.
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to the value passed when adding
            the command.
            
            If given as `True` only the message's content will be processed by Discord.
        
        message : `None`, ``Message``, Optional (Keyword only)
            Whether the interaction's message should be edited.
        event : `None`, ``InteractionEvent``, Optional (Keyword only)
            A specific event ot answer instead of the command's.
        """
        self._is_abort = False
        self._parameters = parameters = {}
        self._message = message
        self._event = event
        
        if (content is not ...):
            parameters['content'] = content
        
        if (embed is not ...):
            parameters['embed'] = embed
        
        if (file is not ...):
            parameters['file'] = file
        
        if (allowed_mentions is not ...):
            parameters['allowed_mentions'] = allowed_mentions
        
        if (components is not ...):
            parameters['components'] = components
        
        if (tts is not ...):
            parameters['tts'] = tts
        
        if (show_for_invoking_user_only is not ...):
            parameters['show_for_invoking_user_only'] = show_for_invoking_user_only
    
    def _get_response_parameters(self, allowed_parameters):
        """
        Gets response parameters to pass to a ``Client`` method.
        
        Parameters
        ----------
        allowed_parameters : `tuple` of `str`
            Allowed parameters to be passed to the respective client method.
        
        Returns
        -------
        response_parameters : `dict` of (`str`, `Any`) items
            Parameters to pass the the respective client method.
        """
        parameters = self._parameters
        response_parameters = {}
        for key in allowed_parameters:
            try:
                value = parameters[key]
            except KeyError:
                continue
            
            response_parameters[key] = value
        
        return response_parameters
    
    def get_request_coroutines(self, client, interaction_event, show_for_invoking_user_only, is_return):
        """
        Gets request coroutine buildable from the ``InteractionResponse``.
        
        This method is a generator, which should be used inside of a `for` loop.
        
        client : ``Client``
            The client who will send the responses if applicable.
        interaction_event : ``InteractionEvent``
            The respective event to respond on.
        show_for_invoking_user_only : `bool`
            Whether the response message should only be shown for the invoking user.
        is_return : `bool`
            Whether the response is used in a return and we do not require response message.
        
        Yields
        -------
        request_coro : `None` or `coroutine`
        """
        event = self._event
        if (event is not None):
            interaction_event = event
        
        interaction_event_type = interaction_event.type
        if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
            message = self._message
            if message is not ...:
                response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'components',
                    'embed', 'file'))
                
                if message is None:
                    yield client.interaction_response_message_edit(interaction_event, **response_parameters)
                else:
                    yield client.interaction_followup_message_edit(interaction_event, message, **response_parameters)
                return
            
            show_for_invoking_user_only = self._parameters.get(
                'show_for_invoking_user_only',
                show_for_invoking_user_only,
            )
            
            if ('file' in self._parameters):
                need_acknowledging = True
            elif self._is_abort:
                need_acknowledging = False
            elif is_return:
                need_acknowledging = False
            elif interaction_event.is_unanswered():
                need_acknowledging = True
            else:
                need_acknowledging = False
            
            if need_acknowledging:
                yield client.interaction_response_message_create(
                    interaction_event,
                    show_for_invoking_user_only = show_for_invoking_user_only,
                )
            
            response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed',
                'file', 'tts', 'components'))
            
            if (not need_acknowledging):
                response_parameters['show_for_invoking_user_only'] = show_for_invoking_user_only
            
            
            yield client.interaction_followup_message_create(interaction_event, **response_parameters)
            return
        
        elif interaction_event.type is INTERACTION_TYPE_MESSAGE_COMPONENT:
            response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'components'))
            if response_parameters:
                yield client.interaction_component_message_edit(interaction_event, **response_parameters)
            else:
                yield client.interaction_component_acknowledge(interaction_event)
            
            return
        
        # no more cases
    
    def __repr__(self):
        """Returns the slash response's representation."""
        repr_parts = ['<', self.__class__.__name__, ' ']
        if self._is_abort:
            repr_parts.append('(abort) ')
        
        parameters = self._parameters
        if parameters:
            for key, value in parameters.items():
                repr_parts.append(key)
                repr_parts.append('=')
                repr_parts.append(repr(value))
                repr_parts.append(', ')
            
            repr_parts[-1] = '>'
        else:
            repr_parts.append('>')
        
        return ''.join(repr_parts)


def abort(content=..., *, embed=..., file=..., allowed_mentions=..., components=..., tts=...,
        show_for_invoking_user_only=..., message=..., event=None):
    """
    Aborts the slash response with sending the passed parameters as a response.
    
    The abortion auto detects `show_for_invoking_user_only` if not given. Not follows the command's preference.
    If only a string `content` is given, `show_for_invoking_user_only` will become `True`, else `False`. The reason of
    becoming `False` at that case is, Discord ignores every other field except string content.
    
    Parameters
    ----------
    content : `str`, ``EmbedBase``, `Any`, Optional
        The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
        if any other non `str` or ``EmbedBase`` instance is given, then will be casted to string.
        
        If given as ``EmbedBase`` instance, then is sent as the message's embed.
    embed : ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional (Keyword only)
        The embedded content of the message.
        
        If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `TypeError` is raised.
    file : `Any`, Optional (Keyword only)
        A file to send. Check ``Client._create_file_form`` for details.
    allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
            , Optional (Keyword only)
        Which user or role can the message ping (or everyone). Check ``Client._parse_allowed_mentions`` for details.
    components : `None`, ``ComponentBase``, (`set`, `list`) of ``ComponentBase``, Optional (Keyword only)
        Components attached to the message.
    tts : `bool`, Optional (Keyword only)
        Whether the message is text-to-speech.
    show_for_invoking_user_only : `bool`, Optional (Keyword only)
        Whether the sent message should only be shown to the invoking user.
        
        If given as `True`, only the message's content and embeds and components will be processed by Discord.
    
    Raises
    ------
    InteractionAbortedError
        The exception which aborts the interaction, then yields the response.
    message : `None`, ``Message``, Optional (Keyword only)
        Whether the interaction's message should be edited.
    event : `None`, ``InteractionEvent``, Optional (Keyword only)
        A specific event ot answer instead of the command's.
    """
    if show_for_invoking_user_only is ...:
        if (file is not ...):
            show_for_invoking_user_only = False
        else:
            show_for_invoking_user_only = True
    
    response = InteractionResponse(content, embed=embed, file=file, allowed_mentions=allowed_mentions, components=components,
        tts=tts, show_for_invoking_user_only=show_for_invoking_user_only, message=message, event=event)
    response._is_abort = True
    raise InteractionAbortedError(response)


class InteractionAbortedError(BaseException):
    """
    An ``InteractionAbortedError`` is raised when a slash command is aborted. This class holds the response to send to
    the client.
    
    Attributes
    ----------
    response : ``InteractionResponse``
        The response to send.
    """
    def __init__(self, response):
        """
        Creates a new ``InteractionAbortedError`` instance with the given response.
        
        Parameters
        ----------
        response : ``InteractionResponse``
            The response to send.
        """
        self.response = response
        BaseException.__init__(self, response)
    
    def __repr__(self):
        """Returns the exception's representation."""
        return f'{self.__class__.__name__}({self.response!r})'


async def process_auto_completer_coroutine(client, interaction_event, coroutine):
    """
    Processes a slasher application command coroutine.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    coroutine : `Coroutine`
        A coroutine which will produce command response.
    
    Raises
    ------
    BaseException
        Any exception raised by `coroutine`.
    """
    response = await coroutine
    await client.interaction_application_command_autocomplete(interaction_event, response)
