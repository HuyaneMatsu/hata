# -*- coding: utf-8 -*-
__all__ = ('ALL_COMPLETED', 'AbstractChildWatcher', 'AbstractEventLoop', 'AbstractEventLoopPolicy', 'AbstractServer',
    'BaseEventLoop', 'BaseProactorEventLoop', 'BaseProtocol', 'BaseSelectorEventLoop', 'BaseTransport',
    'BoundedSemaphore', 'BufferedProtocol', 'CancelledError', 'Condition', 'DatagramProtocol', 'DatagramTransport',
    'DefaultEventLoopPolicy', 'Event', 'FIRST_COMPLETED', 'FIRST_EXCEPTION', 'FastChildWatcher', 'Future', 'Handle',
    'IncompleteReadError', 'InvalidStateError', 'IocpProactor', 'LifoQueue', 'LimitOverrunError', 'Lock',
    'MultiLoopChildWatcher', 'PIPE', 'PidfdChildWatcher', 'PipeHandle', 'Popen', 'PriorityQueue', 'ProactorEventLoop',
    'Protocol', 'Queue', 'QueueEmpty', 'QueueFull', 'ReadTransport', 'SafeChildWatcher', 'SelectorEventLoop',
    'Semaphore', 'SendfileNotAvailableError', 'StreamReader', 'StreamReaderProtocol', 'StreamWriter',
    'SubprocessProtocol', 'SubprocessTransport', 'Task', 'ThreadedChildWatcher', 'TimeoutError', 'TimerHandle',
    'Transport', 'WindowsProactorEventLoopPolicy', 'WindowsSelectorEventLoopPolicy', 'WriteTransport', '_enter_task',
    '_get_running_loop', '_leave_task', '_register_task', '_set_running_loop', '_unregister_task', 'all_tasks',
    'as_completed', 'coroutine', 'create_subprocess_exec', 'create_subprocess_shell', 'create_task', 'current_task',
    'ensure_future', 'gather', 'get_child_watcher', 'get_event_loop', 'get_event_loop_policy', 'get_running_loop',
    'iscoroutine', 'iscoroutinefunction', 'isfuture', 'new_event_loop', 'open_connection', 'pipe', 'run',
    'run_coroutine_threadsafe', 'set_child_watcher', 'set_event_loop', 'set_event_loop_policy', 'shield', 'sleep',
    'staggered_race', 'start_server', 'to_thread', 'wait', 'wait_for', 'wrap_future', )

import sys, warnings
from threading import current_thread, enumerate as list_threads, main_thread
from subprocess import PIPE

from ...env import BACKEND_ONLY
from ...backend.utils import WeakReferer, alchemy_incendiary, KeepType, WeakKeyDictionary
from ...backend.event_loop import EventThread
from ...backend.futures import Future as HataFuture, Lock as HataLock, AsyncQue, Task as HataTask, WaitTillFirst, \
    WaitTillAll, WaitTillExc, future_or_timeout, sleep as hata_sleep, shield as hata_shield, WaitContinuously, \
    Event as HataEvent
from ...backend.executor import Executor

IS_UNIX = (sys.platform != 'win32')

EVENT_LOOP_RELATION = WeakKeyDictionary()
del WeakKeyDictionary

for thread in list_threads():
    if isinstance(thread, EventThread) and thread.should_run:
        EVENT_LOOP_RELATION[main_thread()] = thread
        break
else:
    if (not BACKEND_ONLY):
        from ...discord.client_core import KOKORO
        EVENT_LOOP_RELATION[main_thread()] = KOKORO
        del KOKORO


# Additions to EventThread
@KeepType(EventThread)
class EventThread:
    
    call_soon_threadsafe = EventThread.call_soon_thread_safe
    
    def getaddrinfo(self, host, port, *, family=0, type=0, proto=0, flags=0):
        return self.get_address_info(host, port, family=family, type=type, protocol=proto, flags=flags)
    
    getnameinfo = EventThread.get_name_info
    sock_recv = EventThread.socket_receive
    sock_sendall = EventThread.socket_sendall
    sock_connect = EventThread.socket_connect
    sock_accept =EventThread.socket_accept
    
    # Required by aio-http 3.6
    def is_running(self):
        return self.running
    
    
    # Required by aio-http 3.6
    def get_debug(self):
        return False
    
    EventThread.get_debug = get_debug
    del get_debug
    
    # Required by aio-http 3.6
    def is_closed(self):
        return (not self.running)
    
    # Required by dpy 3.8
    def add_signal_handler(self, sig, callback, *args):
        pass
    
    # Required by dpy 3.8
    def run_forever(self):
        local_thread = current_thread()
        if isinstance(local_thread, EventThread):
            raise RuntimeError('Cannot call `loop.run_until_complete` inside of a loop')
        
        self.wake_up()
        self.join()
    
    # Required by dpy 3.8
    def run_until_complete(self, future):
        local_thread = current_thread()
        if isinstance(local_thread, EventThread):
            raise RuntimeError('Cannot call `loop.run_until_complete` inside of a loop')
        
        self.run(future)
    
    # Required by dpy 3.8
    def close(self):
        self.stop()
    
    def call_exception_handler(self, context):
        message = context.pop('message')
        exception = context.pop('exception', None)
        in_ = []
        for key, value in context.items():
            in_.append(key)
            in_.append(': ')
            in_.append(repr(value))
            in_.append(', ')
        
        if in_:
            del in_[-1]
            in_ = ''.join(in_)
        else:
            in_ = None
        
        extracted = [
            'Unexpected exception occurred',
                ]
        
        if (in_ is not None):
            extracted.append('at ')
            extracted.append(in_)
        
        extracted.append(': ')
        extracted.append(message)
        extracted.append('\n')
        
        if exception is None:
            self.render_exc_async(exception, extracted)
        else:
            extracted.append('*no exception provided*\n')
            sys.stderr.write(''.join(extracted))


async def in_coro(fut):
    return await fut

# Required by aio-http 3.7
def asyncio_run_in_executor(self, executor, func=..., *args):
    # We ignore the executor parameter.
    # First handle if the call is from hata. If called from hata, needs to return a `Future`.
    if func is ...:
        return Executor.run_in_executor(self, executor)
    
    # if the call is from async-io it needs to return a coroutine
    if args:
        func = alchemy_incendiary(func, args)
    
    return in_coro(Executor.run_in_executor(self, func))

EventThread.run_in_executor = asyncio_run_in_executor
del asyncio_run_in_executor



# We accept different names, so we need to define a dodge system, so here we go
hata_EventThread_subprocess_shell = EventThread.subprocess_shell

async def asyncio_subprocess_shell(self, *args, preexecution_function=None, creation_flags=0, preexec_fn=None,
        creationflags=0, startupinfo=None, startup_info=None, **kwargs):
    
    if preexec_fn is not None:
        preexecution_function = preexec_fn
    
    if creationflags != 0:
        creation_flags = creationflags
    
    if startupinfo is not None:
        startup_info = startupinfo
    
    return await hata_EventThread_subprocess_shell(self, *args, preexecution_function=preexecution_function,
        creation_flags=creation_flags, startupinfo=startup_info, **kwargs)

EventThread.subprocess_shell = asyncio_subprocess_shell
del asyncio_subprocess_shell


hata_EventThread_subprocess_exec = EventThread.subprocess_exec

async def asyncio_subprocess_exec(self, *args, preexecution_function=None, creation_flags=0, preexec_fn=None,
        creationflags=0, startupinfo=None, startup_info=None, **kwargs):
    
    if preexec_fn is not None:
        preexecution_function = preexec_fn
    
    if creationflags != 0:
        creation_flags = creationflags
    
    if startupinfo is not None:
        startup_info = startupinfo
    
    return await hata_EventThread_subprocess_exec(self, *args, preexecution_function=preexecution_function,
        creation_flags=creation_flags, startup_info=startup_info, **kwargs)

EventThread.subprocess_exec = asyncio_subprocess_exec
del asyncio_subprocess_exec


