# -*- coding: utf-8 -*-
__all__ = ('APPLICATION_COMMANDS', 'APPLICATIONS', 'CHANNELS', 'CLIENTS', 'DISCOVERY_CATEGORIES', 'EMOJIS', 'EULAS',
    'GUILDS', 'INTEGRATIONS', 'INVITES', 'KOKORO', 'MESSAGES', 'ROLES', 'TEAMS', 'USERS', 'start_clients',
    'stop_clients', )

import sys, gc
from time import perf_counter
from threading import current_thread

from ..backend.utils import WeakValueDictionary
from ..backend.futures import Future, sleep, CancelledError, future_or_timeout, Task
from ..backend.event_loop import EventThread

Client = NotImplemented

if (sys.hash_info.width >= 64):
    #if we have 64 bit system we can use array instead of list
    from array import array as Array
    def create_array():
        return Array('Q')
else:
    create_array = list
    
if sys.implementation.name == 'cpython':
    #on CPython bisect is 4~ times faster.
    import bisect
    _relative_index = bisect.bisect_left
    del bisect

else:
    def _relative_index(array, value):
        """
        Return the index where to insert item `value`  in list `array`, assuming `array` is sorted.
        
        Parameters
        ----------
        array : `Any`
            Any sorted indexable type.
        value : `Any`
            The object, which index in the array will be returned.
        
        Returns
        -------
        index : `int`
        """
        bot = 0
        top = len(array)
        while True:
            if bot < top:
                half = (bot+top)>>1
                if array[half] < value:
                    bot = half+1
                else:
                    top = half
                continue
            break
        return bot

