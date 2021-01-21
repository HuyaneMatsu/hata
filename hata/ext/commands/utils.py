# -*- coding: utf-8 -*-
__all__ = ('ChooseMenu', 'Closer', 'Cooldown', 'GUI_STATE_CANCELLED', 'GUI_STATE_CANCELLING', 'GUI_STATE_READY',
    'GUI_STATE_SWITCHING_CTX', 'GUI_STATE_SWITCHING_PAGE', 'Timeouter', 'Pagination', 'WaitAndContinue',
    'ReactionAddWaitfor', 'ReactionDeleteWaitfor', 'multievent', 'wait_for_message', 'wait_for_reaction', )

from ...backend.futures import Task, Future
from ...backend.event_loop import LOOP_TIME

from ...discord.parsers import EventWaitforBase
from ...discord.emoji import BUILTIN_EMOJIS
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.client_core import KOKORO
from ...discord.embed import Embed
from ...discord.channel import ChannelTextBase
from ...discord.message import Message

from .command import CommandWrapper

class ReactionAddWaitfor(EventWaitforBase):
    """
    Implements waiting for `reaction_add` events.
    
    Attributes
    ----------
    waitfors : `WeakValueDictionary` of (``DiscordEntity``, `async-callable`) items
        An auto-added container to store `entity` - `async-callable` pairs.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = `'reaction_add'`
        Predefined name to what the event handler will be added.
    """
    __slots__ = ()
    __event_name__ = 'reaction_add'

class ReactionDeleteWaitfor(EventWaitforBase):
    """
    Implements waiting for `reaction_delete` events.
    
    Attributes
    ----------
    waitfors : `WeakValueDictionary` of (``DiscordEntity``, `async-callable`) items
        An auto-added container to store `entity` - `async-callable` pairs.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = `'reaction_delete'`
        Predefined name to what the event handler will be added.
    """
    __slots__ = ()
    __event_name__ = 'reaction_delete'

class multievent(object):
    """
    Helper class to hold more waitfor event handlers together allowing to add `target` - `waiter` pairs at the same to
    more.
    
    Attributes
    ----------
    events : `tuple` of `Any`
        A `tuple` of the contained event handlers.
    """
    __slots__=('events',)
    
    def __init__(self, *events):
        """
        Creates a `multievent` instance with the given event handlers
        
        Parameters
        ----------
        *events : `Any`
            The event handlers to hold together.
        """
        self.events = events
    
    def append(self, target, waiter):
        """
        Adds the given `target` - `waiter` pair to the contained event handlers.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
        waiter : `async callable`
        """
        for event in self.events:
            event.append(target, waiter)
    
    def remove(self, target, waiter):
        """
        Removes the given `target` - `waiter` pair to the contained event handlers.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
        waiter : `async callable`
        """
        for event in self.events:
            event.remove(target, waiter)

class Timeouter(object):
    """
    Executes timing out feature on ``Pagination`` and on other familiar types.
    
    Attributes
    ----------
    handle : `None` or ``TimerHandle``
        Handle to wake_up the timeouter with it's `.__step` function.
        Set to `None`, when the respective timeout is over or if the timeout is cancelled.
    owner : `Any`
        The object what uses the timeouter.
        Set to `None`, when the respective timeout is over or if the timeout is cancelled.
    timeout : `float`
        The time with what the timeout will be expired when it's current waiting cycle is over.
    """
    __slots__ = ('handle', 'owner', 'timeout')
    def __init__(self, owner, timeout):
        """
        Creates a new ``Timeouter`` instance with the given `owner` and `timeout`.
        
        Parameters
        ----------
        owner : `Any`
            The object what uses the timeouter.
        timeout : `float`
            The time with what the timeout will be expired when it's current waiting cycle is over.
        """
        self.owner = owner
        self.timeout = 0.0
        self.handle = KOKORO.call_later(timeout, self.__step, self)
    
    @staticmethod
    def __step(self):
        """
        Executes a timeouter cycle.
        
        Increases the timeout if ``.timeout`` was updated. If not and applicable, calls it's ``.owner``'s
        `.canceller` with `TimeoutError` and unlinks ``.owner`` and `owner.canceller`,
        """
        timeout = self.timeout
        if timeout > 0.0:
            self.handle = KOKORO.call_later(timeout, self.__step, self)
            self.timeout = 0.0
            return
        
        self.handle = None
        owner = self.owner
        if owner is None:
            return
        
        self.owner = None
        
        canceller = owner.canceller
        if canceller is None:
            return
        
        owner.canceller = None
        Task(canceller(owner, TimeoutError()), KOKORO)
    
    def cancel(self):
        """
        Cancels the timeouter.
        
        Should be called by the timeouter's owner when it is cancelled with an other exception.
        """
        handle = self.handle
        if handle is None:
            return
        
        self.handle = None
        handle.cancel()
        self.owner = None
    
    def set_timeout(self, value):
        """
        Sets the timeouter of the timeouter to the given value.
        """
        handle = self.handle
        if handle is None:
            # Cannot change timeout of expired timeouter
            return
        
        if value <= 0.0:
            self.timeout = 0.0
            handle._run()
            handle.cancel()
            return
        
        now = LOOP_TIME()
        next_step = self.handle.when
        
        planed_end = now+value
        if planed_end < next_step:
            handle.cancel()
            self.handle = KOKORO.call_at(planed_end, self.__step, self)
            return
        
        self.timeout = planed_end-next_step
    
    def get_expiration_delay(self):
        """
        Returns after how much time the timeouter will expire.
        
        If the timeouter already expired, returns `0.0˙.
        
        Returns
        -------
        time_left : `float`
        """
        handle = self.handle
        if handle is None:
            return 0.0
        
        return handle.when-LOOP_TIME()+self.timeout