hata_EventThread_create_connection = EventThread.create_connection

async def asyncio_create_connection(self, *args, protocol=0, proto=0, socket=None, sock=None, local_address=None,
        local_addr = None, **kwargs):
    
    if proto != 0:
        protocol = proto
    
    if sock is not None:
        socket = sock
    
    if local_addr is not None:
        local_address = local_addr
    
    return await hata_EventThread_create_connection(self, *args, protocol=protocol, socket=socket,
        local_address=local_address, **kwargs)

EventThread.create_connection = asyncio_create_connection
del asyncio_create_connection


hata_EventThread_create_datagram_endpoint = EventThread.create_datagram_endpoint

async def asyncio_create_datagram_endpoint(self, protocol_factory, local_addr=None, remote_addr=None,
        local_address=None, remote_address=None, proto=0, protocol=0, reuseport=False, reuse_port=False,
        sock=None, socket=None, **kwargs):
    
    if local_addr is not None:
        local_address = local_addr
    
    if remote_addr is not None:
        remote_address = remote_addr
    
    if proto != 0:
        protocol = proto
    
    if reuseport:
        reuse_port = reuseport
    
    if sock is not None:
        socket = sock
    
    return await hata_EventThread_create_datagram_endpoint(self, protocol_factory, local_address=local_address,
        remote_address=remote_address, protocol=protocol, reuse_port=reuse_port, socket=socket, **kwargs)

EventThread.create_datagram_endpoint = asyncio_create_datagram_endpoint
del asyncio_create_datagram_endpoint


hata_EventThread_create_server = EventThread.create_server

async def asyncio_create_server(self, *args, sock=None, socket=None, reuseport=None, reuse_port=None, **kwargs):

    if reuseport:
        reuse_port = reuseport
    
    if sock is not None:
        socket = sock
    
    return await hata_EventThread_create_server(self, *args, reuse_port=reuse_port, socket=socket, **kwargs)

EventThread.create_server = asyncio_create_server
del asyncio_create_server




# Reimplement async-io features

# asyncio.base_events
# include: BaseEventLoop
BaseEventLoop = EventThread

# async-io.base_futures
# *none*

# async-io.base_subprocess
# *none*

# async-io.base_tasks
# *none*

# async-io.constants
# *none*

# async-io.coroutines
# include: coroutine, iscoroutinefunction, iscoroutine
from types import coroutine
from ...backend.futures import is_coroutine_function as iscoroutinefunction
from ...backend.futures import is_coroutine as iscoroutine

# asyncio.events
# include: AbstractEventLoopPolicy, AbstractEventLoop, AbstractServer, Handle, TimerHandle, get_event_loop_policy,
#    set_event_loop_policy, get_event_loop, set_event_loop, new_event_loop, get_child_watcher, set_child_watcher,
#    _set_running_loop, get_running_loop, _get_running_loop

class AbstractEventLoopPolicy:
    def __new__(cls):
        raise NotImplemented

AbstractEventLoop = EventThread
from ...backend.event_loop import Server as AbstractServer
from ...backend.event_loop import Handle
from ...backend.event_loop import TimerHandle

def get_event_loop_policy():
    raise NotImplementedError

def set_event_loop_policy():
    raise NotImplementedError

def get_event_loop():
    """
    Return a hata event loop.
    
    When called from a coroutine or a callback (e.g. scheduled with call_soon or similar API), this function will
    always return the running event loop.
    
    If there is no running event loop set, the function will return the result of
    `get_event_loop_policy().get_event_loop()` call.
    """
    # If local thread is event loop, return that.
    local_thread = current_thread()
    if isinstance(local_thread, EventThread):
        return local_thread
    
    # If we asked for event_loop, return that
    try:
        event_loop = EVENT_LOOP_RELATION[local_thread]
    except KeyError:
        pass
    else:
        return event_loop
    
    # Maybe there is a running loop?
    if EVENT_LOOP_RELATION:
        for event_loop in EVENT_LOOP_RELATION.values():
            if event_loop.should_run:
                EVENT_LOOP_RELATION[local_thread] = event_loop
                return event_loop
     
    # No event loops yet, create and return
    event_loop = EventThread()
    EVENT_LOOP_RELATION[local_thread] = event_loop
    return event_loop

def set_event_loop(self, loop):
    """Set the event loop."""
    local_thread = current_thread()
    assert (local_thread is loop) or (not isinstance(local_thread, EventThread))
    EVENT_LOOP_RELATION[local_thread] = loop
    
def new_event_loop():
    """Equivalent to calling get_event_loop_policy().new_event_loop()."""
    event_loop =  EventThread()
    local_thread = current_thread()
    if not isinstance(local_thread, EventThread):
        EVENT_LOOP_RELATION.setdefault(local_thread, event_loop)
    
    return event_loop

def get_child_watcher():
    """Equivalent to calling get_event_loop_policy().get_child_watcher()."""
    raise NotImplementedError

def set_child_watcher(watcher):
    """Equivalent to calling get_event_loop_policy().set_child_watcher(watcher)."""
    raise NotImplementedError

def _set_running_loop(loop):
    """
    Set the running event loop.
    
    This is a low-level function intended to be used by event loops.
    This function is thread-specific.
    """
    assert current_thread() is loop

def get_running_loop():
    """
    Return the running event loop.  Raise a RuntimeError if there is none.
    This function is thread-specific.
    """
    loop = _get_running_loop()
    if loop is None:
        raise RuntimeError('no running event loop')
    
    return loop

def _get_running_loop():
    """
    Return the running event loop or None.
    This is a low-level function intended to be used by event loops.
    This function is thread-specific.
    """
    local_thread = current_thread()
    if isinstance(local_thread, EventThread):
        return local_thread

class SendfileNotAvailableError(RuntimeError):
    """
    Sendfile syscall is not available.
    
    Raised if OS does not support sendfile syscall for given socket or file type.
    """

# asyncio.exceptions
# include: CancelledError, InvalidStateError, TimeoutError, IncompleteReadError, LimitOverrunError,
#    SendfileNotAvailableError
from ...backend.futures import CancelledError
from ...backend.futures import InvalidStateError
TimeoutError = TimeoutError

class IncompleteReadError(EOFError):
    """
    Incomplete read error. Attributes:
    
    - partial: read bytes string before the end of stream was reached
    - expected: total number of expected bytes (or None if unknown)
    """
    def __init__(self, partial, expected):
        EOFError.__init__(self, f'{len(partial)} bytes read on a total of {expected!r} expected bytes')
        self.partial = partial
        self.expected = expected

    def __reduce__(self):
        return type(self), (self.partial, self.expected)


class LimitOverrunError(Exception):
    """
    Reached the buffer limit while looking for a separator.
    
    Attributes:
    - consumed: total number of to be consumed bytes.
    """
    def __init__(self, message, consumed):
        Exception.__init__(self, message)
        self.consumed = consumed

    def __reduce__(self):
        return type(self), (self.args[0], self.consumed)

# asyncio.format_helpers
# *none*

# asyncio.futures
# Include: Future, wrap_future, isfuture

class Future:
    """
    This class is *almost* compatible with concurrent.futures.Future.
    
    Differences:
    
    - This class is not thread-safe.
    
    - result() and exception() do not take a timeout argument and
      raise an exception when the future isn't done yet.
    
    - Callbacks registered with add_done_callback() are always called
      via the event loop's call_soon().
    
    - This class is not compatible with the wait() and as_completed()
      methods in the concurrent.futures package.
    
    (In Python 3.4 or later we may be able to unify the implementations.)
    """
    def __new__(cls, *, loop=None):
        if loop is None:
            loop = get_event_loop()
        
        return HataFuture(loop)
    
    def __instancecheck__(cls, instance):
        return isinstance(instance, HataFuture)

    def __subclasscheck__(cls, klass):
        return issubclass(klass, HataFuture) or (klass is cls)

# get_loop is new in python 3.7 and required by aiosqlite
def asyncio_get_loop(self):
    return self._loop

HataFuture.get_loop = asyncio_get_loop
del asyncio_get_loop


