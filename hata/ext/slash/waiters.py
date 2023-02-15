__all__ = ('Timeouter', 'iter_component_interactions', 'wait_for_component_interaction',)

from collections import deque

from scarletio import Future, LOOP_TIME

from ...discord.client import Client
from ...discord.core import APPLICATION_ID_TO_CLIENT, KOKORO
from ...discord.interaction import InteractionEvent
from ...discord.message import Message

from .components import acknowledge_component_interaction


class Timeouter:
    """
    Executes timing out feature on ``Pagination`` and on other familiar types.
    
    Attributes
    ----------
    _handle : `None`, ``TimerHandle``
        Handle to wake_up the timeouter with it's `._step` function.
        Set to `None`, when the respective timeout is over or if the timeout is cancelled.
    _owner : `Any`
        The object what uses the timeouter.
        Set to `None`, when the respective timeout is over or if the timeout is cancelled.
    _timeout : `float`
        The time with what the timeout will be expired when it's current waiting cycle is over.
    """
    __slots__ = ('_handle', '_owner', '_timeout')
    
    
    def __init__(self, owner, timeout):
        """
        Creates a new ``Timeouter`` with the given `owner` and `timeout`.
        
        Parameters
        ----------
        owner : `Any`
            The object what uses the timeouter.
        timeout : `float`
            The time with what the timeout will be expired when it's current waiting cycle is over.
        """
        self._owner = owner
        self._timeout = 0.0
        self._handle = KOKORO.call_later(timeout, type(self)._step, self)
    
    
    def _step(self):
        """
        Executes a timeouter cycle.
        
        Increases the timeout if ``.timeout`` was updated. If not and applicable, calls it's ``.owner``'s
        `.canceller` with `TimeoutError` and unlinks ``.owner`` and `owner.canceller`,
        """
        timeout = self._timeout
        if timeout > 0.0:
            self._handle = KOKORO.call_later(timeout, type(self)._step, self)
            self._timeout = 0.0
            return
        
        self._handle = None
        owner = self._owner
        if (owner is not None):
            self._owner = None
            owner.cancel(TimeoutError())
    
    
    def cancel(self):
        """
        Cancels the timeouter.
        
        Should be called by the timeouter's owner when it is cancelled with an other exception.
        """
        handle = self._handle
        if (handle is not None):
            self._handle = None
            handle.cancel()
            
            self._owner = None
    
    
    def set_timeout(self, value):
        """
        Sets the timeouter of the timeouter to the given value.
        """
        handle = self._handle
        if handle is None:
            # Cannot change timeout of expired timeouter
            return
        
        if value <= 0.0:
            self._timeout = 0.0
            handle.cancel()
            self._step()
            return
        
        now = LOOP_TIME()
        next_step = handle.when
        
        planed_end = now + value
        if planed_end < next_step:
            handle.cancel()
            self._handle = KOKORO.call_at(planed_end, type(self)._step, self)
            return
        
        self._timeout = planed_end - next_step
    
    
    def get_expiration_delay(self):
        """
        Returns after how much time the timeouter will expire.
        
        If the timeouter already expired, returns `0.0˙.
        
        Returns
        -------
        time_left : `float`
        """
        handle = self._handle
        if handle is None:
            return 0.0
        
        return handle.when - LOOP_TIME() + self._timeout


