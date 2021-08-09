# -*- coding: utf-8 -*-
__all__ = ('Pagination',)

from ...backend.utils import copy_docs
from ...backend.futures import CancelledError
from ...discord.core import BUILTIN_EMOJIS
from ...discord.interaction import InteractionEvent
from ...discord.message import Message
from ...discord import ChannelTextBase
from ...discord.exceptions import DiscordException, ERROR_CODES

from .bases import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, \
    GUI_STATE_VALUE_TO_NAME, PaginationBase
from .utils import Timeouter


class Pagination(PaginationBase):
    """
    A builtin option to display paginated messages, allowing the users moving between the pages with arrow emojis.
    
    The class allows modifications and closing it's representations for every user. Also works at private channels.
    
    Picks up on reaction additions and on reaction deletions as well and removes the added reactions on if has
    permission, which might be missing, like in DM-s.
    
    Attributes
    ----------
    _canceller : `None` or `function`
        The function called when the ``Pagination`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    
    _task_flag : `int`
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
    
    _timeouter : `None` or ``Timeouter``
        Executes the timing out feature on the ``Pagination``.
    
    channel : ``ChannelTextBase`` instance
        The channel where the ``Pagination`` is executed.
    
    client : ``Client`` of ``Embed`` (or any compatible)
        The client who executes the ``Pagination``.
    
    message : `None` or ``Message``
        The message on what the ``Pagination`` is executed.
    
    check : `None` or `callable`
        A callable what decides whether the ``Pagination`` should process a received reaction event. Defaults to
        `None`.
        
        Should accept the following parameters:
        +-----------+---------------------------------------------------+
        | Name      | Type                                              |
        +===========+===================================================+
        | event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |
        +-----------+---------------------------------------------------+
        
        > ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    page_index : `int`
        The current page's index.
    
    pages : `indexable`
        An indexable container, what stores the displayable contents.
    
    timeout : `float`
        The timeout of the ``Pagination`` in seconds.
    
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
    LEFT2 = BUILTIN_EMOJIS['track_previous']
    LEFT = BUILTIN_EMOJIS['arrow_backward']
    RIGHT = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2 = BUILTIN_EMOJIS['track_next']
    CANCEL = BUILTIN_EMOJIS['x']
    EMOJIS = (LEFT2, LEFT, RIGHT, RIGHT2, CANCEL,)
    
    __slots__ = ('check', 'page_index', 'pages', 'timeout',)
    
    async def __new__(cls, client, channel, pages, *, timeout=240., message=None, check=None):
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
        timeout : `float`, Optional (Keyword only)
            The timeout of the ``Pagination`` in seconds. Defaults to `240.0`.
        message : `None` or ``Message``, Optional (Keyword only)
            The message on what the ``Pagination`` will be executed. If not given a new message will be created.
            Defaults to `None`.
        check : `None` or `callable`, Optional (Keyword only)
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
        self.page_index = 0
        self._canceller = cls._canceller_function
        self._task_flag = GUI_STATE_READY
        self.message = message
        self.timeout = timeout
        self._timeouter = None
        
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
        except BaseException as err:
            self.cancel(err)
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
        
        if not target_channel.cached_permissions_for(client).can_add_reactions:
            await self.cancel(PermissionError())
            return self
        
        try:
            if len(self.pages)>1:
                for emoji in self.EMOJIS:
                    await client.reaction_add(message, emoji)
            else:
                await client.reaction_add(message, self.CANCEL)
        except BaseException as err:
            self.cancel(err)
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
        
        self._timeouter = Timeouter(self, timeout=timeout)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    @copy_docs(PaginationBase.__call__)
    async def __call__(self, client, event):
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
        task_flag = self._task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self._task_flag = GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page_index = self.page_index-1
                break
            
            if emoji is self.RIGHT:
                page_index = self.page_index+1
                break
            
            if emoji is self.CANCEL:
                self._task_flag = GUI_STATE_CANCELLED
                self.cancel()
                
                try:
                    await client.message_delete(self.message)
                except BaseException as err:
                    self.cancel(err)
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.missing_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}.__call__', err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.LEFT2:
                page_index = 0
                break
            
            if emoji is self.RIGHT2:
                page_index = len(self.pages)-1
                break
            
            return
        
        if page_index < 0:
            page_index = 0
        elif page_index >= len(self.pages):
            page_index = len(self.pages)-1
        
        if self.page_index == page_index:
            return
        
        self.page_index = page_index
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        try:
            await client.message_edit(self.message, self.pages[page_index])
        except BaseException as err:
            self.cancel(err)
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
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
            timeouter.set_timeout(self.timeout)
    
    
    @copy_docs(PaginationBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<', self.__class__.__name__,
            ' client=', repr(self.client),
            ', channel=', repr(self.channel),
            ', state='
        ]
        
        task_flag = self._task_flag
        repr_parts.append(repr(task_flag))
        repr_parts.append(' (')
        
        task_flag_name = GUI_STATE_VALUE_TO_NAME[task_flag]
        
        repr_parts.append(task_flag_name)
        repr_parts.append(')')
        
        # Third party things go here
        repr_parts.append(', pages=')
        repr_parts.append(repr(len(self.pages)))
        repr_parts.append(', page_index=')
        repr_parts.append(repr(self.page_index))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