def wrap_future(future, *, loop=None):
    raise NotImplementedError

def isfuture(obj):
    """
    Check for a Future.
    
    This returns True when obj is a Future instance or is advertising itself as duck-type compatible by setting
    _asyncio_future_blocking.
    See comment in Future for more details.
    """
    return isinstance(obj, HataFuture)

# asyncio.locks
# Include: Lock, Event, Condition, Semaphore, BoundedSemaphore

class Lock(HataLock):
    """
    Primitive lock objects.
    
    A primitive lock is a synchronization primitive that is not owned by a particular coroutine when locked.
    A primitive lock is in one of two states, 'locked' or 'unlocked'.
    
    It is created in the unlocked state. It has two basic methods,acquire() and release(). When the state is unlocked,
    acquire()changes the state to locked and returns immediately. When the state is locked, acquire() blocks until a
    call to release() in an other coroutine changes it to unlocked, then the acquire() call resets it to locked and
    returns. The release() method should only be called in the locked state; it changes the state to unlocked and
    returns immediately. If an attempt is made to release an unlocked lock, a RuntimeError will be raised.
    
    When more than one coroutine is blocked in acquire() waiting for the state to turn to unlocked, only one coroutine
    proceeds when a release() call resets the state to unlocked; first coroutine which is blocked in acquire() is being
    processed.
    
    acquire() is a coroutine and should be called with 'await'.
    
    Locks also support the asynchronous context management protocol. 'async with lock' statement should be used.
    
    Usage:
    
        ```
        lock = Lock()
        ...
        await lock.acquire()
        try:
            ...
        finally:
            lock.release()
        ```
    
    Context manager usage:
        ```
        lock = Lock()
        ...
        async with lock:
             ...
         ```
     
    Lock objects can be tested for locking state:
    
        ```
        if not lock.locked():
           await lock.acquire()
        else:
           # lock is acquired
           ...
        ```
    """
    # Required by dpy
    __slots__ = ('__weakref__', )
    
    def __new__(cls, *, loop=None):
        if loop is None:
            loop = get_event_loop()
        
        return HataLock.__new__(cls, loop)
    
    def __instancecheck__(cls, instance):
        return isinstance(instance, HataLock)
    
    def __subclasscheck__(cls, klass):
        return issubclass(klass, HataLock) or (klass is cls)


class Event:
    """
    Asynchronous equivalent to threading.Event.
    
    Class implementing event objects. An event manages a flag that can be set to true with the set() method and reset
    to false with the clear() method. The wait() method blocks until the flag is true. The flag is initially false.
    """
    def __new__(cls, *, loop=None):
        if loop is None:
            loop = get_event_loop()
        
        return HataEvent(loop)
    
    def __instancecheck__(cls, instance):
        return isinstance(instance, HataEvent)
    
    def __subclasscheck__(cls, klass):
        return issubclass(klass, HataEvent) or (klass is cls)

class Condition:
    """
    Asynchronous equivalent to threading.Condition.
    
    This class implements condition variable objects. A condition variable allows one or more coroutines to wait until
    they are notified by another coroutine.
    
    A new Lock object is created and used as the underlying lock.
    """
    
    def __new__(cls, lock=None, *, loop=None):
        raise NotImplementedError

class Semaphore:
    """
    A Semaphore implementation.
    
    A semaphore manages an internal counter which is decremented by each acquire() call and incremented by each
    release() call. The counter can never go below zero; when acquire() finds that it is zero, it blocks, waiting until
    some other thread calls release().
    
    Semaphores also support the context management protocol.
    
    The optional argument gives the initial value for the internal counter; it defaults to 1. If the value given is
    less than 0, ValueError is raised.
    """
    def __new__(cls, value=1, *, loop=None):
        raise NotImplementedError

class BoundedSemaphore:
    """
    A bounded semaphore implementation.
    
    This raises ValueError in release() if it would increase the value above the initial value.
    """
    def __new__(cls, value=1, *, loop=None):
        raise NotImplementedError

# asyncio.proactor_events
# Include: BaseProactorEventLoop

BaseProactorEventLoop = EventThread # Note, that hata has no proactor event_loop implemneted.

# asyncio.protocols
# Include: BaseProtocol, Protocol, DatagramProtocol, SubprocessProtocol, BufferedProtocol

class BaseProtocol:
    """
    Common base class for protocol interfaces.
    
    Usually user implements protocols that derived from BaseProtocol like Protocol or ProcessProtocol.
    
    The only case when BaseProtocol should be implemented directly is write-only transport like write pipe.
    """
    __slots__ = ()
    
    def connection_made(self, transport):
        pass
    
    def connection_lost(self, exception):
        pass
    
    def pause_writing(self):
        pass
    
    def resume_writing(self):
        pass

class Protocol(BaseProtocol):
    """
    Interface for stream protocol.
    
    The user should implement this interface. They can inherit from this class but don't need to. The implementations
    here do Nothing (they don't raise exceptions).
    
    When the user wants to requests a transport, they pass a protocol factory to a utility function
    (e.g., EventLoop.create_connection()).
    
    When the connection is made successfully, connection_made() is called with a suitable transport object.
    Then data_received() will be called 0 or more times with data (bytes) received from the transport; finally,
    connection_lost() will be called exactly once with either an exception object or None as an argument.
    
    State machine of calls:
    
      start -> CM [-> DR*] [-> ER?] -> CL -> end
    
    - CM: connection_made()
    - DR: data_received()
    - ER: eof_received()
    - CL: connection_lost()
    """

    __slots__ = ()

    def data_received(self, data):
        pass

    def eof_received(self):
        pass

class DatagramProtocol(BaseProtocol):
    """Interface for datagram protocol."""

    __slots__ = ()

    def datagram_received(self, data, addr):
        pass

    def error_received(self, exc):
        pass

class SubprocessProtocol(BaseProtocol):
    """Interface for protocol for subprocess calls."""

    __slots__ = ()

    def pipe_data_received(self, fd, data):
        pass

    def pipe_connection_lost(self, fd, exception):
        pass

    def process_exited(self):
        pass


class BufferedProtocol(BaseProtocol):
    """
    Interface for stream protocol with manual buffer control.
    
    Important: this has been added to asyncio in Python 3.7 *on a provisional basis*!  Consider it as an experimental
    API that might be changed or removed in Python 3.8.
    
    Event methods, such as `create_server` and `create_connection`, accept factories that return protocols that
    implement this interface. The idea of BufferedProtocol is that it allows to manually allocate and control the
    receive buffer. Event loops can then use the buffer provided by the protocol to avoid unnecessary data copies.
    This can result in noticeable performance improvement for protocols that receive big amounts of data.
    Sophisticated protocols can allocate the buffer only once at creation time.
    
    State machine of calls:
    
      start -> CM [-> GB [-> BU?]]* [-> ER?] -> CL -> end
      
    - CM: connection_made()
    - GB: get_buffer()
    - BU: buffer_updated()
    - ER: eof_received()
    - CL: connection_lost()
    """

    __slots__ = ()

    def get_buffer(self, sizehint):
        pass

    def buffer_updated(self, nbytes):
        pass

    def eof_received(self):
        pass

# asyncio.queues
# Include Queue, PriorityQueue, LifoQueue, QueueFull, QueueEmpty

class QueueEmpty(Exception):
    """
    Sendfile syscall is not available.
    
    Raised if OS does not support sendfile syscall for given socket or file type.
    """
    def __init__(cls, *args):
        raise NotImplementedError

class QueueFull(Exception):
    """
    Sendfile syscall is not available.
    
    Raised if OS does not support sendfile syscall for given socket or file type.
    """
    def __init__(self, *args):
        raise NotImplementedError

def Queue(maxsize=0, *, loop=None):
    if loop is None:
        loop = get_event_loop()
    
    if maxsize:
        max_length = maxsize
    else:
        max_length = None
    
    return AsyncQue(loop, max_length=max_length)

