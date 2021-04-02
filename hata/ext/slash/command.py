# -*- coding: utf-8 -*-
__all__ = ('SlashCommand', 'SlashCommandPermissionOverwriteWrapper', 'SlashCommandWrapper', 'SlashResponse', 'Slasher',
    'abort', )
import warnings
from threading import current_thread
from functools import partial as partial_func
import reprlib

from ...backend.futures import Task, is_coroutine_generator, WaitTillAll
from ...backend.analyzer import CallableAnalyzer
from ...backend.event_loop import EventThread
from ...backend.utils import WeakReferer, DOCS_ENABLED

from ...discord.client_core import KOKORO, ROLES, CHANNELS
from ...discord.parsers import route_value, EventHandlerBase, InteractionEvent, check_name, Router, route_name, \
    _EventHandlerManager, INTERACTION_EVENT_RESPONSE_STATE_NONE, INTERACTION_EVENT_RESPONSE_STATE_DEFERRED, \
    INTERACTION_EVENT_RESPONSE_STATE_RESPONDED
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.embed import EmbedBase
from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake, preconvert_bool
from ...discord.client import Client
from ...discord.user import UserBase, User
from ...discord.role import Role
from ...discord.channel import ChannelBase
from ...discord.preinstanced import ApplicationCommandOptionType, InteractionType
from ...discord.interaction import ApplicationCommandOption, ApplicationCommandOptionChoice, ApplicationCommand, \
    ApplicationCommandPermissionOverwrite
from ...discord.limits import APPLICATION_COMMAND_OPTIONS_MAX, APPLICATION_COMMAND_CHOICES_MAX, \
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX, \
    APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX, \
    APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX


INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command

UNLOADING_BEHAVIOUR_DELETE = 0
UNLOADING_BEHAVIOUR_KEEP = 1
UNLOADING_BEHAVIOUR_INHERIT = 2

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


def raw_name_to_display(raw_name):
    """
    Converts the given raw application command name and converts it to it's display name.
    
    Parameters
    ----------
    raw_name : `str`
        The name to convert.
    
    Returns
    -------
    display_name : `str`
        The converted name.
    """
    return '-'.join([w for w in raw_name.strip('_ ').lower().replace(' ', '-').replace('_', '-').split('-') if w])


async def get_request_coros(client, interaction_event, show_for_invoking_user_only, response):
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
    
    Yields
    -------
    request_coro : `None` or `coroutine`
    """
    response_state = interaction_event._response_state
    if (response is None):
        if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
            yield client.interaction_response_message_create(interaction_event,
                show_for_invoking_user_only=show_for_invoking_user_only)
        
        return
    
    if isinstance(response, (str, EmbedBase)) or is_only_embed(response):
        if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
            yield client.interaction_response_message_create(interaction_event, response,
                show_for_invoking_user_only=show_for_invoking_user_only)
            return
        
        if response_state == INTERACTION_EVENT_RESPONSE_STATE_DEFERRED:
            yield client.interaction_response_message_edit(interaction_event, response)
            return
        
        if response_state == INTERACTION_EVENT_RESPONSE_STATE_RESPONDED:
            yield client.interaction_followup_message_create(interaction_event, response,
                show_for_invoking_user_only=show_for_invoking_user_only)
            return
        
        # No more cases
        return
        
    if is_coroutine_generator(response):
        response = await process_command_gen(client, interaction_event, show_for_invoking_user_only, response)
        async for request_coro in get_request_coros(client, interaction_event, show_for_invoking_user_only, response):
            yield request_coro
        
        return
    
    if isinstance(response, SlashResponse):
        for request_coro in response.get_request_coros(client, interaction_event, show_for_invoking_user_only):
            yield request_coro
        
        return
    
    if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
        yield client.interaction_response_message_create(interaction_event,
            show_for_invoking_user_only=show_for_invoking_user_only)
        
        return
    
    # No more cases
    return


async def process_command_gen(client, interaction_event, show_for_invoking_user_only, coro):
    """
    Processes a slash command coroutine generator.
    
    This function os a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    show_for_invoking_user_only : `bool`
        Whether the response message should only be shown for the invoking user.
    coro : `CoroutineGenerator`
        A coroutine generator with will send command response.
    
    Returns
    -------
    response : `Any`
        Returned object by the coroutine generator.
    
    Raises
    ------
    BaseException
        Any exception raised by `coro`.
    """
    response_message = None
    response_exception = None
    while True:
        if response_exception is None:
            step = coro.asend(response_message)
        else:
            step = coro.athrow(response_exception)
        
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
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # Message's channel deleted; Can we get this?
                        ERROR_CODES.invalid_access, # Client removed.
                        ERROR_CODES.invalid_permissions, # Permissions changed meanwhile; Can we get this?
                        ERROR_CODES.cannot_message_user, # User has dm-s disallowed; Can we get this?
                        ERROR_CODES.unknown_interaction, # We times out, do not drop error.
                            ):
                    return
            
            raise
        
        else:
            # We set it first, since if `get_request_coros` yields nothing, we would be meowed up.
            response_message = None
            response_exception = None
            
            async for request_coro in get_request_coros(client, interaction_event, show_for_invoking_user_only,
                    response):
                try:
                    response_message = await request_coro
                except BaseException as err:
                    # `response_message` may have be set before with an iteration, so reset it.
                    response_message = None
                    response_exception = err
                    break
    
    
    return response


async def process_command_coro(client, interaction_event, show_for_invoking_user_only, coro):
    """
    Processes a slash command coroutine.
    
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
    coro : `coroutine`
        A coroutine with will send command response.
    
    Raises
    ------
    BaseException
        Any exception raised by `coro`.
    """
    if is_coroutine_generator(coro):
        response = await process_command_gen(client, interaction_event, show_for_invoking_user_only, coro)
    else:
        try:
            response = await coro
        except InteractionAbortedError as err:
            response = err.response
    
    async for request_coro in get_request_coros(client, interaction_event, show_for_invoking_user_only, response):
        try:
            await request_coro
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted; Can we get this?
                        ERROR_CODES.invalid_access, # client removed.
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile; Can we get this?
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed; Can we get this?
                        ERROR_CODES.unknown_interaction, # we timed out, do not drop error.
                            ):
                    return
            
            raise


class SlashResponse:
    """
    Rich interaction response message usable with `return` or with `yield` statements.
    
    May pass it's parameters to any oft he following method depending on control flow.
    
    - ``Client.interaction_response_message_create``
    - ``Client.interaction_response_message_edit``
    - ``Client.interaction_followup_message_create``
    
    Attributes
    ----------
    -force_new_message : `bool`
        Whether a new message should be forced out from Discord and being retrieved.
    _parameters : `dict` of (`str`, `Any`) items
        Parameters to pass to the respective ``Client`` functions.
        
        Can have the following keys:
        
        - `'allowed_mentions'`
        - `'content'`
        - `'embed'`
        - `'file'`
        - `'show_for_invoking_user_only'`
        - `'tts'`
    """
    __slots__ = ('_force_new_message', '_parameters',)
    
    def __init__(self, content=..., *, embed=..., file=..., allowed_mentions=..., tts=...,
            show_for_invoking_user_only=..., force_new_message=False):
        """
        Creates a new ``SlashResponse`` instance with the given parameters.
        
        Parameters
        ----------
        content : `str`, ``EmbedBase``, `Any`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str` or ``EmbedBase`` instance is given, then will be casted to string.
            
            If given as ``EmbedBase`` instance, then is sent as the message's embed.
            
        embed : ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `TypeError` is raised.
        file : `Any`, Optional
            A file to send. Check ``Client._create_file_form`` for details.
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` ), Optional
            Which user or role can the message ping (or everyone). Check ``Client._parse_allowed_mentions`` for details.
        tts : `bool`, Optional
            Whether the message is text-to-speech.
        show_for_invoking_user_only : `bool`, Optional
            Whether the sent message should only be shown to the invoking user. Defaults to the value passed when adding
            the command.
            
            If given as `True` only the message's content will be processed by Discord.
        force_new_message : `int` or `bool`, Optional
            Whether a new message should be forced out from Discord allowing the client to retrieve a new ``Message``
            object as well. Defaults to `False`.
            
            If given as `-1` will only force new message if the event already deferred.
        """
        self._force_new_message = force_new_message
        self._parameters = parameters = {}
        
        if (content is not ...):
            parameters['content'] = content
        
        if (embed is not ...):
            parameters['embed'] = embed
        
        if (file is not ...):
            parameters['file'] = file
        
        if (allowed_mentions is not ...):
            parameters['allowed_mentions'] = allowed_mentions
        
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
    
    def get_request_coros(self, client, interaction_event, show_for_invoking_user_only):
        """
        Gets request coroutine buildable from the ``SlashResponse``.
        
        This method is a generator, which should be used inside of a `for` loop.
        
        client : ``Client``
            The client who will send the responses if applicable.
        interaction_event : ``InteractionEvent``
            The respective event to respond on.
        show_for_invoking_user_only : `bool`
            Whether the response message should only be shown for the invoking user.
        
        Yields
        -------
        request_coro : `None` or `coroutine`
        """
        response_state = interaction_event._response_state
        force_new_message = self._force_new_message
        if force_new_message:
            if force_new_message > 0:
                if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
                    yield client.interaction_response_message_create(interaction_event)
                
                response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'file',
                    'tts'))
                response_parameters['show_for_invoking_user_only'] = \
                    self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                
                yield client.interaction_followup_message_create(interaction_event, **response_parameters)
                return
            else:
                if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
                    if 'file' in self._parameters:
                        show_for_invoking_user_only = \
                            self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                        
                        yield client.interaction_response_message_create(interaction_event,
                            show_for_invoking_user_only=show_for_invoking_user_only)
                        
                        response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'file',
                            'tts'))
                        
                        yield client.interaction_response_message_edit(interaction_event, **response_parameters)
                    else:
                        response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'tts'))
                        response_parameters['show_for_invoking_user_only'] = \
                            self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                        
                        yield client.interaction_response_message_create(interaction_event, **response_parameters)
                    return
                
                response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'file',
                    'tts'))
                response_parameters['show_for_invoking_user_only'] = \
                    self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                
                yield client.interaction_followup_message_create(interaction_event, **response_parameters)
                return
        
        else:
            if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
                if 'file' in self._parameters:
                    show_for_invoking_user_only = \
                        self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                    
                    yield client.interaction_response_message_create(interaction_event,
                        show_for_invoking_user_only=show_for_invoking_user_only)
                    
                    response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'file',
                        'tts'))
                    
                    yield client.interaction_response_message_edit(interaction_event, **response_parameters)
                else:
                    response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'tts'))
                    response_parameters['show_for_invoking_user_only'] = \
                        self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                    
                    yield client.interaction_response_message_create(interaction_event, **response_parameters)
                return
            
            if response_state == INTERACTION_EVENT_RESPONSE_STATE_DEFERRED:
                response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed' 'file',))
                
                yield client.interaction_response_message_edit(interaction_event, **response_parameters)
                return
            
            if response_state == INTERACTION_EVENT_RESPONSE_STATE_RESPONDED:
                response_parameters = self._get_response_parameters(('allowed_mentions', 'content', 'embed', 'file',
                    'tts'))
                response_parameters['show_for_invoking_user_only'] = \
                    self._parameters.get('show_for_invoking_user_only', show_for_invoking_user_only)
                
                yield client.interaction_followup_message_create(interaction_event, **response_parameters)
                return
    
    def __repr__(self):
        """Returns the slash response's representation."""
        result = ['<', self.__class__.__name__, ' ']
        if self._force_new_message:
            result.append('(force new message) ')
        
        parameters = self._parameters
        if parameters:
            for key, value in parameters.items():
                result.append(key)
                result.append('=')
                result.append(repr(value))
                result.append(', ')
            
            result[-1] = '>'
        else:
            result.append('>')
        
        return ''.join(result)


