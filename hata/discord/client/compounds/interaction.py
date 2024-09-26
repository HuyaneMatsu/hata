__all__ = ()

from warnings import warn

from scarletio import Compound
from scarletio.web_common import FormData

from ...application import Application
from ...bases import maybe_snowflake
from ...builder.serialization import create_serializer
from ...builder.serialization_configuration import SerializationConfiguration
from ...component import ButtonStyle, InteractionForm
from ...http import DiscordApiClient
from ...interaction import InteractionEvent, InteractionResponseContext, InteractionResponseType, InteractionType
from ...message import Message, MessageFlag
from ...message.message.utils import try_resolve_interaction_message
from ...message.message_builder import (
    MessageBuilderInteractionComponentEdit, MessageBuilderInteractionFollowupCreate,
    MessageBuilderInteractionFollowupEdit, MessageBuilderInteractionResponseCreate,
    MessageBuilderInteractionResponseEdit
)

from ..functionality_helpers import application_command_autocomplete_choice_parser
from ..request_helpers import get_message_id

MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY = MessageFlag().update_by_keys(invoking_user_only = True)


MESSAGE_SERIALIZER_INTERACTION_FOLLOWUP_CREATE = create_serializer(
    MessageBuilderInteractionFollowupCreate,
    SerializationConfiguration(
        [
            MessageBuilderInteractionFollowupCreate.allowed_mentions,
            MessageBuilderInteractionFollowupCreate.attachments,
            MessageBuilderInteractionFollowupCreate.components,
            MessageBuilderInteractionFollowupCreate.content,
            MessageBuilderInteractionFollowupCreate.embeds,
            MessageBuilderInteractionFollowupCreate.flags,
            MessageBuilderInteractionFollowupCreate.poll,
            MessageBuilderInteractionFollowupCreate.show_for_invoking_user_only,
            MessageBuilderInteractionFollowupCreate.tts,
        ],
        False,
    )
)

MESSAGE_SERIALIZER_INTERACTION_FOLLOWUP_EDIT = create_serializer(
    MessageBuilderInteractionFollowupEdit,
    SerializationConfiguration(
        [
            MessageBuilderInteractionFollowupEdit.allowed_mentions,
            MessageBuilderInteractionFollowupEdit.attachments,
            MessageBuilderInteractionFollowupEdit.components,
            MessageBuilderInteractionFollowupEdit.content,
            MessageBuilderInteractionFollowupEdit.embeds,
            MessageBuilderInteractionFollowupEdit.flags,
        ],
        True,
    )
)


MESSAGE_SERIALIZER_INTERACTION_COMPONENT_EDIT = create_serializer(
    MessageBuilderInteractionComponentEdit,
    SerializationConfiguration(
        [
            MessageBuilderInteractionComponentEdit.allowed_mentions,
            MessageBuilderInteractionComponentEdit.components,
            MessageBuilderInteractionComponentEdit.content,
            MessageBuilderInteractionComponentEdit.embeds,
            MessageBuilderInteractionComponentEdit.flags,
        ],
        True,
    )
)

MESSAGE_SERIALIZER_INTERACTION_RESPONSE_CREATE = create_serializer(
    MessageBuilderInteractionResponseCreate,
    SerializationConfiguration(
        [
            MessageBuilderInteractionResponseCreate.allowed_mentions,
            MessageBuilderInteractionResponseCreate.components,
            MessageBuilderInteractionResponseCreate.content,
            MessageBuilderInteractionResponseCreate.embeds,
            MessageBuilderInteractionResponseCreate.flags,
            MessageBuilderInteractionResponseCreate.poll,
            MessageBuilderInteractionResponseCreate.tts,
        ],
        True,
    )
)


MESSAGE_SERIALIZER_INTERACTION_RESPONSE_EDIT = create_serializer(
    MessageBuilderInteractionResponseEdit,
    SerializationConfiguration(
        [
            MessageBuilderInteractionResponseEdit.allowed_mentions,
            MessageBuilderInteractionResponseEdit.attachments,
            MessageBuilderInteractionResponseEdit.components,
            MessageBuilderInteractionResponseEdit.content,
            MessageBuilderInteractionResponseEdit.embeds,
            MessageBuilderInteractionResponseEdit.flags,
            MessageBuilderInteractionResponseEdit.poll,
        ],
        True,
    )
)


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
            f'{type(form).__name__}; {form!r}.'
        )
    
    return True