def PriorityQueue(maxsize=0, *, loop=None):
    """
    A subclass of Queue; retrieves entries in priority order (lowest first).

    Entries are typically tuples of the form: (priority number, data).
    """
    raise NotImplementedError

def LifoQueue(maxsize=0, *, loop=None):
    """A subclass of Queue that retrieves most recently added entries first."""
    raise NotImplementedError

# asyncio.runners
# Include: run

def run(main, *, debug=None):
    """
    Execute the coroutine and return the result.
    
    This function runs the passed coroutine, taking care of managing the asyncio event loop and finalizing asynchronous
    generators.
    
    This function cannot be called when another asyncio event loop is running in the same thread.
    
    If debug is True, the event loop will be run in debug mode.
    
    This function always creates a new event loop and closes it at the end. It should be used as a main entry point for
    asyncio programs, and should ideally only be called once.
    
    Example:
    
        ```
        async def main():
            await asyncio.sleep(1)
            print('hello')
        
        asyncio.run(main())
        ```
    """
    local_loop = current_thread()
    if isinstance(local_loop, EventThread):
        raise RuntimeError('asyncio.run() cannot be called from a running event loop')
    
    if not iscoroutine(main):
        raise ValueError(f'a coroutine was expected, got {main!r}')
    
    for thread in list_threads():
        if isinstance(thread, EventThread):
            loop = thread
            break
    else:
        loop = None
    
    if loop is None:
        loop = EventThread()
        try:
            loop.run(main)
        finally:
            loop.stop()
    else:
        loop.run(main)

# asyncio.selector_events
# Include: BaseSelectorEventLoop

BaseSelectorEventLoop = EventThread

# asyncio.sslproto
# *none*

# asyncio.staggered_race
# Include: staggered_race

async def staggered_race(coro_fns, delay, *, loop=None):
    """
    Run coroutines with staggered start times and take the first to finish.
    
    This method takes an iterable of coroutine functions. The first one is started immediately. From then on, whenever
    the immediately preceding one fails (raises an exception), or when *delay* seconds has passed, the next coroutine
    is started. This continues until one of the coroutines complete successfully, in which case all others are
    cancelled, or until all coroutines fail.
    
    The coroutines provided should be well-behaved in the following way:
    
    * They should only `return` if completed successfully.
    
    * They should always raise an exception if they did not complete successfully. In particular, if they handle
    cancellation, they should probably reraise, like this::
    
        ```
        try:
            # do work
        except asyncio.CancelledError:
            # undo partially completed work
            raise
        ```
    
    Args:
        coro_fns: an iterable of coroutine functions, i.e. callables that return a coroutine object when called. Use
        ``functools.partial`` or lambdas to pass arguments.
        
        delay: amount of time, in seconds, between starting coroutines. If `None`, the coroutines will run
        sequentially.
        
        loop: the event loop to use.
    
    Returns:
        tuple *(winner_result, winner_index, exceptions)* where
        
        - *winner_result*: the result of the winning coroutine, or `None` if no coroutines won.
        - *winner_index*: the index of the winning coroutine in `coro_fns`, or `None` if no coroutines won. If the
            winning coroutine may return None on success, *winner_index* can be used to definitively determine whether
            any coroutine won.
        - *exceptions*: list of exceptions returned by the coroutines. `len(exceptions)` is equal to the number of
            coroutines actually started, and the order is the same as in `coro_fns`. The winning coroutine's entry
            is `None`.
    """
    raise NotImplementedError

# asyncio.streams
# Include: StreamReader, StreamWriter, StreamReaderProtocol, open_connection, start_server

_DEFAULT_LIMIT = 1<<16

async def open_connection(host=None, port=None, *, loop=None, limit=_DEFAULT_LIMIT, **kwds):
    """
    A wrapper for create_connection() returning a (reader, writer) pair.
    
    The reader returned is a StreamReader instance; the writer is a StreamWriter instance.
    
    The arguments are all the usual arguments to create_connection() except protocol_factory; most common are
    positional host and port, with various optional keyword arguments following.
    
    Additional optional keyword arguments are loop (to set the event loop instance to use) and limit (to set the buffer
    limit passed to the StreamReader).
    
    (If you want to customize the StreamReader and/or StreamReaderProtocol classes, just copy the code -- there's
    really nothing special here except some convenience.)
    """
    if loop is None:
        loop = get_event_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    reader = StreamReader(limit=limit, loop=loop)
    protocol = StreamReaderProtocol(reader, loop=loop)
    transport, _ = await loop.create_connection(lambda: protocol, host, port, **kwds)
    writer = StreamWriter(transport, protocol, reader, loop)
    return reader, writer

async def start_server(client_connected_cb, host=None, port=None, *, loop=None, limit=_DEFAULT_LIMIT, **kwds):
    """
    Start a socket server, call back for each client connected. The first parameter, `client_connected_cb`, takes two
    parameters: client_reader, client_writer. client_reader is a StreamReader object, while client_writer is a
    StreamWriter object. This parameter can either be a plain callback function or a coroutine; if it is a coroutine,
    it will be automatically converted into a Task.
    
    The rest of the arguments are all the usual arguments to loop.create_server() except protocol_factory; most common
    are positional host and port, with various optional keyword arguments following.  The return value is the same as
    loop.create_server().
    
    Additional optional keyword arguments are loop (to set the event loop instance to use) and limit (to set the buffer
    limit passed to the StreamReader).
    
    The return value is the same as loop.create_server(), i.e. a Server object which can be used to stop the service.
    """
    if loop is None:
        loop = get_event_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    def factory():
        reader = StreamReader(limit=limit, loop=loop)
        protocol = StreamReaderProtocol(reader, client_connected_cb, loop=loop)
        return protocol
    
    return await loop.create_server(factory, host, port, **kwds)

class FlowControlMixin(Protocol):
    """
    Reusable flow control logic for StreamWriter.drain().
    
    This implements the protocol methods pause_writing(), resume_writing() and connection_lost().  If the subclass
    overrides these it must call the super methods.
    
    StreamWriter.drain() must wait for _drain_helper() coroutine.
    """
    def __init__(self, loop=None):
        if loop is None:
            loop = get_event_loop()
        
        self._loop = loop
        self._paused = False
        self._drain_waiter = None
        self._connection_lost = False
    
    def pause_writing(self):
        assert not self._paused
        self._paused = True
    
    def resume_writing(self):
        assert self._paused
        self._paused = False
        
        waiter = self._drain_waiter
        if waiter is not None:
            self._drain_waiter = None
            waiter.set_result_if_pending(None)
    
    def connection_lost(self, exception):
        self._connection_lost = True
        if not self._paused:
            return
        waiter = self._drain_waiter
        if waiter is None:
            return
        self._drain_waiter = None
        
        if exception is None:
            waiter.set_result_if_pending(None)
        else:
            waiter.set_exception_if_pending(exception)
    
    async def _drain_helper(self):
        if self._connection_lost:
            raise ConnectionResetError('Connection lost')
        if not self._paused:
            return
        waiter = self._drain_waiter
        assert waiter is None or waiter.cancelled()
        waiter = self._loop.create_future()
        self._drain_waiter = waiter
        await waiter
    
    def _get_close_waiter(self, stream):
        raise NotImplementedError