def abort(content=..., *, embed=..., file=..., allowed_mentions=..., tts=..., show_for_invoking_user_only=...,):
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
    embed : ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional
        The embedded content of the message.
        
        If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `TypeError` is raised.
    file : `Any`, Optional
        A file to send. Check ``Client._create_file_form`` for details.
    allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` ), Optional
        Which user or role can the message ping (or everyone). Check ``Client._parse_allowed_mentions`` for details.
    tts : `bool`, Optional
        Whether the message is text-to-speech.
    show_for_invoking_user_only : `bool`, Optional
        Whether the sent message should only be shown to the invoking user.
        
        If given as `True`, only the message's content will be processed by Discord.
    
    Raises
    ------
    InteractionAbortedError
        The exception which aborts the interaction, then yields the response.
    """
    if show_for_invoking_user_only is ...:
        if (embed is not ...):
            show_for_invoking_user_only = False
        elif (file is not ...):
            show_for_invoking_user_only = False
        elif (allowed_mentions is not ...):
            show_for_invoking_user_only = False
        elif (tts is not ...):
            show_for_invoking_user_only = False
        elif (content is ...):
            show_for_invoking_user_only = True
        elif is_only_embed(content):
            show_for_invoking_user_only = False
        else:
            show_for_invoking_user_only = True
    
    
    response = SlashResponse(content, embed=embed, file=file, allowed_mentions=allowed_mentions, tts=tts,
        show_for_invoking_user_only=show_for_invoking_user_only, force_new_message=-1)
    
    raise InteractionAbortedError(response)


class InteractionAbortedError(BaseException):
    """
    An ``InteractionAbortedError`` is raised when a slash command is aborted. This class holds the response to send to
    the client.
    
    Attributes
    ----------
    response : ``SlashResponse``
        The response to send.
    """
    def __init__(self, response):
        """
        Creates a new ``InteractionAbortedError`` instance with the given response.
        
        Parameters
        ----------
        response : ``SlashResponse``
            The response to send.
        """
        self.response = response
        BaseException.__init__(self, response)
    
    def __repr__(self):
        """Returns the exception's representation."""
        return f'{self.__class__.__name__}({self.response!r})'


class SlashCommandWrapper:
    """
    Wraps a slash command enabling the wrapper to postprocess the created slash command.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    """
    __slots__ = ('_wrapped',)
    def __new__(cls):
        """
        Creates a partial function to wrap a slash command.
        
        Subclasses should overwrite this method.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlashCommandWrapper._decorate``
            Partial function to wrap a slash command.
        """
        return partial_func(cls._decorate, cls)
    
    def _decorate(cls, wrapped):
        """
        Wraps the given command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlashCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._wrapped = wrapped
        return self
    
    def apply(self, slash_command):
        """
        Applies the wrapper's changes on the respective slash command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
        """
        pass
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}>'
    
    def fetch_function_and_wrappers_back(self):
        """
        Fetches back the source function and all the wrappers, the returns them.
        
        Returns
        -------
        function : `Any`
            The wrapped function.
        wrappers : `list` of ``SlashCommandWrapper`` instances
            The fetched back wrappers.
        """
        wrappers = [self]
        maybe_wrapper = self._wrapped
        while True:
            if isinstance(maybe_wrapper, SlashCommandWrapper):
                wrappers.append(maybe_wrapper)
                maybe_wrapper = maybe_wrapper._wrapped
            else:
                function = maybe_wrapper
                break
        
        wrappers.reverse()
        return function, wrappers


class SlashCommandPermissionOverwriteWrapper(SlashCommandWrapper):
    """
    Wraps a slash to command allowing / disallowing it only for the given user or role inside of a guild.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    _guild_id : `int`
        The guild id where the overwrites should be applied to.
    _overwrite : ``ApplicationCommandPermissionOverwrite``
        The permission overwrite to apply.
    """
    __slots__ = ('_guild_id', '_overwrite')
    def __new__(cls, guild, target, allow):
        """
        Creates a partial function to wrap a slash command.
        
        Parameters
        ----------
        guild : ``Guild`` or `int`
            The guild's identifier where the overwrite is applied.
        target : ``User``, ``Client`` or ``Role``, `tuple` ((``User``, ``UserBase``, ``Role`` type) or \
                `str` (`'Role'`, `'role'`, `'User'`, `'user'`), `int`)
            The target entity of the overwrite
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role`` instance
            - ``User`` instance
            - ``Client`` instance
            - `tuple` (``Role`` type, `int`)
            - `tuple` (``User`` type, `int`)
            - `tuple` (``UserBase`` type, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlashCommandWrapper._decorate``
            Partial function to wrap a slash command.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, (int, str)):
            guild_id = preconvert_snowflake(guild, 'guild')
        else:
            raise TypeError(f'`guild` can be given neither as `{Guild.__class__.__name__}`, and as `int` instance, '
                f'got {guild.__class__.__name__}.')
        
        overwrite = ApplicationCommandPermissionOverwrite(target, allow)
        
        return partial_func(cls._decorate, cls, guild_id, overwrite)
    
    def _decorate(cls, guild_id, overwrite, wrapped):
        """
        Wraps given command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild id where the overwrites should be applied to.
        overwrite : ``ApplicationCommandPermissionOverwrite``
            The permission overwrite to apply.
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlashCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._guild_id = guild_id
        self._overwrite = overwrite
        self._wrapped = wrapped
        return self

    def apply(self, slash_command):
        """
        Applies the wrapper's changes on the respective slash command.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
        """
        slash_command.add_overwrite(self._guild_id, self._overwrite)
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}, guild_id={self._guild_id!r}, ' \
            f'overwrite={self._overwrite!r}>'


async def converter_int(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `int`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `int`
        If conversion fails, then returns `None`.
    """
    try:
        value = int(value)
    except ValueError:
        value = None
    
    return value


async def converter_str(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `str`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `str`
        If conversion fails, then returns `None`.
    """
    return value

BOOL_TABLE = {
    str(True) : True,
    str(False): False,
        }

async def converter_bool(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `bool`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `bool`
        If conversion fails, then returns `None`.
    """
    return BOOL_TABLE.get(value)


async def converter_snowflake(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to a snowflake.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    snowflake : `None` or ``int``
        If conversion fails, then returns `None`.
    """
    try:
        snowflake = int(value)
    except ValueError:
        snowflake = None
    else:
        if (snowflake < (1<<22)) or (snowflake > ((1<<64)-1)):
            snowflake = None
    
    return snowflake


async def converter_user(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to ``UserBase`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    user : `None`, ``User`` or ``Client``
        If conversion fails, then returns `None`.
    """
    user_id = await converter_snowflake(client, interaction, value)
    
    if user_id is None:
        user = None
    else:
        resolved_users = interaction.resolved_users
        if resolved_users is None:
            user = None
        else:
            user = resolved_users.get(user_id)
        
        if user is None:
            try:
                user = await client.user_get(user_id)
            except ConnectionError:
                user = 0
            except DiscordException as err:
                if err.code == ERROR_CODES.unknown_user:
                    user = None
                else:
                    raise
    return user


async def converter_role(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to ``Role`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``Role``
        If conversion fails, then returns `None`.
    """
    role_id = await converter_snowflake(client, interaction, value)
    
    if role_id is None:
        role = None
    else:
        resolved_roles = interaction.resolved_roles
        if resolved_roles is None:
            role = None
        else:
            role = resolved_roles.get(role_id)
        
        if role is None:
            role = ROLES.get(role_id)
    
    return role


async def converter_channel(client, interaction, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to ``ChannelBase`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``ChannelBase`` instance
        If conversion fails, then returns `None`.
    """
    channel_id = await converter_snowflake(client, interaction, value)
    
    if channel_id is None:
        channel = None
    else:
        resolved_channels = interaction.resolved_channels
        if resolved_channels is None:
            channel = None
        else:
            channel = resolved_channels.get(channel_id)
        
        if channel is None:
            channel = CHANNELS.get(channel_id)
    
    return channel


ANNOTATION_TYPE_STR        = 0
ANNOTATION_TYPE_INT        = 1
ANNOTATION_TYPE_BOOL       = 2
ANNOTATION_TYPE_USER       = 3
ANNOTATION_TYPE_USER_ID    = 4
ANNOTATION_TYPE_ROLE       = 5
ANNOTATION_TYPE_ROLE_ID    = 6
ANNOTATION_TYPE_CHANNEL    = 7
ANNOTATION_TYPE_CHANNEL_ID = 8
ANNOTATION_TYPE_NUMBER     = 9

STR_ANNOTATION_TO_ANNOTATION_TYPE = {
    'str'        : ANNOTATION_TYPE_STR        ,
    'int'        : ANNOTATION_TYPE_INT        ,
    'bool'       : ANNOTATION_TYPE_BOOL       ,
    'user'       : ANNOTATION_TYPE_USER       ,
    'user_id'    : ANNOTATION_TYPE_USER_ID    ,
    'role'       : ANNOTATION_TYPE_ROLE       ,
    'role_id'    : ANNOTATION_TYPE_ROLE_ID    ,
    'channel'    : ANNOTATION_TYPE_CHANNEL    ,
    'channel_id' : ANNOTATION_TYPE_CHANNEL_ID ,
    'number'     : ANNOTATION_TYPE_NUMBER     ,
        }

# Used at repr
ANNOTATION_TYPE_TO_STR_ANNOTATION = {
    ANNOTATION_TYPE_STR        : 'str'        ,
    ANNOTATION_TYPE_INT        : 'int'        ,
    ANNOTATION_TYPE_BOOL       : 'bool'       ,
    ANNOTATION_TYPE_USER       : 'user'       ,
    ANNOTATION_TYPE_USER_ID    : 'user_id'    ,
    ANNOTATION_TYPE_ROLE       : 'role'       ,
    ANNOTATION_TYPE_ROLE_ID    : 'role_id'    ,
    ANNOTATION_TYPE_CHANNEL    : 'channel'    ,
    ANNOTATION_TYPE_CHANNEL_ID : 'channel_id' ,
    ANNOTATION_TYPE_NUMBER     : 'number'     ,
        }

TYPE_ANNOTATION_TO_ANNOTATION_TYPE = {
    str          : ANNOTATION_TYPE_STR     ,
    int          : ANNOTATION_TYPE_INT     ,
    bool         : ANNOTATION_TYPE_BOOL    ,
    UserBase     : ANNOTATION_TYPE_USER    ,
    User         : ANNOTATION_TYPE_USER    ,
    Role         : ANNOTATION_TYPE_ROLE    ,
    ChannelBase  : ANNOTATION_TYPE_CHANNEL ,
        }

ANNOTATION_TYPE_TO_CONVERTER = {
    ANNOTATION_TYPE_STR        : converter_str       ,
    ANNOTATION_TYPE_INT        : converter_int       ,
    ANNOTATION_TYPE_BOOL       : converter_bool      ,
    ANNOTATION_TYPE_USER       : converter_user      ,
    ANNOTATION_TYPE_USER_ID    : converter_snowflake ,
    ANNOTATION_TYPE_ROLE       : converter_role      ,
    ANNOTATION_TYPE_ROLE_ID    : converter_snowflake ,
    ANNOTATION_TYPE_CHANNEL    : converter_channel   ,
    ANNOTATION_TYPE_CHANNEL_ID : converter_snowflake ,
    ANNOTATION_TYPE_NUMBER     : converter_int       ,
        }

# `int` Discord fields are broken and they are refusing to fix it, use string instead.
# Reference: https://github.com/discord/discord-api-docs/issues/2448
ANNOTATION_TYPE_TO_OPTION_TYPE = {
    ANNOTATION_TYPE_STR        : ApplicationCommandOptionType.string  ,
    ANNOTATION_TYPE_INT        : ApplicationCommandOptionType.string  ,
    ANNOTATION_TYPE_BOOL       : ApplicationCommandOptionType.boolean ,
    ANNOTATION_TYPE_USER       : ApplicationCommandOptionType.user    ,
    ANNOTATION_TYPE_USER_ID    : ApplicationCommandOptionType.user    ,
    ANNOTATION_TYPE_ROLE       : ApplicationCommandOptionType.role    ,
    ANNOTATION_TYPE_ROLE_ID    : ApplicationCommandOptionType.role    ,
    ANNOTATION_TYPE_CHANNEL    : ApplicationCommandOptionType.channel ,
    ANNOTATION_TYPE_CHANNEL_ID : ApplicationCommandOptionType.channel ,
    ANNOTATION_TYPE_NUMBER     : ApplicationCommandOptionType.integer ,
        }

def parse_annotation_type_and_choice(annotation_value, annotation_name):
    """
    Parses annotation type and choices out from an an annotation value.
    
    Parameters
    ----------
    annotation_value : `str`, `type`, `list`, `dict`
        The annotation's value.
    annotation_name : `str`
        The annotation's name.
    
    Returns
    -------
    annotation_type : `int`
        Internal identifier about the annotation.
    choices : `None` or `dict` of (`int` or `str`, `str`)
        Choices if applicable.
    
    TypeError
        - If `annotation_value` is `list` instance, but it's elements do not match the `tuple` (`str`, `str` or `int`)
            pattern.
        - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
        - If `annotation_value` is unexpected.
    ValueError
        - If `annotation_value` is `str` instance, but not any of the expected ones.
        - If `annotation_value` is `type` instance, but not any of the expected ones.
        - If `choice` amount is out of the expected range [1:25].
        - If a `choice` name is duped.
        - If a `choice` values are mixed types.
    """
    if isinstance(annotation_value, str):
        annotation_value = annotation_value.lower()
        try:
            annotation_type = STR_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Argument `{annotation_name}` has annotation not refers to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    elif isinstance(annotation_value, type):
        try:
            annotation_type = TYPE_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Argument `{annotation_name}` has annotation not refers to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    else:
        if isinstance(annotation_value, list):
            for index, annotation_choice in enumerate(annotation_value):
                if (not isinstance(annotation_choice, tuple)) or (len(annotation_choice) != 2):
                    raise TypeError(f'Argument `{annotation_name}` was given as a `list` annotation, but it\'s element '
                        f'{index} not matches the expected structure: `tuple` (`str`, `str` or `int`), got '
                        f'{annotation_choice!r}.')
        
        elif isinstance(annotation_value, dict):
            annotation_value = list(annotation_value.items())
        else:
            raise TypeError(f'Argument `{annotation_name}` has annotation not set neither as `tuple`, `str`, `type`, '
                f'`list` or `dict`, got {annotation_value.__class__.__name__}.')
        
        choices_length = len(annotation_value)
        if choices_length < 1 or choices_length > APPLICATION_COMMAND_CHOICES_MAX:
            raise ValueError(f'Argument `{annotation_name}` choice length out of expected range '
                f'[1:{APPLICATION_COMMAND_CHOICES_MAX}], got {choices_length!r}.')
        
        names = []
        values = []
        
        for index, annotation_choice in enumerate(annotation_value):
            name, value = annotation_choice
            if (not isinstance(name, str)) or (not isinstance(value, (str, int))):
                raise TypeError(f'Argument `{annotation_name}` was given as a `list` or `dict` annotation, but it\'s '
                    f'element {index} not matches the expected structure: `tuple` (`str`, `str` or `int`), got '
                    f'{annotation_choice!r}.')
            
            names.append(name)
            values.append(value)
        
        # Filter dupe names
        length = 0
        dupe_checker = set()
        for name in names:
            dupe_checker.add(name)
            new_length = len(dupe_checker)
            if new_length == length:
                raise ValueError(f'Duped choice name in annotation: `{annotation_name}`.')
            
            length = new_length
        
        # Filter dupe types
        expected_type = None
        for value in values:
            if isinstance(value, str):
                type_ = str
            else:
                type_ = int
            
            if expected_type is None:
                expected_type = type_
                continue
            
            if expected_type is not type_:
                raise ValueError(f'Mixed choice value types in annotation: `{annotation_name}`.')
        
        if expected_type is str:
            annotation_type = ANNOTATION_TYPE_STR
        else:
            annotation_type = ANNOTATION_TYPE_INT
        
        choices = {value:name for value, name in zip(values, names)}
    
    return annotation_type, choices


class ArgumentConverter:
    """
    Converter class for choice based converters.
    
    Attributes
    ----------
    choices : `None` or `dict` of (`str` or `int`, `str`)
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    converter : `func`
        The converter to use to convert a value to it's desired type.
    default : `bool`
        Default value of the parameter.
    description : `None` or `str`
        The parameter's description.
    name : `str`
        The parameter's description.
    required : `bool`
        Whether the the parameter is required.
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = ('choices', 'converter', 'default', 'description', 'name', 'required', 'type')
    
    def __new__(cls, argument):
        """
        Creates a new argument converter from the given argument.
        
        Parameters
        ----------
        argument : ``Argument``
            The argument to create converter from.
        
        Raises
        ------
        TypeError
            - if the `argument` has no annotation.
            - If `annotation_value` is `list` instance, but it's elements do not match the `tuple`
                (`str`, `str` or `int`) pattern.
            - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
            - If `annotation_value` is unexpected.
            - If `annotation` is not `tuple`.
            - If `annotation` 1st element is not `str` instance.
        ValueError
            - If `annotation` is a `tuple`, but it's length is not range [2:3].
            - If `annotation_value` is `str` instance, but not any of the expected ones.
            - If `annotation_value` is `type` instance, but not any of the expected ones.
            - If `choice` amount is out of the expected range [1:25].
            - If a `choice` name is duped.
            - If a `choice` values are mixed types.
            - If `annotation` 1st element's range is out of the expected range [2:100].
        """
        argument_name = argument.name
        if not argument.has_annotation:
            raise TypeError(f'Argument `{argument_name}` has no annotation.')
        
        annotation = argument.annotation
        if not isinstance(annotation, tuple):
            raise TypeError(f'Argument `{argument_name}` is not `tuple` instances, got {annotation.__class__.__name__}.')
            
        annotation_tuple_length = len(annotation)
        if annotation_tuple_length not in (2, 3):
            raise ValueError(f'Argument `{argument_name}` has annotation as `tuple`, but it\'s length is not in range [2:3], '
                f'got {annotation_tuple_length!r}, {annotation_tuple_length!r}.')
        
        annotation_value, description = annotation[:2]
        annotation_type, choices = parse_annotation_type_and_choice(annotation_value, argument_name)
        
        if (description is not None) and (not isinstance(description, str)):
            raise TypeError(f'Argument `{argument_name}` has annotation description is not `str` instance, got '
                f'{description.__class__.__name__}.')
        
        description_length = len(description)
        if description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or \
                description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX:
            raise ValueError(f'Argument `{argument_name}` has annotation description\'s length is out of the expected '
                f'range [{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:'
                f'{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got {description_length}; {description!r}.')
        
        if argument.has_default:
            default = argument.default
            required = False
        else:
            default = None
            required = True
        
        if len(annotation) == 3:
            name = annotation[2]
            
            if type(name) is str:
                pass
            elif isinstance(name, str):
                name = str(name)
            else:
                raise TypeError(f'`Argument `{argument_name}` has name given as non `str` instance, got '
                    f'{name.__class__.__name__}.')
        else:
            name = argument_name
        
        name = raw_name_to_display(name)
        self = object.__new__(cls)
        self.choices = choices
        self.converter = ANNOTATION_TYPE_TO_CONVERTER[annotation_type]
        self.default = default
        self.description = description
        self.name = name
        self.required = required
        self.type = annotation_type
        return self
    
    async def __call__(self, client, interaction, value):
        """
        Calls the argument converter to convert the given `value` to it's desired state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective ``InteractionEvent``.
        interaction : ``ApplicationCommandInteraction``
            The received application command interaction.
        value : `str`
            ``ApplicationCommandInteractionOption.value``.
        
        Returns
        -------
        passed : `bool`
            Whether the conversion passed.
        value : `None` or ``Any`` instance
            If conversion fails, always returns `None`.
        """
        if value is None:
            if self.required:
                passed = False
            else:
                passed = True
                value = self.default
        else:
            value = await self.converter(client, interaction, value)
            if value is None:
                if self.required:
                    passed = False
                else:
                    passed = True
                    value = self.default
            else:
                choices = self.choices
                if choices is None:
                    passed = True
                else:
                    if value in choices:
                        passed = True
                    else:
                        passed = False
                        value = None
        
        return passed, value
    
    def __repr__(self):
        """Returns the argument converter's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self.name),
            ', type=',
            ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type],
            ', description=',
            reprlib.repr(self.description)
                ]
        
        if not self.required:
            result.append(', default=')
            result.append(repr(self.default))
        
        choices = self.choices
        if (choices is not None):
            result.append(', choices=')
            result.append(repr(choices))
        
        result.append('>')
        
        return ''.join(result)
    
    
    def as_option(self):
        """
        Converts the argument to an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        choices = self.choices
        if choices is None:
            option_choices = None
        else:
            option_choices = [ApplicationCommandOptionChoice(name, str(value)) for value, name in choices.items()]
        
        option_type = ANNOTATION_TYPE_TO_OPTION_TYPE[self.type]
        
        return ApplicationCommandOption(self.name, self.description, option_type, required=self.required,
            choices=option_choices)


