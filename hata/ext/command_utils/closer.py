# -*- coding: utf-8 -*-
__all__ = ('Closer', )

from ...backend.futures import CancelledError
from ...backend.utils import copy_docs
from ...discord.core import BUILTIN_EMOJIS
from ...discord.interaction import InteractionEvent
from ...discord.message import Message
from ...discord import ChannelTextBase
from ...discord.exceptions import DiscordException, ERROR_CODES

from .bases import GUI_STATE_READY, PaginationBase
from .utils import Timeouter

class Closer(PaginationBase):
    """
    Familiar to ``Pagination``, but can be used if the given content has only 1 page, so only an `x` would show up.
    
    Picks up on reaction additions by any users.
    
    Attributes
    ----------
    _canceller : `None` or `function`
        The function called when the ``Closer`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    
    _task_flag : `int`
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
    
    _timeouter : `None` or ``Timeouter``
        Executes the timing out feature on the ``Closer``.
    
    channel : ``ChannelTextBase`` instance
        The channel where the ``Closer`` is executed.
    
    client : ``Client`` of ``Embed`` (or any compatible)
        The client who executes the ``Closer``.
    
    message : `None` or ``Message``
        The message on what the ``Closer`` is executed.
    
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
    
    Class Attributes
    ----------------
    CANCEL : ``Emoji`` = `BUILTIN_EMOJIS['x']`
        The emoji used to cancel the ``Closer``.
    """
    CANCEL = BUILTIN_EMOJIS['x']
    
    __slots__ = ('check',)
    
    async def __new__(cls, client, channel, content, *, timeout=240., message=None, check=None):
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
        timeout : `float`, Optional (Keyword Only)
            The timeout of the ``Closer`` in seconds. Defaults to `240.0`.
        message : `None` or ``Message``, Optional (Keyword Only)
            The message on what the ``Closer`` will be executed. If not given a new message will be created.
            Defaults to `None`.
        check : `None` or `callable`, Optional (Keyword Only)
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
        self._canceller = cls._canceller_function
        self._task_flag = GUI_STATE_READY
        self.message = message
        self._timeouter = None
        
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
            self.cancel(PermissionError())
            return self
        
        try:
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
        return self
    
    
    @copy_docs(PaginationBase.__call__)
    async def __call__(self, client, event):
        if event.user.is_bot:
            return
        
        if (event.emoji is not self.CANCEL):
            return
        
        task_flag = self._task_flag
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
        
        self.cancel(CancelledError())
