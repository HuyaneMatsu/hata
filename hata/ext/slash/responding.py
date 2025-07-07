__all__ = ('abort', 'InteractionAbortedError', 'InteractionResponse',)

from itertools import islice

from scarletio import is_coroutine_generator, skip_ready_cycle

from ...discord.application_command import ApplicationCommandTargetType
from ...discord.client import Client
from ...discord.component import InteractionForm
from ...discord.interaction import InteractionType
from ...discord.message import (
    MessageBuilderBase, MessageBuilderInteractionComponentEdit, MessageBuilderInteractionFollowupCreate,
    MessageBuilderInteractionFollowupEdit, MessageBuilderInteractionResponseCreate,
    MessageBuilderInteractionResponseEdit
)

from .conversions import CONVERSION_ABORT, CONVERSION_INTERACTION_EVENT, CONVERSION_MESSAGE
from .response_modifier import (
    get_show_for_invoking_user_only_from, get_show_for_invoking_user_only_of, get_wait_for_acknowledgement_of
)


INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component
INTERACTION_TYPE_FORM_SUBMIT = InteractionType.form_submit
INTERACTION_TYPE_AUTOCOMPLETE = InteractionType.application_command_autocomplete


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
        Object yielded or returned by the command coroutine.
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
                (
                    (interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND) and
                    (interaction_event.target_type is not ApplicationCommandTargetType.embedded_activity_launch)
                ) or
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
            
            if (
                (interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND) and
                (interaction_event.target_type is ApplicationCommandTargetType.embedded_activity_launch)
            ):
                if not interaction_event.is_unanswered():
                    return
                
                yield client.interaction_embedded_activity_launch(
                    interaction_event,
                    get_wait_for_acknowledgement_of(response_modifier),
                )
                return
        
        # no more cases
        return
    
    # wait for async acknowledgement if applicable
    await interaction_event._wait_for_async_task_completion()
    
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
    
    if not isinstance(response, InteractionResponse):
        if isinstance(response, tuple):
            response = InteractionResponse(*response)
        else:
            response = InteractionResponse(response)
    
    for request_coroutine in response.get_request_coroutines(
        client,
        interaction_event,
        response_modifier,
    ):
        yield request_coroutine
    
    # No more cases
    return


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
                    maybe_response_message = await request_coroutine
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    # `response_message` may have be set before with an iteration, so reset it.
                    response_message = None
                    response_exception = err
                    break
                
                else:
                    # It can happen that the first request creates the response message and the second one edits it.
                    if (maybe_response_message is not None):
                        response_message = maybe_response_message
                        maybe_response_message = None
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