def generate_argument_parsers(func):
    """
    Parses the given `func`'s arguments.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlashCommand``.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    argument_parsers : `tuple` of ``ArgumentConverter``
        Argument converters for the given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only arguments.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
        - If `func` accepts less than `2` arguments.
        - If `func` accepts more than `27` arguments.
        - If `func`'s 0th argument is annotated, but not as ``Client``.
        - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
        - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
            `tuple` (`str`, `str` or `int`) pattern.
        - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
            (`str`, `str` or `int`) pattern.
        - If an argument's `annotation_value` is unexpected.
        - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
    ValueError
        - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
        - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
        - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
        - If an argument's `choice` amount is out of the expected range [1:25].
        - If an argument's `choice` name is duped.
        - If an argument's `choice` values are mixed types.
    """
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async() or analyzer.is_async_generator():
        real_analyzer = analyzer
        should_instance = False
    
    elif analyzer.can_instance_to_async_callable() or analyzer.can_instance_to_async_generator():
        real_analyzer = CallableAnalyzer(func.__call__, as_method=True)
        if (not real_analyzer.is_async()) and (not real_analyzer.is_async_generator()):
            raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got '
                f'{func!r}.')
        
        should_instance = True
    
    else:
        raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.')
    
    
    keyword_only_argument_count = real_analyzer.get_non_default_keyword_only_argument_count()
    if keyword_only_argument_count:
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts keyword only arguments.')
    
    if real_analyzer.accepts_args():
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts *args.')
    
    if real_analyzer.accepts_kwargs():
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts **kwargs.')

    
    arguments = real_analyzer.get_non_reserved_positional_arguments()
    
    argument_count = len(arguments)
    if argument_count < 2:
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at least 2 arguments: '
            f'`client` and `interaction_event`, meanwhile it accepts only {argument_count}.')
    
    if argument_count > 2+APPLICATION_COMMAND_OPTIONS_MAX:
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at maximum `27` arguments: '
            f', meanwhile it accepts up to {argument_count}.')
    
    client_argument = arguments[0]
    if client_argument.has_default:
        raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
            'reserved, meanwhile it should not have.')
    
    if client_argument.has_annotation and (client_argument.annotation is not Client):
        raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the client\'s argument slot, '
            f'what is not `{Client.__name__}`.')
    
    
    message_argument = arguments[1]
    if message_argument.has_default:
        raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
            f'reserved, meanwhile it should not have.')
    
    if message_argument.has_annotation and (message_argument.annotation is not InteractionEvent):
        raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the interaction_event\'s argument '
            f'slot what is not `{InteractionEvent.__name__}`.')
    
    argument_parsers = []
    
    for argument in arguments[2:]:
        argument_parser = ArgumentConverter(argument)
        argument_parsers.append(argument_parser)
    
    argument_parsers = tuple(argument_parsers)
    
    if should_instance:
        func = analyzer.insatnce()
    
    return func, argument_parsers


def normalize_description(description):
    """
    Normalizes a docstrings.
    
    Parameters
    ----------
    description : `str` or `None`
        The docstring to clear.
    
    Returns
    -------
    cleared : `str` or `None`
        The cleared docstring. If `docstring` was given as `None` or is detected as empty, will return `None`.
    """
    if description is None:
        return None
    
    lines = description.splitlines()
    for index in reversed(range(len(lines))):
        line = lines[index]
        line = line.strip()
        if line:
            lines[index] = line
        else:
            del lines[index]
    
    if not lines:
        return None
    
    return ' '.join(lines)