class StreamReaderProtocol(FlowControlMixin, Protocol):
    """
    Helper class to adapt between Protocol and StreamReader. (This is a helper class instead of making StreamReader
    itself a Protocol subclass, because the StreamReader has other potential uses, and to prevent the user of the
    StreamReader to accidentally call inappropriate methods of the protocol.)
    """
    def __init__(self, stream_reader, client_connected_cb=None, loop=None):
        FlowControlMixin.__init__(self, loop=loop)
        if stream_reader is not None:
            self._stream_reader_wr = WeakReferer(stream_reader)
        else:
            self._stream_reader_wr = None
        
        if client_connected_cb is not None:
            self._strong_reader = stream_reader
        
        self._reject_connection = False
        self._stream_writer = None
        self._transport = None
        self._client_connected_cb = client_connected_cb
        self._over_ssl = False
        self._closed = self._loop.create_future()
    
    @property
    def _stream_reader(self):
        if self._stream_reader_wr is None:
            return None
        return self._stream_reader_wr()
    
    def connection_made(self, transport):
        if self._reject_connection:
            transport.abort()
            return
        
        self._transport = transport
        reader = self._stream_reader
        if reader is not None:
            reader.set_transport(transport)
        
        self._over_ssl = (transport.get_extra_info('sslcontext') is not None)
        if self._client_connected_cb is not None:
            self._stream_writer = StreamWriter(transport, self, reader, self._loop)
            res = self._client_connected_cb(reader, self._stream_writer)
            if iscoroutine(res):
                self._loop.create_task(res)
            self._strong_reader = None
    
    def connection_lost(self, exception):
        reader = self._stream_reader
        if reader is not None:
            if exception is None:
                reader.feed_eof()
            else:
                reader.set_exception(exception)
        
        closed = self._closed
        if exception is None:
            closed.set_result_if_pending(None)
        else:
            closed.set_exception_if_pending(exception)
        
        FlowControlMixin.connection_lost(self, exception)
        self._stream_reader_wr = None
        self._stream_writer = None
        self._transport = None
    
    def data_received(self, data):
        reader = self._stream_reader
        if reader is not None:
            reader.feed_data(data)
    
    def eof_received(self):
        reader = self._stream_reader
        if reader is not None:
            reader.feed_eof()
        
        if self._over_ssl:
            return False
        return True
    
    def _get_close_waiter(self, stream):
        return self._closed
    
    def __del__(self):
        closed = self._closed
        if closed.done() and not closed.cancelled():
            closed.exception()


class StreamWriter:
    def __init__(self, transport, protocol, reader, loop):
        self._transport = transport
        self._protocol = protocol
        assert reader is None or isinstance(reader, StreamReader)
        self._reader = reader
        self._loop = loop
        self._complete_fut = self._loop.create_future()
        self._complete_fut.set_result(None)

    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
            'transport=',
            repr(self._transport)
                ]
        
        reader = self._reader
        if reader is not None:
            result.append(' reader=')
            result.append(repr(reader))
        
        result.append('>')
        
        return ''.join(result)
    
    @property
    def transport(self):
        return self._transport

    def write(self, data):
        self._transport.write(data)

    def writelines(self, data):
        self._transport.writelines(data)

    def write_eof(self):
        return self._transport.write_eof()

    def can_write_eof(self):
        return self._transport.can_write_eof()

    def close(self):
        return self._transport.close()

    def is_closing(self):
        return self._transport.is_closing()

    async def wait_closed(self):
        await self._protocol._get_close_waiter(self)

    def get_extra_info(self, name, default=None):
        return self._transport.get_extra_info(name, default)

    async def drain(self):
        if self._reader is not None:
            exception = self._reader.exception()
            if exception is not None:
                raise exception
        
        if self._transport.is_closing():
            future = self._loop.create_future()
            future.set_result(None)
            await future
        
        await self._protocol._drain_helper()


class StreamReader:
    def __init__(self, limit=_DEFAULT_LIMIT, loop=None):
        if limit <= 0:
            raise ValueError('Limit cannot be <= 0')

        self._limit = limit
        if loop is None:
            loop = get_event_loop()
        
        self._loop = loop
        self._buffer = bytearray()
        self._eof = False
        self._waiter = None
        self._exception = None
        self._transport = None
        self._paused = False
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        buffer = self._buffer
        if buffer:
            result.append(' ')
            result.append(repr(len(buffer)))
            result.append(' bytes')
        
        if self._eof:
            result.append(' eof')
        
        limit = self._limit
        if limit != _DEFAULT_LIMIT:
            result.append(' limit=')
            result.append(repr(limit))
        
        waiter = self._waiter
        if waiter is not None:
            result.append(' waiter=')
            result.append(repr(waiter))
        
        exception = self._exception
        if exception is not None:
            result.append(' exception')
            result.append(repr(exception))
        
        
        transport = self._transport
        if transport is not None:
            result.append(' transport')
            result.append(repr(transport))
        
        if self._paused:
            result.append(' paused')
        
        result.append('>')
        
        return ''.join(result)
    
    def exception(self):
        return self._exception
    
    def set_exception(self, exception):
        self._exception = exception
        
        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            waiter.set_exception_if_pending(exception)
    
    def _wake_up_waiter(self):
        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            waiter.set_result_if_pending(None)
    
    def set_transport(self, transport):
        assert self._transport is None, 'Transport already set'
        self._transport = transport
    
    def _maybe_resume_transport(self):
        if self._paused and len(self._buffer) <= self._limit:
            self._paused = False
            self._transport.resume_reading()
    
    def feed_eof(self):
        self._eof = True
        self._wake_up_waiter()
    
    def at_eof(self):
        return self._eof and not self._buffer
    
    def feed_data(self, data):
        assert not self._eof, 'feed_data after feed_eof'
        
        if not data:
            return
        
        self._buffer.extend(data)
        self._wake_up_waiter()
        
        if (self._transport is not None) and (not self._paused) and (len(self._buffer) > (self._limit<<1)):
            try:
                self._transport.pause_reading()
            except NotImplementedError:
                self._transport = None
            else:
                self._paused = True
    
    async def _wait_for_data(self, func_name):
        if self._waiter is not None:
            raise RuntimeError(f'{func_name}() called while another coroutine is already waiting for incoming data')
        
        assert not self._eof, '_wait_for_data after EOF'
        
        if self._paused:
            self._paused = False
            self._transport.resume_reading()
        
        self._waiter = self._loop.create_future()
        try:
            await self._waiter
        finally:
            self._waiter = None
    
    async def readline(self):
        sep = b'\n'
        seplen = len(sep)
        try:
            line = await self.readuntil(sep)
        except IncompleteReadError as err:
            return err.partial
        except LimitOverrunError as err:
            if self._buffer.startswith(sep, err.consumed):
                del self._buffer[:err.consumed + seplen]
            else:
                self._buffer.clear()
            self._maybe_resume_transport()
            raise ValueError(err.args[0])
        return line
    
    async def readuntil(self, separator=b'\n'):
        seplen = len(separator)
        if seplen == 0:
            raise ValueError('Separator should be at least one-byte string')
        
        exception = self._exception
        if exception is not None:
            raise exception
        
        offset = 0
        
        while True:
            buflen = len(self._buffer)
            
            if buflen - offset >= seplen:
                isep = self._buffer.find(separator, offset)
                
                if isep != -1:
                    break
                
                offset = buflen + 1 - seplen
                if offset > self._limit:
                    raise LimitOverrunError('Separator is not found, and chunk exceed the limit', offset)
            
            if self._eof:
                chunk = bytes(self._buffer)
                self._buffer.clear()
                raise IncompleteReadError(chunk, None)
            
            await self._wait_for_data('readuntil')
        
        if isep > self._limit:
            raise LimitOverrunError('Separator is found, but chunk is longer than limit', isep)
        
        chunk = self._buffer[:isep + seplen]
        del self._buffer[:isep + seplen]
        self._maybe_resume_transport()
        return bytes(chunk)

    async def read(self, n=-1):
        exception = self._exception
        if exception is not None:
            raise exception
        
        if n == 0:
            return b''
        
        if n < 0:
            blocks = []
            while True:
                block = await self.read(self._limit)
                if not block:
                    break
                blocks.append(block)
            return b''.join(blocks)

        if not self._buffer and not self._eof:
            await self._wait_for_data('read')
        
        data = bytes(self._buffer[:n])
        del self._buffer[:n]
        
        self._maybe_resume_transport()
        return data

    async def readexactly(self, n):
        if n < 0:
            raise ValueError('readexactly size can not be less than zero')
        
        exception = self._exception
        if exception is not None:
            raise exception
        
        if n == 0:
            return b''
        
        while len(self._buffer) < n:
            if self._eof:
                incomplete = bytes(self._buffer)
                self._buffer.clear()
                raise IncompleteReadError(incomplete, n)

            await self._wait_for_data('readexactly')

        if len(self._buffer) == n:
            data = bytes(self._buffer)
            self._buffer.clear()
        else:
            data = bytes(self._buffer[:n])
            del self._buffer[:n]
        self._maybe_resume_transport()
        return data
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        val = await self.readline()
        if val == b'':
            raise StopAsyncIteration
        return val