class ClientDictionary(object):
    """
    A dictionary like data object for storing directly ``Client`` objects.
    
    Attributes
    ----------
    _elements : `list` of ``Client``
        The stored ``Client`` objects sorted by their id.
    _ids : (`array` of `uint64`) if sys.bit >= 64 else (`list` of `int`)
        The client's from `._elements` in a sorted form.
    _next : `int`
        The next added ``Client``'s auto id, if it has no id set.
    """
    __slots__ = ('_elements', '_ids', '_next',)
    
    def __init__(self):
        """
        Creates a ``ClientDictionary``.
        """
        self._elements = []
        self._ids = create_array()
        self._next = 1
    
    def append(self, client):
        """
        Appends the container with the passed ``Client``. If the client has no `.id` set yet, auto generates one for
        it.
        
        Parameters
        ----------
        client : ``Client``
            The client to add to the container.
        
        Raises
        ------
        RuntimeError:
            If an object with it's respective `.id` same as `client`'s is already added to the container.
        """
        id_ = client.id
        
        if id_ < 4194304:
            id_ = self._next
            client.id = id_
            self._next = id_+1
        
        array = self._ids
        index = _relative_index(array, id_)
        
        if index == len(array): #put it at the last place
            array.append(id_)
            self._elements.append(client)
            return
        
        if array[index] == id_:  #this object is already at the container, lets check it!
            if self._elements[index] is client:
                return
            #hah, got u!
            raise RuntimeError('Two different objects added with same id')
        
        #insert it at the right place
        array.insert(index, id_)
        self._elements.insert(index, client)
    
    def remove(self, client):
        """
        Removes the passed ``Client`` from the container. If the ``Client`` is not at the container, then will not
        raise.
        
        Parameters
        ----------
        client : ``Client``
        """
        id_ = client.id
        
        if id_ == 0:
            return #not in the container
        
        array = self._ids
        index = _relative_index(array, id_)
        
        if index == len(array): #not in the container
            return
        
        if array[index] != id_:  #this object is not at the container, lets remove it
            return
        
        del array[index]
        del self._elements[index]
    
    #familiar to normal remove
    def remove_by_id(self, id_):
        """
        Removes a ``Client`` by it's `.id` from the container. If no client is with the specified `.id` at the
        container, will not raise.
        
        Parameters
        ----------
        id_ : `int`
            The `.id` of a client to remove.
        """
        array = self._ids
        index = _relative_index(array, id_)
        
        if index == len(array): #not in the container
            return
        
        if array[index] != id_:  #this object is not at the container, lets remove it
            return
        
        del array[index]
        del self._elements[index]
    
    def update(self, client, new_id):
        """
        Updates a client at the container with a new id. Sets the new `.id` of the client and modifies it's position
        at the container if needed.
        
        Parameters
        ----------
        client : ``Client``
            The client, what's `.id` will be updated.
        new_id : `int`
            The new `.id` of the client
            
        Raises
        ------
        RuntimeError
            If an object with it's respective `.id` is same as `new_id` is already added to the container.
        """
        old_id = client.id
        client.id = new_id
        array = self._ids
        old_index = _relative_index(array, old_id)
        
        if old_index == len(array) or array[old_index] != old_id: #not in the container?
            self.append(client)
            return
        
        new_index=_relative_index(array,new_id)
        
        #above or under?
        if old_index < new_index:
            move = 1
            new_index-=1
        elif old_index > new_index:
            move = -1
        else:
            if array[new_index] == new_id:
                #hah, got u!
                raise RuntimeError('Two different objects added with same id')
            return

        #move ids
        index = old_index
        while True:
            if index == new_index:
                break
            array[index] = array[index+move]
            index += move
        #put our at the right place
        array[index] = new_id
        
        elements = self._elements
        #move object
        index = old_index
        while True:
            if index == new_index:
                break
            elements[index] = elements[index+move]
            index += move
        #put our at the right place
        elements[index] = client

    def __getitem__(self, id_):
        """Returns the client for the specified id."""
        array = self._ids
        index = _relative_index(array, id_)
        if index == len(array) or array[index] != id_:
            raise KeyError(f'{id_!r} is not in the {self.__class__.__name__}')
        return self._elements[index]
    
    def get(self, id_, default=None):
        """
        Returns the client of the client dictionary for the given id.
        
        Parameters
        ----------
        default : `Any`, Optional
            Default value to return value if the client is not found.
        
        Returns
        -------
        client : ``Client`` or `default`
        """
        array = self._ids
        index = _relative_index(array, id_)
        if index == len(array) or array[index] != id_:
            return default
        return self._elements[index]
    
    def __contains__(self, client):
        """Returns whether the client is at the container."""
        id_ = client.id
        array = self._ids
        index = _relative_index(array, id_)
        if index == len(array):
            return False
        return (array[index] == id_)
    
    def __len__(self):
        """Returns the length of the container."""
        return len(self._ids)
    
    def index(self, client):
        """
        Returns the index, where the container stores the specific client.
        
        Parameters
        ----------
        client : ``Client``
            The client, what's index will be returned.
        
        Returns
        -------
        index : `int`
        
        Raises
        ------
        ValueError
            The client is not at the container.
        """
        id_ = client.id
        array = self._ids
        index = _relative_index(array, id_)
        if index == len(array) or array[index] != id_:
            raise ValueError(f'{client!r} is not in the {self.__class__.__name__}')
        return index
        
    def __iter__(self):
        """Returns an iterator over the clients stored by the container."""
        return iter(self._elements)

    def __reversed__(self):
        """Returns a reversed iterator over the clients stored by the container."""
        return reversed(self._elements)
    
    def count(self, client):
        """
        Counts how much time the passed client is at the container. Because the container contains only unique
        elements, it can return either `0` or `1`.
        
        Parameters
        ----------
        client : ``Client``
            The client to count.
        
        Returns
        -------
        count : `int`
        """
        id_ = client.id
        array = self._ids
        index = _relative_index(array, id_)
        if index == len(array):
            return 0
        if array[index] == id_:
            return 1
        return 0
    
    def copy(self):
        """
        Copies the container.
        
        Returns
        -------
        new : ``ClientDictionary``
        """
        new = list.__new__(type(self))
        new._ids = self._ids.copy()
        new._elements = self._elements.copy()
        new._next = self._next
        return new
    
    def __repr__(self):
        """Returns the representation of the container."""
        result = [self.__class__.__name__,'([']
        elements = self._elements
        stop = len(elements)
        if stop:
            stop -=1
            index = 0
            while index < stop:
                result.append(repr(elements[index]))
                result.append(', ')
                index += 1
            result.append(repr(elements[index]))
        result.append('])')
        
        return ''.join(result)