class ComponentInteractionWaiter:
    """
    Waiter class for button press.
    
    Parameters
    ----------
    _check : `None`, `callable`
        The check to call to validate whether the response is sufficient.
    _finished : `bool`
        Whether the waiter finished.
    _future : ``Future``
        The waiter future.
    _message : ``Message``
        The waited interaction component's message.
    _timeouter : `None`, ``Timeouter``
        Executes the timeout feature on the waiter.
    """
    __slots__ = ('_check', '_finished', '_future', '_message', '_timeouter')
    
    def __new__(cls, client, message, check, timeout):
        """
        Creates a new ``ComponentInteractionWaiter`` with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who will wait for component interaction.
        message : ``Message``
            The waited interaction component's message.
        check : `None`, `callable`
            The check to call to validate whether the response is sufficient.
        timeout : `None`, `float`
            The timeout till the waiting is done. If expires, `TimeoutError` is raised to ``._future``.
        """
        self = object.__new__(cls)
        self._finished = False
        self._future = Future(KOKORO)
        self._message = message
        self._check = check
        self._timeouter = None
        
        if (timeout is not None):
            self._timeouter = Timeouter(self, timeout)
        
        client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def __call__(self, interaction_event):
        """
        Calls the component interaction waiter checking whether the respective event is sufficient setting the waiter's
        result.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event
        """
        check = self._check
        if check is None:
            self._future.set_result_if_pending(interaction_event)
            should_acknowledge = False
        else:
            try:
                result = check(interaction_event)
            except BaseException as err:
                self._future.set_exception_if_pending(err)
                should_acknowledge = False
            else:
                if isinstance(result, bool):
                    if result:
                        self._future.set_result_if_pending(interaction_event)
                        should_acknowledge = False
                    else:
                        should_acknowledge = True
                
                else:
                    self._future.set_result_if_pending((interaction_event, result))
                    should_acknowledge = False
        
        if should_acknowledge:
            await acknowledge_component_interaction(interaction_event)
        else:
            self.cancel()
    
    
    def __await__(self):
        """Awaits the waiter's result."""
        return (yield from self._future)
    
    
    def cancel(self, exception = None):
        """
        Cancels the component waiter.
        
        Parameters
        ----------
        exception : `None`, ``BaseException`` = `None`, Optional
            The exception to cancel the waiter with.
        """
        if self._finished:
            return
        
        self._finished = True
        
        timeouter = self._timeouter
        if (timeouter is not None):
            self._timeouter = None
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
    _check : `None`, `callable`
        The check to call to validate whether the response is sufficient.
    _exception : `None`, ``BaseException``
        Whether the waiter finished with an exception.
    _finished : `bool`
        Whether the interaction iterator is finished.
    _future : `None`, ``Future``
        The waiter future.
    _message : ``Message``
        The waited interaction component's message.
    _queue : `None`, `collections.deque`
        A deque used to queue up interactions if needed.
    _timeouter : `None`, ``Timeouter``
        Executes the timeout feature on the waiter.
    count : `int`
        The maximal amount of events to yield.
    timeout : `None`, `float`
        The timeout after `TimeoutError` should be raised if no sufficient event is received.
    """
    __slots__ = (
        '_check', '_exception', '_finished', '_future', '_message', '_queue', '_timeouter', 'count', 'timeout'
    )
    
    def __new__(cls, client, message, check, timeout, count):
        """
        Creates a new ``ComponentInteractionWaiter`` with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who will wait for component interaction.
        message : ``Message``
            The waited interaction component's message.
        check : `None`, `callable`
            The check to call to validate whether the response is sufficient.
        timeout : `None`, `float`
            The timeout till the waiting is done. If expires, `TimeoutError` is raised to ``._future``.
        count : `int`
            The maximal amount of events to yield.
        """
        self = object.__new__(cls)
        self._exception = None
        self._future = None
        self._finished = False
        self._message = message
        self._check = check
        self._timeouter = None
        self._queue = None
        self.timeout = timeout
        self.count = count
        
        if (timeout is not None):
            self._timeouter = Timeouter(self, timeout)
        
        client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def __call__(self, interaction_event):
        """
        Calls the component interaction iterator checking whether the respective event is sufficient setting the waiter's
        result.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event
        """
        check = self._check
        if check is None:
            self._feed_result(interaction_event)
            should_acknowledge = False
        else:
            try:
                result = check(interaction_event)
            except BaseException as err:
                self.cancel(err)
                should_acknowledge = False
            else:
                if isinstance(result, bool):
                    if result:
                        self._feed_result(interaction_event)
                        should_acknowledge = False
                    else:
                        should_acknowledge = True
                
                else:
                    self._feed_result((interaction_event, result))
                    should_acknowledge = False
        
        if should_acknowledge:
            await acknowledge_component_interaction(interaction_event)
    
    
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
        
        count = self.count - 1
        if count:
            self.count = count
        else:
            self.cancel()
    
    def __await__(self):
        """Awaits the iterator's next result."""
        future = self._future
        if (future is None):
            # As it should be
            queue = self._queue
            if queue is None:
                # Check finished here :KoishiWink:
                if self._finished:
                    exception = self._exception
                    if (exception is None):
                        return None
                    else:
                        raise exception
                
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
    
    
    def cancel(self, exception = None):
        """
        Cancels the component iterator.
        
        Parameters
        ----------
        exception : `None`, ``BaseException`` = `None`, Optional
            The exception to cancel the waiter with.
        """
        if self._finished:
            return
        
        self._finished = True
        self._exception = exception
        
        timeouter = self._timeouter
        if (timeouter is not None):
            self._timeouter = None
            timeouter.cancel()
        
        message = self._message
        client = get_client_from_message(message)
        client.slasher.remove_component_interaction_waiter(message, self)
        
        future = self._future
        if (future is not None):
            if (exception is None):
                future.set_result_if_pending(None)
            else:
                future.set_exception_if_pending(exception)


