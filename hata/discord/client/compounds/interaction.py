__all__ = ()

import warnings

from scarletio import Compound


from ...allowed_mentions import parse_allowed_mentions
from ...application import Application
from ...bases import maybe_snowflake
from ...component import InteractionForm
from ...http import DiscordHTTPClient
from ...interaction import InteractionEvent, InteractionResponseContext, InteractionResponseType, InteractionType

from ...message import Message, MessageFlag
from ...message.utils import try_resolve_interaction_message

from ..functionality_helpers import application_command_autocomplete_choice_parser
from ..request_helpers import add_file_to_message_data, get_components_data, validate_content_and_embed


MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY = MessageFlag().update_by_keys(invoking_user_only=True)
MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS = MessageFlag().update_by_keys(embeds_suppressed=True)


def _assert__interaction_event_type(interaction_event):
    """
    Asserts whether the interaction event's type is correct.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Respective interaction event.
    
    Raises
    ------
    AssertionError
        - If `interaction_event` is not ``InteractionEvent``.
    """
    if not isinstance(interaction_event, InteractionEvent):
        raise AssertionError(
            f'`interaction` can be `{InteractionEvent.__name__}`, got '
            f'{interaction_event.__class__.__name__}; {interaction_event!r}.'
        )
    
    return True


def _assert__application_id(application_id):
    """
    Asserts whether the client's application is synced by checking the `application_id`'s value.
    
    Parameters
    ----------
    application_id : `int`
        Client's application's id.
    
    Raises
    ------
    AssertionError
        - If the client's application is not yet synced..
    """
    if application_id == 0:
        raise AssertionError(
            'The client\'s application is not yet synced.'
        )
    
    return True


def _assert__form(form):
    """
    Asserts whether the form's type is correct.
    
    Parameters
    ----------
    form : ``InteractionForm``
        Respective form.
    
    Raises
    ------
    AssertionError
        - If `form` is not ``InteractionForm``.
    """
    if not isinstance(form, InteractionForm):
        raise AssertionError(
            f'`form` can be `{InteractionForm.__name__}`, got '
            f'{form.__class__.__name__}; {form!r}.'
        )
    
    return True


def _assert__show_for_invoking_user_only(show_for_invoking_user_only):
    """
    Asserts whether the given `show_for_invoking_user_only`'s type is correct.
    
    Parameters
    ----------
    show_for_invoking_user_only : ``bool``
        Whether the sent message should only be shown to the invoking user.
    
    Raises
    ------
    AssertionError
        - If `show_for_invoking_user_only` is not ``bool``.
    """
    if not isinstance(show_for_invoking_user_only, bool):
        raise AssertionError(
            f'`show_for_invoking_user_only` can be `bool`, got '
            f'{show_for_invoking_user_only.__class__.__name__}; {show_for_invoking_user_only!r}.'
        )
    
    return True


def _assert__suppress_embeds(suppress_embeds):
    """
    Asserts whether the given `suppress_embeds`'s type is correct.
    
    Parameters
    ----------
    suppress_embeds : ``bool``
        Whether the message's embeds should be suppressed initially.
    
    Raises
    ------
    AssertionError
        - If `suppress_embeds` is not ``bool``.
    """
    if not isinstance(suppress_embeds, bool):
        raise AssertionError(
            f'`suppress_embeds` can be `bool`, got '
            f'{suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
        )
    
    return True


def _assert__tts(tts):
    """
    Asserts whether the given `tts`'s type is correct.
    
    Parameters
    ----------
    tts : ``bool``
        Whether the message is text-to-speech.
    
    Raises
    ------
    AssertionError
        - If `tts` is not ``bool``.
    """
    if not isinstance(tts, bool):
        raise AssertionError(
            f'`tts` can be `bool`, got '
            f'{tts.__class__.__name__}; {tts!r}.'
        )
    
    return True


