# -*- coding: utf-8 -*-
__all__ = ('ReactionAddWaitfor', 'ReactionDeleteWaitfor', 'MessageCreateWaitfor', 'WaitAndContinue',
    'wait_for_message', 'wait_for_reaction')

from ...backend import Task, Future
from ...discord.parsers import EventWaitforBase
from ...discord.client_core import KOKORO

from .utils import Timeouter

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

class MessageCreateWaitfor(EventWaitforBase):
    """
    Implements waiting for `message_create` events.
    
    Attributes
    ----------
    waitfors : `WeakValueDictionary` of (``DiscordEntity``, `async-callable`) items
        An auto-added container to store `entity` - `async-callable` pairs.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = `'message_create'`
        Predefined name to what the event handler will be added.
    """
    __slots__ = ()
    __event_name__ = 'message_create'


class WaitAndContinue:
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
        self.timeouter = Timeouter(self, timeout)
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
