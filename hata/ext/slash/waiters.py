__all__ = ('iter_component_interaction', 'wait_for_component_interaction',)

from collections import deque

from ...backend.futures import Future
from ...backend.event_loop import LOOP_TIME

from ...discord.client_core import APPLICATION_ID_TO_CLIENT, KOKORO
from ...discord.message import Message
from ...discord.parsers import InteractionEvent
from ...discord.client import Client


class Timeouter:
    """
    Executes timing out feature on ``Pagination`` and on other familiar types.
    
    Attributes
    ----------
    handle : `None` or ``TimerHandle``
        Handle to wake_up the timeouter with it's `._step` function.
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
        self.handle = KOKORO.call_later(timeout, type(self)._step, self)
    
    
    def _step(self):
        """
        Executes a timeouter cycle.
        
        Increases the timeout if ``.timeout`` was updated. If not and applicable, calls it's ``.owner``'s
        `.canceller` with `TimeoutError` and unlinks ``.owner`` and `owner.canceller`,
        """
        timeout = self.timeout
        if timeout > 0.0:
            self.handle = KOKORO.call_later(timeout, type(self)._step, self)
            self.timeout = 0.0
            return
        
        self.handle = None
        owner = self.owner
        if owner is None:
            return
        
        self.owner = None
        
        owner.cancel(TimeoutError())
    
    
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
            handle.cancel()
            self._step()
            return
        
        now = LOOP_TIME()
        next_step = self.handle.when
        
        planed_end = now+value
        if planed_end < next_step:
            handle.cancel()
            self.handle = KOKORO.call_at(planed_end, type(self)._step, self)
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


class ComponentInteractionWaiter:
    """
    Waiter class for button press.
    
    Parameters
    ----------
    _check : `None` or `callable`
        The check to call to validate whether the response is sufficient.
    _finished : `bool`
        Whether the waiter finished.
    _future : ``Future``
        The waiter future.
    _message : ``Message``
        The waited interaction component's message.
    _timeouter : `None` or ``Timeouter``
        Executes the timeout feature on the waiter.
    """
    __slots__ = ('_check', '_finished', '_future', '_message', '_timeouter')
    def __new__(cls, client, message, check, timeout):
        """
        Creates a new ``ComponentInteractionWaiter`` instance with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who will wait for component interaction.
        message : ``Message``
            The waited interaction component's message.
        check : `None` or `callable`
            The check to call to validate whether the response is sufficient.
        timeout : `None` or `float`
            The timeout till the waiting is done. If expires, `TimeoutError` is raised to ``._future``.
        """
        self = object.__new__(cls)
        self._finished = False
        self._future = Future(KOKORO)
        self._message = message
        self._check = check
        self._timeouter = None
        
        if timeout is None:
            self._timeouter = Timeouter(self, timeout)
        
        client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def __call__(self, event):
        """
        Calls the component interaction waiter checking whether the respective event is sufficient setting the waiter's
        result.
        
        This method is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event
        """
        check = self._check
        if check is None:
            self._future.set_result_if_pending(event)
        else:
            try:
                result = check(event)
            except BaseException as err:
                self._future.set_exception_if_pending(err)
            else:
                if type(result) is bool:
                    if result:
                        self._future.set_result_if_pending(event)
                    else:
                        return
                
                else:
                    self._future.set_result_if_pending((event, result))
        
        self.cancel()
    
    
    def __await__(self):
        """Awaits the waiter's result."""
        return (yield from self._future)
    
    
    def cancel(self, exception=None):
        """
        Cancels the component waiter.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            The exception to cancel the waiter with.
        """
        if self._finished:
            return
        
        self._finished = False
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        message = self._message
        client = get_client_from_message(message)
        client.slasher.remove_component_interaction_waiter(message, self)
        
        future = self._future
        if exception is None:
            future.set_result_if_pending(None)
        else:
            future.set_exception_if_pending(exception)


