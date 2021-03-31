# -*- coding: utf-8 -*-
__all__ = ('ChooseMenu', )

from ...backend.futures import Task
from ...discord.client_core import KOKORO
from ...discord.emoji import BUILTIN_EMOJIS
from ...discord.parsers import InteractionEvent
from ...discord.message import Message
from ...discord.channel import ChannelTextBase
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.embed import Embed

from .utils import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, \
    GUI_STATE_SWITCHING_CTX, Timeouter


class ChooseMenu:
    """
    Familiar to ``Pagination``, but instead of just displaying multiple pages of text, it allows the user to select
    a displayed option.
    
    The class allows modifications and closing it's representations for every user. Also works at private channels.
    
    Picks up on reaction additions and on reaction deletions as well and removes the added reactions on if has
    permission, which might be missing, like in DM-s.
    
    Attributes
    ----------
    canceller : `None` or `function`
        The function called when the ``ChooseMenu`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    channel : ``ChannelTextBase`` instance
        The channel where the ``ChooseMenu`` is executed.
    check : `None` or `callable`
        A callable what decides whether the ``ChooseMenu`` should process a received reaction event. Defaults to
        `None`.
        
        Should accept the following parameters:
        +-----------+---------------------------------------------------+
        | Name      | Type                                              |
        +===========+===================================================+
        | event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |
        +-----------+---------------------------------------------------+
        
        Note, that ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    client : ``Client``
        The client who executes the ``ChooseMenu``.
    embed : ``EmbedBase`` instance
        An embed base, what's description and footer will be rendered with the given choices and with information
        about the respective page.
    message : `None` or ``Message``
        The message on what the ``ChooseMenu`` is executed.
    selected : `int`
        The currently selected option of the ``ChooseMenu``.
    choices : `indexable` of `Any`
        An indexable container, what stores the displayable choices.
        
        It's elements's type can be different from each other, and different structures act differently as well.
        There are the following cases:
        
        - If an element is `str` instance, then it will be used as an option's title and when selecting it, only that
            variable will be passed to the respective function when selected.
        
        - If an element is neither `str` or `tuple`, then it's `repr` will be used as an option's title, and only that
            variable will be passed to the respective function when selected.
        
        - If an element is `tuple` instance, then it's first element will be displayed as title. If it is `str`, then
            will be just simply added, however if not, then it's `repr` will be used. If selecting a `tuple` option,
            then it's element will be passed to the respective function.
    
    task_flag : `int`
        A flag to store the state of the ``ChooseMenu``.
        
        Possible values:
        +---------------------------+-------+-----------------------------------------------------------------------+
        | Respective name           | Value | Description                                                           |
        +===========================+=======+=======================================================================+
        | GUI_STATE_READY           | 0     | The ChooseMenu does nothing, is ready to be used.                     |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_PAGE  | 1     | The ChooseMenu is currently changing it's page.                       |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLING      | 2     | The ChooseMenu is currently changing it's page, but it was cancelled  |
        |                           |       | meanwhile.                                                            |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLED       | 3     | The ChooseMenu is, or is being cancelled right now.                   |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_CTX   | 4     | The ChooseMenu is switching context. Not used by the default class,   |
        |                           |       | but expected.                                                         |
        +---------------------------+-------+-----------------------------------------------------------------------+
    timeout : `float`
        The timeout of the ``ChooseMenu`` in seconds.
    timeouter : `None` or ``Timeouter``
        Executes the timing out feature on the ``ChooseMenu``.
    prefix : `None` or `str`
        A prefix displayed before each option.
    selector : `async-callable`
        An `async-callable`, what is ensured when an option is selected.
        
        If the ``ChooseMenu`` is created only with `1` option, then it is ensured initially instead of creating the
        ``ChooseMenu`` itself. At this case, if `message` was not given (or given as `None`), then the `message`
        passed to the `selector` will be `None` as well.
        
        At least 3 parameters are passed to the `selector`:
        +-------------------+-------------------------------+
        | Respective name   | Type                          |
        +===================+===============================+
        | client            | ``Client``                    |
        +-------------------+-------------------------------+
        | channel           | ``ChannelTextBase`` instance  |
        +-------------------+-------------------------------+
        | message           | ``Message`` or `None`         |
        +-------------------+-------------------------------+
        
        The rest of the parameters depend on the respective choice (an elements of ``choices``). If the element is a
        `tuple` instance, then it's element will be passed, however if the choice is any other type, then only that
        object will be passed.
    
    Class Attributes
    ----------------
    UP : ``Emoji`` = `BUILTIN_EMOJIS['arrow_up_small']`
        The emoji used to move on the displayed option one above.
    DOWN : ``Emoji`` = `BUILTIN_EMOJIS['arrow_down_small']`
        The emoji used to move on the displayed option one under.
    LEFT : ``Emoji`` = `BUILTIN_EMOJIS['arrow_backward']`
        The emoji used to move on the previous page.
    RIGHT : ``Emoji`` = `BUILTIN_EMOJIS['arrow_forward']`
        The emoji used to move on the next page.
    SELECT : ``Emoji`` = `BUILTIN_EMOJIS['ok']`
        The emoji used to select an option.
    CANCEL : ``Emoji`` = `BUILTIN_EMOJIS['x']`
        The emoji used to cancel the ``ChooseMenu``.
    EMOJIS_RESTRICTED : `tuple` (`Emoji`, `Emoji`, `Emoji`, `Emoji`) = `(UP, DOWN, SELECT, CANCEL)`
        Restricted emojis, added when the choose menu has only options for 1 page.
    EMOJIS : `tuple` (`Emoji`, `Emoji`, `Emoji`, `Emoji`, `Emoji`, `Emoji`) = `(UP, DOWN, LEFT, RIGHT, SELECT, CANCEL)`
        Emojis added to the choose menu.
    """
    UP     = BUILTIN_EMOJIS['arrow_up_small']
    DOWN   = BUILTIN_EMOJIS['arrow_down_small']
    LEFT   = BUILTIN_EMOJIS['arrow_backward']
    RIGHT  = BUILTIN_EMOJIS['arrow_forward']
    SELECT = BUILTIN_EMOJIS['ok']
    CANCEL = BUILTIN_EMOJIS['x']
    EMOJIS_RESTRICTED = (UP, DOWN, SELECT, CANCEL)
    EMOJIS = (UP, DOWN, LEFT, RIGHT, SELECT, CANCEL)
    
    __slots__ = ('canceller', 'channel', 'check', 'client', 'embed', 'message', 'selected', 'choices', 'task_flag',
        'timeout', 'timeouter', 'prefix', 'selector')
    
    async def __new__(cls, client, channel, choices, selector, embed=Embed(), timeout=240., message=None, prefix=None,
            check=None):
        """
        Creates a new choose menu with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who executes the ``ChooseMenu``.
        channel : ``ChannelTextBase`` instance or ``Message``
            The channel where the ``ChooseMenu`` is executed. Pass it as a ``Message`` instance to send a reply.
            
            If given as ``InteractionEvent``, then will acknowledge it and create a new message with it as well.
            Although will not acknowledge it if `message` is given.
        
        choices : `indexable` of `Any`
            An indexable container, what stores the displayable choices.
            
            It's elements's type can be different from each other, and different structures act differently as well.
            There are the following cases:
            
            - If an element is `str` instance, then it will be used as an option's title and when selecting it, only
                that variable will be passed to the respective function when selected.
            
            - If an element is neither `str` or `tuple`, then it's `repr` will be used as an option's title, and only
                that variable will be passed to the respective function when selected.
            
            - If an element is `tuple` instance, then it's first element will be displayed as title. If it is `str`,
                then will be just simply added, however if not, then it's `repr` will be used. If selecting a `tuple`
                option, then it's element will be passed to the respective function.
        selector : `async-callable`
            An `async-callable`, what is ensured when an option is selected.
            
            If the ``ChooseMenu`` is created only with `1` option, then it is ensured initially instead of creating
            the ``ChooseMenu`` itself. At this case, if `message` was not given (or given as `None`), then the
            `message` passed to the `selector` will be `None` as well.
            
            At least 3 parameters are passed to the `selector`:
            +-------------------+-----------------------------------------------------------+
            | Respective name   | Type                                                      |
            +===================+===========================================================+
            | client            | ``Client``                                                |
            +-------------------+-----------------------------------------------------------+
            | channel           | ``ChannelTextBase``, ``Message`` or ``InteractionEvent``  |
            +-------------------+-----------------------------------------------------------+
            | message           | ``Message`` or `None`                                     |
            +-------------------+-----------------------------------------------------------+
            
            The rest of the parameters depend on the respective choice (an elements of ``choices``). If the element is a
            `tuple` instance, then it's element will be passed, however if the choice is any other type, then only that
            object will be passed.
        embed : ``Embed`` (or any compatible)
            An embed base, what's description and footer will be rendered with the given choices and with information
            about the respective page. Defaults to an empty ``Embed`` instance.
        timeout : `float`, Optional
            The timeout of the ``ChooseMenu`` in seconds. Defaults to `240.0`.
        message : `None` or ``Message``, Optional
            The message on what the ``ChooseMenu`` will be executed. If not given a new message will be created.
            Defaults to `None`.
        prefix : `None` or `str`, Optional
            A prefix displayed before each option. Defaults to `None`.
        check : `None` or `callable`, Optional
            A callable what decides whether the ``ChooseMenu`` should process a received reaction event. Defaults to
            `None`.
            
            Should accept the following parameters:
            +-----------+---------------------------------------------------+
            | Name      | Type                                              |
            +===========+===================================================+
            | event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |
            +-----------+---------------------------------------------------+
            
            Note, that ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
            
            Should return the following values:
            +-------------------+-----------+
            | Name              | Type      |
            +===================+===========+
            | should_process    | `bool`    |
            +-------------------+-----------+
            
        Returns
        -------
        self : `None` or ``ChooseMenu``
            If `choices`'s length is less than `2`, then returns `None`.
        
        Raises
        ------
        TypeError
            `channel`'s type is incorrect.
        ValueError
            If `prefix` was not given as `None` and it's length is over `64` characters.
        """
        if (prefix is not None) and (len(prefix) > 100):
            raise ValueError(f'Please pass a prefix, what is shorter than 100 characters, got {prefix!r}.')
        
        if isinstance(channel, ChannelTextBase):
            target_channel = channel
            received_interaction = False
        elif isinstance(channel, Message):
            target_channel = channel.channel
            received_interaction = False
        elif isinstance(channel, InteractionEvent):
            target_channel = channel.channel
            received_interaction = True
        else:
            raise TypeError(f'`channel` can be given only as `{ChannelTextBase.__name__}`, `{Message.__name__}` '
                f'of as {InteractionEvent.__name__} instance, got {channel.__class__.__name__}.')
        
        result_ln = len(choices)
        if result_ln < 2:
            if result_ln == 1:
                choice = choices[0]
                if isinstance(choice, tuple):
                    coro = selector(client, channel, message, *choice)
                else:
                    coro = selector(client, channel, message, choice)
                await coro
            return None
        
        self = object.__new__(cls)
        self.check = check
        self.client = client
        self.channel = target_channel
        self.choices = choices
        self.selector = selector
        self.selected = 0
        self.canceller = cls._canceller
        self.task_flag = GUI_STATE_READY
        self.message = message
        self.timeout = timeout
        self.timeouter = None
        self.prefix = prefix
        self.embed = embed
        
        try:
            if message is None:
                if received_interaction:
                    if not channel.is_acknowledged():
                        await client.interaction_response_message_create(channel)
                    
                    message = await client.interaction_followup_message_create(channel, embed=self._render_embed())
                else:
                    message = await client.message_create(channel, embed=self._render_embed())
                self.message = message
            else:
                await client.message_edit(message, embed=self._render_embed())
            
            if not target_channel.cached_permissions_for(client).can_add_reactions:
                return self
            
            for emoji in (self.EMOJIS if (len(choices) > 10) else self.EMOJIS_RESTRICTED):
                await client.reaction_add(message, emoji)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return self
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                            ):
                    return self
            
            raise
        
        self.timeouter = Timeouter(self, timeout=timeout)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    def _render_embed(self):
        """
        Renders the choose menu's embed's description with it's choices of the respective page and it's footer
        with page information.
        
        Returns
        -------
        embed : ``Embed`` (or any compatible)
            The rendered embed.
        """
        selected = self.selected
        choices = self.choices
        index = (selected//10)*10
        end = index+10
        if len(choices) < end:
            end = len(choices)
        
        parts = []
        prefix = self.prefix
        left_length = 195
        if (prefix is not None):
            left_length -= len(prefix)
        
        while True:
            title = choices[index]
            if isinstance(title,tuple):
                if not title:
                    title = ''
                else:
                    title = title[0]
            
            if not isinstance(title,str):
                title = str(title)
            
            if len(title) > left_length:
                space_position = title.rfind(' ', left_length-25, left_length)
                if space_position == -1:
                    space_position = left_length-3
                
                title = title[:space_position]+'...'
            
            if index == selected:
                if (prefix is not None):
                    parts.append('**')
                    parts.append(prefix)
                    parts.append('** ')
                parts.append('**')
                parts.append(title)
                parts.append('**\n')
            else:
                if (prefix is not None):
                    parts.append(prefix)
                    parts.append(' ')
                parts.append(title)
                parts.append('\n')
            
            index +=1
            if index == end:
                break
        
        embed = self.embed
        embed.description = ''.join(parts)
        
        current_page = (selected//10)+1
        limit = len(choices)
        page_limit = (limit//10)+1
        start = end-9
        if start < 1:
            start = 1
        if end == len(choices):
            end -= 1
        limit -= 1
        
        embed.add_footer(f'Page {current_page}/{page_limit}, {start} - {end} / {limit}, selected: {selected+1}')
        return embed
    
    async def __call__(self, client, event):
        """
        Called when a reaction is added or removed from the respective message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who executes the ``ChooseMenu``
        event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
            The received event.
        """
        if event.user.is_bot:
            return
        
        if (event.emoji not in (self.EMOJIS if len(self.choices)>10 else self.EMOJIS_RESTRICTED)):
            return
        
        client = self.client
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        check = self.check
        if (check is not None):
            try:
                should_continue = check(event)
            except BaseException as err:
                await client.events.error(client, f'{self!r}.__call__', err)
                return
            
            if not should_continue:
                return
        
        task_flag = self.task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if event.emoji is self.CANCEL:
                    self.task_flag = GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        message = self.message
        
        while True:
            emoji = event.emoji
            if emoji is self.UP:
                selected = self.selected-1
                break
            
            if emoji is self.DOWN:
                selected = self.selected+1
                break
            
            if emoji is self.LEFT:
                selected = self.selected-10
                break
            
            if emoji is self.RIGHT:
                selected = self.selected+10
                break
            
            if emoji is self.CANCEL:
                self.task_flag = GUI_STATE_CANCELLED
                try:
                    await client.message_delete(message)
                except BaseException as err:
                    self.cancel()
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.invalid_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}.__call__', err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.SELECT:
                self.task_flag = GUI_STATE_SWITCHING_CTX
                self.cancel()
                
                try:
                    if self.channel.cached_permissions_for(client).can_manage_messages:
                        await client.reaction_clear(message)
                    
                    else:
                        for emoji in self.EMOJIS:
                            await client.reaction_delete_own(message, emoji)
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_message, # message already deleted
                                ERROR_CODES.unknown_channel, # channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}.__call__', err)
                    return
                
                selector = self.selector
                try:
                    choice = self.choices[self.selected]
                    channel = self.channel
                    if isinstance(choice, tuple):
                        coro = selector(client, channel, message, *choice)
                    else:
                        coro = selector(client, channel, message, choice)
                    await coro
                except BaseException as err:
                    await client.events.error(client, f'{self!r}.__call__ when calling {selector!r}', err)
                return
            
            return
        
        if selected < 0:
            selected = 0
        elif selected >= len(self.choices):
            selected = len(self.choices)-1
        
        if self.selected == selected:
            return
        
        self.selected = selected
        self.task_flag = GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(message, embed=self._render_embed())
        except BaseException as err:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message already deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                            ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if self.task_flag == GUI_STATE_CANCELLING:
            self.task_flag = GUI_STATE_CANCELLED
            try:
                await client.message_delete(message)
            except BaseException as err:
                
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                await client.events.error(client, f'{self!r}.__call__', err)
                return
            
            self.cancel()
            return
        
        self.task_flag = GUI_STATE_READY
        self.timeouter.set_timeout(self.timeout)
    
    async def _canceller(self, exception,):
        """
        Used when the ``ChooseMenu`` is cancelled.
        
        First of all removes the choose menu from waitfors, so it will not wait for reaction events, then sets the
        ``.task_flag`` of the it to `GUI_STATE_CANCELLED`.
        
        If `exception` is given as `TimeoutError`, then removes the ``ChooseMenu``'s reactions from the respective
        message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance
            Exception to cancel the ``ChooseMenu`` with.
        """
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self.task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self.task_flag = GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except BaseException as err:
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.unknown_channel, # channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}._canceller', err)
                    return
            return
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        # we do nothing
    
    def cancel(self, exception=None):
        """
        Cancels the choose menu, if it is not cancelled yet.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance, Optional
            Exception to cancel the choose menu with. Defaults to `None`
        """
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)

    def __repr__(self):
        """Returns the choose menu's representation."""
        result = [
            '<', self.__class__.__name__,
            ' client=', repr(self.client),
            ', choices=', repr(len(self.choices)),
            ', selected=', repr(self.selected),
            ', channel=', repr(self.channel),
            ', selector=', repr(self.selector),
                ]
        
        prefix = self.prefix
        if (prefix is not None):
            result.append(', prefix=')
            result.append(repr(prefix))
        
        result.append(', task_flag=')
        task_flag = self.task_flag
        result.append(repr(task_flag))
        result.append(' (')
        
        task_flag_name = (
            'GUI_STATE_READY',
            'GUI_STATE_SWITCHING_PAGE',
            'GUI_STATE_CANCELLING',
            'GUI_STATE_CANCELLED',
            'GUI_STATE_SWITCHING_CTX',
                )[task_flag]
        
        result.append(task_flag_name)
        result.append(')>')
        
        return ''.join(result)