class SlashCommand:
    """
    Class to wrap an application command providing interface for ``Slasher``.
    
    Attributes
    ----------
    _command : `None` or ``SlashCommandFunction``
        The command of the slash command.
    _overwrites : `None` or `dict` of (`int`, `list` of ``ApplicationCommandPermissionOverwrite``)
        Permission overwrites applied to the slash command.
    _registered_application_command_ids : `None` or `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    _schema : `None` or ``ApplicationCommand``
        Internal slot used by the ``.get_schema`` method.
    _unloading_behaviour : `int`
        Behaviour what describes what should happen when the command is removed from the slasher.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_DELETE    | 0     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_KEEP      | 1     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_INHERIT   | 2     |
        +-------------------------------+-------+
    
    _sub_commands  : `None` or `dict` of (`str`, ``SlashCommandFunction`` or ``SlashSubCommand``) items
        Sub-commands of the slash command.
        
        Mutually exclusive with the ``._command`` parameter.
    allow_by_default : `bool`
        Whether the command is enabled by default for everyone who has `use_application_commands` permission.
    description : `str`
        Application command description. It's length can be in range [2:100].
    guild_ids : `None` or `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    is_default : `bool`
        Whether the command is the default command in it's category.
    is_global : `bool`
        Whether the command is a global command.
        
        Guild commands have ``.guild_ids`` set as `None`.
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    Notes
    -----
    ``SlashCommand`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_command', '_overwrites', '_registered_application_command_ids', '_schema',
        '_sub_commands', '_unloading_behaviour', 'allow_by_default', 'description', 'guild_ids', 'is_default',
        'is_global', 'name')
    
    def _register_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Registers an application command's identifier to the ``SlashCommand`.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        guild_id : `int`
            The guild where the application command is in.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            registered_application_command_ids = self._registered_application_command_ids = {}
        
        registered_application_command_ids[guild_id] = application_command_id
    
    def _unregister_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Unregisters an application command's identifier from the ``SlashCommand`.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id, where the application command is in.
        application_command_id : `int`
            The application command's identifier.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            try:
                maybe_application_command_id = registered_application_command_ids[guild_id]
            except KeyError:
                pass
            else:
                if maybe_application_command_id == application_command_id:
                    del registered_application_command_ids[guild_id]
                    
                    if not registered_application_command_ids:
                        self._registered_application_command_ids = None
    
    def _pop_command_id_for(self, guild_id):
        """
        Pops the given application command id from the command for the respective guild.
        
        Parameters
        ----------
        guild_id : `int`
            A guild's identifier.
        
        Returns
        -------
        application_command_id : `int`
            The popped application command's identifier. Returns `0` if nothing is matched.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            application_command_id = 0
        else:
            application_command_id = registered_application_command_ids.pop(guild_id, 0)
        
        return application_command_id
    
    def _iter_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if (registered_application_command_ids is not None):
            yield from registered_application_command_ids.values()
    
    def _exhaust_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command and removes them.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if (registered_application_command_ids is not None):
            while registered_application_command_ids:
                guild_id, application_command_id = registered_application_command_ids.popitem()
                yield application_command_id
            
            self._registered_application_command_ids = None
    
    def _iter_sync_ids(self):
        """
        Iterates over all the respective sync ids of the command. If the command is a guild bound command, then will
        iterate over it's guild's id-s.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        sync_id : `int`
        """
        if self.is_global:
            yield SYNC_ID_GLOBAL
            return
        
        guild_ids = self.guild_ids
        if guild_ids is None:
            yield SYNC_ID_NON_GLOBAL
            return
        
        yield from guild_ids
    
    def _iter_guild_ids(self):
        """
        Iterates over all the guild identifiers used by the command.
        
        Yields
        ------
        guild_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            for sync_id in registered_application_command_ids:
                if sync_id > (1<<22):
                    yield sync_id
    
    @classmethod
    def from_class(cls, klass, kwargs=None):
        """
        The method use when creating a ``SlashCommand`` instance from a class.
        
        Extra `kwargs` are supported as well for special the use cases.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attributes of the given `klass` are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
                Description of the command.
            - command : `async-callable`
                If no description was provided, then the class's `.__doc__` will be picked up.
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
                To which guild(s) the command is bound to.
            - is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_for_invoking_user_only : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the response message should only be shown for the invoking user. Defaults to `False`.
            - is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the slash command is the default command in it's category.
            - delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command should be deleted from Discord when removed.
            - `allow_by_default` : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        kwargs, `None` or `dict` of (`str`, `Any`) items, Optional
            Additional parameters arguments. Defaults to `None`.
            
            The expected keyword arguments are the following:
            
            - guild
            - is_global
            - show_for_invoking_user_only
            - is_default
            - allow_by_default
        
        Returns
        -------
        self : ``SlashCommand``
        
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `tuple`, `set`) of
                (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `27` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        """
        klass_type = klass.__class__
        if not issubclass(klass_type, type):
            raise TypeError(f'Expected `type` instance, got {klass_type.__name__}.')
        
        name = getattr(klass, 'name', None)
        if name is None:
            name = klass.__name__
        
        command = getattr(klass, 'command', None)
        if command is None:
            command = getattr(klass, name, None)
        
        description = getattr(klass, 'description', None)
        if description is None:
            description = klass.__doc__
        
        is_global = getattr(klass, 'is_global', None)
        guild = getattr(klass, 'guild', None)
        show_for_invoking_user_only = getattr(klass, 'show_for_invoking_user_only', None)
        is_default = getattr(klass, 'is_default', None)
        delete_on_unload = getattr(klass, 'delete_on_unload', None)
        allow_by_default = getattr(klass, 'allow_by_default', None)
        
        if (kwargs is not None) and kwargs:
            if (description is None):
                description = kwargs.pop('description', None)
            else:
                try:
                    del kwargs['description']
                except KeyError:
                    pass
            
            if (is_global is None):
                is_global = kwargs.pop('is_global', None)
            else:
                try:
                    del kwargs['is_global']
                except KeyError:
                    pass
            
            if (show_for_invoking_user_only is None):
                show_for_invoking_user_only = kwargs.pop('show_for_invoking_user_only', None)
            else:
                try:
                    del kwargs['show_for_invoking_user_only']
                except KeyError:
                    pass
            
            if (guild is None):
                guild = kwargs.pop('guild', None)
            else:
                try:
                    del kwargs['guild']
                except KeyError:
                    pass
            
            if (is_default is None):
                is_default = kwargs.pop('is_default', None)
            else:
                try:
                    del kwargs['is_default']
                except KeyError:
                    pass
            
            if (delete_on_unload is None):
                delete_on_unload = kwargs.pop('delete_on_unload', None)
            else:
                try:
                    del kwargs['delete_on_unload']
                except KeyError:
                    pass
            
            if (allow_by_default is None):
                allow_by_default = kwargs.pop('allow_by_default', None)
            else:
                try:
                    del kwargs['allow_by_default']
                except KeyError:
                    pass
            
            if kwargs:
                raise TypeError(f'`{cls.__name__}.from_class` did not use up some kwargs: `{kwargs!r}`.')
        
        return cls(command, name, description, show_for_invoking_user_only, is_global, guild, is_default,
            delete_on_unload, allow_by_default)
    
    @classmethod
    def from_kwargs(cls, command, name, kwargs):
        """
        Called when a slash command is created before adding it..
        
        Parameters
        ----------
        command : `async-callable`
            The async callable added as the command itself.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The name to be used instead of the passed `command`'s.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additional keyword arguments.
            
            The expected keyword arguments are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
            - is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            - show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
            - is_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            - delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            - allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
        
        Returns
        -------
        self : ``SlashCommand``
        
        Raises
        ------
        TypeError
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `tuple`, `set`) of
                (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `27` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        """
        if (kwargs is None) or (not kwargs):
            description = None
            show_for_invoking_user_only = None
            is_global = None
            guild = None
            is_default = None
            delete_on_unload = None
            allow_by_default = None
        else:
            description = kwargs.pop('description', None)
            show_for_invoking_user_only = kwargs.pop('show_for_invoking_user_only', None)
            is_global = kwargs.pop('is_global', None)
            guild = kwargs.pop('checks', None)
            is_default = kwargs.pop('is_default', None)
            delete_on_unload = kwargs.pop('delete_on_unload', None)
            allow_by_default = kwargs.pop('allow_by_default', None)
            
            if kwargs:
                raise TypeError(f'type `{cls.__name__}` not uses: `{kwargs!r}`.')
        
        return cls(command, name, description, show_for_invoking_user_only, is_global, guild, is_default,
            delete_on_unload, allow_by_default)
    
    @classmethod
    def _check_maybe_route(cls, variable_name, variable_value, route_to, validator):
        """
        Helper class of ``SlashCommand`` parameter routing.
        
        Parameters
        ----------
        variable_name : `str`
            The name of the respective variable
        variable_value : `str`
            The respective value to route maybe.
        route_to : `int`
            The value how much times the routing should happen. by default should be given as `0` if no routing was
            done yet.
        validator : `callable` or `None`
            A callable, what validates the given `variable_value`'s value and converts it as well if applicable.
        
        Returns
        -------
        processed_value : `str`
            Processed value returned by the `validator`. If routing is happening, then a `tuple` of those values is
            returned.
        route_to : `int`
            The amount of values to route to.
        
        Raises
        ------
        ValueError
            Value is routed but to a bad count amount.
        BaseException
            Any exception raised by `validator`.
        """
        if (variable_value is not None) and isinstance(variable_value, tuple):
            route_count = len(variable_value)
            if route_count == 0:
                processed_value = None
            elif route_count == 1:
                variable_value = variable_value[0]
                if variable_value is ...:
                    variable_value = None
                
                if validator is None:
                    processed_value = variable_value
                else:
                    processed_value = validator(variable_value)
            else:
                if route_to == 0:
                    route_to = route_count
                elif route_to == route_count:
                    pass
                else:
                    raise ValueError(f'{cls.__class__.__name__} `{variable_name}` is routed to `{route_count}`, '
                        f'meanwhile something else is already routed to `{route_to}`.')
                
                if validator is None:
                    processed_value = variable_value
                else:
                    processed_values = []
                    for value in variable_value:
                        if (value is not ...):
                            value = validator(value)
                        
                        processed_values.append(value)
                    
                    processed_value = tuple(processed_values)
        
        else:
            if validator is None:
                processed_value = variable_value
            else:
                processed_value = validator(variable_value)
        
        return processed_value, route_to
    
    @staticmethod
    def _validate_show_for_invoking_user_only(show_for_invoking_user_only):
        """
        Validates the given `show_for_invoking_user_only` value.
        
        Parameters
        ----------
        show_for_invoking_user_only : `None` or `bool`
            The `show_for_invoking_user_only` value to validate.
        
        Returns
        -------
        show_for_invoking_user_only : `bool`
            The validated `show_for_invoking_user_only` value.
        
        Raises
        ------
        TypeError
            If `show_for_invoking_user_only` was not given as `None` nor as `bool` instance.
        """
        if show_for_invoking_user_only is None:
            show_for_invoking_user_only = False
        else:
            show_for_invoking_user_only = preconvert_bool(show_for_invoking_user_only, 'show_for_invoking_user_only')
        
        return show_for_invoking_user_only
    
    @staticmethod
    def _validate_is_global(is_global):
        """
        Validates the given `is_global` value.
        
        Parameters
        ----------
        is_global : `None` or `bool`
            The `is_global` value to validate.
        
        Returns
        -------
        is_global : `bool`
            The validated `is_global` value.
        
        Raises
        ------
        TypeError
            If `is_global` was not given as `None` nor as `bool` instance.
        """
        if is_global is None:
            is_global = False
        else:
            is_global = preconvert_bool(is_global, 'is_global')
        
        return is_global
    
    @staticmethod
    def _validate_1_guild(guild):
        """
        Validates 1 guild value.
        
        Parameters
        ----------
        guild : ``Guild`` or `int`
            The guild value to validate.
        
        Returns
        -------
        guild_id : `int`
            Validated guild value converted to `int` instance.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int` instance.
        ValueError
            If `guild` is an integer out of uint64 value range.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, (int, str)):
            guild_id = preconvert_snowflake(guild, 'guild')
        else:
            raise TypeError(f'`guild` was not given neither as `{Guild.__class__.__name__}`, neither as `int` '
                f'instance, got {guild.__class__.__name__}.')
        
        return guild_id
    
    @classmethod
    def _validate_guild(cls, guild):
        """
        Validates the given `guild` value.
        
        Parameters
        ----------
        guild : `None`, `int`, ``Guild``, (`list`, `set`) of (`int`, ``Guild``
            The `is_global` value to validate.
        
        Returns
        -------
        guild_ids : `None` or `set` of `int`
            The validated `guild` value.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
        ValueError
            - If `guild` is given as an empty container.
            - If `guild` is or contains an integer out of uint64 value range.
        """
        if guild is None:
            guild_ids = None
        else:
            guild_ids = set()
            if isinstance(guild, (list, set)):
                for guild_value in guild:
                    guild_id = cls._validate_1_guild(guild_value)
                    guild_ids.add(guild_id)
            else:
                guild_id = cls._validate_1_guild(guild)
                guild_ids.add(guild_id)
            
            if not guild_ids:
                raise ValueError(f'`guild` cannot be given as empty container, got {guild!r}.')
        
        return guild_ids
    
    @staticmethod
    def _validate_name(name):
        """
        Validates the given name.
        
        Parameters
        ----------
        name : `None` or `str`
            A command's respective name.
        
        Returns
        -------
        name : `None` or `str`
            The validated name.
        
        Raises
        ------
        TypeError
            If `name` is not given as `None` neither as `str` instance.
        ValueError
            If `name` length is out of the expected range [1:32].
        """
        if name is not None:
            name_type = name.__class__
            if name_type is str:
                pass
            elif issubclass(name_type, str):
                name = str(name)
            else:
                raise TypeError(f'`name` can be only given as `None` or as `str` instance, got {name_type.__name__}; '
                    f'{name!r}.')
            
            name_length = len(name)
            if name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or \
                    name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX:
                raise ValueError(f'`name` length is out of the expected range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                    f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {name_length!r}; {name!r}.')
        
        return name
    
    @staticmethod
    def _validate_is_default(is_default):
        """
        Validates the given `is_default` value.
        
        Parameters
        ----------
        is_default : `None` or `bool`
            The `is_default` value to validate.
        
        Returns
        -------
        is_default : `bool`
            The validated `is_default` value.
        
        Raises
        ------
        TypeError
            If `is_default` was not given as `None` nor as `bool` instance.
        """
        if is_default is None:
            is_default = False
        else:
            is_default = preconvert_bool(is_default, 'is_default')
        
        return is_default
    
    @staticmethod
    def _validate_delete_on_unload(delete_on_unload):
        """
        Validates the given `delete_on_unload` value.
        
        Parameters
        ----------
        delete_on_unload : `None` or `bool`
            The `delete_on_unload` value to validate.
        
        Returns
        -------
        unloading_behaviour : `int`
            The validated `delete_on_unload` value.
        
        Raises
        ------
        TypeError
            If `delete_on_unload` was not given as `None` nor as `bool` instance.
        """
        if delete_on_unload is None:
            unloading_behaviour = UNLOADING_BEHAVIOUR_INHERIT
        else:
            delete_on_unload = preconvert_bool(delete_on_unload, 'delete_on_unload')
            if delete_on_unload:
                unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
            else:
                unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        return unloading_behaviour
    
    @staticmethod
    def _validate_allow_by_default(allow_by_default):
        """
        Validates the given `allow_by_default` value.
        
        Parameters
        ----------
        allow_by_default : `None` or `bool`
            The `allow_by_default` value to validate.
        
        Returns
        -------
        allow_by_default : `bool`
            The validated `allow_by_default` value.
        
        Raises
        ------
        TypeError
            If `allow_by_default` was not given as `None` nor as `bool` instance.
        """
        if allow_by_default is None:
            allow_by_default = True
        else:
            allow_by_default = preconvert_bool(allow_by_default, 'allow_by_default')
        
        return allow_by_default
    
    @staticmethod
    def _generate_description_from(command, description):
        """
        Generates description from the command and it's maybe given description.
        
        Parameters
        ----------
        command : `None` or `callable`
            The command's function.
        description : `Any`
            The command's description.
        
        Returns
        -------
        description : `str`
            The generated description.
        
        Raises
        ------
        TypeError
            - If `str` description could not be detected.
            - If both `command` and `description` are `None`.
        ValueError
            If `description` length is out of range [2:100].
        """
        if description is None:
            if command is None:
                raise TypeError(f'`description` is a required parameter if `command` is given as `None`.')
            
            description = getattr(command, '__doc__', None)
        
        if (description is None) or (not isinstance(description, str)):
            raise TypeError(f'`description` or `command.__doc__` is not given or is given as `None`.')
            
        description = normalize_description(description)
        
        if description is None:
            description_length = 0
        else:
            description_length = len(description)
        
        if description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or \
                description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX:
            raise ValueError(f'`description` length is out of the expected range '
                f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got '
                f'{description_length!r}; {description!r}.')
        
        return description
    
    def __new__(cls, command, name, description, show_for_invoking_user_only, is_global, guild, is_default,
            delete_on_unload, allow_by_default):
        """
        Creates a new ``SlashCommand`` instance with the given parameters.
        
        Parameters
        ----------
        command : `None` or `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
            Description to use instead of the function's docstring.
        show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
            Whether the response message should only be shown for the invoking user. Defaults to `False`.
        is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
            To which guild(s) the command is bound to.
        is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            Whether the slash command is the default command in it's category.
        delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        self : ``SlashCommand``
        
        Raises
        ------
        TypeError
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `None` or `bool` instance.
            - If `is_global` was not given as 7None` or `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `27` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        """
        # Check for routing
        if (command is not None) and isinstance(command, SlashCommandWrapper):
            command, wrappers = command.fetch_function_and_wrappers_back()
        else:
            wrappers = None
        
        route_to = 0
        name, route_to = cls._check_maybe_route('name', name, route_to, cls._validate_name)
        description, route_to = cls._check_maybe_route('description', description, route_to, None)
        show_for_invoking_user_only, route_to = cls._check_maybe_route('show_for_invoking_user_only',
            show_for_invoking_user_only, route_to, cls._validate_show_for_invoking_user_only)
        is_global, route_to = cls._check_maybe_route('is_global', is_global, route_to, cls._validate_is_global)
        guild_ids, route_to = cls._check_maybe_route('guild', guild, route_to, cls._validate_guild)
        is_default, route_to = cls._check_maybe_route('is_default', is_default, route_to, cls._validate_is_default)
        unloading_behaviour, route_to = cls._check_maybe_route('delete_on_unload', delete_on_unload, route_to,
            cls._validate_delete_on_unload)
        allow_by_default, route_to = cls._check_maybe_route('allow_by_default', allow_by_default, route_to,
            cls._validate_allow_by_default)
        
        if route_to:
            name = route_name(command, name, route_to)
            
            default_description = cls._generate_description_from(command, None)
            show_for_invoking_user_only = route_value(show_for_invoking_user_only, route_to)
            is_global = route_value(is_global, route_to)
            guild_ids = route_value(guild_ids, route_to)
            is_default = route_value(is_default, route_to)
            unloading_behaviour = route_value(unloading_behaviour, route_to)
            allow_by_default = route_value(allow_by_default, route_to)
            
            description = [
                cls._generate_description_from(command, description)
                    if ((description is None) or (description is not default_description)) else default_description
                for description in description]
            
        else:
            name = check_name(command, name)
            
            sub_name_length = len(name)
            if sub_name_length < APPLICATION_COMMAND_NAME_LENGTH_MIN or \
                    sub_name_length > APPLICATION_COMMAND_NAME_LENGTH_MAX:
                raise ValueError(f'`name` length is out of the expected range '
                    f'[{APPLICATION_COMMAND_NAME_LENGTH_MIN}:'
                    f'{APPLICATION_COMMAND_NAME_LENGTH_MAX}], got {sub_name_length!r}; {name!r}.')
            
            description = cls._generate_description_from(command, description)
        
        if command is None:
            argument_parsers = None
        else:
            command, argument_parsers = generate_argument_parsers(command)
        
        if route_to:
            router = []
            
            for name, description, show_for_invoking_user_only, is_global, guild_ids, is_default, unloading_behaviour,\
                    allow_by_default in zip(name, description, show_for_invoking_user_only, is_global, guild_ids,
                        is_default, unloading_behaviour, allow_by_default):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                        f'guild={guild!r}')
                
                name = raw_name_to_display(name)
                
                if (command is None):
                    command_function = None
                    sub_commands = {}
                else:
                    command_function = SlashCommandFunction(command, argument_parsers, name, description,
                        show_for_invoking_user_only, is_default)
                    sub_commands = None
                
                self = object.__new__(cls)
                self._command = command_function
                self._sub_commands = sub_commands
                self.description = description
                self.guild_ids = guild_ids
                self.is_global = is_global
                self.name = name
                self._schema = None
                self._registered_application_command_ids = None
                self.is_default = is_default
                self._unloading_behaviour = unloading_behaviour
                self.allow_by_default = allow_by_default
                self._overwrites = None
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                    f'guild={guild!r}')
            
            name = raw_name_to_display(name)
            
            if (command is None):
                sub_commands = {}
                command_function = None
            else:
                command_function = SlashCommandFunction(command, argument_parsers, name, description,
                    show_for_invoking_user_only, is_default)
                sub_commands = None
            
            self = object.__new__(cls)
            self._command = command_function
            self._sub_commands = sub_commands
            self.description = description
            self.guild_ids = guild_ids
            self.is_global = is_global
            self.name = name
            self._schema = None
            self._registered_application_command_ids = None
            self.is_default = is_default
            self._unloading_behaviour = unloading_behaviour
            self.allow_by_default = allow_by_default
            self._overwrites = None
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    def __repr__(self):
        """returns the slash command's representation."""
        result = ['<', self.__class__.__name__, ' name=', repr(self.name), ' type=']
        
        guild_ids  = self.guild_ids
        if guild_ids is None:
            if self.is_global:
                type_name = 'global'
            else:
                type_name = 'non-global'
        else:
            type_name = 'guild bound'
        
        result.append(type_name)
        
        if not self.allow_by_default:
            result.append(', allow_by_default=False')
        
        if (guild_ids is not None):
            result.append(', guild_ids=')
            result.append(repr(guild_ids))
        
        unloading_behaviour = self._unloading_behaviour
        if unloading_behaviour != UNLOADING_BEHAVIOUR_INHERIT:
            result.append(', unloading_behaviour=')
            if unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
                unloading_behaviour_name = 'delete'
            else:
                unloading_behaviour_name = 'keep'
            
            result.append(unloading_behaviour_name)
        
        result.append('>')
        
        return ''.join(result)
    
    def __str__(self):
        """Returns the slash command's name."""
        return self.name
    
    async def __call__(self, client, interaction_event):
        """
        Calls the slash command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        options = interaction_event.interaction.options
        
        command = self._command
        if (command is not None):
            await command(client, interaction_event, options)
            return
        
        if (options is None) or (len(options) != 1):
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            return
        
        await sub_command(client, interaction_event, option.options)
    
    def get_schema(self):
        """
        Returns an application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        schema = self._schema
        if schema is None:
            schema = self._schema = self.as_schema()
        
        return schema
    
    def as_schema(self):
        """
        Creates a new application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        command = self._command
        if command is None:
            sub_commands = self._sub_commands
            options = [sub_command.as_option() for sub_command in sub_commands.values()]
        else:
            argument_parsers = command._argument_parsers
            if argument_parsers:
                options = [argument_parser.as_option() for argument_parser in argument_parsers]
            else:
                options = None
        
        return ApplicationCommand(self.name, self.description, allow_by_default=self.allow_by_default,
            options=options, )
    
    def as_sub(self):
        """
        Returns the slash command as a sub-command or sub-category.
        
        Returns
        -------
        new : ``SlashCommandFunction`` or ``SlashCommandCategory``
        """
        command = self._command
        if command is not None:
            return command
        
        return SlashCommandCategory(self)
        
    def copy(self):
        """
        Copies the slash command.
        
        Returns
        -------
        new : ``ApplicationCommand``
        """
        command = self._command
        if (command is not None):
            command = command.copy()
        
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            sub_commands = {category_name: category.copy() for category_name, category in sub_commands.items()}
        
        guild_ids = self.guild_ids
        if (guild_ids is not None):
            guild_ids = guild_ids.copy()
        
        new = object.__new__(type(self))
        new._command = command
        new._sub_commands = sub_commands
        new._registered_application_command_ids = None
        new._schema = None
        new.description = self.description
        new.guild_ids = guild_ids
        new.is_global = self.is_global
        new.name = self.name
        new._unloading_behaviour = self._unloading_behaviour
        new.allow_by_default = self.allow_by_default
        
        if (sub_commands is not None):
            parent_reference = None
            for sub_command in sub_commands.values():
                if isinstance(sub_command, SlashCommandCategory):
                    if parent_reference is None:
                        parent_reference = WeakReferer(new)
                    sub_command._parent_reference = parent_reference
        
        overwrites = self._overwrites
        if (overwrites is not None):
            overwrites = {guild_id: overwrite.copy() for guild_id, overwrite in overwrites.items()}
        
        new._overwrites = overwrites
        return new
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands or sub-categories to the slash command.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        
        Raises
        ------
        RuntimeError
            The ``SlashCommand`` is not a category.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self.__class__.__name__} is not a category.')
        
        return _EventHandlerManager(self)
    
    def __setevent__(self, func, name, description=None, show_for_invoking_user_only=None, is_global=None, guild=None,
            is_default=None, delete_on_unload=None, allow_by_default=None):
        """
        Adds a sub-command under the slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description to use instead of the function's docstring.
        show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the response message should only be shown for the invoking user. Defaults to `False`.
        is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)), Optional
            To which guild(s) the command is bound to.
        is_default : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the command is the default command in it's category.
        delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        self : ``SlashCommand``
        
        Raises
        ------
        TypeError
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` argument.
            - If `func` accepts more than `27` argument.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self.__class__.__name__} is not a category.')
        
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, type(self)):
            self._add_command(func)
            return self
        
        command = type(self)(func, name, description, show_for_invoking_user_only, is_global, guild, is_default,
            delete_on_unload, allow_by_default)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command or sub-category.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attributes of the given `klass` are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
                Description of the command.
            - command : `async-callable`
                If no description was provided, then the class's `.__doc__` will be picked up.
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
                To which guild(s) the command is bound to.
            - is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the response message should only be shown for the invoking user. Defaults to `False`.
            - is_default : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the command is the default command in it's category.
            - delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command should be deleted from Discord when removed.
            - allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        self : ``SlashCommand``
         
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `27` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = type(self).from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def _add_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(f'The {self.__class__.__name__} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).')
        
        if command.is_default:
            for sub_command in sub_commands.values():
                if sub_command.is_default:
                    raise RuntimeError(f'The category can have only 1 default command.')
        
        sub_commands[command.name] = command.as_sub()
        self._schema = None
    
    def __eq__(self, other):
        """Returns whether the two slash commands are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._command != other._command:
            return False
        
        if self._sub_commands != other._sub_commands:
            return False
        
        if self._unloading_behaviour != other._unloading_behaviour:
            return False
        
        if self.description != other.description:
            return False
        
        if self.guild_ids != other.guild_ids:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        if self.is_global != other.is_global:
            return False
        
        if self.name != other.name:
            return False
        
        if self.allow_by_default != other.allow_by_default:
            return False
        
        if self._overwrites != other._overwrites:
            return False
        
        return True
    
    def add_overwrite(self, guild_id, overwrite):
        """
        Adds an overwrite to the slash command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id where the overwrite will be applied.
        overwrite : ``ApplicationCommandPermissionOverwrite`` or `None`
            The permission overwrite to add
        
        Raises
        ------
        AssertionError
            - Each command in each guild can have up to `10` overwrite, which is already reached.
        """
        overwrites = self._overwrites
        if overwrites is None:
            self._overwrites = overwrites = {}
        
        overwrites_for_guild = overwrites.get(guild_id)
        
        if __debug__:
            if (overwrites_for_guild is not None) and \
                    (len(overwrites_for_guild) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX):
                raise AssertionError(f'`Each command in each guild can have up to '
                    f'{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX} overwrite,s which is already reached.')
        
        if (overwrites_for_guild is not None) and (overwrite is not None):
            target_id = overwrite.target_id
            for index in range(len(overwrites_for_guild)):
                overwrite_ = overwrites_for_guild[index]
                
                if overwrite_.target_id != target_id:
                    continue
                
                if overwrite.allow == overwrite_.allow:
                    return
                
                del overwrites_for_guild[index]
                
                if overwrites_for_guild:
                    return
                
                overwrites[guild_id] = None
                return
        
        if overwrite is None:
            if overwrites_for_guild is None:
                overwrites[guild_id] = None
        else:
            if overwrites_for_guild is None:
                overwrites[guild_id] = overwrites_for_guild = []
            
            overwrites_for_guild.append(overwrite)
    
    def get_overwrites_for(self, guild_id):
        """
        Returns the slash command's overwrites for the given guild.
        
        Returns
        -------
        overwrites : `None` or `list` of ``ApplicationCommandPermissionOverwrite``
            Returns `None` instead of an empty list.
        """
        overwrites = self._overwrites
        if overwrites is None:
            return
        
        return overwrites.get(guild_id)

    def _get_sync_permission_ids(self):
        """
        Gets the permission overwrite guild id-s which should be synced.
        """
        permission_sync_ids = set()
        guild_ids = self.guild_ids
        # If the command is guild bound, sync it in every guild, if not, then sync it in every guild where it has an
        # an overwrite.
        if (guild_ids is None):
            overwrites = self._overwrites
            if (overwrites is not None):
                permission_sync_ids.update(guild_ids)
        else:
            permission_sync_ids.update(guild_ids)
        
        return permission_sync_ids


