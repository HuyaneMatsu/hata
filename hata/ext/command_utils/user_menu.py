__all__ = ('UserMenuFactory', 'UserMenuRunner', 'UserPagination',)

from scarletio import CallableAnalyzer, CancelledError, copy_docs

from ...discord import Channel
from ...discord.core import BUILTIN_EMOJIS
from ...discord.emoji import Emoji
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.interaction import InteractionEvent
from ...discord.message import Message
from ...discord.preconverters import preconvert_bool

from .bases import (
    GUI_STATE_CANCELLED, GUI_STATE_CANCELLING, GUI_STATE_READY, GUI_STATE_SWITCHING_CTX, GUI_STATE_SWITCHING_PAGE,
    GUI_STATE_VALUE_TO_NAME, PaginationBase
)
from .utils import Timeouter


def validate_check(check):
    """
    Validates the given check.
    
    Parameters
    ----------
    check : `None` of `callable`
        The check to validate.
    
    Raises
    ------
    TypeError
        If `check` is not `None` neither a non-async function accepting 1 parameter.
    """
    if check is None:
        return
    
    analyzer = CallableAnalyzer(check, as_method=True)
    if analyzer.is_async():
        raise TypeError(
            f'`check` should have NOT be be `async` function, got {check!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(
            f'`check` should accept `1` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {check!r}.'
        )
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`check` should accept `1` parameters, meanwhile the given one expects '
                    f'up to `{max_!r}`, got `{check!r}`.'
                )


def validate_invoke(invoke):
    """
    Validates the given invoker.
    
    Parameters
    ----------
    invoke : `callable`
        The invoker to validate.
    
    Raises
    ------
    TypeError
        If `invoke` is not async callable or accepts not 1 parameter.
    """
    if invoke is None:
        raise TypeError(
            f'`invoke` function cannot be `None`.'
        )
    
    analyzer = CallableAnalyzer(invoke, as_method=True)
    if not analyzer.is_async():
        raise TypeError(
            f'`invoke` can be `CoroutineFunction`, got {invoke!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(
            f'`invoke` should accept `1` parameter, meanwhile the given one expects at '
            f'least `{min_!r}`, got {invoke!r}.'
        )
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`invoke` should accept `1` parameters, meanwhile the given one expects '
                    f'up to `{max_!r}`, got {invoke!r}.'
                )


def validate_initial_invoke(initial_invoke):
    """
    Validates the given default content getter.
    
    Parameters
    ----------
    initial_invoke : `callable`
        The default content getter to validate.
    
    Raises
    ------
    TypeError
        If `initial_invoke` is not async callable or accepts any parameters.
    """
    if initial_invoke is None:
        raise TypeError(
            f'`initial_invoke` function cannot be `None`.'
        )
    
    analyzer = CallableAnalyzer(initial_invoke, as_method=True)
    if not analyzer.is_async():
        raise TypeError(
            f'`initial_invoke` should have be `async` function, got {initial_invoke!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 0:
        raise TypeError(
            f'`initial_invoke` should accept `0` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {initial_invoke!r}.'
        )
    
    if min_ != 0:
        if max_ < 0:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`initial_invoke` should accept `0` parameters, meanwhile the given one '
                    f'expects up to `{max_!r}`, got {initial_invoke!r}.'
                )


def validate_close(close):
    """
    Validates the given closer.
    
    Parameters
    ----------
    close : `callable`
        The closer to validate.
    
    Raises
    ------
    TypeError
        If `close` is not async callable or accepts not 1 parameter.
    """
    if close is None:
        raise TypeError(
            f'`close` function cannot be `None`.'
        )
    
    analyzer = CallableAnalyzer(close, as_method=True)
    if not analyzer.is_async():
        raise TypeError(
            f'`close` should have be `async` function, got {close!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(
            f'`close` should accept `1` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {close!r}.'
        )
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`close` should accept `1` parameters, meanwhile the given one expects '
                    f'up to `{max_!r}`, got {close!r}.'
                )


