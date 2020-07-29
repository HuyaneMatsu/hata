# -*- coding: utf-8 -*-
__all__ = ('ChooseMenu', 'Cooldown', 'GUI_STATE_CANCELLED', 'GUI_STATE_CANCELLING', 'GUI_STATE_READY',
    'GUI_STATE_SWITCHING_CTX', 'GUI_STATE_SWITCHING_PAGE', 'Timeouter', 'Pagination', 'WaitAndContinue',
    'ReactionAddWaitfor', 'ReactionDeleteWaitfor', 'multievent', 'prefix_by_guild', 'wait_for_message',
    'wait_for_reaction', )

from time import monotonic

from ...backend.futures import Task, Future

from ...discord.parsers import EventWaitforBase
from ...discord.emoji import BUILTIN_EMOJIS
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.client_core import KOKORO
from ...discord.embed import Embed

from .command import CommandWrapper

class ReactionAddWaitfor(EventWaitforBase):
    __slots__ = ()
    __event_name__ = 'reaction_add'

class ReactionDeleteWaitfor(EventWaitforBase):
    __slots__ = ()
    __event_name__ = 'reaction_delete'

class multievent(object):
    __slots__=('events',)
    
    def __init__(self,*events):
        self.events=events
    
    def append(self, target, waiter):
        for event in self.events:
            event.append(target, waiter)
    
    def remove(self, target, waiter):
        for event in self.events:
            event.remove(target, waiter)

class Timeouter(object):
    __slots__ = ('handler', 'owner', 'timeout')
    def __init__(self,owner,timeout):
        self.owner=owner
        self.timeout=timeout
        self.handler=KOKORO.call_later(timeout,self.__step,self)
    
    @staticmethod
    def __step(self):
        timeout=self.timeout
        if timeout>0.0:
            self.handler=KOKORO.call_later(timeout,self.__step,self)
            self.timeout=0.0
            return
        
        self.handler=None
        owner=self.owner
        if owner is None:
            return
        
        self.owner=None
        
        canceller=owner.canceller
        if canceller is None:
            return
        owner.canceller=None
        Task(canceller(owner,TimeoutError()),KOKORO)
        
        
    def cancel(self):
        handler=self.handler
        if handler is None:
            return
        
        self.handler=None
        handler.cancel()
        self.owner=None
    
    def set_timeout(self,value):
        handler=self.handler
        if handler is None:
            # Cannot change timeout of expired timeouter
            return
        
        if value<=0.0:
            self.timeout=0.0
            handler._run()
            handler.cancel()
            return
        
        now=monotonic()
        next_step=self.handler.when
        
        planed_end=now+value
        if planed_end<next_step:
            handler.cancel()
            self.handler=KOKORO.call_at(planed_end,self.__step,self)
            return
        
        self.timeout=planed_end-next_step
        
    def get_expiration_delay(self):
        return self.handler.when-monotonic()+self.timeout

GUI_STATE_READY          = 0
GUI_STATE_SWITCHING_PAGE = 1
GUI_STATE_CANCELLING     = 2
GUI_STATE_CANCELLED      = 3
GUI_STATE_SWITCHING_CTX  = 4