class SlashCommandFunction:
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _argument_parsers : `tuple` of ``ArgumentConverter``
        Parsers to parse command parameters.
    _command : `async-callable˛
        The command's function to call.
    description : `str`
        The slash command's description.
    is_default : `bool`
        Whether the command is the default command in it's category.
    name : `str`
        The name of the slash command. It's length can be in range [1:32].
    show_for_invoking_user_only : `bool`
        Whether the response message should only be shown for the invoker user.
    """
    __slots__ = ('_argument_parsers', '_command', 'category', 'description', 'is_default', 'name',
        'show_for_invoking_user_only')
    
    def __new__(cls, command, argument_parsers, name, description, show_for_invoking_user_only, is_default):
        """
        Creates a new ``SlashCommandFunction`` instance with the given parameters-
        
        Parameters
        ----------
        command : `async-callable`
            The command's function to call.
        argument_parsers : `tuple` of ``ArgumentConverter``
            Parsers to parse command parameters.
        name : `str`
            The name of the slash command.
        description : `str`
            The slash command's description.
        show_for_invoking_user_only : `bool`
            Whether the response message should only be shown for the invoking user.
        is_default : `bool`
            Whether the command is the default command in it's category.
        """
        self = object.__new__(cls)
        self._command = command
        self._argument_parsers = argument_parsers
        self.show_for_invoking_user_only = show_for_invoking_user_only
        self.description = description
        self.name = name
        self.is_default = is_default
        return self
    
    async def __call__(self, client, interaction_event, options):
        """
        Calls the slash command function.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None` or `list` of ``InteractionEventChoice``
            Options bound to the function.
        """
        parameters = []
        
        parameter_relation = {}
        if (options is not None):
            for option in options:
                parameter_relation[option.name] = option.value
        
        for argument_parser in self._argument_parsers:
            value = parameter_relation.get(argument_parser.name)
            
            passed, parameter = await argument_parser(client, interaction_event.interaction, value)
            if not passed:
                return
            
            parameters.append(parameter)
        
        coro = self._command(client, interaction_event, *parameters)
        try:
            await process_command_coro(client, interaction_event, self.show_for_invoking_user_only, coro)
        except BaseException as err:
            await client.events.error(client, f'{self!r}.__call__', err)
    
    def __repr__(self):
        """Returns the application command option's representation."""
        result = ['<', self.__class__.__name__, ' name=', repr(self.name), ', description=', repr(self.description)]
        if self.is_default:
            result.append(', is_default=True')
        
        if self.show_for_invoking_user_only:
            result.append(', show_for_invoking_user_only=True')
        
        result.append('>')
        
        return ''.join(result)
    
    def as_option(self):
        """
        Returns the slash command function as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        argument_parsers = self._argument_parsers
        if argument_parsers:
            options = [argument_parser.as_option() for argument_parser in argument_parsers]
        else:
            options = None
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.sub_command,
            options=options, default=self.is_default)
    
    def copy(self):
        """
        Copies the slash command function.
        
        They are not mutable, so just returns itself.
        
        Returns
        -------
        self : ``SlashCommandFunction``
        """
        return self

    def __eq__(self, other):
        """Returns whether the two slash command functions are equal."""
        if type(self) is not type(other):
            return False
        
        if self._command != other._command:
            return False
        
        if self._argument_parsers != other._argument_parsers:
            return False
        
        if self.show_for_invoking_user_only != other.show_for_invoking_user_only:
            return False
        
        if self.description != other.description:
            return False
        
        if self.name != other.name:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        return True


class SlashCommandCategory:
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _sub_commands : `dict` of (`str`, ``SlashCommandFunction``) items
        The sub-commands of the category.
    _parent_reference : `None` or ``WeakReferer`` to ``SlashCommand
        The parent slash command of the category if any.
    description : `str`
        The slash command's description.
    is_default : `bool`
        Whether the command is the default command in it's category.
    name : `str`
        The name of the slash sub-category.
    """
    __slots__ = ('_sub_commands', '_parent_reference', 'description', 'is_default', 'name')
    
    def __new__(cls, slash_command):
        """
        Creates a new ``SlashCommandCategory`` instance with the given parameters.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
            The parent slash command.
        """
        self = object.__new__(cls)
        self.name = slash_command.name
        self.description = slash_command.description
        self._sub_commands = {}
        self._parent_reference = WeakReferer(slash_command)
        self.is_default = slash_command.is_default
        return self
    
    async def __call__(self, client, interaction_event, options):
        """
        Calls the slash command category.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None` or `list` of ``InteractionEventChoice``
            Options bound to the category.
        """
        if (options is None) or len(options) != 1:
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            return
        
        await sub_command(client, interaction_event, option.options)
    
    def as_option(self):
        """
        Returns the slash command category as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        sub_commands = self._sub_commands
        if sub_commands:
            options = [sub_command.as_option() for sub_command in sub_commands]
        else:
            options = None
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.sub_command_group,
            options=options, default=self.is_default)
    
    def copy(self):
        """
        Copies the slash command category.
        
        Returns
        -------
        new : ``SlashCommandCategory``
        """
        sub_commands = {category_name: category.copy() for category_name, category in self._sub_commands.items()}
        
        new = object.__new__(type(self))
        new._sub_commands = sub_commands
        new.description = self.description
        new.name = self.name
        new._parent_reference = None
        return new
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands under the sub-category.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)
    
    def __setevent__(self, func, name, description=None, show_for_invoking_user_only=None, is_global=None, guild=None,
            is_default=None, delete_on_unload=None, allow_by_default=None):
        """
        Adds a sub-command under the slash category.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description to use instead of the function's docstring.
        show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the response message should only be shown for the invoking user. Defaults to `False`.
        is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)), Optional
            To which guild(s) the command is bound to.
        is_default : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the command is the default command in it's category.
        delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        self : ``SlashCommandCategory``
        
        Raises
        ------
        TypeError
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` argument.
            - If `func` accepts more than `27` argument.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, SlashCommand):
            self._add_command(func)
            return self
        
        command = SlashCommand(func, name, description, show_for_invoking_user_only, is_global, guild, is_default,
            delete_on_unload, allow_by_default)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attributes of the given `klass` are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
                Description of the command.
            - command : `async-callable`
                If no description was provided, then the class's `.__doc__` will be picked up.
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
                To which guild(s) the command is bound to.
            - is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the response message should only be shown for the invoking user. Defaults to `False`.
            - is_default : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the command is the default command in it's category.
            - delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command should be deleted from Discord when removed.
            - allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        self : ``SlashCommandCategory``
         
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `27` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = SlashCommand.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def _add_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(f'The {self.__class__.__name__} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).')
        
        as_sub = command.as_sub()
        if isinstance(as_sub, type(self)):
            raise RuntimeError('Cannot add anymore sub-category under sub-categories.')
        
        if command.is_default:
            for sub_command in sub_commands.values():
                if sub_command.is_default:
                    raise RuntimeError(f'The category can have only 1 default command.')
        
        sub_commands[command.name] = as_sub
        
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            parent = parent_reference()
            if (parent is not None):
                parent._schema = None
    
    def __eq__(self, other):
        """Returns whether the two slash commands categories are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.description != other.description:
            return False
        
        if self._sub_commands != other._sub_commands:
            return False
        
        if self.is_default != other.is_default:
            return False
        
        return True

def match_application_commands_to_commands(application_commands, commands, match_schema):
    """
    Matches the given application commands to slash commands.
    
    Parameters
    ----------
    application_commands : `list` of ``ApplicationCommand``
        Received application commands.
    commands : `None` or `list` of ``SlashCommand``
        A list of slash commands if any.
    match_schema : `bool`
        Whether schema or just name should be matched.
    
    Returns
    -------
    commands : `None` or `list` of ``SlashCommand``
        The remaining matched commands.
    matched : `None` or `list` of `tuple` (``ApplicationCommand``, ``SlashCommand`)
        The matched commands in pairs.
    """
    matched = None
    
    if (commands is not None):
        for application_command_index in reversed(range(len(application_commands))):
            application_command = application_commands[application_command_index]
            application_command_name = application_command.name
            
            for command_index in reversed(range(len(commands))):
                command = commands[command_index]
                
                if command.name != application_command_name:
                    continue
                
                if match_schema:
                    if (command.get_schema() != application_command):
                        continue
                
                del application_commands[application_command_index]
                del commands[command_index]
                
                if matched is None:
                    matched = []
                
                matched.append((application_command, command))
        
        if not commands:
            commands = None
    
    return commands, matched


COMMAND_STATE_IDENTIFIER_NONE = 0
COMMAND_STATE_IDENTIFIER_ADDED = 1
COMMAND_STATE_IDENTIFIER_REMOVED = 2
COMMAND_STATE_IDENTIFIER_ACTIVE = 3
COMMAND_STATE_IDENTIFIER_KEPT = 4
COMMAND_STATE_IDENTIFIER_NON_GLOBAL = 5

class CommandChange:
    """
    Represents an added or removed command inside of ``CommandState._changes``
    
    Attributes
    ----------
    added : `bool`
        Whether the command was added.
    command : ``SlashCommand``
        The command itself.
    """
    __slots__ = ('added', 'command')
    def __init__(self, added, command):
        """
        Creates a new command change instance.
        
        Parameters
        ----------
        added : `bool`
            Whether the command was added.
        command : ``SlashCommand``
            The command itself.
        """
        self.added = added
        self.command = command
    
    def __repr__(self):
        """returns the command change's representation."""
        return f'{self.__class__.__name__}(added={self.added!r}, command={self.command!r})'
    
    def __iter__(self):
        """Unpacks the command change."""
        yield self.added
        yield self.command
    
    def __len__(self):
        """Helper for unpacking."""
        return 2

