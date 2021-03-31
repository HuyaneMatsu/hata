# -*- coding: utf-8 -*-
__all__ = ('Pagination',)

from ...backend.futures import Task
from ...discord.client_core import KOKORO
from ...discord.emoji import BUILTIN_EMOJIS
from ...discord.parsers import InteractionEvent
from ...discord.message import Message
from ...discord import ChannelTextBase
from ...discord.exceptions import DiscordException, ERROR_CODES

from .utils import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, \
    GUI_STATE_SWITCHING_CTX, Timeouter


class Pagination:
    """
    A builtin option to display paginated messages, allowing the users moving between the pages with arrow emojis.
    
    The class allows modifications and closing it's representations for every user. Also works at private channels.
    
    Picks up on reaction additions and on reaction deletions as well and removes the added reactions on if has
    permission, which might be missing, like in DM-s.
    
    Attributes
    ----------
    canceller : `None` or `function`
        The function called when the ``Pagination`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    channel : ``ChannelTextBase`` instance
        The channel where the ``Pagination`` is executed.
    check : `None` or `callable`
        A callable what decides whether the ``Pagination`` should process a received reaction event. Defaults to
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
    
    client : ``Client`` of ``Embed`` (or any compatible)
        The client who executes the ``Pagination``.
    message : `None` or ``Message``
        The message on what the ``Pagination`` is executed.
    page : `int`
        The current page's index.
    pages : `indexable`
        An indexable container, what stores the displayable ``Embed``-s.
    task_flag : `int`
        A flag to store the state of the ``Pagination``.
        
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
    timeout : `float`
        The timeout of the ``Pagination`` in seconds.
    timeouter : `None` or ``Timeouter``
        Executes the timing out feature on the ``Pagination``.
    
    Class Attributes
    ----------------
    LEFT2 : ``Emoji`` = `BUILTIN_EMOJIS['track_previous']`
        The emoji used to move to the first page.
    LEFT : ``Emoji`` = `BUILTIN_EMOJIS['arrow_backward']`
        The emoji used to move to the previous page.
    RIGHT : ``Emoji`` = `BUILTIN_EMOJIS['arrow_forward']`
        The emoji used to move on the next page.
    RIGHT2 : ``Emoji`` = `BUILTIN_EMOJIS['track_next']`
        The emoji used to move on the last page.
    CANCEL : ``Emoji`` = `BUILTIN_EMOJIS['x']`
        The emoji used to cancel the ``Pagination``.
    EMOJIS : `tuple` (`Emoji`, `Emoji`, `Emoji`, `Emoji`, `Emoji`) = `(LEFT2, LEFT, RIGHT, RIGHT2, CANCEL,)`
        The emojis to add on the respective message in order.
    """
    LEFT2  = BUILTIN_EMOJIS['track_previous']
    LEFT   = BUILTIN_EMOJIS['arrow_backward']
    RIGHT  = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2 = BUILTIN_EMOJIS['track_next']
    CANCEL = BUILTIN_EMOJIS['x']
    EMOJIS = (LEFT2, LEFT, RIGHT, RIGHT2, CANCEL,)
    
    __slots__ = ('canceller', 'channel', 'check', 'client', 'message', 'page', 'pages', 'task_flag', 'timeout', 'timeouter')
    
    async def __new__(cls, client, channel, pages, timeout=240., message=None, check=None):
        """
        Creates a new pagination with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who will execute the ``Pagination``.
        channel : ``ChannelTextBase`` instance, ``Message``, ``InteractionEvent``
            The channel where the ``Pagination`` will be executed. Pass it as a ``Message`` instance to send a reply.
            
            If given as ``InteractionEvent``, then will acknowledge it and create a new message with it as well.
            Although will not acknowledge it if `message` is given.
        
        pages : `indexable-container`
            An indexable container, what stores the displayable pages.
        timeout : `float`, Optional
            The timeout of the ``Pagination`` in seconds. Defaults to `240.0`.
        message : `None` or ``Message``, Optional
            The message on what the ``Pagination`` will be executed. If not given a new message will be created.
            Defaults to `None`.
        check : `None` or `callable`, Optional
            A callable what decides whether the ``Pagination`` should process a received reaction event. Defaults to
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
        self : `None` or ``Pagination``
            If `pages` is an empty container, returns `None`.
        
        Raises
        ------
        TypeError
            `channel`'s type is incorrect.
        """
        if not pages:
            return None
        
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
        
        self = object.__new__(cls)
        self.check = check
        self.client = client
        self.channel = target_channel
        self.pages = pages
        self.page = 0
        self.canceller = cls._canceller
        self.task_flag = GUI_STATE_READY
        self.message = message
        self.timeout = timeout
        self.timeouter = None
        
        try:
            if message is None:
                if received_interaction:
                    if not channel.is_acknowledged():
                        await client.interaction_response_message_create(channel)
                    
                    message = await client.interaction_followup_message_create(channel, pages[0])
                else:
                    message = await client.message_create(channel, pages[0])
                self.message = message
            else:
                await client.message_edit(message, pages[0])
            
            if not target_channel.cached_permissions_for(client).can_add_reactions:
                return self
            
            if len(self.pages)>1:
                for emoji in self.EMOJIS:
                    await client.reaction_add(message, emoji)
            else:
                await client.reaction_add(message, self.CANCEL)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                            ):
                    return None
            
            raise
        
        self.timeouter = Timeouter(self, timeout=timeout)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    async def __call__(self, client, event):
        """
        Called when a reaction is added or removed from the respective message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who executes the ``Pagination``
        event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
            The received event.
        """
        if event.user.is_bot:
            return
        
        if (event.emoji not in self.EMOJIS):
            return
        
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
        
        emoji = event.emoji
        task_flag = self.task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag = GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page = self.page-1
                break
            
            if emoji is self.RIGHT:
                page = self.page+1
                break
            
            if emoji is self.CANCEL:
                self.task_flag = GUI_STATE_CANCELLED
                try:
                    await client.message_delete(self.message)
                except BaseException as err:
                    self.cancel()
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}.__call__', err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.LEFT2:
                page = 0
                break
            
            if emoji is self.RIGHT2:
                page = len(self.pages)-1
                break
            
            return
        
        if page < 0:
            page = 0
        elif page >= len(self.pages):
            page = len(self.pages)-1
        
        if self.page == page:
            return
        
        self.page = page
        self.task_flag = GUI_STATE_SWITCHING_PAGE
        
        try:
            await client.message_edit(self.message, self.pages[page])
        except BaseException as err:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.invalid_access, # client removed
                            ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if self.task_flag == GUI_STATE_CANCELLING:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            try:
                await client.message_delete(self.message)
            except BaseException as err:
                
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, #message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                await client.events.error(client, f'{self!r}.__call__', err)
                return
            
            return
            
        self.task_flag = GUI_STATE_READY
        self.timeouter.set_timeout(self.timeout)
    
    async def _canceller(self, exception):
        """
        Used when the ``Pagination`` is cancelled.
        
        First of all removes the pagination from waitfors, so it will not wait for reaction events, then sets the
        ``.task_flag`` of the it to `GUI_STATE_CANCELLED`.
        
        If `exception` is given as `TimeoutError`, then removes the ``Pagination``'s reactions from the respective
        message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance
            Exception to cancel the ``Pagination`` with.
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
                    
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
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
        # We do nothing.
    
    def cancel(self, exception=None):
        """
        Cancels the pagination, if it is not cancelled yet.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance, Optional
            Exception to cancel the pagination with. Defaults to `None`
        """
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)
    
    def __repr__(self):
        """Returns the pagination's representation."""
        result = [
            '<', self.__class__.__name__,
            ' client=', repr(self.client),
            ', pages=', repr(len(self.pages)),
            ', page=', repr(self.page),
            ', channel=', repr(self.channel),
            ', task_flag='
                ]
        
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

