__all__ = ('abort', 'InteractionAbortedError', 'InteractionResponse',)

from scarletio import is_coroutine_generator, skip_ready_cycle

from ...discord.client import Client
from ...discord.component import InteractionForm
from ...discord.embed import Embed
from ...discord.interaction import InteractionType

from .response_modifier import (
    get_show_for_invoking_user_only_from, get_show_for_invoking_user_only_of, get_wait_for_acknowledgement_of,
    un_map_pack_response_creation_modifier, un_map_pack_response_edition_modifier
)


INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component
INTERACTION_TYPE_FORM_SUBMIT = InteractionType.form_submit
INTERACTION_TYPE_AUTOCOMPLETE = InteractionType.application_command_autocomplete


def is_only_embed(maybe_embeds):
    """
    Checks whether the given value is a `tuple`, `list` containing only `embed-like`-s.
    
    Parameters
    ----------
    maybe_embeds : (`tuple`, `list`) of `Embed`, `object`
        The value to check whether is a `tuple`, `list` containing only `embed-like`-s.
    
    Returns
    -------
    is_only_embed : `bool`
    """
    if not isinstance(maybe_embeds, (list, tuple)):
        return False
    
    for maybe_embed in maybe_embeds:
        if not isinstance(maybe_embed, Embed):
            return False
    
    return True


async def get_request_coroutines(client, interaction_event, response_modifier, response, is_return):
    """
    Gets request coroutine after an output from a command coroutine. Might return `None` if there is nothing to send.
    
    This function is an async iterable coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    response : `object`
        object object yielded or returned by the command coroutine.
    is_return : `bool`
        Whether the response is used in a return and we do not require response message.
    
    Yields
    -------
    request_coroutine : `None`, `CoroutineType`
    """
    interaction_event_type = interaction_event.type
    
    # unanswered auto completions are a special case, where we want to auto complete if the event is unanswered.
    if (interaction_event_type is INTERACTION_TYPE_AUTOCOMPLETE) and interaction_event.is_unanswered():
        yield client.interaction_application_command_autocomplete(interaction_event, response)
        return
    
    if (response is None):
        if interaction_event.is_unanswered():
            if (
                (interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND) or
                (interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT)
            ):
                if (not is_return):
                    # This usually means, the command is uncompleted
                    yield client.interaction_application_command_acknowledge(
                        interaction_event,
                        get_wait_for_acknowledgement_of(response_modifier),
                        show_for_invoking_user_only = get_show_for_invoking_user_only_of(response_modifier),
                    )
                
                return
            
            if interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
                if is_return:
                    # Maybe the user launched up an other task to handle the component interaction. If this happened,
                    # we just need to skip a ready cycle
                    await skip_ready_cycle()
                    
                    # If the user indeed launched up an other task, we leave.
                    if not interaction_event.is_unanswered():
                        return
                
                yield client.interaction_component_acknowledge(
                    interaction_event,
                    get_wait_for_acknowledgement_of(response_modifier),
                )
                
                return
        
        # no more cases
        return
    
    # wait for async acknowledgement if applicable
    await interaction_event._wait_for_async_task_completion()
    
    if isinstance(response, (str, Embed)) or is_only_embed(response):
        async for request_coroutine in _get_request_coroutines_from_value(
            client,
            interaction_event,
            response_modifier,
            response,
            is_return,
        ):
            yield request_coroutine
        
        return
    
    if isinstance(response, InteractionForm):
        yield client.interaction_form_send(interaction_event, response)
        return
    
    if is_coroutine_generator(response):
        response = await process_command_coroutine_generator(
            client,
            interaction_event,
            response_modifier,
            response,
        )
        
        async for request_coroutine in get_request_coroutines(
            client,
            interaction_event,
            response_modifier,
            response,
            is_return,
        ):
            yield request_coroutine
        
        return
    
    if isinstance(response, InteractionResponse):
        for request_coroutine in response.get_request_coroutines(
            client,
            interaction_event,
            response_modifier,
            is_return,
        ):
            yield request_coroutine
        
        return
    
    response = str(response)
    if len(response) > 2000:
        response = response[:2000]
    
    async for request_coroutine in _get_request_coroutines_from_value(
        client,
        interaction_event,
        response_modifier,
        response,
        is_return,
    ):
        yield request_coroutine
    
    # No more cases
    return