class CommandState:
    """
    Represents command's state inside of a guild.
    
    Attributes
    ----------
    _active : `None` or `list` of ``SlashCommand``
        Active slash commands, which were added.
    _changes : `None` or `list` of ``CommandChange``
        Newly added or removed commands in order.
    _is_non_global : `bool`
        Whether the command state is a command state of non global commands.
    _kept : `None` or `list` of ``SlashCommand``
        Slash commands, which are removed, but should not be deleted.
    """
    __slots__ = ('_active', '_changes', '_is_non_global', '_kept', )
    def __init__(self, is_non_global):
        """
        Creates a new ``CommandState`` instance.
        """
        self._changes = None
        self._active = None
        self._kept = None
        self._is_non_global = is_non_global
    
    def __repr__(self):
        """Returns the command state's representation."""
        result = ['<', self.__class__.__name__]
        if self._is_non_global:
            result.append(' (non global)')
        
        active = self._active
        if (active is not None) and active:
            result.append(' active=[')
            
            for command in active:
                result.append(command.name)
                result.append(', ')
            
            result[-1] = ']'
            
            should_add_comma = True
        else:
            should_add_comma = False
            
        kept = self._kept
        if (kept is not None) and kept:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' kept=[')
            
            for command in kept:
                result.append(command.name)
                result.append(', ')
            
            result[-1] = ']'
        
        changes = self._changes
        if (changes is not None):
            if should_add_comma:
                result.append(',')
            
            result.append(' changes=')
            result.append(repr(changes))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_should_add_commands(self):
        """
        Returns the commands, which should be added.
        
        Returns
        -------
        commands : `list` of ``SlashCommand``
        """
        commands = []
        active = self._active
        if (active is not None):
            commands.extend(active)
        
        changes = self._changes
        if (changes is not None):
            for added, command in changes:
                command_name = command.name
                
                for index in range(len(commands)):
                    if commands[index].name != command_name:
                        continue
                    
                    if added:
                        commands[index] = command
                    else:
                        del commands[index]
                    
                    break
                
                else:
                    if added:
                        commands.append(command)
        
        return commands
    
    def get_should_keep_commands(self):
        """
        Returns the commands, which should be kept.
        
        Returns
        -------
        commands : `list` of ``SlashCommand``
        """
        commands = []
        kept = self._kept
        if (kept is not None):
            commands.extend(kept)
        
        changes = self._changes
        if (changes is not None):
            for command_change_state in changes:
                command_name = command_change_state.command.name
                
                for index in range(len(commands)):
                    if commands[index].name != command_name:
                        continue
                    
                    del commands[index]
                    break
        
        return commands
    
    def get_should_remove_commands(self):
        """
        Returns the commands, which should be removed.
        
        Returns
        -------
        commands : `list` of ``SlashCommand``
        """
        commands = []
        
        changes = self._changes
        if (changes is not None):
            for added, command in changes:
                command_name = command.name
                
                for index in range(len(commands)):
                    if commands[index].name != command_name:
                        continue
                
                    if added:
                        del commands[index]
                    else:
                        commands[index] = command
                    
                    break
                else:
                    if not added:
                        commands.append(command)
        
        return commands
    
    def _try_purge_from_changes(self, name):
        """
        Purges the commands with the given names from the changed ones.
        
        Parameters
        ----------
        name : `str`
            The command's name.
        
        Returns
        -------
        purged_from_identifier : `int`
            From which internal container was the command purged from.
            
            Can be any of the following values:
            
            +-----------------------------------+-------+
            | Respective name                   | Value |
            +===================================+=======+
            | COMMAND_STATE_IDENTIFIER_NONE     | 0     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ADDED    | 1     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_REMOVED  | 2     |
            +-----------------------------------+-------+
        
        command : `None` or ``SlashCommand``
            The purged command if any.
        """
        changes = self._changes
        if (changes is not None):
            for index in range(len(changes)):
                command_change_state = changes[index]
                command = command_change_state.command
                if command.name != name:
                    continue
                
                del changes[index]
                if not changes:
                    self._changes = None
                
                if command_change_state.added:
                    purged_from_identifier = COMMAND_STATE_IDENTIFIER_ADDED
                else:
                    purged_from_identifier = COMMAND_STATE_IDENTIFIER_REMOVED
                
                return purged_from_identifier, command
        
        return COMMAND_STATE_IDENTIFIER_NONE, None
    
    def _try_purge(self, name):
        """
        Tries to purge the commands from the given name from the command state.
        
        Parameters
        ----------
        name : `str`
            The respective command's name.
        
        Returns
        -------
        purged_from_identifier : `int`
            From which internal container was the command purged from.
            
            Can be any of the following values:
            
            +-----------------------------------+-------+
            | Respective name                   | Value |
            +===================================+=======+
            | COMMAND_STATE_IDENTIFIER_NONE     | 0     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ADDED    | 1     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_REMOVED  | 2     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ACTIVE   | 3     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_KEPT     | 4     |
            +-----------------------------------+-------+
        
        command : `None` or ``SlashCommand``
            The purged command if any.
        """
        from_changes_result = self._try_purge_from_changes(name)
        
        active = self._active
        if (active is not None):
            for index in range(len(active)):
                command = active[index]
                if command.name == name:
                    del active[index]
                    if not active:
                        self._active = None
                    
                    return COMMAND_STATE_IDENTIFIER_ACTIVE, command
        
        kept = self._kept
        if (kept is not None):
            for index in range(len(kept)):
                command = kept[index]
                if command.name == name:
                    del kept[index]
                    if not kept:
                        self._kept = None
                    
                    return COMMAND_STATE_IDENTIFIER_KEPT, command
        
        return from_changes_result
    
    def activate(self, command):
        """
        Adds the command to the ``CommandState`` as active.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command.
        """
        if self._is_non_global:
            return
        
        self._try_purge(command.name)
        active = self._active
        if active is None:
            self._active = active = []
        
        active.append(command)
    
    def keep(self, command):
        """
        Marks the command, as it should be kept.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command.
        """
        if self._is_non_global:
            return
        
        self._try_purge(command.name)
        kept = self._kept
        if kept is None:
            self._kept = kept = []
        
        kept.append(command)
    
    def delete(self, command):
        """
        Deletes the command from the command state.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command.
        """
        if self._is_non_global:
            return
        
        self._try_purge(command.name)
    
    def add(self, command):
        """
        Adds a command to the ``CommandState``.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The command to add.
        
        Returns
        -------
        command : ``SlashCommand``
            The existing command or the given one.
        
        action_identifier : `int`
            The action what took place.
            
            It's value can be any of the following:
            
            +---------------------------------------+-------+
            | Respective name                       | Value |
            +=======================================+=======+
            | COMMAND_STATE_IDENTIFIER_ADDED        | 1     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ACTIVE       | 3     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_KEPT         | 4     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_NON_GLOBAL   | 5     |
            +---------------------------------------+-------+
        """
        if self._is_non_global:
            existing_command, purge_identifier = self._try_purge(command.name)
            active = self._active
            if active is None:
                self._active = active = []
            
            active.append(command)
            return existing_command, COMMAND_STATE_IDENTIFIER_NON_GLOBAL
        
        kept = self._kept
        if (kept is not None):
            command_name = command.name
            
            for index in range(len(kept)):
                kept_command = kept[index]
                if kept_command.name != command_name:
                    continue
                
                if kept_command != command:
                    continue
                
                del kept[index]
                if not kept:
                    self._kept = None
                
                self._try_purge_from_changes(command_name)
                return kept_command, COMMAND_STATE_IDENTIFIER_KEPT
        
        active = self._active
        if (active is not None):
            command_name = command.name
            
            for index in range(len(active)):
                active_command = active[index]
                if active_command.name != command_name:
                    continue
                
                if active_command != command:
                    continue
                
                del active[index]
                if not active:
                    self._active = None
                
                self._try_purge_from_changes(command_name)
                return active_command, COMMAND_STATE_IDENTIFIER_ACTIVE
        
        changes = self._changes
        if changes is None:
            self._changes = changes = []
        
        change = CommandChange(True, command)
        changes.append(change)
        return command, COMMAND_STATE_IDENTIFIER_ADDED
    
    def remove(self, command, slasher_unloading_behaviour):
        """
        Removes the command from the ``CommandState``.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The command to add.
        slasher_unloading_behaviour : `int`
            The parent slasher's unload behaviour.
            
            Can be any of the following:
            
            +-------------------------------+-------+
            | Respective name               | Value |
            +-------------------------------+-------+
            | UNLOADING_BEHAVIOUR_DELETE    | 0     |
            +-------------------------------+-------+
            | UNLOADING_BEHAVIOUR_KEEP      | 1     |
            +-------------------------------+-------+
        
        Returns
        -------
        command : ``SlashCommand``
            The existing command or the given one.
        action_identifier : `int`
            The action what took place.
            
            It's value can be any of the following:
            
            +---------------------------------------+-------+
            | Respective name                       | Value |
            +=======================================+=======+
            | COMMAND_STATE_IDENTIFIER_REMOVED      | 2     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ACTIVE       | 3     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_KEPT         | 4     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_NON_GLOBAL   | 5     |
            +---------------------------------------+-------+
        """
        unloading_behaviour = command._unloading_behaviour
        if unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
            should_keep = False
        elif unloading_behaviour == UNLOADING_BEHAVIOUR_KEEP:
            should_keep = True
        else: # if unloading_behaviour == UNLOADING_BEHAVIOUR_INHERIT:
            if slasher_unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
                should_keep = False
            else: # if slasher_unloading_behaviour == UNLOADING_BEHAVIOUR_KEEP:
                should_keep = True
        
        if self._is_non_global:
            existing_command, purge_identifier = self._try_purge(command.name)
            if should_keep:
                kept = self._kept
                if kept is None:
                    self._kept = kept = []
                
                kept.append(command)
            
            return existing_command, COMMAND_STATE_IDENTIFIER_NON_GLOBAL
        
        if should_keep:
            self._try_purge_from_changes(command.name)
            
            kept = self._kept
            if (kept is not None):
                command_name = command.name
                
                for index in range(len(kept)):
                    kept_command = kept[index]
                    if kept_command.name != command_name:
                        continue
                    
                    if kept_command != command:
                        continue
                    
                    return kept_command, COMMAND_STATE_IDENTIFIER_KEPT
            
            active = self._active
            if (active is not None):
                command_name = command.name
                
                for index in range(len(active)):
                    active_command = active[index]
                    if active_command.name != command_name:
                        continue
                    
                    if active_command != command:
                        continue
                    
                    del active[index]
                    if not active:
                        self._active = None
                    
                    kept = self._kept
                    if kept is None:
                        self._kept = kept = []
                    
                    kept.append(active_command)
                    return active_command, COMMAND_STATE_IDENTIFIER_ACTIVE
            
            kept = self._kept
            if kept is None:
                self._kept = kept = []
            
            kept.append(command)
            return command, COMMAND_STATE_IDENTIFIER_KEPT
        
        # We do not purge active
        kept = self._kept
        if (kept is not None):
            command_name = command.name
            
            for index in range(len(kept)):
                kept_command = kept[index]
                if kept_command.name != command_name:
                    continue
                
                if kept_command != command:
                    continue
                
                del kept[index]
                break
        
        changes = self._changes
        if changes is None:
            self._changes = changes = []
        
        change = CommandChange(True, command)
        changes.append(change)
        return command, COMMAND_STATE_IDENTIFIER_REMOVED


SYNC_ID_GLOBAL = 0
SYNC_ID_MAIN = 1
SYNC_ID_NON_GLOBAL = 2