class InteractionResponse(
    MessageBuilderInteractionComponentEdit,
    MessageBuilderInteractionFollowupCreate,
    MessageBuilderInteractionFollowupEdit,
    MessageBuilderInteractionResponseCreate,
    MessageBuilderInteractionResponseEdit,
    MessageBuilderBase,
):
    """
    Message builder for interaction responses.
    
    May pass it's parameters to any of the following method depending on control flow.
    
    - ``Client.interaction_application_command_acknowledge``
    - ``Client.interaction_application_command_autocomplete``
    - ``Client.interaction_component_acknowledge``
    - ``Client.interaction_component_message_edit``
    - ``Client.interaction_embedded_activity_launch``
    - ``Client.interaction_followup_message_create``
    - ``Client.interaction_followup_message_edit``
    - ``Client.interaction_response_message_create``
    - ``Client.interaction_response_message_edit``
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    
    abort = CONVERSION_ABORT
    interaction_event = CONVERSION_INTERACTION_EVENT
    message = CONVERSION_MESSAGE
    
    
    def __new__(cls, *positional_parameters, **keyword_parameters):
        """
        Parameters
        ----------
        *positional_parameters : Positional parameters
            Additional parameters to create the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to create the message with.
        
        Other Parameters
        ----------------
        abort : `None`, `bool`, Optional (Keyword only)
            Whether the interaction response is dropped from ``abort``.
        
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        attachments : `None | object`, Optional (Keyword only)
            Attachments to send.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
        
        content : `None`, `str`, Optional
            The message's content if given.
        
        poll : `None`, ``Poll``, Optional
            The message's poll.
            
            > Response message must be created or else discord will ignore the `poll` field.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
        
        event : ``None | InteractionEvent`` = `None`, Optional
            Alternative for `interaction_event`.
        
        file : `None | object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None | object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's flags.
        
        interaction_event : ``None | InteractionEvent`` = `None`, Optional
            A specific event ot answer instead of the command's.
        
        message : `None`, ``Message``, Optional (Keyword only)
            Whether the interaction's message should be edited.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user.
        
        silent : `bool` = `False`, Optional (Keyword only)
            Whether the message should be delivered silently.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        voice_attachment : ``None | VoiceAttachment``, Optional (Keyword only)
            Modifies the message to be a voice message, allowing it to contain just a single voice attachment.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - if a parameter's value is incorrect.
        """
        positional_parameters_length = len(positional_parameters)
        if not positional_parameters_length:
            self = MessageBuilderBase.__new__(cls)
        
        else:
            self = positional_parameters[0]
            if isinstance(self, cls):
                if positional_parameters_length > 1:
                    self._with_positional_parameters(islice(positional_parameters, 1, positional_parameters_length))
            
            else:
                self = MessageBuilderBase.__new__(cls)
                self._with_positional_parameters(positional_parameters)
        
        if keyword_parameters:
            self._with_keyword_parameters(keyword_parameters)
        
        return self
    
    
    def get_request_coroutines(self, client, interaction_event, response_modifier):
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
        
        Yields
        -------
        request_coroutine : `None`, `CoroutineType`
        """
        event = self.interaction_event
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
            for message in self._try_pull_field_value(CONVERSION_MESSAGE):
                if (response_modifier is not None):
                    response_modifier.apply_to_edition(self)
                
                if message is None:
                    yield client.interaction_response_message_edit(interaction_event, self)
                else:
                    # Note: here we cannot put `poll` on the message.
                    yield client.interaction_followup_message_edit(interaction_event, message, self)
                return
            
            # If an application command interaction with embedded activity launch check whether we want to indeed
            # launch it
            if (
                (interaction_event.target_type is ApplicationCommandTargetType.embedded_activity_launch) and
                interaction_event.is_unanswered() and
                (not self.abort)
            ):
                yield client.interaction_embedded_activity_launch(
                    interaction_event,
                    get_wait_for_acknowledgement_of(response_modifier),
                )
                if (response_modifier is not None):
                    response_modifier.apply_to_creation(self)
                
                yield client.interaction_followup_message_create(interaction_event, self)
                return
            
            if (not interaction_event.is_unanswered()):
                need_acknowledging = False
            elif (self.attachments is not None) or (self.voice_attachment is not None):
                need_acknowledging = True
            elif self.abort:
                need_acknowledging = False
            else:
                need_acknowledging = False
            
            if need_acknowledging:
                yield client.interaction_application_command_acknowledge(
                    interaction_event,
                    show_for_invoking_user_only = get_show_for_invoking_user_only_from(self, response_modifier),
                )
            
            if (response_modifier is not None):
                response_modifier.apply_to_creation(self)
            
            if need_acknowledging or (not interaction_event.is_unanswered()):
                if (interaction_event.message is None) and (not interaction_event.is_responded()):
                    yield client.interaction_response_message_edit(interaction_event, self)
                else:
                    yield client.interaction_followup_message_create(interaction_event, self)
            else:
                yield client.interaction_response_message_create(interaction_event, self)
            
            return
        
        if (
            (interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT) or
            (
                (interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT) and
                (interaction_event.message is not None)
            )
        ):
            if self.abort:
                # If we are aborting we acknowledge it (if not yet) and create a new message.
                if interaction_event.is_unanswered():
                    yield client.interaction_component_acknowledge(interaction_event)
                
                if (response_modifier is not None):
                    response_modifier.apply_to_creation(self)
                
                yield client.interaction_followup_message_create(interaction_event, self)
                
            elif interaction_event.is_unanswered():
                if (self.attachments is not None) or (self.voice_attachment is not None):
                    need_acknowledging = True
                else:
                    need_acknowledging = False
                
                if need_acknowledging:
                    yield client.interaction_component_acknowledge(
                        interaction_event,
                    )
                
                # Note: here we cannot put `poll` on the message.
                if (response_modifier is not None):
                    response_modifier.apply_to_edition(self)
                
                if need_acknowledging:
                    yield client.interaction_component_acknowledge(
                        interaction_event,
                        get_wait_for_acknowledgement_of(response_modifier),
                    )
                
                yield client.interaction_component_message_edit(interaction_event, self)
            
            elif interaction_event.is_deferred():
                yield client.interaction_response_message_edit(interaction_event, self)
            
            elif interaction_event.is_responded():
                if (response_modifier is not None):
                    response_modifier.apply_to_creation(self)
                
                yield client.interaction_followup_message_create(interaction_event, self)
            
            return
        
        if (interaction_event_type is INTERACTION_TYPE_AUTOCOMPLETE):
            if interaction_event.is_unanswered():
                yield client.interaction_application_command_autocomplete(interaction_event, None)
            
            if (response_modifier is not None):
                response_modifier.apply_to_creation(self)
            
            yield client.interaction_followup_message_create(interaction_event, self)
            return
        
        # no more cases


def abort(
    *positional_parameters,
    show_for_invoking_user_only = True,
    **keyword_parameters,
):
    """
    Aborts the slash response with sending the passed parameters as a response.
    
    The abortion auto detects `show_for_invoking_user_only` if not given. Not follows the command's preference.
    If only a string `content` is given, `show_for_invoking_user_only` will become `True`, else `False`. The reason of
    becoming `False` at that case is, Discord ignores every other field except string content.
    
    Parameters
    ----------
    *positional_parameters : Positional parameters
        Additional parameters to create the message with.
    
    show_for_invoking_user_only : `bool` = `True`, Optional (Keyword only)
        Whether the sent message should only be shown to the invoking user.
    
    **keyword_parameters : Keyword parameters
        Additional parameters to create the message with.
    
    Other Parameters
    ----------------
    allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
            (`str`, ``UserBase``, ``Role`` ) , Optional
        Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
        for details.
    
    attachments : `None | object`, Optional (Keyword only)
        Attachments to send.
    
    components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
        Components attached to the message.
    
    content : `None`, `str`, Optional
        The message's content if given.
    
    poll : `None`, ``Poll``, Optional
        The message's poll.
        
        > Response message must be created or else discord will ignore the `poll` field.
    
    embed : `None`, `Embed`, Optional
        Alternative for `embeds`.
    
    embeds : `None`, `list<Embed>`, Optional
        The new embedded content of the message.
    
    event : ``None | InteractionEvent`` = `None`, Optional
        Alternative for `interaction_event`.
    
    file : `None | object`, Optional (Keyword only)
        Alternative for `attachments`.
    
    files : `None | object`, Optional (Keyword only)
        Alternative for `attachments`.
    
    flags : `int`, ``MessageFlag`, Optional
        The message's flags.
    
    interaction_event : ``None | InteractionEvent`` = `None`, Optional
        A specific event ot answer instead of the command's.
    
    message : `None`, ``Message``, Optional (Keyword only)
        Whether the interaction's message should be edited.
    
    silent : `bool` = `False`, Optional (Keyword only)
        Whether the message should be delivered silently.
    
    suppress_embeds : `bool` = `False`, Optional (Keyword only)
        Whether the message's embeds should be suppressed initially.
    
    tts : `bool` = `False`, Optional (Keyword only)
        Whether the message is text-to-speech.
    
    voice_attachment : ``None | VoiceAttachment``, Optional (Keyword only)
        Modifies the message to be a voice message, allowing it to contain just a single voice attachment.
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - if a parameter's value is incorrect.
    InteractionAbortedError
        - The exception which aborts the interaction, then yields the response.
    """
    raise InteractionAbortedError(
        InteractionResponse(
            *positional_parameters,
            **keyword_parameters,
            abort = True,
            show_for_invoking_user_only = show_for_invoking_user_only,
        )
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