CHANNELS = WeakValueDictionary()
CLIENTS = ClientDictionary()
EMOJIS = WeakValueDictionary()
GUILDS = WeakValueDictionary()
INTEGRATIONS = WeakValueDictionary()
MESSAGES = WeakValueDictionary()
ROLES = WeakValueDictionary()
TEAMS = WeakValueDictionary()
USERS = WeakValueDictionary()
DISCOVERY_CATEGORIES = WeakValueDictionary()
EULAS = WeakValueDictionary()
APPLICATIONS = WeakValueDictionary()
INVITES = WeakValueDictionary()
APPLICATION_COMMANDS = WeakValueDictionary()

def start_clients():
    """
    Starts up all the not running clients.
    
    Can be called from any thread.
    """
    for client in CLIENTS:
        if client.running:
            continue
        
        Task(client.connect(), KOKORO)
    
    if (current_thread() is not KOKORO):
        KOKORO.wake_up()

def stop_clients():
    """
    Stops all the running clients.
    
    Can be called from any thread.
    """
    for client in CLIENTS:
        if client.running:
            Task(client.disconnect(), KOKORO)
    
    if (current_thread() is not KOKORO):
        KOKORO.wake_up()

KOKORO = EventThread(daemon=False, name='KOKORO')

GC_CYCLER = KOKORO.cycle(1200.)

if sys.implementation.name == 'pypy':
    def manual_gc_call(cycler):
        gc.collect()
    
    GC_CYCLER.append(manual_gc_call, (1<<31)-1)
    
    del manual_gc_call

HEARTBEAT_TIMEOUT = 20.0