def _process_interaction_response(interaction_event, interaction_response_data):
    """
    Processes interaction event trying to create a message from it.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        Interaction to acknowledge.
    
    interaction_response_data : `None | dict<str, object>`
        Interaction response data.
    
    Returns
    -------
    message : `None | Message`
        Returns `None` on failure.
    """
    if (interaction_response_data is None):
        return None
    
    nested_data = interaction_response_data.get('resource', None)
    if (nested_data is None):
        return None
    
    message_data = nested_data.get('message', None)
    if (message_data is None):
        return None
    
    message = interaction_event.channel._create_new_message(message_data)
    try_resolve_interaction_message(message, interaction_event)
    return message


class ClientCompoundInteractionEndpoints(Compound):
    
    application : Application
    api : DiscordApiClient
    
    
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
        
        Returns
        -------
        response_message : `None | Message`
            Returns a message oon success.
            If `wait` was given as `False` then `None`.
        
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
        DiscordException Not Found (404), code = 10062: Unknown interaction
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
        coroutine = self.api.interaction_response_message_create(
            interaction_event.id, interaction_event.token, data, {'with_response': True}
        )
        
        if not wait:        
            await context.ensure(coroutine, _process_interaction_response)
            return
        
        async with context:
            interaction_response_data = await coroutine
        
        # Example response
        # {
        #     'interaction': {
        #         'id': '...',
        #         'type': 2,
        #         'response_message_id': '...',
        #         'response_message_loading': True,
        #         'response_message_ephemeral': False,
        #         'channel_id': '...',
        #         'guild_id': '...'
        #     },
        #     'resource': {
        #         'type': 4,
        #         'message': {...},
        #      }
        #  }
        
        return _process_interaction_response(interaction_event, interaction_response_data)
    
    
    async def interaction_application_command_autocomplete(self, interaction_event, choices):
        """
        Forwards auto completion choices for the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to acknowledge.
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
        DiscordException Not Found (404), code = 10062: Unknown interaction
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
            await self.api.interaction_response_message_create(
                interaction_event.id, interaction_event.token, data, None
            )
        
        # Example output:
        # {
        #     'interaction': {
        #         'id': '...',
        #         'type': 4,
        #         'channel_id': '...',
        #         'guild_id': '...',
        #     }
        # }
        # No need to handle
    
    
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
        DiscordException Not Found (404), code = 10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        if not interaction_event.is_unanswered():
            warn(
                (
                    f'`{type(self).__name__}.interaction_response_form` called on an interaction already '
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
                f'form, got `{interaction_event.type.name}`; {interaction_event!r}; form = {form!r}.'
            )
        
        # Build payload
        data = {
            'data': form.to_data(),
            'type': InteractionResponseType.form.value,
        }
        
        async with InteractionResponseContext(interaction_event, False, True):
            await self.api.interaction_response_message_create(
                interaction_event.id, interaction_event.token, data, None
            )
            
        # Example response:
        # {
        #     'interaction': {
        #         'id': '...',
        #         'type': 2,
        #         'channel_id': '...',
        #         'guild_id': '...',
        #     }
        # }
        # No need to handle.
        
        return None
    
    
    async def interaction_response_message_create(
        self, interaction_event, *positional_parameters, **keyword_parameters,
    ):
        """
        Sends an interaction response. After receiving an ``InteractionEvent``, you should acknowledge it within
        `3` seconds to perform followup actions.
        
        Not like ``.message_create``, this endpoint can be called without any content to still acknowledge the
        interaction event. This method also wont return a ``Message`` object (thank to Discord), but at least
        ``.interaction_followup_message_create`` will. To edit or delete this message, you can use
        ``.interaction_response_message_edit`` and ``.interaction_response_message_delete``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to respond to.
        
        *positional_parameters : Positional parameters
            Additional parameters to create the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to create the message with.

        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
        
        content : `None`, `str`, Optional
            The message's content if given.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's flags.
        
        poll : `None`, ``Poll``, Optional
            The message's poll.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user.
        
        silent : `bool` = `False`, Optional (Keyword only)
            Whether the message should be delivered silently.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Returns
        -------
        response_message : `None | Message`
            Returns a message on success.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code = 10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        message_data = MESSAGE_SERIALIZER_INTERACTION_RESPONSE_CREATE(positional_parameters, keyword_parameters)
        
        data = {}
        if message_data:
            data['data'] = message_data
        
        flags = message_data.get('flags', -1)
        
        # is_deferring
        if len(message_data) - (flags != -1):
            is_deferring = False
        else:
            is_deferring = True
        
        # show_for_invoking_user_only
        if flags != -1 and flags & MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY:
            show_for_invoking_user_only = True
        else:
            show_for_invoking_user_only = False
        
        if is_deferring:
            response_type = InteractionResponseType.source
        else:
            response_type = InteractionResponseType.message_and_source
        
        data['type'] = response_type.value
        
        async with InteractionResponseContext(interaction_event, is_deferring, show_for_invoking_user_only):
            interaction_response_data = await self.api.interaction_response_message_create(
                interaction_event.id, interaction_event.token, data, {'with_response': True}
            )
            
        # Example output:
        # {
        #     'interaction': {
        #         'id': '1287034694394712105',
        #         'type': 2,
        #         'response_message_id': '...',
        #         'response_message_loading': False,
        #         'response_message_ephemeral': False,
        #         'channel_id': '...',
        #         'guild_id': '...'
        #     },
        #     'resource': {
        #         'type': 4,
        #         'message': {...},
        #     },
        # }
        
        output = _process_interaction_response(interaction_event, interaction_response_data)
        return output
    
    
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
        DiscordException Not Found (404), code = 10062: Unknown interaction
        ```
        """
        assert _assert__interaction_event_type(interaction_event)
        
        # Do not ack twice
        if not interaction_event.is_unanswered():
            return
        
        data = {'type': InteractionResponseType.component.value}
        
        context = InteractionResponseContext(interaction_event, True, False)
        coroutine = self.api.interaction_response_message_create(
            interaction_event.id, interaction_event.token, data, None
        )
        
        
        if wait:
            async with context:
                await coroutine
        else:
            await context.ensure(coroutine)
        
        # Example output:
        # {
        #     'interaction': {
        #         'id': '...',
        #         'type': 3,
        #         'response_message_id': '...',
        #         'response_message_loading': False,
        #         'response_message_ephemeral': False,
        #         'channel_id': '...',
        #         'guild_id': '...',
        #     }
        # }
        # No need to handle.
    
    
    async def interaction_response_message_edit(
        self, interaction_event, *positional_parameters, **keyword_parameters,
    ):
        """
        Edits the given `interaction`'s source response. If the source interaction event was only deferred, this call
        will send the message as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction, what's source response message will be edited.
        
        *positional_parameters : Positional parameters
            Additional parameters to edit the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to edit the message with.
        
        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        attachments : `None`, `object`, Optional (Keyword only)
            Attachments to send.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        content : `None`, `str`, Optional
            The new content of the message.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
            
            By passing it as `None`, you can remove the old.
        
        file : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's new flags.
        
        poll : `None`, ``Poll``, Optional
            The message's poll.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        message_data = MESSAGE_SERIALIZER_INTERACTION_RESPONSE_EDIT(positional_parameters, keyword_parameters)
        if not message_data:
            return
        
        async with InteractionResponseContext(interaction_event, False, False):
            await self.api.interaction_response_message_edit(
                application_id, interaction_event.id, interaction_event.token, message_data
            )
    
    
    async def interaction_component_message_edit(
        self, interaction_event, *positional_parameters, **keyword_parameters
    ):
        """
        Edits the given component interaction's source message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction, what's source response message will be edited.
        
        *positional_parameters : Positional parameters
            Additional parameters to edit the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to edit the message with.
        
        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        content : `None`, `str`, Optional
            The new content of the message.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
            
            By passing it as `None`, you can remove the old.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's new flags.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        message_data = MESSAGE_SERIALIZER_INTERACTION_COMPONENT_EDIT(positional_parameters, keyword_parameters)
        
        if message_data:
            data = {
                'data': message_data,
                'type': InteractionResponseType.component_message_edit.value,
            }
            deferring = False
        
        else:
            data = {
                'type': InteractionResponseType.component.value,
            }
            deferring = True
        
        
        async with InteractionResponseContext(interaction_event, deferring, False):
            await self.api.interaction_response_message_create(
                interaction_event.id, interaction_event.token, data, None
            )
        
        # Example output:
        # {
        #     'interaction': {
        #         'id': '1287060293226336436',
        #         'type': 3,
        #         'response_message_id': '1287059561995309096',
        #         'response_message_loading': False,
        #         'response_message_ephemeral': False,
        #         'channel_id': '1226776881496461312',
        #         'guild_id': '388267636661682178'
        #     },
        #     'resource': {
        #         'type': 7,
        #         'message': {...},
        #     }
        # }
    
    
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
        
        await self.api.interaction_response_message_delete(application_id, interaction_event.id, interaction_event.token)
    
    
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
        
        
        message_data = await self.api.interaction_response_message_get(
            application_id, interaction_event.id, interaction_event.token
        )
        
        return Message.from_data(message_data)
    
    
    async def interaction_followup_message_create(
        self, interaction_event, *positional_parameters, **keyword_parameters
    ):
        """
        Sends a followup message with the given interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to create followup message with.
        
        *positional_parameters : Positional parameters
            Additional parameters to create the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to create the message with.
        
        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        attachments : `None`, `object`, Optional (Keyword only)
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
        
        file : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's flags.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user.
        
        silent : `bool` = `False`, Optional (Keyword only)
            Whether the message should be delivered silently.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        
        Returns
        -------
        message : `None`, ``Message``
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        assert _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        message_data = MESSAGE_SERIALIZER_INTERACTION_FOLLOWUP_CREATE(positional_parameters, keyword_parameters)
        if not message_data:
            return
        
        # show_for_invoking_user_only
        if isinstance(message_data, FormData):
            flags = message_data.fields[0].value.get('flags', 0)
        else:
            flags = message_data.get('flags', 0)
        if flags & MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY:
            show_for_invoking_user_only = True
        else:
            show_for_invoking_user_only = False
        
        
        async with InteractionResponseContext(interaction_event, False, show_for_invoking_user_only):
            message_data = await self.api.interaction_followup_message_create(
                application_id, interaction_event.id, interaction_event.token, message_data
            )
        
        message = interaction_event.channel._create_new_message(message_data)
        try_resolve_interaction_message(message, interaction_event)
        return message
    
    
    async def interaction_followup_message_edit(
        self, interaction_event, message, *positional_parameters, **keyword_parameters,
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
        
        *positional_parameters : Positional parameters
            Additional parameters to edit the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to edit the message with.
        
        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        attachments : `None`, `object`, Optional (Keyword only)
            Attachments to send.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        content : `None`, `str`, Optional
            The new content of the message.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
            
            By passing it as `None`, you can remove the old.
        
        file : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's new flags.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
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
                    f'`message` can be `{Message.__name__}`, `int`, got '
                    f'{message.__class__.__name__}, {message!r}.'
                )
        
        message_data = MESSAGE_SERIALIZER_INTERACTION_FOLLOWUP_EDIT(positional_parameters, keyword_parameters)
        if not message_data:
            return
        
        async with InteractionResponseContext(interaction_event, False, False):
            # We receive the new message data, but we do not update the message, so dispatch events can get the
            # difference.
            await self.api.interaction_followup_message_edit(
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
        
        await self.api.interaction_followup_message_delete(
            application_id, interaction_event.id, interaction_event.token, message_id
        )
    
    
    async def interaction_followup_message_get(self, interaction_event, message):
        """
        Gets a previously sent message with an interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        message : ``Message``, `int`
            The message or it's identifier to get.
        
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
        
        message_id = get_message_id(message)
        
        message_data = await self.api.interaction_followup_message_get(
            application_id, interaction_event.id, interaction_event.token, message_id
        )
        
        return Message.from_data(message_data)
    
    
    async def interaction_require_subscription(self, interaction_event):
        """
        Requires the user to subscribe to the application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Interaction to respond to.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if not interaction_event.is_unanswered():
            warn(
                (
                    f'`{type(self).__name__}.interaction_require_subscription` is deprecated. '
                    f'Please use a component with `{ButtonStyle.__name__}.subscription` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
        
        _assert__interaction_event_type(interaction_event)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        data = {'type': InteractionResponseType.require_subscription.value}
        
        async with InteractionResponseContext(interaction_event, False, True):
            # Uses the same endpoint as message create
            await self.api.interaction_response_message_create(
                interaction_event.id, interaction_event.token, data, None
            )