class ComponentInteractionIterator:
    """
    Component interaction iterator which goes brr.
    
    Parameters
    ----------
    _check : `None` or `callable`
        The check to call to validate whether the response is sufficient.
    _exception : `None` or ``BaseException``
        Whether the waiter finished with an exception.
    _future : `None` or ``Future``
        The waiter future.
    _message : ``Message``
        The waited interaction component's message.
    _queue : `None` or `collections.deque`
        A deque used to queue up interactions if needed.
    _timeouter : `None` or ``Timeouter``
        Executes the timeout feature on the waiter.
    timeout : `None` or `float`
        The timeout after `TimeoutError` should be raised if no sufficient event is received.
    """
    __slots__ = ('_check', '_exception', '_future', '_message', '_queue', '_timeouter', 'timeout')
    def __new__(cls, client, message, check, timeout):
        """
        Creates a new ``ComponentInteractionWaiter`` instance with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who will wait for component interaction.
        message : ``Message``
            The waited interaction component's message.
        check : `None` or `callable`
            The check to call to validate whether the response is sufficient.
        timeout : `None` or `float`
            The timeout till the waiting is done. If expires, `TimeoutError` is raised to ``._future``.
        """
        self = object.__new__(cls)
        self._exception = None
        self._future = None
        self._message = message
        self._check = check
        self._timeouter = None
        self._queue = None
        self.timeout = timeout
        
        if timeout is None:
            self._timeouter = Timeouter(self, timeout)
        
        client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def __call__(self, event):
        """
        Calls the component interaction iterator checking whether the respective event is sufficient setting the waiter's
        result.
        
        This method is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event
        """
        check = self._check
        if check is None:
            self._feed_result(event)
        else:
            try:
                result = check(event)
            except BaseException as err:
                self.cancel(err)
            else:
                if type(result) is bool:
                    if result:
                        self._feed_result(event)
                    else:
                        return
                
                else:
                    self._feed_result((event, result))
    
    
    def _feed_result(self, result):
        """
        Feeds result to the iterators output.
        
        Parameters
        ----------
        result : `Any`
            The result to feed.
        """
        future = self._future
        if future is None:
            queue = self._queue
            if queue is None:
                queue = self._queue = deque()
            
            queue.append(result)
        else:
            self._future.set_result_if_pending(result)
        
        # Lol
        timeout = self.timeout
        timeouter = self._timeouter
        if (timeout is not None) and (timeouter is not None):
            self._timeouter.set_timeout(timeout)
    
    
    def __await__(self):
        """Awaits the iterator's next result."""
        exception = self._exception
        if (exception is not None):
            raise exception
        
        future = self._future
        if (future is None):
            # As it should be
            queue = self._queue
            if queue is None:
                future = self._future = Future(KOKORO)
            else:
                result = queue.popleft()
                if not queue:
                    self._queue = None
                
                return result
        
        try:
            return (yield from future)
        finally:
            self._future = None
    
    
    def cancel(self, exception=None):
        set_exception = self._exception
        if (set_exception is not None):
            return
        
        if (exception is None):
            exception = StopAsyncIteration()
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        message = self._message
        client = get_client_from_message(message)
        client.slasher.remove_component_interaction_waiter(message, self)
        
        future = self._future
        if (future is not None):
            future.set_exception_if_pending(exception)


def get_client_from_message(message):
    """
    Tries the get the respective client instance form the message.
    
    RuntimeError
        The message or interaction is bound to a 3rd party application.
    """
    user = message.author
    if isinstance(user, Client):
        client = user
    else:
        application_id = message.application_id
        if application_id:
            try:
                client = APPLICATION_ID_TO_CLIENT[application_id]
            except KeyError as err:
                raise RuntimeError(f'The message is bound to a 3rd party application, got: {message!r}.') from err
        else:
            raise RuntimeError(f'The given message has no bound interaction, got {message!r}.')
    
    return client


async def get_interaction_client_and_message(event_or_message, timeout):
    """
    Gets the respective client and message if the given interaction event or message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message.
    timeout : `None` or `float`
        The maximal amount of time wait for interaction response.
    
    Returns
    -------
    client : ``Client``
        The client who executed the interaction or sent the message.
    message : ``Message``
        The interactions's message.
    
    Raises
    ------
    TimeoutError
        If interaction even was not received before timeout.
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent`` instance.
    RuntimeError
        - The message or interaction is bound to a 3rd party application.
        - The given message message has no bound interaction.
    """
    if isinstance(event_or_message, Message):
        message = event_or_message
        client = get_client_from_message(message)
    
    elif isinstance(event_or_message, InteractionEvent):
        message = await event_or_message.wait_for_response_message(timeout=timeout)
        
        try:
            client = APPLICATION_ID_TO_CLIENT[event_or_message.application_id]
        except KeyError as err:
            raise RuntimeError(f'The message or interaction is bound to a 3rd party application, got: '
                f'{event_or_message!r}.') from err
    
    else:
        raise TypeError(f'`event_or_message` can be either `{Message.__name__}` or `{InteractionEvent.__name__}` '
            f'instance, got {event_or_message.__class__.__name__}.')
    
    return client, message


async def wait_for_component_interaction(event_or_message, *, timeout=None, check=None):
    """
    Waits for interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message to wait component on.
    timeout : `None` or `float`, Optional (Keyword only)
        The maximal amount of time wait
    check : `None` or `callable`, Optional (Keyword only)
        Checks whether the received ``InteractionEvent`` instances pass the requirements.
    
    Returns
    ------
    interaction_event : ``InteractionEvent``
    
    Raises
    ------
    TimeoutError
        No component interaction was received in time
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent`` instance.
    RuntimeError
        - The message or interaction is bound to a 3rd party application.
        - The given message message has no bound interaction.
    """
    client, message = await get_interaction_client_and_message(event_or_message, timeout)
    return await ComponentInteractionWaiter(client, message, check, timeout)


async def iter_component_interaction(event_or_message, *, timeout=None, check=None):
    """
    Iterates component interactions.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message to wait component on.
    timeout : `None` or `float`, Optional (Keyword only)
        The maximal amount of time wait
    check : `None` or `callable`, Optional (Keyword only)
        Checks whether the received ``InteractionEvent`` instances pass the requirements.
    
    Yields
    ------
    interaction_event : ``InteractionEvent``
    
    Raises
    ------
    TimeoutError
        No component interaction was received in time
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent`` instance.
    RuntimeError
        - The message or interaction is bound to a 3rd party application.
        - The given message message has no bound interaction.
    """
    client, message = await get_interaction_client_and_message(event_or_message, timeout)
    
    component_interaction_iterator = ComponentInteractionIterator(client, message, check, timeout)
    while True:
        try:
            yield await component_interaction_iterator
        except:
            component_interaction_iterator.cancel()
            raise