class Kokoro(object):
    """
    A beater for Discord gateways.
    
    Attributes
    ----------
    beat_task : `None` or ``Task``
        The beat task of kokoro's gateway. Set by ``._task`` meanwhile it's gateway is connected.
    beat_waiter : `None` or ``Future``
        `.beater` task's waiter. Sleeps `.beater` between two beat.
    beater : `None` or ``Task`` of ``._keep_beating``
        A task what sends a beating payload to Discord. Set only meanwhile kokoro is in the middle of a beat.
    gateway : ``DiscordGateway`` or ``DiscordGatewayVoice``
        Kokoro's owner gateway.
    interval : `float`
        The time needed to be waited between two beats.
    last_answer : `float`
        The time of the last answered heartbeat event in `perf_counter` time.
    last_send : `float`
        The last time when kokoro sent a heartbeat event in `last_send` time.
    latency : `float`
        The time interval between the last beat and the response's time. Defaults to `.DEFAULT_LATENCY` if no beat was
        done yet.
    running : `bool`
        Whether the kokoro should run and restart itself.
    should_beat : `bool`
        Whether the kokoro should keep beating.
    task : `None` or ``Task`` of ``._start``
        The main keep alive task of kokoro.
    ws_waiter : `None` or ``Future``
        The waiter of kokoro, what waits for it's gateway to connect it's websocket.
    
    Class attributes
    ----------------
    DEFAULT_LATENCY : `float` = `9999.0`
        The default latency of kokoro. Better than using `inf`.
    """
    __slots__ = ('beat_task', 'beat_waiter', 'beater', 'gateway', 'interval', 'last_answer', 'last_send', 'latency',
        'running', 'should_beat', 'task', 'ws_waiter')
    
    DEFAULT_LATENCY = 9999.0
    
    async def __new__(cls, gateway):
        """
        Creates a ``Kokoro`` instance bound to it's gateway.
        
        This method is a coroutine.
        
        Parameters
        ----------
        gateway : ``DiscordGateway`` or ``DiscordGatewayVoice``
            The gateway of kokoro.
        
        Returns
        -------
        kokoro : ``Kokoro``
        
        Notes
        -----
        Before the coroutine returns a full loop is done to ensure `._start` is already started up.
        """
        self = object.__new__(cls)
        
        self.gateway = gateway
        self.interval = 40.0 # we set it from outside
        self.running = False
        now_ = perf_counter()
        self.last_answer = now_
        self.last_send = now_
        self.latency = self.DEFAULT_LATENCY
        self.ws_waiter = None
        self.beater = None
        self.beat_task = None
        self.beat_waiter = None
        self.task = Task(self._start(), KOKORO)
        
        #skip 1 loop
        future = Future(KOKORO)
        future.set_result(None)
        await future
        
        return self
    
    async def restart(self):
        """
        Restarts kokoro.
        
        This method is a coroutine.
        """
        self.cancel()
        future = Future(KOKORO)
        future.set_result(None)
        await future #skip 1 loop
        self.task = Task(self._start(), KOKORO)
        await future #skip 1 loop
    
    async def _start(self):
        """
        The main keep alive task of kokoro.
        
        The control flow of the method is the following:
            - Set `.ws_waiter` and wait till it is done. If it is done, means that kokoro's gateway is connected.
                If it was cancelled meanwhile, means the beat task should stop.
            - Sets `.beater` to ``._keep_beating`` and awaits it. This is the main beater of kokoro and runs meanwhile
                it's gateway is connected. This task can be cancelled, but we ignore that case.
            - If `.running` is still `True`, repeat.
        
        This method is a coroutine.
        """
        self.running = True
        while True:
            #wait for start
            try:
                waiter = Future(KOKORO)
                self.ws_waiter = waiter
                await waiter
            except CancelledError:
                #kokoro cancelled, client shuts down
                break
            finally:
                self.ws_waiter = None
            
            #keep beating
            try:
                beater = Task(self._keep_beating(), KOKORO)
                self.beater = beater
                await beater
            except CancelledError:
                #connection cancelled, lets wait for it
                pass
            finally:
                #make sure
                self.beater = None
            
            if self.running:
                continue
            
            break
        
        self.task = None
     
    async def _keep_beating(self):
        """
        The beater task of kokoro.
        
        The control flow of tze method is the following:
            - If `.should_beat` is not `True`, break out.
            - Wait `.interval` time and set the waiting ``Future`` to `self.beat_waiter`. If kokoro is cancelled, or
                if it should beat now, it is cancelled and we repeat the loop.
            - If we did not get answer since last beating (what is triggered first from outside), then we stop the
                gateway. We also break out from the loop to terminate the beating state and we will wait for the
                websocket to connect again.
            - We beat one with starting `gateway._beat` as a ``Task`` and setting it to `.beat_task`. If the task is
                not completed before it's respective timeout, we stop the gateway here as well. We also break out
                from the loop to terminate the beating state and we will wait for the websocket to connect again.
                This task can also be cancelled. If cancellation occurs, we repeat the loop.
            - If the beating task is done, we update `.last_send` to the current `perf_counter` time. Repeat the loop.
        
        This method is a coroutine.
        """
        self.last_answer = perf_counter()
        gateway = self.gateway
        self.should_beat = True
        while self.should_beat:
            waiter = sleep(self.interval, KOKORO)
            self.beat_waiter = waiter
            try:
                await waiter
            except CancelledError:
                self.last_send = perf_counter()
                continue
            
            self.beat_waiter = None
            
            if (self.last_answer+self.interval+HEARTBEAT_TIMEOUT)-perf_counter() <= 0.0:
                self.should_beat = False
                Task(gateway.terminate(), KOKORO)
                break
            
            try:
                task = Task(gateway._beat(), KOKORO)
                future_or_timeout(task, HEARTBEAT_TIMEOUT)
                self.beat_task = task
                await task
            except TimeoutError:
                self.should_beat = False
                Task(gateway.terminate(), KOKORO)
                break
            except CancelledError:
                continue
            finally:
                self.beat_task = None
            
            self.last_send = perf_counter()
    
    def start_beating(self):
        """
        Starts kokoro's beating. Handles all the cases around the board to do so.
        """
        # case 1 : we are not running
        if not self.running:
            Task(self._start_beating(), KOKORO)
            return
        
        #case 2 : we wait for ws
        waiter = self.ws_waiter
        if waiter is not None:
            waiter.set_result(None)
            return
        
        #case 3 : we wait for beat response
        waiter = self.beat_waiter
        if waiter is not None:
            waiter.cancel()
            return
        
        #case 4 : we are beating
        task = self.beat_task
        if task is not None:
            task.cancel()
            return
    
    async def _start_beating(self):
        """
        Internal method to start beating when kokoro is not running.
        
        This method is a coroutine.
        """
        #starts kokoro, then beating
        self.task = Task(self._start(), KOKORO)
        #skip 1 loop
        future = Future(KOKORO)
        future.set_result(None)
        await future
        
        waiter = self.ws_waiter
        if waiter is not None:
            waiter.set_result(None)
    
    def answered(self):
        """
        When gateway received answer after beating, it's gateway calls this method.
        
        This method updates `.last_answer` and `.latency` as well. Because of the updated `.last_answer`,
        ``._keep_beating`` task will know that it's gateway is still connected.
        """
        now_ = perf_counter()
        self.last_answer = now_
        self.latency = now_-self.last_send
    
    def terminate(self):
        """
        Terminates kokoro till restart. Called when it's gateway will resume it's connection.
        """
        #case 1 : we are not running
        if not self.running:
            return
        
        #case 2 : we are waiting for ws
        waiter = self.ws_waiter
        if waiter is not None:
            #it is fine, that is what we should do
            return
        
        #case 2 : we are beating
        beater = self.beater
        if beater is not None:
            self.should_beat = False
            
            #case 3.1 : we wait to beat
            waiter = self.beat_waiter
            if waiter is not None:
                waiter.cancel()
                return
            
            #case 3.2: we are beating
            task = self.beat_task
            if task is not None:
                task.cancel()
                return
            
    def cancel(self):
        """
        Stops kokoro. Called when it's gateway is closing.
        """
        #case 1 : we are not running
        if not self.running:
            return
        self.running = False
        
        #case 2 : we are waiting for ws
        waiter = self.ws_waiter
        if (waiter is not None):
            waiter.cancel()
            return
        
        #case 3 : we are beating
        beater = self.beater
        if beater is not None:
            self.should_beat = False
            
            #case 3.1 : we wait to beat
            waiter = self.beat_waiter
            if waiter is not None:
                waiter.cancel()
                return
            
            #case 3.2: we are beating
            task = self.beat_task
            if task is not None:
                task.cancel()
                return
            
    async def beat_now(self):
        """
        Sends a heartbeat event now. If kokoro is not at beating state, or anywhere in between, resets itself as it just
        received a heartbeat answer right now.
        
        This method is a coroutine.
        """
        while True: #GOTO
            #case 1 : we are not running:
            if not self.running:
                Task(self._start_beating(), KOKORO)
                should_beat_now = True # True = send beat data
                break
            
            # case 2 : we wait for ws
            waiter = self.ws_waiter
            if waiter is not None:
                waiter.set_result(None)
                should_beat_now = True # True = send beat data
                break
            
            # case 3 : we wait to beat
            waiter = self.beat_waiter
            if waiter is not None:
                # better skip a beat
                waiter.cancel()
                should_beat_now = True # True = send beat data
                break
            
            # case 4 : we already beat
##            task=self.beat_task
##            if task is not None:
##                should_beat_now=False
##                break
            
            should_beat_now = False
            break
        
        if should_beat_now:
            await self.gateway._beat()
        else:
            self.answered()
            
    if __debug__:
        def __del__(self):
            # bug?
            waiter = self.ws_waiter
            if waiter is not None:
                waiter.__silence__()
            
            # despair?
            waiter = self.beat_waiter
            if waiter is not None:
                waiter.__silence__()
            
    def __repr__(self):
        """Returns kokoro's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' client=',
            repr(self.gateway.client.full_name),
            ' state=',
                ]
        
        if self.task is None:
            state = 'stopped'
        elif self.beater is None:
            state = 'waiting for websocket'
        else:
            state = 'beating'
        
        result.append(state)
        result.append('>')
        
        return ''.join(result)


del WeakValueDictionary
del ClientDictionary
del sys