def get_client_from_message(message):
    """
    Tries the get the respective client instance form the message.
    
    Raises
    ------
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
                raise RuntimeError(
                    f'The message is bound to a 3rd party application, got: {message!r}.'
                ) from err
        else:
            raise RuntimeError(
                f'The given message has no bound interaction, got {message!r}.'
            )
    
    return client


def get_client_from_interaction_event(interaction_event):
    """
    Gets the respective client of an interaction event.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The interaction event.
    
    Returns
    -------
    client : ``Client``
        The client who executed the interaction.
    
    Raises
    ------
    RuntimeError
        - The interaction is bound to a 3rd party application.
    """
    try:
        client = APPLICATION_ID_TO_CLIENT[interaction_event.application_id]
    except KeyError as err:
        raise RuntimeError(
            f'The message or interaction is bound to a 3rd party application, got: {interaction_event!r}.'
        ) from err
    
    return client


async def get_interaction_client_and_message(event_or_message, timeout):
    """
    Gets the respective client and message if the given interaction event or message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message.
    timeout : `None`, `float`
        The maximal amount of time wait for interaction response.
    
    Returns
    -------
    client : ``Client``
        The client who executed the interaction or sent the message.
    message : ``Message``
        The interaction's message.
    
    Raises
    ------
    TimeoutError
        If interaction even was not received before timeout.
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent``.
    RuntimeError
        - The message or interaction is bound to a 3rd party application.
        - The given message message has no bound interaction.
    """
    if isinstance(event_or_message, Message):
        message = event_or_message
        client = get_client_from_message(message)
    
    elif isinstance(event_or_message, InteractionEvent):
        message = await event_or_message.wait_for_response_message(timeout = timeout)
        client = get_client_from_interaction_event(event_or_message)
    
    else:
        raise TypeError(
            f'`event_or_message` can be `{Message.__name__}`, `{InteractionEvent.__name__}` , got '
            f'{event_or_message.__class__.__name__}; {event_or_message!r}.'
        )
    
    return client, message


async def wait_for_component_interaction(event_or_message, *, timeout = None, check = None):
    """
    Waits for interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message to wait component on.
    timeout : `None`, `float` = `None`, Optional (Keyword only)
        The maximal amount of time wait
    check : `None`, `callable` = `None`, Optional (Keyword only)
        Checks whether the received ``InteractionEvent``-s pass the requirements.
    
    Returns
    ------
    interaction_event : ``InteractionEvent``
    
    Raises
    ------
    TimeoutError
        No component interaction was received in time
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent``.
    RuntimeError
        - The message or interaction is bound to a 3rd party application.
        - The given message message has no bound interaction.
    """
    client, message = await get_interaction_client_and_message(event_or_message, timeout)
    return await ComponentInteractionWaiter(client, message, check, timeout)


async def iter_component_interactions(event_or_message, *, timeout = None, check = None, count=-1):
    """
    Iterates component interactions.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message to wait component on.
    timeout : `None`, `float` = `None`, Optional (Keyword only)
        The maximal amount of time wait
    check : `None`, `callable` = `None`, Optional (Keyword only)
        Checks whether the received ``InteractionEvent``-s pass the requirements.
    count : `int` = `-1`, Optional (Keyword only)
        The maximal amount of events to yield.
        
        Giving it as negative number will yield infinitely.
    
    Yields
    ------
    interaction_event : ``InteractionEvent``
    
    Raises
    ------
    TimeoutError
        No component interaction was received in time
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent``.
    RuntimeError
        - The message or interaction is bound to a 3rd party application.
        - The given message message has no bound interaction.
    """
    client, message = await get_interaction_client_and_message(event_or_message, timeout)
    
    # First do validation, then check.
    if not count:
        return
    
    component_interaction_iterator = ComponentInteractionIterator(client, message, check, timeout, count)
    try:
        while True:
            result = await component_interaction_iterator
            if result is None:
                return
            
            yield result
            continue
    finally:
        component_interaction_iterator.cancel()