class ClientCompoundInteractionEndpoints(Compound):
    
    application : Application
    http : DiscordHTTPClient
    
    
    async def interaction_application_command_acknowledge(
        self, interaction_event, wait = True, *, show_for_invoking_user_only = False
    ):
        """
        Acknowledges the given application command interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to acknowledge
        wait : `bool` = `True`, Optional
            Whether the interaction should be ensured asynchronously.
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to `False`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        # Do not ack twice
        if not interaction_event.is_unanswered():
            return
        
        data = {'type': InteractionResponseType.source.value}
        
        if show_for_invoking_user_only:
            data['data'] = {'flags': MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY}
        
        context = InteractionResponseContext(interaction_event, True, show_for_invoking_user_only)
        coroutine = self.http.interaction_response_message_create(interaction_event.id, interaction_event.token, data)
        
        if wait:
            async with context:
                await coroutine
        else:
            await context.ensure(coroutine)
    
    
    async def interaction_application_command_autocomplete(self, interaction_event, choices):
        """
        Forwards auto completion choices for the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to acknowledge
        choices : `None`, `iterable` of `str`
            Choices to show for the user.
        
        Raises
        ------
        TypeError
            If `choice` is neither `None` nor `iterable`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        # Do not auto complete twice
        if not interaction_event.is_unanswered():
            return
        
        choices = application_command_autocomplete_choice_parser(choices)
        
        data = {
            'type': InteractionResponseType.application_command_autocomplete_result.value,
            'data': {
                'choices': choices,
            },
        }
        
        async with InteractionResponseContext(interaction_event, True, False):
            await self.http.interaction_response_message_create(interaction_event.id, interaction_event.token, data)
    
    
    async def interaction_form_send(self, interaction_event, form):
        """
        Responds on an interaction with a form.
        
        This function is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to respond to.
        form : ``InteractionForm``
            The to respond with.
        
        Raises
        ------
        RuntimeError
            If cannot respond with a form on the given `interaction`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Discord do not returns message data, so the method cannot return a ``Message`` either.
        
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        if not interaction_event.is_unanswered():
            warnings.warn(
                (
                    f'`{self.__class__.__name__}.interaction_response_form` called on an interaction already '
                    f'acknowledged / answered: {interaction_event!r}. Returning `None`.'
                ),
                ResourceWarning,
                stacklevel = 2,
            )
            
            return None
        
        assert _assert__form(form)
        
        if (
            (interaction_event.type is not InteractionType.application_command) and
            (interaction_event.type is not InteractionType.message_component)
        ):
            raise RuntimeError(
                f'Only `application_command` and `message_component` interactions can be answered with '
                f'form, got `{interaction_event.type.name}`; {interaction_event!r}; form={form!r}.'
            )
        
        # Build payload
        data = {
            'data': form.to_data(),
            'type': InteractionResponseType.form.value,
        }
        
        async with InteractionResponseContext(interaction_event, False, True):
            await self.http.interaction_response_message_create(interaction_event.id, interaction_event.token, data)
        
        return None
    
    
    async def interaction_response_message_create(
        self,
        interaction_event,
        content = None,
        *,
        allowed_mentions = ...,
        components = None,
        embed = None,
        show_for_invoking_user_only = False,
        suppress_embeds = False,
        tts = False,
    ):
        """
        Sends an interaction response. After receiving an ``InteractionEvent``, you should acknowledge it within
        `3` seconds to perform followup actions.
        
        Not like ``.message_create``, this endpoint can be called without any content to still acknowledge the
        interaction event. This method also wont return a ``Message`` object (thank to Discord), but at least
        ``.interaction_followup_message_create`` will. To edit or delete this message, you can use
        ``.interaction_response_message_edit`` and ``interaction_response_message_delete``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to respond to.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `None`, Optional
            The interaction response's content if given. If given as `str` or empty string, then no content will be
            sent, meanwhile if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``Component``, (`tuple`, `list`) of (``Component``, (`tuple`, `list`) of \
                ``Component``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the interaction response.
            
            If `embed` and `content` parameters are both given as ``EmbedBase``, then `AssertionError` is
            raised.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to `False`.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If `components` type is incorrect.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Discord do not returns message data, so the method cannot return a ``Message`` either.
        
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        content, embed = validate_content_and_embed(content, embed, False)
        components = get_components_data(components, False)
        
        assert _assert__show_for_invoking_user_only(show_for_invoking_user_only)
        assert _assert__suppress_embeds(suppress_embeds)
        assert _assert__tts(tts)
        
        # Build payload
        
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not None):
            message_data['components'] = components
            contains_content = True
        
        if tts:
            message_data['tts'] = True
        
        if message_data:
            is_deferring = False
        else:
            is_deferring = True
        
        flags = 0
        
        if show_for_invoking_user_only:
            flags |= MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY
        
        if suppress_embeds:
            flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        if flags:
            message_data['flags'] = flags
            contains_content = True
        
        data = {}
        if contains_content:
            data['data'] = message_data
        
        if is_deferring:
            response_type = InteractionResponseType.source
        else:
            response_type = InteractionResponseType.message_and_source
        
        data['type'] = response_type.value
        
        async with InteractionResponseContext(interaction_event, is_deferring, show_for_invoking_user_only):
            await self.http.interaction_response_message_create(interaction_event.id, interaction_event.token, data)
        
        # No message data is returned by Discord, return `None`.
        return None
    
    
    async def interaction_component_acknowledge(self, interaction_event, wait = True):
        """
        Acknowledges the given component interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to acknowledge
        wait : `bool` = `True`, Optional
            Whether the interaction should be ensured asynchronously.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        # Do not ack twice
        if not interaction_event.is_unanswered():
            return
        
        data = {'type': InteractionResponseType.component.value}
        
        context = InteractionResponseContext(interaction_event, True, False)
        coroutine = self.http.interaction_response_message_create(interaction_event.id, interaction_event.token, data)
        
        
        if wait:
            async with context:
                await coroutine
        else:
            await context.ensure(coroutine)
    
    
    async def interaction_response_message_edit(
        self,
        interaction_event,
        content = ...,
        *,
        embed = ...,
        file = ...,
        allowed_mentions = ...,
        components = ...,
    ):
        """
        Edits the given `interaction`'s source response. If the source interaction event was only deferred, this call
        will send the message as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction, what's source response message will be edited.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``Component``, (`tuple`, `list`) of (``Component``, (`tuple`, `list`) of \
                ``Component``), Optional (Keyword only)
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Cannot editing interaction messages, which were created with `show_for_invoking_user_only=True`:
        
        ```
        DiscordException Not Found (404), code=10008: Unknown Message
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        # Discord docs say, content can be nullable, but nullable content is just ignored.
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        
        async with InteractionResponseContext(interaction_event, False, False):
            await self.http.interaction_response_message_edit(
                application_id, interaction_event.id, interaction_event.token, message_data
            )
    
    
    async def interaction_component_message_edit(
        self,
        interaction_event,
        content = ...,
        *,
        embed = ...,
        allowed_mentions = ...,
        components = ...,
    ):
        """
        Edits the given component interaction's source message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction, what's source response message will be edited.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        data = {
            'data': message_data,
            'type': InteractionResponseType.component_message_edit.value,
        }
        
        
        async with InteractionResponseContext(interaction_event, False, False):
            await self.http.interaction_response_message_create(interaction_event.id, interaction_event.token, data)
    
    
    async def interaction_response_message_delete(self, interaction_event):
        """
        Deletes the given `interaction`'s source response message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction, what's source response message will be deleted.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        await self.http.interaction_response_message_delete(application_id, interaction_event.id, interaction_event.token)
    
    
    async def interaction_response_message_get(self, interaction_event):
        """
        Gets the given `interaction`'s source response message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction, what's source response message will be deleted.
        
        Returns
        -------
        message : ``Message``
            The created message.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        
        message_data = await self.http.interaction_response_message_get(
            application_id, interaction_event.id, interaction_event.token
        )
        
        return Message.from_data(message_data)
    
    
    async def interaction_followup_message_create(
        self,
        interaction_event,
        content = None,
        *,
        allowed_mentions = ...,
        components = None,
        embed = None,
        file = None,
        show_for_invoking_user_only = False,
        suppress_embeds = False,
        tts = False,
    ):
        """
        Sends a followup message with the given interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to create followup message with.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `True`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        

        components : `None`, ``Component``, (`tuple`, `list`) of (``Component``, (`tuple`, `list`) of \
                ``Component``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any` = `None`, Optional
            A file to send. Check ``create_file_form`` for details.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to `False`.
            
            Invoking user only messages can have attachments too. These attachments are purged by Discord after a set
            amount of time (2 weeks), so do not rely on reusing their url.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech. Defaults to `False`.
        
        
        Returns
        -------
        message : `None`, ``Message``
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        content, embed = validate_content_and_embed(content, embed, False)
        components = get_components_data(components, False)
        
        assert _assert__show_for_invoking_user_only(show_for_invoking_user_only)
        assert _assert__suppress_embeds(suppress_embeds)
        assert _assert__tts(tts)
        
        # Build payload
        
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not None):
            message_data['components'] = components
            contains_content = True
        
        if tts:
            message_data['tts'] = True
        
        flags = 0
        
        if show_for_invoking_user_only:
            flags |= MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY
        
        if suppress_embeds:
            flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        if flags:
            message_data['flags'] = flags
        
        message_data = add_file_to_message_data(message_data, file, contains_content, False)
        if message_data is None:
            return
        
        async with InteractionResponseContext(interaction_event, False, show_for_invoking_user_only):
            message_data = await self.http.interaction_followup_message_create(application_id, interaction_event.id,
                interaction_event.token, message_data)
        
        message = interaction_event.channel._create_new_message(message_data)
        try_resolve_interaction_message(message, interaction_event)
        return message
    
    
    async def interaction_followup_message_edit(
        self,
        interaction_event,
        message,
        content = ...,
        *,
        embed = ...,
        file = ...,
        allowed_mentions = ...,
        components = ...,
    ):
        """
        Edits the given interaction followup message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        
        message : ``Message``, `int`
            The interaction followup's message to edit.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as `str` then the message's content will be edited with it. If given as any non ``EmbedBase``
            instance, then it will be cased to string first.
            
            By passing it as empty string, you can remove the message's content.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        components : `None`, ``Component``, (`tuple`, `list`) of (``Component``, (`tuple`, `list`) of \
                ``Component``), Optional (Keyword only)
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If `message` was not given neither as ``Message``, `int`.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Cannot editing interaction messages, which were created with `show_for_invoking_user_only=True`:
        
        ```
        DiscordException Not Found (404), code=10008: Unknown Message
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        # Detect message id
        # 1.: Message
        # 2.: int (str)
        # 5.: raise
        
        if isinstance(message, Message):
            message_id = message.id
        else:
            message_id = maybe_snowflake(message)
            if (message_id is None):
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `int`, got '
                    f'{message.__class__.__name__}, {message!r}.'
                )
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        # Discord docs say, content can be nullable, but nullable content is just ignored.
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        
        async with InteractionResponseContext(interaction_event, False, False):
            # We receive the new message data, but we do not update the message, so dispatch events can get the
            # difference.
            await self.http.interaction_followup_message_edit(
                application_id, interaction_event.id, interaction_event.token, message_id, message_data
            )
    
    
    async def interaction_followup_message_delete(self, interaction_event, message):
        """
        Deletes an interaction's followup message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        message : ``Message``, `int`
            The interaction followup's message to edit.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        # Detect message id
        # 1.: Message
        # 2.: int (str)
        # 5.: raise
        
        if isinstance(message, Message):
            message_id = message.id
        else:
            message_id = maybe_snowflake(message)
            if (message_id is None):
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `int`, got {message.__class__.__name__}; {message!r}.'
                )
        
        await self.http.interaction_followup_message_delete(
            application_id, interaction_event.id, interaction_event.token, message_id
        )
    
    
    async def interaction_followup_message_get(self, interaction_event, message_id):
        """
        Gets a previously sent message with an interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        message_id : `int`
            The webhook's message's identifier to get.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            - If `message_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        
        message_id_value = maybe_snowflake(message_id)
        if message_id_value is None:
            raise TypeError(
                f'`message_id` can be `int`, got {message_id.__class__.__name__}; {message_id!r}.'
            )
        
        message_data = await self.http.interaction_followup_message_get(
            application_id, interaction_event.id, interaction_event.token, message_id
        )
        
        return Message.from_data(message_data)