class UserMenuFactory:
    """
    Attributes
    ----------
    allow_third_party_emojis : `bool`
        Whether the runner should pick up 3rd party emojis, listed outside of `emojis`.
    
    check : `None`, `function`
        The function to call when checking whether an event should be called.
        
        Should accept the following parameters:
        
        +-----------+---------------------------------------------------+
        | Name      | Type                                              |
        +===========+===================================================+
        | event     | ``ReactionAddEvent``, ``ReactionDeleteEvent``     |
        +-----------+---------------------------------------------------+
        
        > ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    close : `None`, `async-function`
        Function to call when the pagination is closed.
        
        Should accept the following parameters:
        
        +-----------+---------------------------+
        | Name      | Type                      |
        +===========+===========================+
        | exception | `None`, `BaseException`   |
        +-----------+---------------------------+
    
    close_emoji : `None`, ``Emoji``
        The emoji which triggers closing.
    
    emojis : `None`, `tuple` of ``Emoji``
        The emojis to add on the message.
    
    initial_invoke : `async-function`
        Function to generate the default page of the menu.
        
        Should accept no parameters and return the following:
        
        +-----------+-----------------------------------+
        | Name      | Type                              |
        +===========+===================================+
        | response  | `None`, `str`, ``Embed``          |
        +-----------+-----------------------------------+
    
    invoke : `async-function`
        The function call for result when invoking the menu.
        
        Should accept the following parameters:
        
        +-----------+---------------------------------------------------+
        | Name      | Type                                              |
        +===========+===================================================+
        | event     | ``ReactionAddEvent``, ``ReactionDeleteEvent``     |
        +-----------+---------------------------------------------------+
        
        > ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        
        +-----------+-----------------------------------+
        | Name      | Type                              |
        +===========+===================================+
        | response  | `None`, `str`, ``Embed``          |
        +-----------+-----------------------------------+
    
    klass : `type`
        The factory class.
    
    timeout : `float`
        The time after the menu should be closed.
        
        > Define it as non-positive to never timeout. Not recommended.
    """
    __slots__ = (
        'allow_third_party_emojis', 'check', 'close', 'close_emoji', 'emojis', 'initial_invoke', 'invoke',
        'klass', 'timeout'
    )
    
    def __new__(cls, klass):
        """
        Parameters
        ----------
        klass : `type`
            The type to create factory from.
        
        Raises
        ------
        TypeError
            - If `klass` was not given as `type`.
            - If `klass.check` is not `None` neither a non-async function accepting 1 parameter.
            - If `invoke` is not async callable or accepts not 1 parameter.
            - If `close_emoji` is neither `None`, ``Emoji``.
            - If `emojis` is neither `None` nor `tuple`, `list`.
            - If `emojis` contains a non ``Emoji`` element.
            - If `initial_invoke` is not async callable or accepts any parameters.
            - If `timeout` is not convertible to float.
            - If `closed` is neither `None` nor `async-callable`.
            - If `allow_third_party_emojis` was not given as `bool`.
        ValueError
            - If `emojis` length is over 20.
        """
        if not isinstance(klass, type):
            raise TypeError(
                f'`klass` can be `type`, got {klass.__class__.__name__}; {klass!r}.'
            )
        
        check = getattr(klass, 'check', None)
        validate_check(check)
        
        invoke = getattr(klass, 'invoke', None)
        validate_invoke(invoke)
        
        close_emoji = getattr(klass, 'close_emoji', None)
        if (close_emoji is not None) and (not isinstance(close_emoji, Emoji)):
            raise TypeError(
                f'`close_emoji can be `None`, `{Emoji.__name__}`, got '
                f'{close_emoji.__class__.__name__}; {close_emoji!r}'
            )
            
        emojis = getattr(klass, 'emojis', None)
        if (emojis is not None):
            if not isinstance(emojis, (tuple, list)):
                raise TypeError(
                    f'`emojis` can be `None`, `list`, `tuple`, got '
                    f'{emojis.__class__.__name__}; {emojis!r}.'
                )
            
            # Making sure
            emojis = tuple(emojis)
            for emoji in emojis:
                if not isinstance(emoji, Emoji):
                    raise TypeError(
                        f'`emojis` can contain `{Emoji.__name__}` elements, got '
                        f'{emoji.__class__.__name__}; {emoji!r}; emojis={emojis!r}.'
                    )
            
            emojis_length = len(emojis)
            if emojis_length == 0:
                emojis = None
            
            elif emojis_length > 20:
                raise ValueError(
                    f'`emojis` can contain up to `20` emojis, got {emojis_length!r}; {emojis!r}.'
                )
        
        initial_invoke = getattr(klass, 'initial_invoke', None)
        validate_initial_invoke(initial_invoke)
        
        timeout = getattr(klass, 'timeout', None)
        if timeout is None:
            timeout = -1.0
        else:
            try:
                timeout = float(timeout)
            except (TypeError, ValueError) as err:
                raise TypeError(
                    f'`timeout` cannot be converted to `float`, got {timeout.__class__.__mame__}; {timeout!r}'
                ) from err
        
        close = getattr(klass, 'close', None)
        validate_close(close)
        
        allow_third_party_emojis = getattr(klass, 'allow_third_party_emojis', None)
        if (allow_third_party_emojis is None):
            allow_third_party_emojis = False
        else:
            allow_third_party_emojis = preconvert_bool(allow_third_party_emojis, 'allow_third_party_emojis')
        
        self = object.__new__(cls)
        self.klass = klass
        self.check = check
        self.close_emoji =close_emoji
        self.emojis = emojis
        self.initial_invoke = initial_invoke
        self.invoke = invoke
        self.timeout = timeout
        self.close = close
        self.allow_third_party_emojis = allow_third_party_emojis
        
        return self
    
    
    def __repr__(self):
        """Returns the user menu factory's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' klass=',
            self.klass.__name__,
        ]
        emojis = self.emojis
        if (emojis is not None):
            repr_parts.append(', emojis=(')
            index = 0
            limit = len(emojis)
            while True:
                emoji = emojis[index]
                repr_parts.append(emoji.name)
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append(')')
            
        close_emoji = self.close_emoji
        if (close_emoji is not None):
            repr_parts.append(', close_emoji=')
            repr_parts.append(close_emoji.name)
        
        allow_third_party_emojis = self.allow_third_party_emojis
        if allow_third_party_emojis:
            repr_parts.append(', allow_third_party_emojis=')
            repr_parts.append(repr(allow_third_party_emojis))
        
        timeout = self.timeout
        if timeout > 0.0:
            repr_parts.append(', timeout=')
            repr_parts.append(repr(timeout))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    async def __call__(self, client, channel, *args, **kwargs):
        """
        Instances the factory creating an ``UserMenuRunner``.
        
        This method is a coroutine.
        
        Returns
        -------
        user_menu_runner : ``UserMenuRunner``
        """
        return await UserMenuRunner(self, client, channel, *args, **kwargs)


class UserMenuRunner(PaginationBase):
    """
    Menu factory runner.
    
    Parameters
    ----------
    _canceller : `None`, `function`
        The function called when the ``UserMenuRunner`` is cancelled or when it expires. This is a onetime use and
        after it was used, is set as `None`.
    
    _task_flag : `int`
        A flag to store the state of the ``UserMenuRunner``.
        
        Possible values:
        +---------------------------+-------+-----------------------------------------------------------------------+
        | Respective name           | Value | Description                                                           |
        +===========================+=======+=======================================================================+
        | GUI_STATE_READY           | 0     | The Pagination does nothing, is ready to be used.                     |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_PAGE  | 1     | The Pagination is currently changing it's page.                       |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLING      | 2     | The pagination is currently changing it's page, but it was cancelled  |
        |                           |       | meanwhile.                                                            |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLED       | 3     | The pagination is, or is being cancelled right now.                   |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_CTX   | 4     | The Pagination is switching context. Not used by the default class,   |
        |                           |       | but expected.                                                         |
        +---------------------------+-------+-----------------------------------------------------------------------+
    
    _timeouter : `None`, ``Timeouter``
        Executes the timing out feature on the ``UserMenuRunner``.
    
    channel : ``Channel``
        The channel where the ``UserMenuRunner`` is executed.
    
    client : ``Client``
        The client who executes the ``UserMenuRunner``.
    
    message : `None`, ``Message``
        The message on what the ``UserMenuRunner`` is executed.
    
    _factory : ``UserMenuFactory``
        The factory of the menu containing it's details.
    
    _instance : `None`, `object`
        The respective ``UserMenuFactory``'s class instanced.
    """
    __slots__ = ('_factory', '_instance',)
    
    async def __new__(cls, factory, client, channel, *args, message = None, **kwargs):
        """
        Creates a new user menu runner instance with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        factory : ``UserMenuFactory``
            The respective user menu factory to execute.
        client : ``Client``
            The client who executes the ``UserMenuRunner``.
        channel : ``Channel``
            The channel where the ``UserMenuRunner`` is executed.
        *args : Parameters
            Additional parameters to pass to the factory's class's constructor.
        message : `None`, ``Message`` = `None`, Optional (Keyword Only)
            The message to use instead of creating a new one.
        **kwargs : Keyword parameters
            Additional keyword parameters to pass to the factory's class's constructor.
        
        Raises
        ------
        TypeError
            `channel`'s type is incorrect.
        """
        if isinstance(channel, Channel):
            target_channel = channel
            received_interaction = False
        elif isinstance(channel, Message):
            target_channel = channel.channel
            received_interaction = False
        elif isinstance(channel, InteractionEvent):
            target_channel = channel.channel
            received_interaction = True
        else:
            raise TypeError(
                f'`channel` can be `{Channel.__name__}`, `{Message.__name__}`, `{InteractionEvent.__name__}`, '
                f'got {channel.__class__.__name__}; {channel!r}.'
            )
        
        self = object.__new__(cls)
        self.client = client
        self.channel = target_channel
        self._canceller = cls._canceller_function
        self._task_flag = GUI_STATE_READY
        self.message = message
        self._factory = factory
        self._instance = None
        self._timeouter = None
        
        instance = factory.klass(self, *args, **kwargs)
        self._instance = instance
        
        default_content = await factory.initial_invoke(instance)
        
        # Leave if nothing to do.
        if default_content is None:
            self._task_flag = GUI_STATE_CANCELLED
            self._canceller = None
            return self
        
        try:
            if message is None:
                if received_interaction:
                    if not channel.is_acknowledged():
                        await client.interaction_response_message_create(channel)
                    
                    message = await client.interaction_followup_message_create(channel, default_content)
                else:
                    message = await client.message_create(channel, default_content)
                self.message = message
            else:
                await client.message_edit(message, default_content)
        except BaseException as err:
            self.cancel(err)
            if isinstance(err, GeneratorExit):
                raise
            
            if isinstance(err, ConnectionError):
                return self
            
            if isinstance(err, DiscordException):
                if err.code in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                ):
                    return self
            
            raise
        
        if self._task_flag in (GUI_STATE_CANCELLED, GUI_STATE_SWITCHING_CTX):
            self.cancel(None)
            return self
        
        emojis = factory.emojis
        if (emojis is not None):
            if not target_channel.cached_permissions_for(client).can_add_reactions:
                await self.cancel(PermissionError())
                return self
            
            try:
                for emoji in emojis:
                    await client.reaction_add(message, emoji)
            except BaseException as err:
                self.cancel(err)
                if isinstance(err, GeneratorExit):
                    raise
                
                if isinstance(err, ConnectionError):
                    return self
                
                if isinstance(err, DiscordException):
                    if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ):
                        return self
                
                raise
        
        timeout = factory.timeout
        if timeout >= 0.0:
            timeouter = Timeouter(self, timeout)
        else:
            timeouter = None
        self._timeouter = timeouter
        
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        
        return self
    
    
    @copy_docs(PaginationBase.__call__)
    async def __call__(self, client, event):
        if event.user.bot:
            return
        
        emojis = self._factory.emojis
        if (emojis is None) or (event.emoji not in emojis):
            if not self._factory.allow_third_party_emojis:
                return
        else:
            if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
                return
        
        check = self._factory.check
        if (check is not None):
            try:
                should_process = check(self._instance, event)
            except BaseException as err:
                await client.events.error(client, f'{self!r}.__call__', err)
                return
            
            if not should_process:
                return
        
        task_flag = self._task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if event.emoji is self._factory.close_emoji:
                    self._task_flag = GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        try:
            content = await self._factory.invoke(self._instance, event)
        except GeneratorExit as err:
            self.cancel(err)
            raise
        
        except BaseException as err:
            self.cancel(err)
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if content is None:
            return
        
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(self.message, content)
        except BaseException as err:
            self.cancel(err)
            
            if isinstance(err, GeneratorExit):
                raise
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                    ERROR_CODES.unknown_message, # message already deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if self._task_flag == GUI_STATE_CANCELLING:
            self.cancel(CancelledError())
            return
        
        self._task_flag = GUI_STATE_READY
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.set_timeout(self._factory.timeout)
    
    @copy_docs(PaginationBase._handle_close_exception)
    async def _handle_close_exception(self, exception):
        close = self._factory.close
        if (close is not None):
            try:
                await close(self._instance, exception)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                client = self.client
                await client.events.error(client, f'{self!r}.handle_close_exception', err)
        
        return True
    
    
    @copy_docs(PaginationBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<', self.__class__.__name__,
            ' client=', repr(self.client),
            ', channel = ', repr(self.channel),
            ', state='
        ]
        
        task_flag = self._task_flag
        repr_parts.append(repr(task_flag))
        repr_parts.append(' (')
        
        task_flag_name = GUI_STATE_VALUE_TO_NAME[task_flag]
        
        repr_parts.append(task_flag_name)
        repr_parts.append(')')
        
        # Third party things go here
        repr_parts.append(', factory=')
        repr_parts.append(repr(self._factory))
        repr_parts.append(', instance=')
        repr_parts.append(repr(self._instance))
        
        repr_parts.append('>')
        return ''.join(repr_parts)



class UserPagination:
    """
    Base factorisable instance to execute pagination.
    
    Attributes
    ----------
    menu : ``UserMenuRunner``
        The menu runner running the pagination.
    page_index : `int`
        The current page's index.
    pages : `indexable`
        An indexable container, what stores the displayable contents.
    
    Class Attributes
    ----------------
    left2 : ``Emoji`` = `BUILTIN_EMOJIS['track_previous']`
        The emoji used to move to the first page.
    left : ``Emoji`` = `BUILTIN_EMOJIS['arrow_backward']`
        The emoji used to move to the previous page.
    right : ``Emoji`` = `BUILTIN_EMOJIS['arrow_forward']`
        The emoji used to move on the next page.
    right2 : ``Emoji`` = `BUILTIN_EMOJIS['track_next']`
        The emoji used to move on the last page.
    close_emoji : ``Emoji`` = `BUILTIN_EMOJIS['x']`
        The emoji used to cancel the ``Pagination``.
    emojis : `tuple` (`Emoji`, `Emoji`, `Emoji`, `Emoji`, `Emoji`) = `(left2, left, right, right2, close_emoji,)`
        The emojis to add on the respective message in order.
    timeout : `float`
        The pagination's timeout.
    """
    left2 = BUILTIN_EMOJIS['track_previous']
    left = BUILTIN_EMOJIS['arrow_backward']
    right = BUILTIN_EMOJIS['arrow_forward']
    right2 = BUILTIN_EMOJIS['track_next']
    close_emoji = BUILTIN_EMOJIS['x']
    emojis = (left2, left, right, right2, close_emoji,)
    
    timeout = 240.0
    
    __slots__ = ('menu', 'page_index', 'pages')
    
    def __init__(self, menu, pages):
        """
        Creates a new ``UserMenuRunner`` with the given parameters.
        
        Parameters
        ----------
        menu : ``UserMenuRunner``
            The respective runner which executes the pagination.
        pages : `indexable-container`
            An indexable container, what stores the displayable pages.
        """
        self.menu = menu
        self.pages = pages
        self.page_index = 0
    
    
    async def initial_invoke(self):
        """
        Called initially
        
        This method is a coroutine.
        
        Returns
        -------
        page : `None`, `object`
            The page to kick-off the pagination with.
        """
        pages = self.pages
        pages_length = len(pages)
        if pages_length == 0:
            return None
        
        page = pages[0]
        if pages_length == 1:
            self.menu.cancel()
        
        return page
    
    
    async def invoke(self, event):
        """
        An emoji addition or deletion invoked the pagination.
        
        Parameters
        ----------
        event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
            The received event.
        """
        emoji = event.emoji
        
        if emoji is self.left2:
            page_index = 0
        elif emoji is self.left:
            page_index = self.page_index - 1
            if page_index < 0:
                page_index = 0
        elif emoji is self.right:
            page_index = self.page_index + 1
            if page_index >= len(self.pages):
                page_index = len(self.pages) - 1
        elif emoji is self.right2:
            page_index = len(self.pages) - 1
        else:
            return
        
        if page_index == self.page_index:
            return
        
        self.page_index = page_index
        return self.pages[page_index]
    
    
    async def close(self, exception):
        """
        Closes the pagination.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None`, ``BaseException``
            - `CancelledError` if closed with the close emoji.
            - `TimeoutError` if closed by timeout.
            - `PermissionError` if closed because cant add reactions.
            - object other value is other exception received runtime.
        """
        client = self.menu.client
        if exception is None:
            return
        
        if isinstance(exception, CancelledError):
            try:
                await client.message_delete(self.menu.message)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_access, # client removed
                    ):
                        return
                
                await client.events.error(client, f'{self!r}.close', err)
            
            return
        
        if isinstance(exception, TimeoutError):
            if self.menu.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(self.menu.message)
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ):
                            return
            
                    await client.events.error(client, f'{self!r}.close', exception)
            
            return
        
        if isinstance(exception, PermissionError):
            return
        
        await client.events.error(client, f'{self!r}.close', exception)
        return