class Pagination(object):
    """
    A builtin option to display paginated messages, allowsing the users moving between the pages with arrow emojis.
    The class allows modifications and closing it's representations for every user. Also works at private channels.
    
    Picks up on reaction additions and on reaction deletions as well and removes the added reactions on if has
    permission, which might be missing, like in DM-s.
    
    Attributes
    ----------
    canceller : `None` or `function`
        The function called when the ``Pagination`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    channel : ``ChannelTextBase`` instance
        The channel wehre the ``Pagination`` is executed.
    client : ``Client``
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
        | GUI_STATE_READY           | 0     | The Pagination does nothing an it is ready to be used.                |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_PAGE  | 1     | The Pagination is currently chaning it's page.                        |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLING      | 2     | The pagination is currently chaning it's page, but it was cancelled   |
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
    RIGHT : ``Emoji`` = `BUILTIN_EMOJIS['arrow_forward'`
        The emoji used to move on the next page.
    RIGHT2 : ``Emoji`` = `BUILTIN_EMOJIS['track_next']`
        The emoji used to move on the last page.
    CANCEL : ``Emoji`` = `BUILTIN_EMOJIS['x']`
        The emoji used to cancel the ``Pagination``
    EMOJIS : `tuple` (`Emoji`, `Emoji`, `Emoji`, `Emoji`, `Emoji`) = `(LEFT2, LEFT, RIGHT, RIGHT2, CANCEL,)`
        The emojis to add on the respective message in order.
    """
    LEFT2   = BUILTIN_EMOJIS['track_previous']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['track_next']
    CANCEL  = BUILTIN_EMOJIS['x']
    EMOJIS  = (LEFT2, LEFT, RIGHT, RIGHT2, CANCEL,)
    
    __slots__ = ('canceller', 'channel', 'client', 'message', 'page', 'pages', 'task_flag', 'timeout', 'timeouter')
    
    async def __new__(cls, client, channel, pages, timeout=240., message=None):
        """
        Creates a new pagination with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who will execute the ``Pagination``.
        channel : ``ChannelTextBase`` instance
            The channel wehre the ``Pagination`` will be executed.
        pages : `indexable`
            An indexable container, what stores the displayable ``Embed``-s.
        timeout : `float`, Optional
            The timeout of the ``Pagination`` in seconds. Defaults to `240.0`.
        
        message : `None` or ``Message``, Optional
            The message on what the ``Pagination`` will be executed. If not given a new message will be cretaed.
            Defaults to `None`.
        
        Returns
        -------
        pagination : `Mone` or ``Pagination``
            If `pages` is an empty container, returns `None`.
        """
        if not pages:
            return None
        
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.pages=pages
        self.page=0
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.message=message
        self.timeout=timeout
        self.timeouter=None
        
        try:
            if message is None:
                message = await client.message_create(channel,embed=pages[0])
                self.message=message
            else:
                await client.message_edit(message,embed=pages[0])
            
            if not channel.cached_permissions_for(client).can_add_reactions:
                return self
            
            if len(self.pages)>1:
                for emoji in self.EMOJIS:
                    await client.reaction_add(message,emoji)
            else:
                await client.reaction_add(message,self.CANCEL)
        except BaseException as err:
            if isinstance(err,ConnectionError):
                return None
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return None
            
            raise
        
        self.timeouter=Timeouter(self,timeout=timeout)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    async def __call__(self, client, event):
        """
        Called when a reeaction is added or removed from the respective message.
        
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
        
        emoji = event.emoji
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag=GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            
            if emoji is self.RIGHT:
                page=self.page+1
                break
            
            if emoji is self.CANCEL:
                self.task_flag=GUI_STATE_CANCELLED
                try:
                    await client.message_delete(self.message)
                except BaseException as err:
                    self.cancel()
                    
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}.__call__',err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.LEFT2:
                page=0
                break
            
            if emoji is self.RIGHT2:
                page=len(self.pages)-1
                break
            
            return
        
        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1
        
        if self.page==page:
            return

        self.page=page
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        
        try:
            await client.message_edit(self.message,embed=self.pages[page])
        except BaseException as err:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err,ConnectionError):
                # no internet
                return
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.invalid_access, # client removed
                            ):
                    return
            
            # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client,f'{self!r}.__call__',err)
            return
        
        if self.task_flag==GUI_STATE_CANCELLING:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            
            try:
                await client.message_delete(self.message)
            except BaseException as err:
                
                if isinstance(err,ConnectionError):
                    # no internet
                    return
                
                if isinstance(err,DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, #message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                await client.events.error(client,f'{self!r}.__call__',err)
                return
            
            return
            
        self.task_flag=GUI_STATE_READY
        self.timeouter.set_timeout(self.timeout)
    
    async def _canceller(self, exception,):
        """
        Used when the ``Pagination`` is cancelled.
        
        First of all removes the Pagination ,so it will not wait for reaction events, then sets the ``.task_flag``
        of the ``Pagination`` to `GUI_STATE_CANCELLED`.
        
        If `exception` is given as `TimeoutError`, then removes the ``Pagination``'s reactions from the respective
        message.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            Exception to cancel the ``Pagination`` with.
        """
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self.task_flag=GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception,TimeoutError):
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
                    
                    await client.events.error(client,f'{self!r}._canceller',err)
                    return
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self, exception=None):
        """
        Cancels the pagination, if it is not cancelled yet.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            Exception to cancel the pagination with. Defaults to `None`
        """
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self,exception),KOKORO)
    
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
        
        task_flag=self.task_flag
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
    UP      = BUILTIN_EMOJIS['arrow_up_small']
    DOWN    = BUILTIN_EMOJIS['arrow_down_small']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    SELECT  = BUILTIN_EMOJIS['ok']
    CANCEL  = BUILTIN_EMOJIS['x']
    EMOJIS_RESTRICTED = (UP,DOWN,SELECT,CANCEL)
    EMOJIS  = (UP,DOWN,LEFT,RIGHT,SELECT,CANCEL)
    
    __slots__ = ('canceller', 'channel', 'client', 'embed', 'message', 'selected',
        'choices', 'task_flag', 'timeout', 'timeouter', 'prefix', 'selecter')
    
    async def __new__(cls, client, channel, choices, selecter, embed=Embed(), timeout=240., message=None, prefix=None):
        if (prefix is not None) and len(prefix)>100:
            raise ValueError(f'Please pass a prefix, what is shorter than 100 characters, got {prefix!r}')
        
        result_ln=len(choices)
        if result_ln<2:
            if result_ln==1:
                choice = choices[0]
                if isinstance(choice, tuple):
                    await selecter(client, channel, message, *choice)
                else:
                    await selecter(client, channel, message, choice)
            return None
        
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.choices=choices
        self.selecter=selecter
        self.selected = 0
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.message=message
        self.timeout=timeout
        self.timeouter=None
        self.prefix=prefix
        self.embed=embed
        
        try:
            if message is None:
                message = await client.message_create(channel,embed=self._render_embed())
                self.message=message
            else:
                await client.message_edit(message,embed=self._render_embed())
            
            if not channel.cached_permissions_for(client).can_add_reactions:
                return self
            
            for emoji in (self.EMOJIS if len(choices)>10 else self.EMOJIS_RESTRICTED):
                await client.reaction_add(message,emoji)
        except BaseException as err:
            if isinstance(err,ConnectionError):
                return self
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return self
            
            raise
        
        self.timeouter=Timeouter(self,timeout=timeout)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    def _render_embed(self):
        selected = self.selected
        choices = self.choices
        index = (selected//10)*10
        end = index+10
        if len(choices)<end:
            end = len(choices)
        
        parts=[]
        prefix=self.prefix
        left_length = 195
        if (prefix is not None):
            left_length-=len(prefix)
        
        while True:
            title=choices[index]
            if isinstance(title,tuple):
                if not title:
                    title=''
                else:
                    title = title[0]
            
            if not isinstance(title,str):
                title = str(title)
            
            if len(title)>left_length:
                space_position = title.rfind(' ',left_length-25,left_length)
                if space_position==-1:
                    space_position=left_length-3
                
                title = title[:space_position]+'...'
            
            if index==selected:
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
            
            index=index+1
            if index==end:
                break
        
        embed=self.embed
        embed.description=''.join(parts)
        
        current_page = (selected//10)+1
        limit = len(choices)
        page_limit = (limit//10)+1
        start = end-9
        if start<1:
            start=1
        if end==len(choices):
            end-=1
        limit-=1
        
        embed.add_footer(f'Page {current_page}/{page_limit}, {start} - {end} / {limit}, selected: {selected+1}')
        return embed
    
    async def __call__(self,client,event):
        if event.user.is_bot:
            return
        
        if (event.emoji not in (self.EMOJIS if len(self.choices)>10 else self.EMOJIS_RESTRICTED)):
            return
        
        client=self.client
        message=self.message
        
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if event.emoji is self.CANCEL:
                    self.task_flag=GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
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
                self.task_flag=GUI_STATE_CANCELLED
                try:
                    await client.message_delete(message)
                except BaseException as err:
                    self.cancel()
                    
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}.__call__',err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.SELECT:
                self.task_flag=GUI_STATE_SWITCHING_CTX
                self.cancel()
                
                try:
                    if self.channel.cached_permissions_for(client).can_manage_messages:
                        await client.reaction_clear(message)
                    
                    else:
                        for emoji in self.EMOJIS:
                            await client.reaction_delete_own(message,emoji)
                except BaseException as err:
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_message, # message already deleted
                                ERROR_CODES.unknown_channel, # channel deleted
                                ERROR_CODES.invalid_access, # client removed
                                ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}.__call__',err)
                    return
                
                selecter = self.selecter
                try:
                    choice = self.choices[self.selected]
                    channel = self.channel
                    if isinstance(choice, tuple):
                        await selecter(client, channel, message, *choice)
                    else:
                        await selecter(client, channel, message, choice)
                except BaseException as err:
                    await client.events.error(client,f'{self!r}.__call__ when calling {selecter!r}',err)
                return
            
            return
        
        if selected<0:
            selected=0
        elif selected>=len(self.choices):
            selected=len(self.choices)-1
        
        if self.selected==selected:
            return
        
        self.selected=selected
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(message,embed=self._render_embed())
        except BaseException as err:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err,ConnectionError):
                # no internet
                return
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message already deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                            ):
                    return
            
            # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client,f'{self!r}.__call__',err)
            return

        if self.task_flag==GUI_STATE_CANCELLING:
            self.task_flag=GUI_STATE_CANCELLED
            try:
                await client.message_delete(message)
            except BaseException as err:
                
                if isinstance(err,ConnectionError):
                    # no internet
                    return
                
                if isinstance(err,DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel,
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                await client.events.error(client,f'{self!r}.__call__',err)
                return
            
            self.cancel()
            return
        
        self.task_flag=GUI_STATE_READY
        self.timeouter.set_timeout(self.timeout)
    
    async def _canceller(self,exception,):
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self.task_flag=GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception,TimeoutError):
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
                    
                    await client.events.error(client,f'{self!r}._canceller',err)
                    return
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None), KOKORO)

    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' client=', repr(self.client),
            ', choices=', repr(len(self.choices)),
            ', selected=', repr(self.selected),
            ', channel=', repr(self.channel),
            ', selecter=', repr(self.selecter),
                ]
        
        prefix=self.prefix
        if (prefix is not None):
            result.append(', prefix=')
            result.append(repr(prefix))
        
        result.append(', task_flag=')
        task_flag=self.task_flag
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
    __slots__=('canceller', 'check', 'event', 'future', 'target', 'timeouter')
    def __init__(self, future, check, target, event, timeout):
        self.canceller=self.__class__._canceller
        self.future=future
        self.check=check
        self.event=event
        self.target=target
        self.timeouter=Timeouter(self,timeout)
        event.append(target, self)
    
    async def __call__(self, client, *args):
        result = self.check(*args)
        if type(result) is bool:
            if not result:
                return
                
            if len(args)==1:
                args=args[0]
        
        else:
            args=(*args,result,)
        
        self.future.set_result_if_pending(args,)
        
        self.cancel()
        
    async def _canceller(self,exception):
        self.event.remove(self.target, self)
        if exception is None:
            self.future.set_result_if_pending(None)
            return
        
        self.future.set_exception_if_pending(exception)
        
        if not isinstance(exception,TimeoutError):
            return

        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
    
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None),self.future._loop)

def wait_for_reaction(client, message, check, timeout):
    future = Future(KOKORO)
    WaitAndContinue(future, check, message ,client.events.reaction_add, timeout)
    return future

def wait_for_message(client, channel, check, timeout):
    future=Future(KOKORO)
    WaitAndContinue(future, check, channel, client.events.message_create, timeout)
    return future

class prefix_by_guild(dict):
    __slots__=('default', 'orm',)
    
    def __init__(self,default,*orm):
        if type(default) is not str:
            raise TypeError (f'Default expected type str, got type {default.__class__.__name__}')
        self.default=default
        if orm:
            if len(orm)!=3:
                raise TypeError(f'Expected \'engine\', \'table\', \'model\' for orm, but got {len(orm)} elements')
            self.orm=orm
            Task(self._load_orm(),KOKORO)
            KOKORO.wakeup()
            
    def __call__(self,message):
        guild=message.guild
        if guild is not None:
            return self.get(guild.id,self.default)
        return self.default
    
    def __getstate__(self):
        return self.default
    def __setstate__(self,state):
        self.default=state
        self.orm=None
    
    def add(self,guild,prefix):
        guild_id=guild.id
        if guild_id in self:
            if prefix==self.default:
                del self[guild_id]
                if self.orm is not None:
                    Task(self._remove_prefix(guild_id),KOKORO)
                    KOKORO.wakeup()
                return True
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._modify_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
        else:
            if prefix==self.default:
                return False
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._add_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
    
    def to_json_serializable(self):
        result=dict(self)
        result['default']=self.default
        return result
    
    @classmethod
    def from_json_serialization(cls,data):
        self=dict.__new__(cls)
        self.default=data.pop('default')
        for id_,prefix in data.items():
            self[int(id_)]=prefix
        self.orm=None
        return self
    
    async def _load_orm(self,):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            result = await connector.execute(table.select())
            prefixes = await result.fetchall()
            for item in prefixes:
                self[item.guild_id]=item.prefix
    
    async def _add_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.insert(). \
                values(guild_id=guild_id,prefix=prefix))
    
    async def _modify_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.update(). \
                values(prefix=prefix). \
                where(model.guild_id==guild_id))
    
    async def _remove_prefix(self,guild_id):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.delete(). \
                where(model.guild_id==guild_id))
    
    def __repr__(self):
        return f'<{self.__class__.__name__} default=\'{self.default}\' len={self.__len__()}>'
    
    # because it is a builtin subclass, it will have __str__, so we overwrite that as well
    __str__=__repr__
    
class _CD_unit(object):
    __slots__=('expires_at', 'uses_left',)
    def __init__(self,expires_at,uses_left):
        self.expires_at=expires_at
        self.uses_left=uses_left
    
    def __repr__(self):
        return f'{self.__class__.__name__}(expires_at={self.expires_at}, uses_left={self.uses_left})'

class CooldownWrapper(CommandWrapper):
    def shared(self, weight=0, func=None):
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(f'`weight` can be given as `int` instance, got {weight_type.__name__}.')
        
        source_wrapper = self.wrapper
        if weight == 0:
            weight = source_wrapper.weight
        
        new_wrapper = object.__new__(type(self))
        new_wrapper.checker= source_wrapper.checker
        new_wrapper.reset  = source_wrapper.reset
        new_wrapper.cache  = source_wrapper.cache
        new_wrapper.weight = weight
        new_wrapper.limit  = source_wrapper.limit+source_wrapper.weight-weight
        
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
    
    ```py
    from hata import DiscordException, CancelledError, sleep
    from hata.commands. import Cooldown
    
    class CooldownHandler:
        __slots__=('cache',)
        
        def __init__(self):
            self.cache = {}
        
        async def __call__(self, client, message, command, time_left):
            user_id = message.author.id
            try:
                notification, waiter = self.cache[user_id]
            except KeyError:
                pass
            else:
                if notification.channel is message.channel:
                    try:
                        await client.message_edit(notification,
                            f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
                    except DiscordException:
                        pass
                    return
                
                waiter.cancel()
            
            try:
                notification = await client.message_create(message.channel,
                    f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
            except DiscordException:
                return
            
            waiter = client.loop.create_task(self.waiter(client, user_id, notification)
            self.cache[user_id] = (notification, waiter)
    
        async def waiter(self, client, user_id, notification):
            try:
                await sleep(30.)
            except CancelledError:
                pass
            del self.cache[user_id]
            try:
                await client.message_delete(notification)
            except DiscordException:
                pass
    
    @Bot.commands
    @Cooldown('user', 30., handler=CooldownHandler())
    async def ping(client, message):
        await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')
    ```
    
    **Using shared cooldowns:**

    ```py
    from hata import Embed
    from hata.ext.commandsi mport Converter, ConverterFlag
    
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
    cache : `dict` of (``DiscordEntity``, ``_CD_unit``) items
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
        # Validate float.
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
                raise TypeError(f'The given reset is no `float`, neither other numeric convertable to it, got '
                    f'{reset_type.__name__}.')
            
            reset = __float__(reset)
            
        limit_type = limit.__class__
        if limit_type is int:
            pass
        elif issubclass(limit_type, int):
            limit = int(limit)
        else:
            raise TypeError(f'`limit` can be given as `int` instance, got {limit_type.__name__}.')
        
        weight_type = weight.__class__
        if weight_type is int:
            pass
        elif issubclass(weight_type, int):
            weight = int(weight)
        else:
            raise TypeError(f'`weight` can be given as `int` instance, got {weight_type.__name__}.')
        
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
        __slots__ = ('parent', 'handler')
        def __init__(self, parent, handler):
            self.parent = parent
            self.handler = handler
        
        def __call__(self, func):
            return CooldownWrapper(func, self.parent, self.handler)
    
    async def __call__(self, client, message):
        value = self.checker(self, message)
        if not value:
            yield True
            return
        
        yield False
        yield value-monotonic()
        return
    
    @staticmethod
    def _check_user(self,message):
        id_=message.author.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=monotonic()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            KOKORO.call_at(at_,dict.__delitem__,cache,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at
    
    @staticmethod
    def _check_channel(self,message):
        id_=message.channel.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=monotonic()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            KOKORO.call_at(at_,dict.__delitem__,cache,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at
    
    #returns -1. if non guild
    @staticmethod
    def _check_guild(self, message):
        channel=message.channel
        if channel.type in (1,3):
            return -1.
        else:
            id_=channel.guild.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=monotonic()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            KOKORO.call_at(at_,dict.__delitem__,cache, id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at