async def _get_request_coroutines_from_value(client, interaction_event, response_modifier, response, is_return):
    """
    Gets request coroutine after an output from a command coroutine. Might return `None` if there is nothing to send.
    
    This function is an async iterable coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    response : `object`
        object object yielded or returned by the command coroutine.
    is_return : `bool`
        Whether the response is used in a return and we do not require response message.
    
    Yields
    -------
    request_coroutine : `None`, `CoroutineType`
    """
    interaction_event_type = interaction_event.type
    
    if interaction_event.is_responded():
        yield client.interaction_followup_message_create(
            interaction_event,
            response,
            show_for_invoking_user_only = get_show_for_invoking_user_only_of(response_modifier),
        )
    
    else:
        if (
            (interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND) or
            (
                (interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT) and
                (interaction_event.message is None)
            )
        ):
            if interaction_event.is_unanswered():
                yield client.interaction_response_message_create(
                    interaction_event,
                    response,
                    **un_map_pack_response_creation_modifier(response_modifier),
                )
            
            elif interaction_event.is_deferred():
                yield client.interaction_followup_message_create(
                    interaction_event,
                    response,
                    **un_map_pack_response_creation_modifier(response_modifier),
                )
        elif (
            (interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT) or
            (
                (interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT) and
                (interaction_event.message is not None)
            )
        ):
            if interaction_event.is_unanswered():
                yield client.interaction_component_message_edit(
                    interaction_event,
                    response,
                    **un_map_pack_response_edition_modifier(response_modifier),
                )
            
            elif interaction_event.is_deferred():
                yield client.interaction_response_message_edit(
                    interaction_event,
                    response,
                    **un_map_pack_response_edition_modifier(response_modifier),
                )