# asyncio.subprocess
# Include: create_subprocess_exec, create_subprocess_shell

if IS_UNIX:
    async def create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None, loop=None, limit=_DEFAULT_LIMIT,
            **kwargs):
        
        if loop is None:
            loop = get_event_loop()
        else:
            warnings.warn('The loop argument is deprecated since Python 3.8 and scheduled for removal in Python 3.10.',
                          DeprecationWarning, stacklevel=2)
        
        if stdin is None:
            stdin = PIPE
        
        if stdout is None:
            stdout = PIPE
        
        if stderr is None:
            stderr = PIPE
        
        return await loop.subprocess_shell(cmd, stdin=stdin, stdout=stdout, stderr=stderr, **kwargs)
    
    
    async def create_subprocess_exec(program, *args, stdin=None, stdout=None, stderr=None, loop=None,
            limit=_DEFAULT_LIMIT, **kwargs):
        
        if loop is None:
            loop = get_event_loop()
        else:
            warnings.warn('The loop argument is deprecated since Python 3.8 and scheduled for removal in Python 3.10.',
                          DeprecationWarning, stacklevel=2)
            
        if stdin is None:
            stdin = PIPE
        
        if stdout is None:
            stdout = PIPE
        
        if stderr is None:
            stderr = PIPE
        
        return await loop.subprocess_exec(program, *args, stdin=stdin, stdout=stdout, stderr=stderr,
            **kwargs)

else:
    async def create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None, loop=None, limit=_DEFAULT_LIMIT,
            **kwargs):
        raise NotImplementedError
    
    async def create_subprocess_exec(program, *args, stdin=None, stdout=None, stderr=None, loop=None,
            limit=_DEFAULT_LIMIT, **kwargs):
        raise NotImplementedError

# asyncio.tasks
# Include: Task, create_task, FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED, wait, wait_for, as_completed, sleep,
#    gather, shield, ensure_future, run_coroutine_threadsafe, current_task, all_tasks, _register_task,
#    _unregister_task, _enter_task, _leave_task,

class TaskMeta(type):
    def __new__(cls, class_name, class_parents, class_attributes, ignore=False):
        if ignore:
            return type.__new__(cls, class_name, class_parents, class_attributes)
        
        class_parents = list(class_parents)
        class_parents.remove(Task)
        class_parents.insert(0, HataTask)
        class_parents = tuple(class_parents)
        
        class_attributes['__init__'] = cls._subclass_init
        class_attributes['__new__'] = cls._subclass_new
        
        return type.__new__(type, class_name, class_parents, class_attributes)
    
    # Required by dpy
    def _subclass_init(self, *args, **kwargs):
        pass
    
    # Required by dpy
    def _subclass_new(cls, *args, coro=None, loop=None, **kwargs):
        self = HataTask.__new__(cls, coro, loop=loop)
        self.__init__(*args, coro=coro, loop=loop, **kwargs)
        return self

class Task(metaclass=TaskMeta, ignore=True):
    def __new__(cls, coro, loop=None, name=None):
        """A coroutine wrapped in a Future."""
        if not iscoroutine(coro):
            raise TypeError(f'a coroutine was expected, got {coro!r}')
        
        if loop is None:
            loop = get_event_loop()
        
        HataTask(coro, loop)
    
    # Required by aiohttp 3.6
    def current_task(*, loop=None):
        if loop is None:
            loop = get_event_loop()
        else:
            if not isinstance(loop, EventThread):
                raise TypeError(f'`loop` was not given es `{EventThread.__name__}` instance, got '
                    f'{loop.__class__.__name__}.')
        
        return loop.current_task
    
    def __instancecheck__(cls, instance):
        return isinstance(instance, HataTask)
    
    def __subclasscheck__(cls, klass):
        return issubclass(klass, HataTask) or (klass is cls)

def create_task(coro, *, name=None):
    """
    Schedule the execution of a coroutine object in a spawn task.
    
    Return a Task object.
    """
    loop = get_running_loop()
    return HataTask(coro, loop)

FIRST_COMPLETED = 'FIRST_COMPLETED'
FIRST_EXCEPTION = 'FIRST_EXCEPTION'
ALL_COMPLETED = 'ALL_COMPLETED'

async def wait(fs, *, loop=None, timeout=None, return_when=ALL_COMPLETED):
    """
    Wait for the Futures and coroutines given by fs to complete.
    
    The sequence futures must not be empty.
    
    Coroutines will be wrapped in Tasks.
    
    Returns two sets of Future: (done, pending).
    
    Usage:
        ```
        done, pending = await asyncio.wait(fs)
        ```
    
    Note: This does not raise TimeoutError! Futures that aren't done when the timeout occurs are returned in the second
    set.
    """
    if isfuture(fs) or iscoroutine(fs):
        raise TypeError(f'expect a list of futures, not {type(fs).__name__}')
    
    if not fs:
        raise ValueError('Set of coroutines/Futures is empty.')
    
    if return_when not in (FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED):
        raise ValueError(f'Invalid return_when value: {return_when}')
    
    if loop is None:
        loop = get_running_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    if any(iscoroutine(f) for f in set(fs)):
        warnings.warn('The explicit passing of coroutine objects to asyncio.wait() is deprecated since Python 3.8, '
                      'and scheduled for removal in Python 3.11.', DeprecationWarning, stacklevel=2)
    
    fs = {loop.ensure_future(f) for f in set(fs)}
    
    if return_when == FIRST_COMPLETED:
        future_type = WaitTillFirst
    elif return_when == FIRST_EXCEPTION:
        future_type = WaitTillExc
    else:
        future_type = WaitTillAll
    
    future = future_type(fs, loop)
    if timeout is not None:
        future_or_timeout(future, timeout)
    
    return await future

async def wait_for(fut, timeout, *, loop=None):
    """
    Wait for the single Future or coroutine to complete, with timeout.
    
    Coroutine will be wrapped in Task.
    
    Returns result of the Future or coroutine. When a timeout occurs, it cancels the task and raises TimeoutError. To
    avoid the task cancellation, wrap it in shield().
    
    If the wait is cancelled, the task is also cancelled.
    
    This function is a coroutine.
    """
    if loop is None:
        loop = get_running_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    if timeout is None:
        return await fut
    
    fut = loop.ensure_future(fut)
    if timeout <= 0.0:
        if fut.done():
            return fut.result()
    
    future_or_timeout(fut, timeout)
    return await fut

async def _as_completed_task(futures, waiter):
    index = 0
    limit = len(futures)
    while True:
        future = futures[index]
        
        try:
            result = await waiter
        except BaseException as err:
            future.set_exception_if_pending(err)
        else:
            if result is None:
                future.set_exception_if_pending(TimeoutError())
                
                for future in waiter.futures_pending:
                    future.cancel()
                
                while True:
                    index += 1
                    if index == limit:
                        break
                    
                    future = futures[index]
                    future.set_exception_if_pending(TimeoutError())
                    continue
                return
            
            future.set_result_if_pending(result)
        
        index += 1
        if index == limit:
            break
        
        waiter.reset()

def as_completed(fs, *, loop=None, timeout=None):
    """
    Return an iterator whose values are coroutines.
    
    When waiting for the yielded coroutines you'll get the results (or exceptions!) of the original Futures (or
    coroutines), in the order in which and as soon as they complete.
    
    This differs from PEP 3148; the proper way to use this is:
        ```
        for f in as_completed(fs):
            result = await f  # The 'await' may raise.
            # Use result.
        ```
    
    If a timeout is specified, the 'await' will raise TimeoutError when the timeout occurs before all Futures are done.
    
    Note: The futures 'f' are not necessarily members of fs.
    """
    if isfuture(fs) or iscoroutine(fs):
        raise TypeError(f'expect a list of futures, not {type(fs).__name__}')
    
    if loop is None:
        loop = get_event_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    tasks = set()
    for coro_or_future in fs:
        task = loop.ensure_future(coro_or_future)
        tasks.add(task)
    
    if not tasks:
        return []
    
    futures = [HataFuture(loop) for _ in range(len(tasks))]
    waiter = WaitContinuously(tasks, loop)
    if timeout is not None:
        future_or_timeout(waiter, timeout)
    
    HataTask(_as_completed_task(futures, waiter), loop)
    return futures
    

