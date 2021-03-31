# -*- coding: utf-8 -*-
__all__ = ('Closer', )

from ...backend.futures import Task
from ...discord.client_core import KOKORO
from ...discord.emoji import BUILTIN_EMOJIS
from ...discord.parsers import InteractionEvent
from ...discord.message import Message
from ...discord import ChannelTextBase
from ...discord.exceptions import DiscordException, ERROR_CODES

from .utils import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, \
    GUI_STATE_SWITCHING_CTX, Timeouter


class Closer:
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
        channel : ``ChannelTextBase`` instance, ``Message``, ``InteractionEvent``
            The channel where the ``Closer`` will be executed.  Pass it as a ``Message`` instance to send a reply.
        
            If given as ``InteractionEvent``, then will acknowledge it and create a new message with it as well.
            Although will not acknowledge it if `message` is given.
        
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
        self.canceller = cls._canceller
        self.task_flag = GUI_STATE_READY
        self.message = message
        self.timeouter = None
        
        try:
            if message is None:
                if received_interaction:
                    if not channel.is_acknowledged():
                        await client.interaction_response_message_create(channel)
                    
                    message = await client.interaction_followup_message_create(channel, content)
                else:
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