class Slasher(EventHandlerBase):
    """
    Slash command processor.
    
    Attributes
    ----------
    _command_states : `dict` of (`int`, ``CommandState``) items
        The slasher's commands's states.
    
    _command_unloading_behaviour : `int`
        Behaviour to describe what should happen when a command is unloaded.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_DELETE    | 0     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_KEEP      | 1     |
        +-------------------------------+-------+
    
    _sync_done : `set` of `int`
        A set of guild id-s which are synced.
    _sync_permission_tasks : `dict` of (`int`, ``Task``) items
        A dictionary of `guild-id` - `permission getter` tasks.
    _sync_should : `set` of `int`
        A set of guild id-s which should be synced.
    _sync_tasks : `dict` of (`int, ``Task``) items
        A dictionary of guilds, which are in sync at the moment.
    _synced_permissions : `dict` of (`int`, `dict` of (`int`, ``ApplicationCommandPermission``) items) items
        A nested dictionary, which contains application command permission overwrites per guild_id and per command_id.
    command_id_to_command : `dict` of (`int`, ``SlashCommand``) items
        A dictionary where the keys are application command id-s and the keys are their respective command.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = 'interaction_create'
        Tells for the ``EventDescriptor`` that ``Slasher`` is a `interaction_create` event handler.
    SUPPORTED_TYPES : `tuple` (``SlashCommand``, )
        Tells to ``eventlist`` what exact types the ``Slasher`` accepts.
    
    Notes
    -----
    ``Slasher`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_command_states', '_command_unloading_behaviour', '_sync_done',
        '_sync_permission_tasks', '_sync_should', '_sync_tasks', '_synced_permissions', 'command_id_to_command')
    
    __event_name__ = 'interaction_create'
    
    SUPPORTED_TYPES = (SlashCommand, )
    
    def __new__(cls, delete_commands_on_unload=False):
        """
        Creates a new slash command processer.
        
        Parameters
        ----------
        delete_commands_on_unload : `bool`, Optional
            Whether commands should be deleted when unloaded.
        
        Raises
        ------
        TypeError
            If `delete_commands_on_unload` was not given as `bool` instance.
        """
        if type(delete_commands_on_unload) is bool:
            pass
        elif isinstance(delete_commands_on_unload, bool):
            delete_commands_on_unload = bool(delete_commands_on_unload)
        else:
            raise TypeError(f'`delete_commands_on_unload` can be given as `bool` instance, got '
                f'{delete_commands_on_unload.__class__.__name__}.')
        
        if delete_commands_on_unload:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        self = object.__new__(cls)
        self._command_unloading_behaviour = command_unloading_behaviour
        self._command_states = {}
        self._sync_tasks = {}
        self._sync_should = set()
        self._sync_done = set()
        self._sync_permission_tasks = {}
        self._synced_permissions = {}
        
        self.command_id_to_command = {}
        
        return self
    
    async def __call__(self, client, interaction_event):
        """
        Calls the slasher, processing a received interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the interaction.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        if interaction_event.type is not INTERACTION_TYPE_APPLICATION_COMMAND:
            return
        
        try:
            command = await self._try_get_command_by_id(client, interaction_event)
        except ConnectionError:
            return
        except BaseException as err:
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if command is not None:
            await command(client, interaction_event)
    
    
    def __setevent__(self, func, name, description=None, show_for_invoking_user_only=None, is_global=None, guild=None,
            is_default=None, delete_on_unload=None, allow_by_default=None):
        """
        Adds a slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description to use instead of the function's docstring.
        show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the response message should only be shown for the invoking user. Defaults to `False`.
        is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)), Optional
            To which guild(s) the command is bound to.
        is_default : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the command is the default command in it's category.
        delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        func : ``SlashCommand``
             The created or added command.
        
        Raises
        ------
        TypeError
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` argument.
            - If `func` accepts more than `27` argument.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, SlashCommand):
            self._add_command(func)
            return func
        
        command = SlashCommand(func, name, description, show_for_invoking_user_only, is_global, guild, is_default,
            delete_on_unload, allow_by_default)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return command
        
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a slash command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attributes of the given `klass` are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
                Description of the command.
            - command : `async-callable`
                If no description was provided, then the class's `.__doc__` will be picked up.
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
                To which guild(s) the command is bound to.
            - is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_for_invoking_user_only : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the response message should only be shown for the invoking user. Defaults to `False`.
            - is_default : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the command is the default command in it's category.
            - delete_on_unload : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command should be deleted from Discord when removed.
            - allow_by_default : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the command is enabled by default for everyone who has `use_application_commands` permission.
        
        Returns
        -------
        func : ``SlashCommand``
             The created or added command.
         
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_for_invoking_user_only` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `27` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
            - If `is_default` was not given neither as `None`, `bool` or `tuple` of (`bool`, `Ellipsis`).
            - If `delete_on_unload` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`).
            - If `allow_by_default` was not given neither as `None`, `bool` or `tuple` of (`None`, `bool`,
                `Ellipsis`).
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:25].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [1:32].
        """
        command = SlashCommand.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return command
    
    def _add_command(self, command):
        """
        Adds a slash command to the ``Slasher``.
        
        Parameters
        ---------
        command : ``SlashCommand``
            The command to add.
        
        Raises
        ------
        ValueError
            If an already added command's name conflicts with the added one's.
        """
        for sync_id in command._iter_sync_ids():
            if sync_id == SYNC_ID_NON_GLOBAL:
                is_non_global = True
            else:
                is_non_global = False
            
            try:
                command_state = self._command_states[sync_id]
            except KeyError:
                command_state = self._command_states[sync_id] = CommandState(is_non_global)
            
            command, change_identifier = command_state.add(command)
            if change_identifier == COMMAND_STATE_IDENTIFIER_ADDED:
                self._sync_done.discard(sync_id)
                self._sync_should.add(sync_id)
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_ACTIVE:
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_KEPT:
                for application_command_id in command._iter_application_command_ids():
                    self.command_id_to_command[application_command_id] = command
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_NON_GLOBAL:
                continue
    
    def _remove_command(self, command):
        """
        Tries to the given command from the ``Slasher``.
        
        Parameters
        ----------
        command : ``Command``
            The command to remove.
        """
        for sync_id in command._iter_sync_ids():
            if sync_id == SYNC_ID_NON_GLOBAL:
                is_non_global = True
            else:
                is_non_global = False
            
            try:
                command_state = self._command_states[sync_id]
            except KeyError:
                command_state = self._command_states[sync_id] = CommandState(is_non_global)
            
            command, change_identifier = command_state.remove(command, self._command_unloading_behaviour)
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_REMOVED:
                if sync_id == SYNC_ID_NON_GLOBAL:
                    for guild_id in command._iter_guild_ids():
                        self._sync_should.add(sync_id)
                        self._sync_done.discard(sync_id)
                else:
                    self._sync_should.add(sync_id)
                    self._sync_done.discard(sync_id)
                
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_ACTIVE:
                for application_command_id in command._iter_application_command_ids():
                    try:
                        del self.command_id_to_command[application_command_id]
                    except KeyError:
                        pass
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_KEPT:
                continue
    
            if change_identifier == COMMAND_STATE_IDENTIFIER_NON_GLOBAL:
                if (command is not None):
                    for guild_id in command._iter_guild_ids():
                        self._sync_done.discard(guild_id)
                        self._sync_should.add(guild_id)
                continue
    
    def __delevent__(self, func, name, **kwargs):
        """
        A method to remove a command by itself, or by it's function and name combination if defined.
        
        Parameters
        ----------
        func : ``SlashCommand``, ``Router`` of ``SlashCommand``
            The command to remove.
        name : `None` or `str`
            The command's name to remove.
        **kwargs : Keyword Arguments
            Other keyword only arguments are ignored.
        
        Raises
        ------
        TypeError
            If `func` was not given neither as ``SlashCommand`` not as ``Router`` of ``SlashCommand``.
        """
        if isinstance(func, Router):
            for sub_func in func:
                if not isinstance(sub_func, SlashCommand):
                    raise TypeError(f'`func` was not given neither as `{SlashCommand.__name__}`, or '
                        f'`{Router.__name__}` of `{SlashCommand.__name__}` instances, got {func!r}.')
            
            for sub_func in func:
                self._remove_command(sub_func)
                
        elif isinstance(func, SlashCommand):
            self._remove_command(func)
        else:
            raise TypeError(f'`func` was not given neither as `{SlashCommand.__name__}`, or `{Router.__name__}` of '
                f'`{SlashCommand.__name__}` instances, got {func!r}.')
    
    async def _try_get_command_by_id(self, client, interaction_event):
        """
        Tries to get the command by id. If found it, returns it, if not, returns `None`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client instance, who received the interaction event.
        interaction_event : ``InteractionEvent``
            The invoked interaction.
        """
        interaction_id = interaction_event.interaction.id
        try:
            command = self.command_id_to_command[interaction_id]
        except KeyError:
            pass
        else:
            return command
        
        # First request guild commands
        guild = interaction_event.guild
        if (guild is not None):
            guild_id = guild.id
            if not await self._sync_guild(client, guild_id):
                return None
            
            try:
                command = self.command_id_to_command[interaction_id]
            except KeyError:
                pass
            else:
                return command
        
        if not await self._sync_global(client):
            return None
        
        try:
            command = self.command_id_to_command[interaction_id]
        except KeyError:
            pass
        else:
            return command
    
    async def _sync_guild(self, client, guild_id):
        """
        Syncs the respective guild's commands if not yet synced.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        if guild_id in self._sync_done:
            return True
        
        try:
            task = self._sync_tasks[guild_id]
        except KeyError:
            task = self._sync_tasks[guild_id] = Task(self._sync_guild_task(client, guild_id), KOKORO)
        
        return await task
    
    async def _sync_global(self, client):
        """
        Syncs the not yet synced global commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        if SYNC_ID_GLOBAL in self._sync_done:
            return True
        
        try:
            task = self._sync_tasks[SYNC_ID_GLOBAL]
        except KeyError:
            task = self._sync_tasks[SYNC_ID_GLOBAL] = Task(self._sync_global_task(client), KOKORO)
        
        return await task
    
    def _unregister_helper(self, command, command_state, guild_id):
        """
        Unregisters all the call relations of the given command.
        
        Parameters
        ----------
        command : `None` or ``SlashCommand``
            The slash command to unregister.
        command_state : `None` or ``CommandState``
            The command's respective state instance.
        guild_id : `int`
            The respective guild's id.
        """
        if (command is not None):
            command_id = command._pop_command_id_for(guild_id)
            if command_id:
                try:
                    del self.command_id_to_command[command_id]
                except KeyError:
                    pass
            
            if (command_state is not None):
                command_state.delete(command)
    
    def _register_helper(self, command, command_state, guild_id, application_command_id):
        """
        Registers the given command, guild id, application command relationship.
        
        Parameters
        ----------
        command : `None` or ``SlashCommand``
            The slash command to register.
        command_state : `None` or ``CommandState``
            The command's respective state instance.
        guild_id : `int`
            The respective guild's id.
        application_command_id : `int`
            The respective command's identifier.
        """
        if (command is not None):
            self.command_id_to_command[application_command_id] = command
            command._register_guild_and_application_command_id(guild_id, application_command_id)
            if (command_state is not None):
                command_state.activate(command)
    
    def _keep_helper(self, command, command_state, guild_id):
        """
        Marks the given command to be kept at the given guild.
        
        Parameters
        ----------
        command : `None` or ``SlashCommand``
            The slash command to register.
        command_state : `None` or ``CommandState``
            The command's respective state instance.
        guild_id : `int`
            The respective guild's id.
        """
        if (command is not None):
            command_id = command._pop_command_id_for(guild_id)
            if command_id:
                try:
                    del self.command_id_to_command[command_id]
                except KeyError:
                    pass
            
            if (command_state is not None):
                command_state.keep(command)
    
    async def _sync_guild_task(self, client, guild_id):
        """
        Syncs the respective guild's commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        success = False
        
        try:
            application_commands = await client.application_command_guild_get_all(guild_id)
        except BaseException as err:
            # No internet connection
            if not isinstance(err, ConnectionError):
                await client.events.error(client, f'{self!r}._sync_guild_task', err)
        else:
            guild_command_state = self._command_states.get(guild_id)
            if guild_command_state is None:
                guild_added_commands = None
                guild_keep_commands = None
                guild_removed_commands = None
            else:
                guild_added_commands = guild_command_state.get_should_add_commands()
                if not guild_added_commands:
                    guild_added_commands = None
                
                guild_keep_commands = guild_command_state.get_should_keep_commands()
                if not guild_keep_commands:
                    guild_keep_commands = None
                
                guild_removed_commands = guild_command_state.get_should_remove_commands()
                if not guild_removed_commands:
                    guild_removed_commands = None
            
            non_global_command_state = self._command_states.get(SYNC_ID_NON_GLOBAL)
            if non_global_command_state is None:
                non_global_added_commands = None
                non_global_keep_commands = None
            else:
                non_global_added_commands = non_global_command_state.get_should_add_commands()
                if not non_global_added_commands:
                    non_global_added_commands = None
                
                non_global_keep_commands = non_global_command_state.get_should_keep_commands()
                if not non_global_keep_commands:
                    non_global_keep_commands = None
            
            command_create_coroutines = None
            command_edit_coroutines = None
            command_delete_coroutines = None
            command_register_coroutines = None
            
            guild_added_commands, matched = match_application_commands_to_commands(application_commands,
                guild_added_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._register_command(client, command, guild_command_state, guild_id,
                        application_command)
                    
                    if command_register_coroutines is None:
                        command_register_coroutines = []
                    command_register_coroutines.append(coroutine)
            
            non_global_added_commands, matched = match_application_commands_to_commands(application_commands,
                non_global_added_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._register_command(client, command, non_global_command_state, guild_id,
                        application_command)
                    
                    if command_register_coroutines is None:
                        command_register_coroutines = []
                    command_register_coroutines.append(coroutine)
            
            guild_added_commands, matched = match_application_commands_to_commands(application_commands,
                guild_added_commands, False)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._edit_command(client, command, guild_command_state, guild_id,
                        application_command,)
                    if command_edit_coroutines is None:
                        command_edit_coroutines = []
                    command_edit_coroutines.append(coroutine)
            
            non_global_added_commands, matched = match_application_commands_to_commands(application_commands,
                non_global_added_commands, False)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._edit_guild_command_to_non_global(client, command, non_global_command_state,
                        guild_id, application_command)
                    if command_edit_coroutines is None:
                        command_edit_coroutines = []
                    command_edit_coroutines.append(coroutine)
            
            guild_keep_commands, matched = match_application_commands_to_commands(application_commands,
                guild_keep_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    self._keep_helper(command, guild_command_state, guild_id)
            
            non_global_keep_commands, matched = match_application_commands_to_commands(application_commands,
                non_global_keep_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    self._keep_helper(command, non_global_command_state, guild_id)
            
            guild_removed_commands, matched = match_application_commands_to_commands(application_commands,
                guild_removed_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._delete_command(client, command, guild_command_state, guild_id,
                        application_command)
                    if command_delete_coroutines is None:
                        command_delete_coroutines = []
                    command_delete_coroutines.append(coroutine)
            
            if (guild_added_commands is not None):
                while guild_added_commands:
                    command = guild_added_commands.pop()
                    
                    coroutine = self._create_command(client, command, guild_command_state, guild_id)
                    if command_create_coroutines is None:
                        command_create_coroutines = []
                    command_create_coroutines.append(coroutine)
                    continue
            
            while application_commands:
                application_command = application_commands.pop()
                
                coroutine = self._delete_command(client, None, None, guild_id, application_command)
                if command_delete_coroutines is None:
                    command_delete_coroutines = []
                command_delete_coroutines.append(coroutine)
            
            success = True
            for coroutines in (command_register_coroutines, command_delete_coroutines, command_edit_coroutines, \
                    command_create_coroutines):
                if (coroutines is not None):
                    done, pending = await WaitTillAll([Task(coroutine, KOKORO) for coroutine in coroutines], KOKORO)
                    
                    for future in done:
                        if not future.result():
                            success = False
        
        finally:
            try:
                del self._sync_tasks[guild_id]
            except KeyError:
                pass
        
        if success:
            self._sync_should.discard(guild_id)
            self._sync_done.add(guild_id)
        
        return success
    
    async def _sync_global_task(self, client):
        """
        Syncs the global commands off the ``Slasher``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the commands where synced with success.
        """
        success = False
        try:
            application_commands = await client.application_command_global_get_all()
        except BaseException as err:
            # No internet connection
            if not isinstance(err, ConnectionError):
                await client.events.error(client, f'{self!r}._sync_global_commands', err)
            
        else:
            global_command_state = self._command_states.get(SYNC_ID_GLOBAL)
            if global_command_state is None:
                global_added_commands = None
                global_keep_commands = None
                global_removed_commands = None
            else:
                global_added_commands = global_command_state.get_should_add_commands()
                if not global_added_commands:
                    global_added_commands = None
                
                global_keep_commands = global_command_state.get_should_keep_commands()
                if not global_keep_commands:
                    global_keep_commands = None
                
                global_removed_commands = global_command_state.get_should_remove_commands()
                if not global_removed_commands:
                    global_removed_commands = None
            
            command_create_coroutines = None
            command_edit_coroutines = None
            command_delete_coroutines = None
            command_register_coroutines = None
            
            global_added_commands, matched = match_application_commands_to_commands(application_commands,
                global_added_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._register_command(client, command, global_command_state, SYNC_ID_GLOBAL,
                        application_command)
                    
                    if command_register_coroutines is None:
                        command_register_coroutines = []
                    command_register_coroutines.append(coroutine)
            
            global_keep_commands, matched = match_application_commands_to_commands(application_commands,
                global_keep_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    self._keep_helper(command, global_command_state, SYNC_ID_GLOBAL)
            
            global_removed_commands, matched = match_application_commands_to_commands(application_commands,
                global_removed_commands, True)
            if (matched is not None):
                for application_command, command in matched:
                    coroutine = self._delete_command(client, command, global_command_state, SYNC_ID_GLOBAL,
                        application_command)
                    if command_delete_coroutines is None:
                        command_delete_coroutines = []
                    command_delete_coroutines.append(coroutine)
            
            if (global_added_commands is not None):
                while global_added_commands:
                    command = global_added_commands.pop()
                    
                    coroutine = self._create_command(client, command, global_command_state, SYNC_ID_GLOBAL)
                    if command_create_coroutines is None:
                        command_create_coroutines = []
                    command_create_coroutines.append(coroutine)
            
            while application_commands:
                application_command = application_commands.pop()
                
                coroutine = self._delete_command(client, None, None, SYNC_ID_GLOBAL, application_command)
                if command_delete_coroutines is None:
                    command_delete_coroutines = []
                command_delete_coroutines.append(coroutine)
            
            success = True
            for coroutines in (command_register_coroutines, command_delete_coroutines, command_edit_coroutines,
                    command_create_coroutines):
                if (coroutines is not None):
                    done, pending = await WaitTillAll([Task(coroutine, KOKORO) for coroutine in coroutines], KOKORO)
                    
                    for future in done:
                        if not future.result():
                            success = False
        
        finally:
            try:
                del self._sync_tasks[SYNC_ID_GLOBAL]
            except KeyError:
                pass
        
        if success:
            self._sync_should.discard(SYNC_ID_GLOBAL)
            self._sync_done.add(SYNC_ID_GLOBAL)
        
        return success
    
    async def _register_command(self, client, command, command_state, guild_id, application_command):
        """
        Finishes registering the command.
        
        This method is a coroutine.
        
        Attributes
        ----------
        client : ``Client``
            The respective client.
        command : ``SlashCommand``
            The non_global command what replaced the slash command.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was registered successfully.
        """
        if guild_id == SYNC_ID_GLOBAL:
            tasks = []
            for permission_guild_id in command._get_sync_permission_ids():
                task = Task(self._register_command_task(client, command, permission_guild_id, application_command),
                    KOKORO)
                task.append(task)
            
            if tasks:
                await WaitTillAll(tasks, KOKORO)
                
                success = True
                for future in tasks:
                    if not future.result():
                        success = False
                
                if not success:
                    return False
        else:
            await self._register_command_task(client, command, guild_id, application_command)
        
        self._register_helper(command, command_state, guild_id, application_command.id)
        return True
    
    async def _register_command_task(self, client, command, guild_id, application_command):
        """
        Syncs a command's permissions inside of a guild.
        
        This method is a coroutine.
        
        Attributes
        ----------
        client : ``Client``
            The respective client.
        command : ``SlashCommand``
            The non_global command what replaced the slash command.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was registered successfully.
        """
        success, permission = await self._get_permission_for(client, guild_id, application_command.id)
        if not success:
            return False
        
        overwrites = command.get_overwrites_for(guild_id)
        
        if permission is None:
            current_overwrites = None
        else:
            current_overwrites = permission.overwrites
        
        if overwrites != current_overwrites:
            try:
                permission = await client.application_command_permission_edit(guild_id, application_command, overwrites)
            except BaseException as err:
                if not isinstance(err, ConnectionError):
                    await client.events.error(client, f'{self!r}._register_command', err)
                return False
            
            try:
                per_guild = self._synced_permissions[guild_id]
            except KeyError:
                per_guild = self._synced_permissions[guild_id] = {}
            
            per_guild[permission.application_command_id] = permission
        
        return True
    
    async def _edit_guild_command_to_non_global(self, client, command, command_state, guild_id, application_command):
        """
        Edits the given guild command ot a non local one.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : ``SlashCommand``
            The non_global command what replaced the slash command.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            application_command = await client.application_command_guild_edit(guild_id, application_command,
                command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return False
            
            if isinstance(err, DiscordException) and (err.code == ERROR_CODES.unknown_application_command):
                # no command, no problem, lol
                return True
            
            await client.events.error(client, f'{self!r}._edit_guild_command_to_non_global', err)
            return False
        
        return await self._register_command(client, command, command_state, guild_id, application_command)
    
    async def _edit_command(self, client, command, command_state, guild_id, application_command):
        """
        Updates the given guild bound application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : ``SlashCommand``
            The slash command to update the application command to.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            schema = command.get_schema()
            if guild_id == SYNC_ID_GLOBAL:
                coroutine = client.application_command_global_edit(application_command, schema)
            else:
                coroutine = client.application_command_guild_edit(guild_id, application_command, schema)
            await coroutine
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                self._unregister_helper(command, command_state, guild_id)
                return await self._create_command(client, command, command_state, guild_id)
            
            await client.events.error(client, f'{self!r}._edit_command', err)
            return False
        
        return await self._register_command(client, command, command_state, guild_id, application_command)
    
    async def _delete_command(self, client, command, command_state, guild_id, application_command):
        """
        Deletes the given guild bound command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : `None` or ``SlashCommand``
            The slash command to delete.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was deleted successfully.
        """
        try:
            if guild_id == SYNC_ID_GLOBAL:
                coroutine = client.application_command_global_delete(application_command)
            else:
                coroutine = client.application_command_guild_delete(guild_id, application_command)
            await coroutine
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, ok, I guess.
                pass
            else:
                await client.events.error(client, f'{self!r}._delete_command', err)
                return False
        
        self._unregister_helper(command, command_state, guild_id)
        return True
    
    async def _create_command(self, client, command, command_state, guild_id):
        """
        Creates a given guild bound command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : `None` or ``SlashCommand``
            The slash command to create.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        
        Returns
        -------
        success : `bool`
            Whether the command was created successfully.
        """
        try:
            schema = command.get_schema()
            if guild_id == SYNC_ID_GLOBAL:
                coroutine = client.application_command_global_create(schema)
            else:
                coroutine = client.application_command_guild_create(guild_id, schema)
            application_command = await coroutine
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            await client.events.error(client, f'{self!r}._create_command', err)
            return False
        
        return await self._register_command(client, command, command_state, guild_id, application_command)
    
    def do_main_sync(self, client):
        """
        Syncs the slash commands with the client.
        
        The return of the method depends on the thread, from which it was called from.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        task : `bool`, ``Task`` or ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if syncing was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                ``FutureAsyncWrapper``. The task will return `True`, if syncing was successful.
            - If the method was called from any other thread, then waits for the syncing task to finish and returns
                `True`, if it was successful.
        """
        task = Task(self._do_main_sync(client), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(thread, EventThread):
            # `.async_wrap` wakes up KOKORO
            return task.async_wrap(thread)
        
        KOKORO.wake_up()
        return task.sync_wrap().wait()
    
    async def _do_main_sync(self, client):
        """
        Syncs the slash commands with the client. This method is the internal method of ``.do_main_sync``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the sync was successful.
        """
        if not self._sync_should:
            return True
        
        try:
            task = self._sync_tasks[SYNC_ID_MAIN]
        except KeyError:
            task = self._sync_tasks[SYNC_ID_MAIN] = Task(self._do_main_sync_task(client), KOKORO)
        
        return await task
    
    
    async def _do_main_sync_task(self, client):
        """
        Syncs the slash commands with the client. This method is the internal coroutine of the ``._do_main_sync``
        method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the sync was successful.
        """
        try:
            tasks = []
            for guild_id in self._sync_should:
                if guild_id == SYNC_ID_GLOBAL:
                    coro = self._sync_global(client)
                else:
                    coro = self._sync_guild(client, guild_id)
                
                task = Task(coro, KOKORO)
                tasks.append(task)
            
            if tasks:
                done, pending = await WaitTillAll(tasks, KOKORO)
                
                success = True
                for future in done:
                    if not future.result():
                        success = False
            else:
                success = True
            
            return success
        finally:
            try:
                del self._sync_tasks[SYNC_ID_MAIN]
            except KeyError:
                pass
    
    def _maybe_register_guild_command(self, application_command, guild_id):
        """
        Tries to register the given non-global application command to the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just added application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        try:
            non_global_command_state = self._command_states[SYNC_ID_NON_GLOBAL]
        except KeyError:
            return
        
        for command in non_global_command_state.get_should_add_commands():
            if command.get_schema() == application_command:
                self._register_helper(command, non_global_command_state, guild_id, application_command.id)
                break
    
    def _maybe_unregister_guild_command(self, application_command, guild_id):
        """
        Tries to unregister the given non-global application command from the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just deleted application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        try:
            non_global_command_state = self._command_states[SYNC_ID_NON_GLOBAL]
        except KeyError:
            return
        
        for command in non_global_command_state.get_should_add_commands():
            if command.get_schema() == application_command:
                self._unregister_helper(command, non_global_command_state, guild_id)
                break
    
    def __repr__(self):
        """Returns the slasher's representation."""
        return f'<{self.__class__.__name__} sync_should={len(self._sync_should)}, sync_done={len(self._sync_done)}>'
    
    def _get_delete_commands_on_unload(self):
        command_unloading_behaviour = self._command_unloading_behaviour
        if command_unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
            delete_commands_on_unload = True
        else:
            delete_commands_on_unload = False
        
        return delete_commands_on_unload
    
    def _set_delete_commands_on_unload(self, delete_commands_on_unload):
        if type(delete_commands_on_unload) is bool:
            pass
        elif isinstance(delete_commands_on_unload, bool):
            delete_commands_on_unload = bool(delete_commands_on_unload)
        else:
            raise TypeError(f'`delete_commands_on_unload` can be given as `bool` instance, got '
                f'{delete_commands_on_unload.__class__.__name__}.')
        
        if delete_commands_on_unload:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        self._command_unloading_behaviour = command_unloading_behaviour
    
    delete_commands_on_unload = property(_get_delete_commands_on_unload, _set_delete_commands_on_unload)
    del _get_delete_commands_on_unload, _set_delete_commands_on_unload
    if DOCS_ENABLED:
        delete_commands_on_unload.__doc__ = ("""
        A get-set property for changing the slasher's command unloading behaviour.
        
        Accepts and returns any `bool` instance.
        """)
    
    def _maybe_store_application_command_permission(self, permission):
        """
        Stores an application command's new permissions if needed.
        
        Parameters
        ----------
        permission : ``ApplicationCommandPermission``
            The updated application command's permissions.
        """
        try:
            tracked_guild = self._synced_permissions[permission.guild_id]
        except KeyError:
            return
        
        tracked_guild[permission.application_command_id] = permission
    
    async def _get_permission_for(self, client, guild_id, application_command_id):
        """
        Gets the permissions for the given application command in the the respective guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command_id : `int`
            The respective application command's identifier.
        """
        try:
            per_guild = self._synced_permissions[guild_id]
        except KeyError:
            pass
        else:
            return True, per_guild.get(application_command_id)
        
        try:
            sync_permission_task = self._sync_permission_tasks[guild_id]
        except KeyError:
            sync_permission_task = Task(self._sync_permission_task(client, guild_id), KOKORO)
            self._sync_permission_tasks[guild_id] = sync_permission_task
        
        success, per_guild = await sync_permission_task
        if success:
            permission = per_guild.get(application_command_id)
        else:
            permission = None
        
        return success, permission
    
    async def _sync_permission_task(self, client, guild_id):
        """
        Syncs the respective guild's permissions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        per_guild : `None` or `dict` of (`int`, ``ApplicationCommandPermission``) items
            The application command permission for the respective guild. If `success` is `False, this value is
            returned as `None`.
        """
        try:
            try:
                permissions = await client.application_command_permission_get_all_guild(guild_id)
            except BaseException as err:
                if not isinstance(err, ConnectionError):
                    await client.events.error(client, f'{self!r}._sync_permission_task', err)
                
                return False, None
            else:
                try:
                    per_guild = self._synced_permissions[guild_id]
                except KeyError:
                    per_guild = self._synced_permissions[guild_id] = {}
                
                for permission in permissions:
                    per_guild[permission.application_command_id] = permission
                
                return True, per_guild
        finally:
            try:
                del self._sync_permission_tasks[guild_id]
            except KeyError:
                pass