GUI_STATE_READY          = 0
GUI_STATE_SWITCHING_PAGE = 1
GUI_STATE_CANCELLING     = 2
GUI_STATE_CANCELLED      = 3
GUI_STATE_SWITCHING_CTX  = 4

class Pagination(object):
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
        channel : ``ChannelTextBase`` instance or ``Message``
            The channel where the ``Pagination`` will be executed. Pass it as a ``Message`` instance to send a reply.
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
        elif isinstance(channel, Message):
            target_channel = channel.channel
        else:
            raise TypeError('`channel` can be given only as `ChannelTextBase` or as `Message` instance.')
        
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
    
    async def _canceller(self, exception,):
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
        #we do nothing
    
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

class Closer(object):
    """
    Familiar to ``Pagination``, but can be used if the given content has only 1 page, so only an `x` would show up.
    
    Picks up on reaction additions by any users.
    
    Attributes
    ----------
    canceller : `None` or `function`
        The function called when the ``Closer`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    channel : ``ChannelTextBase`` instance
        The channel where the ``Closer`` is executed.
    check : `None` or `callable`
        A callable what decides whether the ``Closer`` should process a received reaction event. Defaults to
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
        The client who executes the ``Closer``.
    message : `None` or ``Message``
        The message on what the ``Closer`` is executed.
    task_flag : `int`
        A flag to store the state of the ``Closer``.
        
        Possible values:
        +---------------------------+-------+-----------------------------------------------------------------------+
        | Respective name           | Value | Description                                                           |
        +===========================+=======+=======================================================================+
        | GUI_STATE_READY           | 0     | The closer does nothing, is ready to be used.                         |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_PAGE  | 1     | The closer is currently changing it's page.                           |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLING      | 2     | The pagination is currently changing it's page, but it was cancelled  |
        |                           |       | meanwhile.                                                            |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLED       | 3     | The pagination is, or is being cancelled right now.                   |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_CTX   | 4     | The closer is switching context. Not used by the default class,       |
        |                           |       | but expected.                                                         |
        +---------------------------+-------+-----------------------------------------------------------------------+
    timeouter : `None` or ``Timeouter``
        Executes the timing out feature on the ``Closer``.
    
    Class Attributes
    ----------------
    CANCEL : ``Emoji`` = `BUILTIN_EMOJIS['x']`
        The emoji used to cancel the ``Closer``.
    """
    CANCEL = BUILTIN_EMOJIS['x']
    
    __slots__ = ('canceller', 'channel', 'check', 'client', 'message', 'task_flag', 'timeouter')
    
    async def __new__(cls, client, channel, content, timeout=240., message=None, check=None):
        """
        Creates a new pagination with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who will execute the ``Closer``.
        channel : ``ChannelTextBase`` instance or ``Message``
            The channel where the ``Closer`` will be executed.  Pass it as a ``Message`` instance to send a reply.
        content : ``Any`
            The displayed content.
        timeout : `float`, Optional
            The timeout of the ``Closer`` in seconds. Defaults to `240.0`.
        message : `None` or ``Message``, Optional
            The message on what the ``Closer`` will be executed. If not given a new message will be created.
            Defaults to `None`.
        check : `None` or `callable`, Optional
            A callable what decides whether the ``Closer`` should process a received reaction event. Defaults to
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
        self : `None` or ``Closer``
        
        Raises
        ------
        TypeError
            `channel`'s type is incorrect.
        """
        if isinstance(channel, ChannelTextBase):
            target_channel = channel
        elif isinstance(channel, Message):
            target_channel = channel.channel
        else:
            raise TypeError('`channel` can be given only as `ChannelTextBase` or as `Message` instance.')
        
        self = object.__new__(cls)
        self.check = check
        self.client = client
        self.channel = target_channel
        self.canceller = cls._canceller
        self.task_flag = GUI_STATE_READY
        self.message = message
        self.timeouter = None
        
        try:
            if message is None:
                message = await client.message_create(channel, content)
                self.message = message
            else:
                await client.message_edit(message, content)
            
            if not target_channel.cached_permissions_for(client).can_add_reactions:
                return self
            
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
        return self
    
    
    async def __call__(self, client, event):
        """
        Called when a reaction is added on the respective message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who executes the ``Closer``
        event : ``ReactionAddEvent``
            The received event.
        """
        if event.user.is_bot:
            return
        
        if (event.emoji is not self.CANCEL):
            return
        
        task_flag = self.task_flag
        if task_flag != GUI_STATE_READY:
            # ignore GUI_STATE_SWITCHING_PAGE and GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
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
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.invalid_access, # client removed
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.__call__', err)
            return
    
    async def _canceller(self, exception,):
        """
        Used when the ``Closer`` is cancelled.
        
        First removes the respective waitfors of the canceller, then set it's ``.task_flag`` of the it to
        `GUI_STATE_CANCELLED`.
        
        If `exception` is given as `TimeoutError`, then removes the ``Closer``'s reactions from the respective
        message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance
            Exception to cancel the ``Closer`` with.
        """
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        
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
        #we do nothing
    
    def cancel(self, exception=None):
        """
        Cancels the closer, if it is not cancelled yet.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance, Optional
            Exception to cancel the closer with. Defaults to `None`
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


class ChooseMenu(object):
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
    embed : ``Embed`` (or any compatible)
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
        elif isinstance(channel, Message):
            target_channel = channel.channel
        else:
            raise TypeError('`channel` can be given only as `ChannelTextBase` or as `Message` instance.')
        
        result_ln = len(choices)
        if result_ln < 2:
            if result_ln == 1:
                choice = choices[0]
                if isinstance(choice, tuple):
                    coro = selector(client, target_channel, message, *choice)
                else:
                    coro = selector(client, target_channel, message, choice)
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

class WaitAndContinue(object):
    """
    Waits for the given event and if the check returns `True` called with the received parameters, then passes them to
    it's waiter future. If check return anything else than `False`, then passes that as well to the future.
    
    Attributes
    -----------
    canceller : `None` `function`
        The canceller function of the ``WaitAndContinue``, what is set to ``._canceller`` by default.
        When ``.cancel`` is called, then this instance attribute is set to `None`.
    check : `callable`
        The check what is called with the received parameters whenever an event is received.
    event : `async-callable`
        The respective event handler on what the waiting is executed.
    future : ``Future``
        The waiter future what's result will be set when the check returns non `False` value.
    target : ``DiscordEntity``
        The target entity on what the waiting is executed.
    timeouter : ``TimeOuter``
        Executes the ``WaitAndContinue`` timeout feature and raise `TimeoutError` to the waiter.
    """
    __slots__ = ('canceller', 'check', 'event', 'future', 'target', 'timeouter', )
    def __init__(self, future, check, target, event, timeout):
        """
        Creates a new ``WaitAndContinue`` instance with the given parameters.
        
        Parameters
        ----------
        future : ``Future`
            The waiter future `what's result will be set when the check returns non `False` value.
        check : `callable`
            The check what is called with the received parameters whenever an event is received.
        target : ``DiscordEntity``
            The target entity on what the waiting is executed.
        event : `async-callable`
            The respective event handler on what the waiting is executed.
        timeout : `float`
            The timeout after `TimeoutError` will be raised to the waiter future.
        """
        self.canceller = self.__class__._canceller
        self.future = future
        self.check = check
        self.event = event
        self.target = target
        self.timeouter = Timeouter(self,timeout)
        event.append(target, self)
    
    async def __call__(self, client, *args):
        """
        Calls the ``WaitAndContinue`` and if it's check returns non `False`, then set's the waiter future's result to
        the received parameters. If `check` returned non `bool`, then passes that value to the waiter as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective event.
        *args : `Any`
            Received parameters given by the respective event handler.
        """
        try:
            result = self.check(*args)
        except BaseException as err:
            self.future.set_exception_if_pending(err)
            self.cancel()
        else:
            if type(result) is bool:
                if not result:
                    return
                
                if len(args) == 1:
                    args = args[0]
            
            else:
                args = (*args, result,)
            
            self.future.set_result_if_pending(args)
            self.cancel()
    
    async def _canceller(self, exception):
        """
        Cancels the ``WaitAndContinue`` with the given exception. If the given `exception` is `BaseException` instance,
        then raises it to the waiter future.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None` or `BaseException`
            Exception to cancel the ``WaitAndContinue``'s ``.future`` with.
        """
        if exception is None:
            self.future.set_exception_if_pending(TimeoutError())
            return
        
        self.event.remove(self.target, self)
        self.future.set_exception_if_pending(exception)
        
        if not isinstance(exception, TimeoutError):
            return
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
    
    def cancel(self):
        """
        Cancels the ``WaitAndContinue``.
        """
        canceller = self.canceller
        if canceller is None:
            return
        
        self.event.remove(self.target, self)
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self, None), KOKORO)


def wait_for_reaction(client, message, check, timeout):
    """
    Executes waiting for reaction on a message with a ``Future`` instance.
    
    Parameters
    ----------
    client : ``Client``
        The client who's `reaction_add` event will be used.
    message : ``Message``
        The target message on what new reactions will be checked.
    check : `callable`
        The check what is called with the received parameters whenever an event is received.
    timeout : `float`
        The timeout after `TimeoutError` will be raised to the waiter future.
    
    Returns
    -------
    future : ``Future``
        The waiter future, what should be awaited.
    """
    future = Future(KOKORO)
    WaitAndContinue(future, check, message, client.events.reaction_add, timeout)
    return future


def wait_for_message(client, channel, check, timeout):
    """
    Executes waiting for messages at a channel with a ``Future`` instance.
    
    Parameters
    ----------
    client : ``Client``
        The client who's `message_create` event will be used.
    channel : ``ChannelBase``
        The target channel where the new messages will be checked.
    check : `callable`
        The check what is called with the received parameters whenever an event is received.
    timeout : `float`
        The timeout after `TimeoutError` will be raised to the waiter future.
    
    Returns
    -------
    future : ``Future``
        The waiter future, what should be awaited.
    """
    future = Future(KOKORO)
    WaitAndContinue(future, check, channel, client.events.message_create, timeout)
    return future


class _CDUnit(object):
    """
    A cooldown unit stored by a ``CooldownWrapper``.
    
    Attributes
    ----------
    expires_at : `float`
        When the cooldown unit will expire in LOOP_TIME time.
    uses_left : `int`
        How much uses are left till the respective entity will be locked by cooldown.
    """
    __slots__ = ('expires_at', 'uses_left',)
    def __init__(self, expires_at, uses_left):
        """
        Creates a new ``_CDUnit`` with the given parameters.
        
        Parameters
        ----------
        expires_at : `float`
            When the cooldown unit will expire in LOOP_TIME time.
        uses_left : `int`
            How much uses are left till the respective entity will be locked by cooldown.
        """
        self.expires_at = expires_at
        self.uses_left = uses_left
    
    def __repr__(self):
        """Returns the object's representation."""
        return f'{self.__class__.__name__}(expires_at={self.expires_at}, uses_left={self.uses_left})'

class CooldownWrapper(CommandWrapper):
    """
    Rich command wrapper of ``Cooldown``. Check ``CommandWrapper`` itself for more details.
    
    This subclass adds `Cooldown.shared` feature to the command wrappers created by ``Cooldown``.
    """
    __slots__ = ()
    def shared(self, weight=0, func=None):
        """
        Creates a new cooldown instance, which cooldown is shared with the source one.
        
        Parameters
        ----------
        weight : `int`, Optional
            The weight of one call. Defaults to `1`.
        func : `async-callable`, Optional
            The wrapped command. If not given, returns a wrapper, what can be used as a decorator.

        Returns
        -------
        wrapper : ``Cooldown._wrapper`` or ``CooldownWrapper``
            If `func` is given, then returns the created ``CooldownWrapper``, if not, then returns a wrapper,
            what can be used as a decorator.
        
        Raises
        ------
        TypeError
            If `weight` is not numeric convertable to `int`.
        """
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(f'`weight` can be given as `int` instance, got {weight_type.__name__}.') from None
        
        source_wrapper = self.wrapper
        if weight == 0:
            weight = source_wrapper.weight
        
        new_wrapper = object.__new__(type(source_wrapper))
        new_wrapper.checker = source_wrapper.checker
        new_wrapper.reset = source_wrapper.reset
        new_wrapper.cache = source_wrapper.cache
        new_wrapper.weight = weight
        new_wrapper.limit = source_wrapper.limit+source_wrapper.weight-weight
        
        if func is None:
            wrapper = source_wrapper._wrapper(new_wrapper, self.handler)
        else:
            wrapper = CooldownWrapper(func, new_wrapper, self.handler)
        
        return wrapper

class Cooldown(object):
    """
    Helper class for implement cooldowns.
    
    > Rework planned.
    
    Examples
    --------
    
    **Using a cooldown handler example:**
    
    ```
    from hata import DiscordException, CancelledError, sleep, ERROR_CODES, KOKORO
    from hata.ext.commands import Cooldown
    
    class CooldownHandler:
        __slots__ = ('cache',)
        
        def __init__(self):
            self.cache = {}
        
        async def __call__(self, client, message, command, time_left):
            user_id = message.author.id
            try:
                notification,waiter = self.cache[user_id]
            except KeyError:
                pass
            else:
                if notification.channel is message.channel:
                    try:
                        await client.message_edit(notification,
                            f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
                    except BaseException as err:
                        if isinstance(err, ConnectionError):
                            return
                        
                        if isinstance(err, DiscordException):
                            if err.code in (
                                    ERROR_CODES.unknown_message, # message deleted
                                    ERROR_CODES.unknown_channel, # channel deleted
                                    ERROR_CODES.invalid_access, # client removed
                                        ):
                                return
                        
                        await client.events.error(client, f'{self!r}.__call__', err)
                    
                    return
                
                waiter.cancel()
            
            try:
                notification = await client.message_create(message.channel,
                    f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                                ):
                        return
                
                await client.events.error(client, f'{self!r}.__call__', err)
            
            waiter = Task(self.waiter(client, user_id, notification), KOKORO)
            self.cache[user_id] = (notification, waiter)
        
        async def waiter(self, client, user_id, notification):
            try:
                await sleep(30., KOKORO)
            except CancelledError:
                pass
            
            del self.cache[user_id]
            
            try:
                await client.message_delete(notification)
            except BaseException as err:
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
    
    @Bot.commands
    @Cooldown('user', 30., handler=CooldownHandler())
    async def ping(client, message):
        await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')
    ```
    
    **Using shared cooldowns:**

    ```
    from hata import Embed
    from hata.ext.commands import Converter, ConverterFlag
    
    @Bot.commands
    @Cooldown('user', 60., limit=3, weight=2, handler=CooldownHandler())
    async def avatar(client, message, user : Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default_code='message.author')):
        url = user.avatar_url_as(size=4096)
        embed = Embed(f'{user:f}\'s avatar', url=url)
        embed.add_image(url)
        await client.message_create(message.channel, embed=embed)
    
    @Bot.commands
    @avatar.shared(weight=1)
    async def myavatar(client, message):
        url = message.author.avatar_url_as(size=4096)
        embed = Embed('Your avatar', url=url)
        embed.add_image(url)
        await client.message_create(message.channel, embed=embed)
    ```
    
    Attributes
    ----------
    cache : `dict` of (``DiscordEntity``, ``_CDUnit``) items
        Cache to remember how much use of the given entity are exhausted already.
    checker : `function`
        Checks after how much time the given entity can use again the respective command.
    limit : `int`
        The amount of how much times the command can be called within a set duration before going on cooldown.
    reset : `float`
        The time after the cooldown resets.
    weight : `int`
        The weight of the command.
    """
    __slots__ = ('cache', 'checker', 'limit', 'reset', 'weight',)
    
    def __new__(cls, for_, reset, limit=1, weight=1, handler=None, func=None):
        """
        Creates a new
        
        Parameters
        ----------
        for_ : `str`
            By what type of entity the cooldown should limit the command.
            
            Possible values:
             - `'user'`
             - `'channel'`
             - `'guild'`
         
        reset : `float`
            The reset time of the cooldown.
        limit : `int`
            The amount of calls after the respective command goes on cooldown.
        weight : `int`, Optional
            The weight of one call. Defaults to `1`.
        handler : `None` or `async-callable`
            Called, when the wrapped command is on cooldown.
            
            If given then 4 parameters will be passed to it:
            +-------------------+---------------+
            | Respective name   | Type          |
            +===================+===============+
            | client            | ``Client``    |
            +-------------------+---------------+
            | message           | ``Message``   |
            +-------------------+---------------+
            | command           | ``Command``   |
            +-------------------+---------------+
            | time_left         | `float`       |
            +-------------------+---------------+
        
        func : `async-callable`, Optional
            The wrapped command. If not given, returns a wrapper, what can be used as a decorator.
        
        Returns
        -------
        wrapper : ``Cooldown._wrapper`` / ``CooldownWrapper``
            If `func` is given, then returns the created ``CooldownWrapper``, if not, then returns a wrapper,
            what can be used as a decorator.
        
        Raises
        ------
        TypeError
            - If `str` is not given as `str` instance.
            - If `weight` is not numeric convertable to `int`.
            - If `reset` is not numeric convertable to `float`.
            - If `limit` is not numeric convertable to `int`.
        ValueError
            - If `for_` is not given as any of the expected value.
        """
        for_type = for_.__class__
        if for_type is str:
            pass
        elif issubclass(for_, str):
            for_ = str(for_)
        else:
            raise TypeError(f'`for_` can be given as `str` instance, got {for_type.__name__}.')
    
        if 'user'.startswith(for_):
            checker = cls._check_user
        elif 'channel'.startswith(for_):
            checker = cls._check_channel
        elif 'guild'.startswith(for_):
            checker = cls._check_guild
        else:
            raise ValueError(f'\'for_\' can be \'user\', \'channel\' or \'guild\', got {for_!r}')
        
        reset_type = reset.__class__
        if (reset_type is not float):
            try:
                __float__ = getattr(reset_type, '__float__')
            except AttributeError:
                raise TypeError(f'The given reset is not `float`, neither other numeric convertable to it, got '
                    f'{reset_type.__name__}.') from None
            
            reset = __float__(reset)
            
        limit_type = limit.__class__
        if limit_type is int:
            pass
        elif issubclass(limit_type, int):
            limit = int(limit)
        else:
            raise TypeError(f'`limit` can be given as `int` instance, got {limit_type.__name__}.') from None
        
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(f'`weight` can be given as `int` instance, got {weight_type.__name__}.') from None
        
        self = object.__new__(cls)
        self.checker = checker
        self.reset = reset
        self.weight = weight
        self.limit = limit-weight
        self.cache = {}
        
        if func is None:
            wrapper = self._wrapper(self, handler)
        else:
            wrapper = CooldownWrapper(func, self, handler)
        
        return wrapper
    
    class _wrapper(object):
        """
        When a parent ``Command`` instance would be created without giving `func` parameter, then a wrapper of this
        type is returned enabling using ``Cooldown` as a decorator, with still giving parameters to it.
        
        Attributes
        ----------
        parent : ``Cooldown``
            The parent cooldown instance.
        handler : `None` or `async-callable`
            Called, when the wrapped command is on cooldown.
            
            If given then 4 parameters will be passed to it:
            +-------------------+---------------+
            | Respective name   | Type          |
            +===================+===============+
            | client            | ``Client``    |
            +-------------------+---------------+
            | message           | ``Message``   |
            +-------------------+---------------+
            | command           | ``Command``   |
            +-------------------+---------------+
            | time_left         | `float`       |
            +-------------------+---------------+
        """
        __slots__ = ('parent', 'handler')
        def __init__(self, parent, handler):
            """
            Creates a new ``Cooldown._wrapper`` instance with the given parameters.
            
            Parameters
            ----------
            parent : ``Cooldown``
                The parent cooldown instance.
            handler : `None` or `async-callable`
                Called, when the wrapped command is on cooldown.
                
                If given then 4 parameters will be passed to it:
                +-------------------+---------------+
                | Respective name   | Type          |
                +===================+===============+
                | client            | ``Client``    |
                +-------------------+---------------+
                | message           | ``Message``   |
                +-------------------+---------------+
                | command           | ``Command``   |
                +-------------------+---------------+
                | time_left         | `float`       |
                +-------------------+---------------+
            """
            self.parent = parent
            self.handler = handler
        
        def __call__(self, func):
            """
            By calling a cooldown's ``._wrapper`` a ``CooldownWrapper`` instance is created and returned, what can be
            added as a command.
            
            Parameters
            ----------
            func : `async-callable`
                The wrapped function by the cooldown to add as a command.

            Returns
            -------
            wrapper : ``CooldownWrapper``
            """
            if func is None:
                raise TypeError('`func` is given as `None`.')
            
            return CooldownWrapper(func, self.parent, self.handler)
    
    async def __call__(self, client, message):
        """
        Calls the cooldown with the respective `client` and `message`, and then yields whether the command can be
        called, and if not, then with what extra parameters the handler should receive.
        
        This method is a coroutine generator.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        
        Yields
        ------
        passed : `bool`
            Whether the command can be called. If not, then yields additional parameters to call the cooldown's
            handler with.
        time_left : `float`
            How much time is left till the cooldown's expiration.
        """
        value = self.checker(self, message)
        if not value:
            yield True
            return
        
        yield False
        yield value-LOOP_TIME()
        return
    
    @staticmethod
    def _check_user(self, message):
        """
        Executes user cooldown check.
        
        Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
        
        Parameters
        ----------
        message : ``Message``
            The received message.
        
        Returns
        -------
        expires_at : `int`
            When the cooldown for the given entity will expire.
        """
        id_ = message.author.id
        
        cache = self.cache
        try:
            unit = cache[id_]
        except KeyError:
            at_ = LOOP_TIME()+self.reset
            cache[id_] = _CDUnit(at_, self.limit)
            KOKORO.call_at(at_, dict.__delitem__, cache, id_)
            return 0.
        
        left = unit.uses_left
        if left > 0:
            unit.uses_left = left-self.weight
            return 0.
        return unit.expires_at
    
    @staticmethod
    def _check_channel(self, message):
        """
        Executes channel cooldown check.
        
        Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
        
        Parameters
        ----------
        message : ``Message``
            The received message.
        
        Returns
        -------
        expires_at : `int`
            When the cooldown for the given entity will expire.
        """
        id_ = message.channel.id
        
        cache = self.cache
        try:
            unit = cache[id_]
        except KeyError:
            at_ = LOOP_TIME()+self.reset
            cache[id_] = _CDUnit(at_, self.limit)
            KOKORO.call_at(at_, dict.__delitem__, cache, id_)
            return 0.
        
        left = unit.uses_left
        if left>0:
            unit.uses_left = left-self.weight
            return 0.
        return unit.expires_at
    
    #returns -1. if non guild
    @staticmethod
    def _check_guild(self, message):
        """
        Executes guild based cooldown check.
        
        Might be set as the ``Cooldown``'s ``.checker`` instance attribute.
        
        Parameters
        ----------
        message : ``Message``
            The received message.
        
        Returns
        -------
        expires_at : `int`
            When the cooldown for the given entity will expire.
            
            If the cooldown limitation is not applicable for the given entity, returns `-1.0`.
        """
        channel = message.channel
        if channel.type in (1, 3):
            return -1.
        else:
            id_ = channel.guild.id
        
        cache = self.cache
        try:
            unit = cache[id_]
        except KeyError:
            at_ = LOOP_TIME()+self.reset
            cache[id_] = _CDUnit(at_,self.limit)
            KOKORO.call_at(at_, dict.__delitem__, cache, id_)
            return 0.
        
        left = unit.uses_left
        if left > 0:
            unit.uses_left = left-self.weight
            return 0.
        return unit.expires_at