async def sleep(delay, result=None, *, loop=None):
    """Coroutine that completes after a given time (in seconds)."""
    if loop is None:
        loop = get_running_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    if delay <= 0.0:
        future = HataFuture(loop)
        future.set_result(None)
        await future
        return result
    
    await hata_sleep(delay, loop)
    return result

def ensure_future(coro_or_future, *, loop=None):
    """
    Wrap a coroutine or an awaitable in a future.
    
    If the argument is a Future, it is returned directly.
    """
    if loop is None:
        loop = get_running_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    return loop.ensure_future(coro_or_future)

class _gatherer_done_cb_return_exceptions(object):
    __slots__ = ('future', )
    def __init__(self, future):
        self.future = future
    
    def __call__(self, gatherer):
        for fut in gatherer.futures_pending:
            fut.cancel()
        
        future = self.future
        if future.done():
            return
        
        gatherer.cancel()
        results = []
        
        try:
            done, pending = gatherer.result()
        except BaseException as err:
            future.set_exception(err)
            return
        
        for fut in done:
            try:
                result = fut.result()
            except BaseException as err:
                result = err
            
            results.append(result)
        
        future.set_result(results)

class _gatherer_done_cb_raise(object):
    __slots__ = ('future', )
    def __init__(self, future):
        self.future = future
    
    def __call__(self, gatherer):
        future = self.future
        if future.done():
            return
        
        try:
            done, pending = gatherer.result()
        except BaseException as err:
            future.set_exception(err)
            return
        
        results = []
        for fut in done:
            try:
                result = fut.result()
            except BaseException as err:
                exception = err
                break
            else:
                results.append(result)
        else:
            # should not happen
            exception = None
            return
        
        if exception is None:
            future.set_result(results)
        else:
            future.set_exception(exception)

class _getherer_cancel_cb(object):
    __slots__ = ('gatherer',)
    def __init__(self, gatherer):
        self.gatherer = gatherer
    
    def __call__(self, future):
        gatherer = self.gatherer
        if gatherer.done():
            return
        
        if not future.cancelled():
            return
        
        for fut in gatherer.futures_done:
            fut.cancel()
        
        gatherer.cancel()

        
def gather(*coros_or_futures, loop=None, return_exceptions=False):
    """
    Return a future aggregating results from the given coroutines/futures. Coroutines will be wrapped in a future and
    scheduled in the event loop. They will not necessarily be scheduled in the same order as passed in.
    
    All futures must share the same event loop. If all the tasks are done successfully, the returned future's result
    is the list of results (in the order of the original sequence, not necessarily the order of results arrival). If
    *return_exceptions* is True, exceptions in the tasks are treated the same as successful results, and gathered in
    the result list; otherwise, the first raised exception will be immediately propagated to the returned future.
    
    Cancellation: if the outer Future is cancelled, all children (that have not completed yet) are also cancelled.
    If any child is cancelled, this is treated as if it raised CancelledError -- the outer Future is *not* cancelled
    in this case. (This is to prevent the cancellation of one child to cause other children to be cancelled.)
    
    If *return_exceptions* is False, cancelling gather() after it has been marked done won't cancel any submitted
    awaitables. For instance, gather can be marked done after propagating an exception to the caller, therefore,
    calling ``gather.cancel()`` after catching an exception (raised by one of the awaitables) from gather won't cancel
    any other awaitables.
    """
    if loop is None:
        loop = get_event_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)
    
    future = HataFuture(loop)
    
    if not coros_or_futures:
        future.set_result([])
        return future
    
    tasks = []
    for coro in coros_or_futures:
        task = loop.ensure_future(loop)
        tasks.append(task)
    
    if return_exceptions:
        gatherer_type = WaitTillAll
        gatherer_done_cb_type = _gatherer_done_cb_return_exceptions
    else:
        gatherer_type = WaitTillExc
        gatherer_done_cb_type = _gatherer_done_cb_raise
    
    gatherer = gatherer_type(tasks, loop)
    future.add_done_callback(_getherer_cancel_cb(gatherer))
    gatherer.add_done_callback(gatherer_done_cb_type(future))
    return future

def shield(arg, *, loop=None):
    """
    Wait for a future, shielding it from cancellation.
    
    The statement
        ```
        res = await shield(something())
        ```
    
    is exactly equivalent to the statement
        ```
        res = await something()
        ```
        
    *except* that if the coroutine containing it is cancelled, the task running in something() is not cancelled. From
    the POV of something(), the cancellation did not happen. But its caller is still cancelled, so the yield-from
    expression still raises CancelledError. Note: If something() is cancelled by other means this will still cancel
    shield().
    
    If you want to completely ignore cancellation (not recommended) you can combine shield() with a try/except clause,
    as follows:
        ```
        try:
            res = await shield(something())
        except CancelledError:
            res = None
        ```
    """
    if loop is None:
        loop = get_running_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.',
                      DeprecationWarning, stacklevel=2)

    return hata_shield(arg, loop)

def run_coroutine_threadsafe(coro, loop):
    """
    Submit a coroutine object to a given event loop.
    
    Return a concurrent.futures.Future to access the result.
    """
    return loop.create_task_thread_safe(coro)

def _register_task(task):
    """Register a new task in asyncio as executed by loop."""

def _enter_task(loop, task):
    pass


def _leave_task(loop, task):
    pass

def _unregister_task(task):
    """Unregister a task."""

def all_tasks(loop=None):
    """Return a set of all tasks for the loop."""
    # We could do this, but we will not.
    return {}

def current_task(loop=None):
    """Return a currently executed task."""
    if loop is None:
        loop = get_running_loop()
    
    return loop.current_task

# asyncio.threads
# Include: to_thread

async def to_thread(func, *args, **kwargs):
    """
    Asynchronously run function *func* in a separate thread.
    
    Any *args and **kwargs supplied for this function are directly passed to *func*. Also, the current
    `contextvars.Context` is propogated, allowing context variables from the main thread to be accessed in the separate
    thread.
    
    Return a coroutine that can be awaited to get the eventual result of *func*.
    """
    loop = get_running_loop()
    return await loop.run_in_executor(alchemy_incendiary(func, args, kwargs))

# asyncio.transports
# Include: BaseTransport, ReadTransport, WriteTransport, Transport, DatagramTransport, SubprocessTransport