async def process_command_coroutine_generator(
    client,
    interaction_event,
    response_modifier,
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
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    coroutine_generator : `CoroutineGeneratorType`
        A coroutine generator with will send command response.
    
    Returns
    -------
    response : `object`
        Returned object by the coroutine generator.
    
    Raises
    ------
    BaseException
        object exception raised by `coroutine_generator`.
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
            
            raise
        
        else:
            # We set it first, since if `get_request_coroutines` yields nothing, we would be meowed up.
            response_message = None
            response_exception = None
            
            async for request_coroutine in get_request_coroutines(
                client,
                interaction_event,
                response_modifier,
                response,
                False,
            ):
                try:
                    response_message = await request_coroutine
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    # `response_message` may have be set before with an iteration, so reset it.
                    response_message = None
                    response_exception = err
                    break
    
    
    return response


async def process_command_coroutine(client, interaction_event, response_modifier, coroutine):
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
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    coroutine : `Coroutine`
        A coroutine which will produce command response.
    
    Raises
    ------
    BaseException
        object exception raised by `CoroutineType`.
    """
    if is_coroutine_generator(coroutine):
        response = await process_command_coroutine_generator(
            client,
            interaction_event,
            response_modifier,
            coroutine,
        )
    else:
        try:
            response = await coroutine
        except InteractionAbortedError as err:
            response = err.response
    
    async for request_coroutine in get_request_coroutines(
        client,
        interaction_event,
        response_modifier,
        response,
        True,
    ):
        await request_coroutine


class InteractionResponse:
    """
    Rich interaction response message usable with `return` or with `yield` statements.
    
    May pass it's parameters to any of the following method depending on control flow.
    
    - ``Client.interaction_response_message_create``
    - ``Client.interaction_response_message_edit``
    - ``Client.interaction_followup_message_create``
    - ``Client.interaction_component_acknowledge``
    - ``Client.interaction_component_message_edit``
    
    Attributes
    ----------
    _abort : `bool`
        Whether the slash response is derived from an ``abort`` call.
    _event : `None`, ``InteractionEvent``
        The interaction event to use instead of the default one.
    _message : `Ellipsis`, `None`, ``Message``.
        Whether a message should be edited instead of creating a new one.
    _parameters : `dict` of (`str`, `object`) items
        Parameters to pass to the respective ``Client`` functions.
        
        Can have the following keys:
        
        - `'allowed_mentions'`
        - `'content'`
        - `'components'`
        - `'embed'`
        - `'file'`
        - `'show_for_invoking_user_only'`
        - '`silent`'
        - `'suppress_embeds'`
        - `'tts'`
    """
    __slots__ = ('_abort', '_event', '_message', '_parameters',)
    
    def __init__(
        self,
        content = ...,
        *,
        allowed_mentions = ...,
        components = ...,
        embed = ...,
        event = None,
        file = ...,
        message = ...,
        show_for_invoking_user_only = ..., 
        silent = ...,
        suppress_embeds = ...,
        tts = ...,
    ):
        """
        Creates a new ``InteractionResponse`` with the given parameters.
        
        Parameters
        ----------
        content : `None`, `str`, ``Embed``, `object`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``Embed`` is given, then will be casted to string.
            
            If given as ``Embed``, then is sent as the message's embed.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``Client._parse_allowed_mentions`` for
            details.
        
        components : `None`, ``Component``, (`set`, `list`) of ``Component``, Optional (Keyword only)
            Components attached to the message.
        
        embed : `None`, ``Embed``, `list` of ``Embed``, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``Embed``, then `TypeError` is raised.

        event : `None`, ``InteractionEvent`` = `None`, Optional (Keyword only)
            A specific event ot answer instead of the command's.
        
        file : `None`, `object`, Optional (Keyword only)
            A file to send. Check ``Client._create_file_form`` for details.
        
        message : `None`, ``Message``, Optional (Keyword only)
            Whether the interaction's message should be edited.
        
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to the value passed when
            adding the command.
        
        silent : `bool`, Optional (Keyword only)
            Whether the message should be delivered silently.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool`, Optional (Keyword only)
            Whether the message is text-to-speech.
        """
        self._abort = False
        self._parameters = parameters = {}
        self._message = message
        self._event = event
        
        if (allowed_mentions is not ...):
            parameters['allowed_mentions'] = allowed_mentions
        
        if (content is not ...):
            parameters['content'] = content
        
        if (components is not ...):
            parameters['components'] = components
        
        if (embed is not ...):
            parameters['embed'] = embed
        
        if (file is not ...):
            parameters['file'] = file
        
        if (show_for_invoking_user_only is not ...):
            parameters['show_for_invoking_user_only'] = show_for_invoking_user_only
        
        if (silent is not ...):
            parameters['silent'] = silent
        
        if (suppress_embeds is not ...):
            parameters['suppress_embeds'] = suppress_embeds
        
        if (tts is not ...):
            parameters['tts'] = tts
    
    
    def set_abort(self):
        """
        Marks the interaction response as an abortion.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self._abort = True
        return self
    
    
    def _get_response_parameters(self, allowed_parameters):
        """
        Gets response parameters to pass to a ``Client`` method.
        
        Parameters
        ----------
        allowed_parameters : `tuple` of `str`
            Allowed parameters to be passed to the respective client method.
        
        Returns
        -------
        response_parameters : `dict` of (`str`, `object`) items
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
    
    
    def get_request_coroutines(self, client, interaction_event, response_modifier, is_return):
        """
        Gets request coroutine buildable from the ``InteractionResponse``.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        client : ``Client``
            The client who will send the responses if applicable.
        interaction_event : ``InteractionEvent``
            The respective event to respond on.
        response_modifier : `None`, ``ResponseModifier``
            Modifies values returned and yielded to command coroutine processor.
        is_return : `bool`
            Whether the response is used in a return and we do not require response message.
        
        Yields
        -------
        request_coroutine : `None`, `CoroutineType`
        """
        event = self._event
        if (event is not None):
            interaction_event = event
        
        interaction_event_type = interaction_event.type
        if (
            (interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND) or
            (
                (interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT) and
                (interaction_event.message is None)
            )
        ):
            message = self._message
            if message is not ...:
                
                response_parameters = self._get_response_parameters((
                    'allowed_mentions', 'content', 'components', 'embed', 'file'
                ))
                if (response_modifier is not None):
                    response_modifier.apply_to_edition(response_parameters)
                
                if message is None:
                    yield client.interaction_response_message_edit(interaction_event, **response_parameters)
                else:
                    yield client.interaction_followup_message_edit(interaction_event, message, **response_parameters)
                return
            
            if (not interaction_event.is_unanswered()):
                need_acknowledging = False
            elif ('file' in self._parameters):
                need_acknowledging = True
            elif self._abort:
                need_acknowledging = False
            elif is_return:
                need_acknowledging = False
            else:
                need_acknowledging = True
            
            if need_acknowledging:
                yield client.interaction_application_command_acknowledge(
                    interaction_event,
                    show_for_invoking_user_only = get_show_for_invoking_user_only_from(
                        self._parameters,
                        response_modifier,
                    ),
                )
            
            response_parameters = self._get_response_parameters((
                'allowed_mentions', 'content', 'components', 'embed', 'file', 'show_for_invoking_user_only', 'silent',
                'suppress_embeds', 'tts'
            ))
            if (response_modifier is not None):
                response_modifier.apply_to_creation(response_parameters)
            
            if need_acknowledging or (not interaction_event.is_unanswered()):
                yield client.interaction_followup_message_create(
                    interaction_event,
                    **response_parameters,
                )
            
            else:
                yield client.interaction_response_message_create(
                    interaction_event,
                    **response_parameters,
                )
            
            return
        
        elif (
            (interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT) or
            (
                (interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT) and
                (interaction_event.message is not None)
            )
        ):
            if self._abort:
                # If we are aborting we acknowledge it (if not yet) and create a new message.
                if interaction_event.is_unanswered():
                    yield client.interaction_component_acknowledge(interaction_event)
                
                response_parameters = self._get_response_parameters((
                    'allowed_mentions', 'content', 'components', 'embed', 'file', 'show_for_invoking_user_only',
                    'silent', 'suppress_embeds', 'tts'
                ))
                if (response_modifier is not None):
                    response_modifier.apply_to_creation(response_parameters)
                
                yield client.interaction_followup_message_create(interaction_event, **response_parameters)
                
            elif interaction_event.is_unanswered():
                if ('file' in self._parameters):
                    need_acknowledging = True
                else:
                    need_acknowledging = False
                
                if need_acknowledging:
                    yield client.interaction_component_acknowledge(
                        interaction_event,
                    )
                
                response_parameters = self._get_response_parameters((
                    'allowed_mentions', 'content', 'components', 'embed', 'file'
                ))
                if (response_modifier is not None):
                    response_modifier.apply_to_edition(response_parameters)
                
                if need_acknowledging:
                    yield client.interaction_response_message_edit(interaction_event, **response_parameters)
                
                elif response_parameters:
                    yield client.interaction_component_message_edit(interaction_event, **response_parameters)
                
                else:
                    yield client.interaction_component_acknowledge(
                        interaction_event,
                        get_wait_for_acknowledgement_of(response_modifier),
                    )
            
            elif interaction_event.is_deferred():
                response_parameters = self._get_response_parameters((
                    'allowed_mentions', 'content', 'components', 'embed', 'file'
                ))
                if response_parameters:
                    yield client.interaction_response_message_edit(interaction_event, **response_parameters)
            
            elif interaction_event.is_responded():
                response_parameters = self._get_response_parameters((
                    'allowed_mentions', 'content', 'components', 'embed', 'file', 'show_for_invoking_user_only',
                    'silent', 'suppress_embeds', 'tts'
                ))
                if (response_modifier is not None):
                    response_modifier.apply_to_creation(response_parameters)
                
                yield client.interaction_followup_message_create(interaction_event, **response_parameters)
            
            return
        
        elif (interaction_event_type is INTERACTION_TYPE_AUTOCOMPLETE):
            if interaction_event.is_unanswered():
                yield client.interaction_application_command_autocomplete(interaction_event, None)
            
            response_parameters = self._get_response_parameters((
                'allowed_mentions', 'content', 'components', 'embed', 'file', 'show_for_invoking_user_only', 'silent',
                'suppress_embeds', 'tts'
            ))
            if (response_modifier is not None):
                response_modifier.apply_to_creation(response_parameters)
            
            yield client.interaction_followup_message_create(
                interaction_event,
                **response_parameters,
            )
            
            return
        
        # no more cases
    
    def __repr__(self):
        """Returns the slash response's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        is_abort = self._abort
        if self._abort:
            repr_parts.append(' abort = ')
            repr_parts.append(repr(is_abort))
            
            field_added = True
        else:
            field_added = False
        
        event = self._event
        if (event is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' event = ')
            repr_parts.append(repr(event))
        
        message = self._message
        if (message is not ...):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' message = ')
            repr_parts.append(repr(message))
        
        for key, value in self._parameters.items():
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' ')
            repr_parts.append(key)
            repr_parts.append(' = ')
            repr_parts.append(repr(value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two interaction responses are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._abort != other._abort:
            return False
        
        if self._event is not other._event:
            return False
        
        if self._message is not other._message:
            return False
        
        if self._parameters != other._parameters:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the interaction response's hash value."""
        hash_value = 0
        
        # _abort
        hash_value ^= self._abort
        
        # _event
        event = self._event
        if (event is not None):
            hash_value ^= hash(event)
        
        # _message
        message = self._message
        if (message is not None):
            hash_value ^= hash(message)
        
        # _parameters
        to_dos = [*self._parameters]
        seed = 0
        
        while to_dos:
            seed += 1
            
            to_do = to_dos.pop()
            try:
                to_do_hash_value = hash(to_do)
            except TypeError:
                if isinstance(to_do, dict):
                    for item in to_do.items():
                        to_dos.extend(item)
                    continue
                
                if getattr(type(to_do), '__iter__', None) is not None:
                    to_dos.extend(to_do)
                    continue
                
                to_do_hash_value = object.__hash__(to_do)
            
            hash_value ^= to_do_hash_value & (seed * seed)
            continue
        
        return hash_value


def abort(
    content = ...,
    *,
    allowed_mentions = ...,
    components = ...,
    embed = ...,
    event = None,
    file = ...,
    message = ...,
    show_for_invoking_user_only = True,
    silent = ...,
    suppress_embeds = ...,
    tts = ...,
):
    """
    Aborts the slash response with sending the passed parameters as a response.
    
    The abortion auto detects `show_for_invoking_user_only` if not given. Not follows the command's preference.
    If only a string `content` is given, `show_for_invoking_user_only` will become `True`, else `False`. The reason of
    becoming `False` at that case is, Discord ignores every other field except string content.
    
    Parameters
    ----------
    content : `None`, `str`, ``Embed``, `object`, Optional
        The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
        if any other non `str`, ``Embed`` is given, then will be casted to string.
        
        If given as ``Embed``, then is sent as the message's embed.
    
    allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
            , Optional (Keyword only)
        Which user or role can the message ping (or everyone). Check ``Client._parse_allowed_mentions`` for details.
    
    components : `None`, ``Component``, (`set`, `list`) of ``Component``, Optional (Keyword only)
        Components attached to the message.
    
    embed : `None` ``Embed``, `list` of ``Embed``, Optional (Keyword only)
        The embedded content of the message.
        
        If `embed` and `content` parameters are both given as  ``Embed``, then `TypeError` is raised.
    
    event : `None`, ``InteractionEvent`` = `None`, Optional (Keyword only)
        A specific event ot answer instead of the command's.
    
    file : `None` `object`, Optional (Keyword only)
        A file to send. Check ``Client._create_file_form`` for details.
    
    message : `None`, ``Message``, Optional (Keyword only)
        Whether the interaction's message should be edited.
    
    show_for_invoking_user_only : `bool` = `True`, Optional (Keyword only)
        Whether the sent message should only be shown to the invoking user.
        
        If given as `True`, only the message's content and embeds and components will be processed by Discord.
        
        Defaults to `True`.
    
    silent : `bool`, Optional (Keyword only)
        Whether the message should be delivered silently.
    
    suppress_embeds : `bool`, Optional (Keyword only)
        Whether the message's embeds should be suppressed initially.
    
    tts : `bool`, Optional (Keyword only)
        Whether the message is text-to-speech.
    
    Raises
    ------
    InteractionAbortedError
        The exception which aborts the interaction, then yields the response.
    """
    raise InteractionAbortedError(
        InteractionResponse(
            content,
            allowed_mentions = allowed_mentions,
            components = components,
            embed = embed,
            event = event,
            file = file,
            message = message,
            show_for_invoking_user_only = show_for_invoking_user_only,
            silent = silent,
            suppress_embeds = suppress_embeds,
            tts = tts,
        ).set_abort(),
    )


class InteractionAbortedError(BaseException):
    """
    An ``InteractionAbortedError`` is raised when a slash command is aborted. This class holds the response to send to
    the client.
    
    Attributes
    ----------
    response : ``InteractionResponse``
        The response to send.
    """
    __slots__ = ('response',)
    
    # This is to support keyword parameters
    __init__ = object.__init__
    
    def __new__(cls, response):
        """
        Creates a new ``InteractionAbortedError`` with the given response.
        
        Parameters
        ----------
        response : ``InteractionResponse``
            The response to send.
        """
        self = BaseException.__new__(cls, response)
        self.response = response
        return self
    
    
    def __repr__(self):
        """Returns the exception's representation."""
        return f'{self.__class__.__name__}({self.response!r})'
    
    
    def __eq__(self, other):
        """Returns whether the two abortions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.response != other.response:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the abortion exception hash value"""
        return hash(self.response)