class BaseTransport:
    __slots__ = ('_extra',)

    def __init__(self, extra=None):
        if extra is None:
            extra = {}
        self._extra = extra

    def get_extra_info(self, name, default=None):
        return self._extra.get(name, default)

    def is_closing(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def set_protocol(self, protocol):
        raise NotImplementedError

    def get_protocol(self):
        raise NotImplementedError


class ReadTransport(BaseTransport):
    __slots__ = ()

    def is_reading(self):
        raise NotImplementedError

    def pause_reading(self):
        raise NotImplementedError

    def resume_reading(self):
        raise NotImplementedError


class WriteTransport(BaseTransport):
    __slots__ = ()

    def set_write_buffer_limits(self, high=None, low=None):
        raise NotImplementedError

    def get_write_buffer_size(self):
        raise NotImplementedError

    def write(self, data):
        raise NotImplementedError

    def writelines(self, list_of_data):
        data = b''.join(list_of_data)
        self.write(data)

    def write_eof(self):
        raise NotImplementedError

    def can_write_eof(self):
        raise NotImplementedError

    def abort(self):
        raise NotImplementedError


class Transport(ReadTransport, WriteTransport):
    """Interface representing a bidirectional transport.
    
    There may be several implementations, but typically, the user does not implement new transports; rather, the
    platform provides some useful transports that are implemented using the platform's best practices.
    
    The user never instantiates a transport directly; they call a utility function, passing it a protocol factory and
    other information necessary to create the transport and protocol.  (E.g. EventLoop.create_connection() or
    EventLoop.create_server().)
    
    The utility function will asynchronously create a transport and a protocol and hook them up by calling the
    protocol's connection_made() method, passing it the transport.
    
    The implementation here raises NotImplemented for every method except writelines(), which calls write() in a loop.
    """

    __slots__ = ()


class DatagramTransport(BaseTransport):
    __slots__ = ()

    def sendto(self, data, addr=None):
        raise NotImplementedError

    def abort(self):
        raise NotImplementedError


class SubprocessTransport(BaseTransport):

    __slots__ = ()

    def get_pid(self):
        raise NotImplementedError

    def get_returncode(self):
        raise NotImplementedError

    def get_pipe_transport(self, fd):
        raise NotImplementedError

    def send_signal(self, signal):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def kill(self):
        raise NotImplementedError


class _FlowControlMixin(Transport):
    """
    All the logic for (write) flow control in a mix-in base class.
    
    The subclass must implement get_write_buffer_size(). It must call_maybe_pause_protocol() whenever the write buffer
    size increases, and _maybe_resume_protocol() whenever it decreases.  It may also override set_write_buffer_limits()
    (e.g. to specify different defaults).
    
    The subclass constructor must call super().__init__(extra).  This will call set_write_buffer_limits().
    
    The user may call set_write_buffer_limits() and get_write_buffer_size(), and their protocol's pause_writing() and
    resume_writing() may be called.
    """

    __slots__ = ('_loop', '_protocol_paused', '_high_water', '_low_water')
    
    def __init__(self, extra=None, loop=None):
        Transport.__init__(extra)
        assert loop is not None
        self._loop = loop
        self._protocol_paused = False
        self._set_write_buffer_limits()

    def _maybe_pause_protocol(self):
        size = self.get_write_buffer_size()
        if size <= self._high_water:
            return
        if not self._protocol_paused:
            self._protocol_paused = True
            try:
                self._protocol.pause_writing()
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as err:
                self._loop.render_exc_async(err, 'protocol.pause_writing() failed\n')
    

    def _maybe_resume_protocol(self):
        if self._protocol_paused and (self.get_write_buffer_size() <= self._low_water):
            self._protocol_paused = False
            try:
                self._protocol.resume_writing()
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as err:
                self._loop.render_exc_async(err, 'protocol.resume_writing() failed\n')
    
    def get_write_buffer_limits(self):
        return (self._low_water, self._high_water)
    
    def _set_write_buffer_limits(self, high=None, low=None):
        if high is None:
            if low is None:
                high = 64 * 1024
            else:
                high = 4 * low
        if low is None:
            low = high >>2

        if not high >= low >= 0:
            raise ValueError(f'high ({high!r}) must be >= low ({low!r}) must be >= 0')

        self._high_water = high
        self._low_water = low

    def set_write_buffer_limits(self, high=None, low=None):
        self._set_write_buffer_limits(high=high, low=low)
        self._maybe_pause_protocol()

    def get_write_buffer_size(self):
        raise NotImplementedError

# asyncio.trsock
# *none*

# asyncio.unix_events
# Include: SelectorEventLoop, AbstractChildWatcher, SafeChildWatcher, FastChildWatcher, PidfdChildWatcher,
#    MultiLoopChildWatcher, ThreadedChildWatcher, DefaultEventLoopPolicy

class AbstractChildWatcher:
    """
    Abstract base class for monitoring child processes.
    
    Objects derived from this class monitor a collection of subprocesses and report their termination or interruption
    by a signal.
    
    New callbacks are registered with .add_child_handler(). Starting a new process must be done within a 'with' block
    to allow the watcher to suspend its activity until the new process if fully registered (this is needed to prevent a
    race condition in some implementations).
    
    Example:
        ```
        with watcher:
            proc = subprocess.Popen("sleep 1")
            watcher.add_child_handler(proc.pid, callback)
        ```
    
    Notes:
        Implementations of this class must be thread-safe. Since child watcher objects may catch the SIGCHLD signal
        and call waitpid(-1), there should be only one active object per process.
    """
    def __new__(cls):
        raise NotImplemented


class PidfdChildWatcher(AbstractChildWatcher):
    """
    Child watcher implementation using Linux's pid file descriptors.
    
    This child watcher polls process file descriptors (pidfds) to await child process termination. In some respects,
    PidfdChildWatcher is a "Goldilocks" child watcher implementation. It doesn't require signals or threads, doesn't
    interfere with any processes launched outside the event loop, and scales linearly with the number of subprocesses
    launched by the event loop. The main disadvantage is that pidfds are specific to Linux, and only work on recent
    (5.3+) kernels.
    """

class BaseChildWatcher(AbstractChildWatcher):
    pass


class SafeChildWatcher(BaseChildWatcher):
    """
    'Safe' child watcher implementation.
    
    This implementation avoids disrupting other code spawning processes by polling explicitly each process in the
    SIGCHLD handler instead of calling os.waitpid(-1).
    
    This is a safe solution but it has a significant overhead when handling a big number of children (O(n) each time
    SIGCHLD is raised)
    """

class FastChildWatcher(BaseChildWatcher):
    """
    'Fast' child watcher implementation.
    
    This implementation reaps every terminated processes by calling os.waitpid(-1) directly, possibly breaking other
    code spawning processes and waiting for their termination.
    
    There is no noticeable overhead when handling a big number of children (O(1) each time a child terminates).
    """

class MultiLoopChildWatcher(AbstractChildWatcher):
    """
    A watcher that doesn't require running loop in the main thread.
    
    This implementation registers a SIGCHLD signal handler on instantiation (which may conflict with other code that
    install own handler for this signal).
    
    The solution is safe but it has a significant overhead when handling a big number of processes (*O(n)* each time a
    SIGCHLD is received).
    """

class ThreadedChildWatcher(AbstractChildWatcher):
    """
    Threaded child watcher implementation.
    
    The watcher uses a thread per process for waiting for the process finish.
    
    It doesn't require subscription on POSIX signal but a thread creation is not free.
    
    The watcher has O(1) complexity, its performance doesn't depend on amount of spawn processes.
    """

class DefaultEventLoopPolicy(AbstractEventLoopPolicy):
    pass

SelectorEventLoop = EventThread

# asyncio.windows_events
# include: SelectorEventLoop, ProactorEventLoop, IocpProactor, DefaultEventLoopPolicy, WindowsSelectorEventLoopPolicy,
#     WindowsProactorEventLoopPolicy

# SelectorEventLoop included already
ProactorEventLoop = EventThread

class IocpProactor:
    """Proactor implementation using IOCP."""

    def __new__(cls, concurrency=0xffffffff):
        raise NotImplementedError

# DefaultEventLoopPolicy included already

class WindowsSelectorEventLoopPolicy(AbstractEventLoopPolicy):
    pass

class WindowsProactorEventLoopPolicy(AbstractEventLoopPolicy):
    pass

# asyncio.windows_utils
# Include : pipe, Popen, PIPE, PipeHandle

BUFSIZE = 8192

def pipe(*, duplex=False, overlapped=(True, True), bufsize=BUFSIZE):
    raise NotImplementedError

class PipeHandle:
    """
    Wrapper for an overlapped pipe handle which is vaguely file-object like.
    
    The IOCP event loop can use these instead of socket objects.
    """
    def __new__(cls, handle):
        raise NotImplementedError

class Popen:
    """
    Replacement for subprocess.Popen using overlapped pipe handles.
    
    The stdin, stdout, stderr are None or instances of PipeHandle.
    """
    def __new__(cls, args, stdin=None, stdout=None, stderr=None, **kwds):
        raise NotImplementedError


del BACKEND_ONLY
del main_thread
